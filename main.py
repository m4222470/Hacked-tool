#!/usr/bin/env python3
"""
السكربت المتكامل لصيد الأصول المخفية والثغرات المحتملة
النسخة النهائية - بنية معيارية قابلة للتوسع (Analyzer Registry)

تم تطبيق جميع التحسينات المتفق عليها:
- إعادة الهيكلة إلى BaseAnalyzer و AnalyzerRegistry
- فصل المحللات في كلاسات مستقلة
- HttpClient مركزي مع Retry و Rate Limiter
- CacheManager بسيط للتكرارات
- Asset كائن موحد للهدف مع ميزات (Features)
- ScoringEngine متقدم يعتمد على الميزات (Feature-based)
- إزالة SessionManager والاعتماد الكلي على HttpClient
- إضافة should_deep_scan لتوفير الوقت بتحليل الأهداف الواعدة فقط
- إضافة VulnProbabilities (تقدير احتمالية الثغرات) لدعم Hybrid Ranking
- Hybrid Ranking: دمج النتيجة العامة (Score) مع احتمالية IDOR لترتيب أكثر ذكاءً
- الحفاظ على جميع الميزات والوظائف الأصلية
"""

import requests
import re
import time
import json
import argparse
import sys
import threading
import logging
from urllib.parse import urljoin, urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeoutError
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import OrderedDict

# -------------------- إعدادات التسجيل --------------------
def setup_logging(debug=False, log_file=None):
    log_level = logging.DEBUG if debug else logging.INFO
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers
    )
    return logging.getLogger(__name__)

# -------------------- الثوابت والإعدادات الافتراضية --------------------
DEFAULT_REQUEST_DELAY = 1
MAX_THREADS = 10
TIMEOUT = 10
DEFAULT_SCORE_THRESHOLD_HIGH = 70
DEFAULT_SCORE_THRESHOLD_MEDIUM = 40
DEFAULT_MAX_CONCURRENT_REQUESTS = 5
DEFAULT_RATE_LIMIT = 10
SSL_ISSUE_SCORE = 2
DEFAULT_GLOBAL_TIMEOUT = 600

VALID_STATUS_CODES = {200, 201, 202, 204, 301, 302, 307, 308, 401, 403, 405, 406, 409, 410, 415, 429, 500, 501, 502, 503}
WARNING_STATUS_CODES = {301, 302, 307, 308, 429, 500, 501, 502, 503}
PROTECTED_STATUS_CODES = {401, 403, 405}

SURFACE_WEIGHT = 0.25
STRUCTURAL_WEIGHT = 0.5
BEHAVIORAL_WEIGHT = 0.25
LOW_LATENCY_THRESHOLD = 0.3
SMALL_CONTENT_LENGTH = 500

# -------------------- Rate Limiter --------------------
class RateLimiter:
    def __init__(self, max_concurrent, rate_per_sec):
        self.max_concurrent = max_concurrent
        self.semaphore = threading.Semaphore(max_concurrent)
        self.rate_per_sec = rate_per_sec
        self.lock = threading.Lock()
        self.last_call = 0
        self.min_interval = 1.0 / rate_per_sec if rate_per_sec > 0 else 0

    def _wait_for_rate(self):
        if self.min_interval <= 0:
            return
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_call = now

    def acquire(self):
        self._wait_for_rate()
        self.semaphore.acquire()

    def release(self):
        self.semaphore.release()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

# -------------------- Cache Manager --------------------
class CacheManager:
    """تخزين بسيط للطلبات المتكررة (في الذاكرة)."""
    def __init__(self, ttl=300):
        self.cache = OrderedDict()
        self.ttl = ttl

    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())
        if len(self.cache) > 1000:
            self.cache.popitem(last=False)

# -------------------- Core HTTP Engine (HttpClient) --------------------
class HttpClient:
    """
    عميل HTTP مركزي يدير جميع الطلبات.
    - Session واحدة مع connection pooling
    - Retry strategy موحد
    - Backoff تلقائي
    - Integration مع rate limiter
    - توحيد الـ headers
    - تخزين مؤقت (cache) للاستجابات
    """
    def __init__(self, ctx: 'ScanContext'):
        self.ctx = ctx
        self.session = requests.Session()
        # إعداد headers قياسية
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        })
        self.session.verify = not ctx.config.insecure
        # إعداد retry strategy
        retry_strategy = requests.adapters.Retry(
            total=2,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = requests.adapters.HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=20,
            pool_maxsize=20
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get(self, url, **kwargs):
        """إرسال طلب GET مع rate limiter."""
        with self.ctx.rate_limiter:
            return self.session.get(url, timeout=TIMEOUT, **kwargs)

    def post(self, url, **kwargs):
        """إرسال طلب POST مع rate limiter."""
        with self.ctx.rate_limiter:
            return self.session.post(url, timeout=TIMEOUT, **kwargs)

    def close(self):
        self.session.close()

# -------------------- Asset Model (كائن موحد مع ميزات واحتمالات ثغرات) --------------------
class Asset:
    """
    كائن واحد يمثل الهدف بكل بياناته.
    - metadata: المعلومات الأساسية (url, status, title, إلخ)
    - findings: قائمة بالاكتشافات من كل محلل
    - features: ميزات مستخرجة (تستخدم في التسجيل واتخاذ القرارات)
    - vuln_probabilities: تقدير احتمالية وجود ثغرات معينة (مثل IDOR)
    - score: النتيجة النهائية (مقياس 0-100)
    - final_priority: الأولوية النهائية بعد الدمج مع احتمالات الثغرات
    """
    def __init__(self, url: str):
        self.url = url
        self.subdomain = urlparse(url).netloc
        self.scheme = urlparse(url).scheme
        self.status: Optional[int] = None
        self.server: str = ""
        self.title: str = ""
        self.content_type: str = ""
        self.headers: Dict = {}
        self.security_headers: Dict = {}      # نتيجة SecurityHeadersAnalyzer
        self.auth_findings: List = []         # نتائج تحليل المصادقة
        self.alive: bool = False
        self.ssl_issue: bool = False
        self.status_valid: bool = False
        self.status_warning: bool = False
        self.status_protected: bool = False
        self.is_api: bool = False
        self.content_sample: str = ""
        self.content_length: int = 0
        self.total_time: float = 0.0
        self.error: Optional[str] = None
        self.low_value: bool = False

        # حقول إضافية للنتائج العميقة (من HiddenFilesAnalyzer, JavaScriptAnalyzer)
        self.hidden_files: List = []           # قائمة بالملفات المخفية المكتشفة
        self.js_endpoints: Set = set()         # نقاط نهاية مستخرجة من JS
        self.js_api_calls: List = []           # استدعاءات API من JS

        # الميزات (Features) بدلاً من الإشارات العامة
        self.features: Dict[str, Any] = {}

        # احتمالات الثغرات (مثلاً IDOR) – يمكن ملؤها بواسطة محلل خاص
        self.vuln_probabilities: Dict[str, float] = {}

        # نتيجة التسجيل (من ScoringEngine)
        self.score: float = 0.0
        self.risk: str = "Low"
        self.factors: List = []                # قائمة العوامل المؤثرة في النتيجة

        # الأولوية النهائية (Hybrid Ranking)
        self.final_priority: float = 0.0

    def to_dict(self) -> Dict:
        """تحويل الكائن إلى قاموس للتقرير النهائي."""
        return {
            "url": self.url,
            "status": self.status,
            "server": self.server,
            "title": self.title,
            "content_type": self.content_type,
            "alive": self.alive,
            "ssl_issue": self.ssl_issue,
            "score": self.score,
            "final_priority": self.final_priority,
            "vuln_probabilities": self.vuln_probabilities,
            "risk": self.risk,
            "factors": self.factors,
            "hidden_files": self.hidden_files,
            "auth_findings": self.auth_findings,
            "js_endpoints": list(self.js_endpoints),
            "js_api_calls": self.js_api_calls
        }

# -------------------- دالة تحديد أولوية التحليل العميق --------------------
def should_deep_scan(asset: Asset) -> bool:
    """
    تحديد ما إذا كان الهدف يستحق فحصاً عميقاً (Hidden, JS, ...).
    يعتمد على الميزات (features) المسجلة مسبقاً.
    """
    features = asset.features

    # إشارات تستحق الفحص العميق
    if features.get("requires_auth"):
        return True

    if features.get("is_admin_path") or features.get("admin_panel_path") or features.get("admin_page"):
        return True

    if features.get("has_numeric_param"):
        return True

    if asset.status in (401, 403):
        return True

    if features.get("is_json_xml") or features.get("content_type_json"):
        return True

    # يمكن إضافة المزيد من الإشارات حسب الحاجة
    return False

# -------------------- دوال مساعدة عامة --------------------
def is_in_scope(url, allowed_domains):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        domain = domain.split(':')[0]
        for allowed in allowed_domains:
            if domain == allowed or domain.endswith('.' + allowed):
                return True
    except Exception:
        pass
    return False

def extract_title(html):
    try:
        match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else ""
    except Exception:
        return ""

def remove_js_comments(js_content):
    try:
        content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        return content
    except Exception:
        return js_content

def is_valid_status(status_code): return status_code in VALID_STATUS_CODES
def is_warning_status(status_code): return status_code in WARNING_STATUS_CODES
def is_protected_status(status_code): return status_code in PROTECTED_STATUS_CODES

# -------------------- ScanConfig --------------------
class ScanConfig:
    def __init__(self, args):
        self.domain = args.domain
        self.allowed_domains = args.allowed if args.allowed else [args.domain]
        self.delay = args.delay
        self.output = args.output
        self.no_js = args.no_js
        self.no_hidden = args.no_hidden
        self.hidden_scan = args.hidden_scan
        self.no_auth = args.no_auth
        self.threshold_high = args.threshold_high
        self.threshold_medium = args.threshold_medium
        self.max_js_domains = args.max_js_domains
        self.max_concurrent = args.max_concurrent
        self.rate_limit = args.rate_limit
        self.global_timeout = args.global_timeout
        self.insecure = args.insecure
        self.debug = args.debug
        self.log_file = args.log_file
        # خيارات إضافية للتحكم في المحللات
        self.enabled_analyzers = []
        if not args.no_hidden:
            self.enabled_analyzers.append("hidden")
        if not args.no_js:
            self.enabled_analyzers.append("js")
        if not args.no_auth:
            self.enabled_analyzers.append("auth")
        self.enabled_analyzers.append("headers")  # دائمًا مفعل

# -------------------- ScanContext (معدل) --------------------
class ScanContext:
    def __init__(self, config: ScanConfig, logger, rate_limiter: RateLimiter, cache_mgr: CacheManager, global_deadline: float):
        self.config = config
        self.logger = logger
        self.rate_limiter = rate_limiter
        self.cache = cache_mgr
        self.global_deadline = global_deadline
        self.http_client = None  # سيتم تعيينه من Orchestrator بعد الإنشاء

# -------------------- TargetDiscovery --------------------
class TargetDiscovery:
    @staticmethod
    def discover(domain: str, delay: float) -> Set[str]:
        subs = set()
        subs.update(TargetDiscovery._crt_sh(domain, delay))
        subs.update(TargetDiscovery._otx(domain, delay))
        subs.update(TargetDiscovery._threatminer(domain, delay))
        subs.add(domain)
        return subs

    @staticmethod
    def _crt_sh(domain, delay):
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        try:
            time.sleep(delay)
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                subs = set()
                for entry in data:
                    name = entry.get('name_value', '')
                    if name:
                        for n in name.split('\n'):
                            if n.endswith(domain):
                                subs.add(n.lower().strip())
                return subs
        except Exception:
            pass
        return set()

    @staticmethod
    def _otx(domain, delay):
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
        try:
            time.sleep(delay)
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                subs = set()
                for entry in data.get('passive_dns', []):
                    hostname = entry.get('hostname', '')
                    if hostname and hostname.endswith(domain):
                        subs.add(hostname.lower().strip())
                return subs
        except Exception:
            pass
        return set()

    @staticmethod
    def _threatminer(domain, delay):
        url = f"https://api.threatminer.org/v2/domain.php?q={domain}&rt=5"
        try:
            time.sleep(delay)
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                subs = set()
                for entry in data.get('results', []):
                    if entry.endswith(domain):
                        subs.add(entry.lower().strip())
                return subs
        except Exception:
            pass
        return set()

# -------------------- BaseAnalyzer (الواجهة الموحدة) --------------------
class BaseAnalyzer:
    """الكلاس الأساسي لجميع المحللات."""
    def __init__(self, name: str):
        self.name = name

    def analyze(self, asset: Asset, context: ScanContext) -> Dict[str, Any]:
        """
        يجب على كل محلل تنفيذ هذه الدالة.
        تعيد قاموسًا يحتوي على النتائج الخاصة به.
        """
        raise NotImplementedError

# -------------------- AnalyzerRegistry --------------------
class AnalyzerRegistry:
    """يسجل المحللات ويدير تنفيذها."""
    def __init__(self):
        self._analyzers = {}

    def register(self, analyzer: BaseAnalyzer):
        self._analyzers[analyzer.name] = analyzer

    def get_enabled(self, enabled_names: List[str]) -> List[BaseAnalyzer]:
        return [self._analyzers[name] for name in enabled_names if name in self._analyzers]

    def run_all(self, asset: Asset, context: ScanContext, enabled_names: List[str]) -> Dict[str, Any]:
        results = {}
        for name in enabled_names:
            if name in self._analyzers:
                try:
                    results[name] = self._analyzers[name].analyze(asset, context)
                except Exception as e:
                    context.logger.error(f"خطأ في المحلل {name}: {e}", exc_info=True)
                    results[name] = {"error": str(e)}
        return results

# -------------------- SecurityHeadersAnalyzer --------------------
class SecurityHeadersAnalyzer(BaseAnalyzer):
    """تحليل رؤوس الأمان."""
    IMPORTANT_HEADERS = {
        "Strict-Transport-Security": {
            "description": "يجبر المتصفح على استخدام HTTPS",
            "risk": "نقص HSTS قد يسمح بهجمات SSL Stripping",
            "secure_values": []
        },
        "Content-Security-Policy": {
            "description": "يمنع XSS والهجمات الأخرى",
            "risk": "نقص CSP يزيد خطر XSS",
            "secure_values": []
        },
        "X-Content-Type-Options": {
            "description": "يمنع المتصفح من تخمين MIME type",
            "risk": "قد يؤدي لثغرات تنفيذ أكواد",
            "secure_values": ["nosniff"]
        },
        "X-Frame-Options": {
            "description": "يمنع التضمين في frames (Clickjacking)",
            "risk": "نقص قد يسمح بـ Clickjacking",
            "secure_values": ["DENY", "SAMEORIGIN"]
        },
        "X-XSS-Protection": {
            "description": "يفعّل حماية XSS في المتصفحات القديمة",
            "risk": "نقص يزيد خطر XSS",
            "secure_values": ["1; mode=block"]
        },
        "Referrer-Policy": {
            "description": "يتحكم بمعلومات الإحالة",
            "risk": "تسريب معلومات",
            "secure_values": []
        },
        "Permissions-Policy": {
            "description": "يتحكم بصلاحيات المتصفح",
            "risk": "نقص قد يسمح باستخدام ميزات حساسة",
            "secure_values": []
        },
        "Cache-Control": {
            "description": "يتحكم بالتخزين المؤقت",
            "risk": "نقص قد يؤدي لتسريب بيانات حساسة",
            "secure_values": ["no-store", "private"]
        }
    }

    def __init__(self):
        super().__init__("headers")

    def analyze(self, asset: Asset, context: ScanContext) -> Dict[str, Any]:
        result = {'present': {}, 'missing': [], 'insecure': []}
        headers_lower = {k.lower(): v for k, v in asset.headers.items()}
        for header, info in self.IMPORTANT_HEADERS.items():
            hl = header.lower()
            if hl in headers_lower:
                val = headers_lower[hl]
                is_secure = True
                if info['secure_values'] and val not in info['secure_values']:
                    is_secure = False
                    result['insecure'].append({'header': header, 'value': val, 'issue': f'القيمة "{val}" غير آمنة'})
                if is_secure:
                    result['present'][header] = val
            else:
                result['missing'].append({'header': header, 'description': info['description'], 'risk': info['risk']})
        return result

# -------------------- HiddenFilesAnalyzer (معدل لتسجيل الميزات) --------------------
class HiddenFilesAnalyzer(BaseAnalyzer):
    HIDDEN_PATHS = [
        "/.git/config", "/.env", "/backup.zip", "/backup.tar.gz", "/backup.sql",
        "/swagger.json", "/swagger.yaml", "/swagger.yml", "/openapi.json", "/openapi.yaml",
        "/api/swagger.json", "/api-docs", "/.aws/credentials", "/.npmrc", "/.bash_history",
        "/.ssh/id_rsa", "/.ssh/id_rsa.pub", "/.gitignore", "/.htaccess", "/.htpasswd",
        "/config.json", "/config.php", "/config.js", "/database.json", "/database.yml",
        "/credentials.json", "/secrets.json", "/secret.key", "/private.key", "/server.key",
        "/dump.sql", "/dump.rdb", "/dump.mongo", "/composer.json", "/package.json",
        "/package-lock.json", "/yarn.lock", "/phpinfo.php", "/info.php", "/test.php",
        "/.well-known/security.txt", "/.well-known/openid-configuration",
        "/.DS_Store", "/.svn/entries", "/.git/HEAD", "/.git/index",
        "/backup/", "/old/", "/temp/", "/test/", "/dev/", "/staging/"
    ]

    def __init__(self):
        super().__init__("hidden")

    def analyze(self, asset: Asset, context: ScanContext) -> Dict[str, Any]:
        if not asset.alive or asset.ssl_issue or not asset.status_valid:
            return {"found": []}
        if not context.config.hidden_scan and asset.status >= 500:
            return {"found": []}

        results = []
        base_url = asset.url
        http = context.http_client
        for path in self.HIDDEN_PATHS:
            if time.time() > context.global_deadline:
                context.logger.debug("Deadline exceeded during hidden scan")
                break
            url = urljoin(base_url, path)
            cache_key = f"hidden:{url}"
            cached = context.cache.get(cache_key)
            if cached:
                if cached.get("found"):
                    results.append(cached)
                continue
            try:
                resp = http.get(url, allow_redirects=False)
                if resp and resp.status_code == 200 and len(resp.content) < 1024*1024:
                    res = {
                        "url": url,
                        "path": path,
                        "status": 200,
                        "content_type": resp.headers.get("Content-Type", ""),
                        "content_length": len(resp.content),
                        "found": True,
                        "snippet": resp.text[:200] + "..." if len(resp.text) > 200 else resp.text
                    }
                    sensitive_keywords = ["password", "secret", "key", "token", "api", "aws", "private"]
                    if any(kw in resp.text.lower() for kw in sensitive_keywords):
                        res["sensitive"] = True
                        res["note"] = "يحتوي على كلمات مفتاحية حساسة"
                    results.append(res)
                    context.cache.set(cache_key, res)
            except Exception:
                continue

        # تسجيل الميزات في asset بناءً على النتائج
        if results:
            normal_count = sum(1 for r in results if not r.get("sensitive"))
            if normal_count > 0:
                asset.features["hidden_file_found"] = normal_count
            sensitive_count = sum(1 for r in results if r.get("sensitive"))
            if sensitive_count > 0:
                asset.features["sensitive_hidden_file"] = sensitive_count

        return {"found": results}

# -------------------- JavaScriptAnalyzer (معدل لتسجيل الميزات) --------------------
class JavaScriptAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__("js")

    def analyze(self, asset: Asset, context: ScanContext) -> Dict[str, Any]:
        if not asset.alive or asset.ssl_issue:
            return {"endpoints": [], "api_calls": []}
        if 'html' not in asset.content_type:
            return {"endpoints": [], "api_calls": []}

        context.logger.info(f"تحليل JS لـ {asset.url}")
        http = context.http_client

        html = context.cache.get(f"html:{asset.url}")
        if not html:
            resp = http.get(asset.url)
            if resp and resp.status_code == 200:
                html = resp.text
                context.cache.set(f"html:{asset.url}", html)
            else:
                return {"endpoints": [], "api_calls": []}

        js_links = self._extract_links(html, asset.url)

        max_js = context.config.max_js_domains
        if max_js > 0:
            js_links = js_links[:max_js]

        all_endpoints = set()
        all_api_calls = []

        with ThreadPoolExecutor(max_workers=3) as exec:
            futures = {exec.submit(self._fetch_js, js, context): js for js in js_links}
            for f in as_completed(futures):
                if time.time() > context.global_deadline:
                    break
                js = futures[f]
                try:
                    content = f.result()
                except Exception:
                    continue
                if content:
                    eps = self._extract_endpoints(content, asset.url)
                    for ep in eps:
                        if is_in_scope(ep, context.config.allowed_domains):
                            all_endpoints.add(ep)
                    api = self._extract_api_calls(content, asset.url)
                    for c in api:
                        if is_in_scope(c["endpoint"], context.config.allowed_domains):
                            c["source_js"] = js
                            all_api_calls.append(c)

        # تسجيل الميزات
        if all_endpoints:
            asset.features["js_endpoints_found"] = len(all_endpoints)
        if all_api_calls:
            asset.features["js_api_calls_found"] = len(all_api_calls)

        return {
            "endpoints": list(all_endpoints),
            "api_calls": all_api_calls
        }

    def _fetch_js(self, js_url, context):
        cache_key = f"js:{js_url}"
        cached = context.cache.get(cache_key)
        if cached:
            return cached
        try:
            http = context.http_client
            resp = http.get(js_url)
            content = resp.text if resp and resp.status_code == 200 else None
            if content:
                context.cache.set(cache_key, content)
            return content
        except Exception:
            return None

    @staticmethod
    def _extract_links(html, base):
        links = []
        for m in re.finditer(r'<script[^>]+src=["\'](.*?)["\']', html, re.IGNORECASE):
            links.append(urljoin(base, m.group(1)))
        return links

    @staticmethod
    def _extract_endpoints(js, base):
        eps = set()
        patterns = [
            r'["\'](https?://[^"\']+)["\']',
            r'["\'](/?[a-zA-Z0-9_\-/]+api[a-zA-Z0-9_\-/]*)["\']',
            r'["\'](/?v[0-9]+/[a-zA-Z0-9_\-/]+)["\']',
            r'["\'](/?graphql)["\']',
            r'["\'](/?admin[a-zA-Z0-9_\-/]*)["\']',
            r'["\'](/?dev[a-zA-Z0-9_\-/]*)["\']',
            r'["\'](/?staging[a-zA-Z0-9_\-/]*)["\']',
            r'["\'](/?test[a-zA-Z0-9_\-/]*)["\']',
            r'["\'](/?old[a-zA-Z0-9_\-/]*)["\']',
        ]
        for pat in patterns:
            for m in re.findall(pat, js):
                m = m.strip()
                if m and len(m) > 3:
                    if m.startswith('http'):
                        eps.add(m)
                    else:
                        eps.add(urljoin(base, m))
        return eps

    @staticmethod
    def _extract_api_calls(js, base):
        calls = []
        clean = remove_js_comments(js)
        pats = [
            (r'fetch\s*\(\s*[\'"]([^\'"]+)[\'"]', "fetch", "GET"),
            (r'fetch\s*\(\s*[\'"]([^\'"]+)[\'"]\s*,\s*\{[^}]*method:\s*[\'"](GET|POST|PUT|DELETE)[\'"]', "fetch_with_method", None),
            (r'axios\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]', "axios", None),
            (r'\$\.ajax\s*\(\s*\{[^}]*url:\s*[\'"]([^\'"]+)[\'"][^}]*method:\s*[\'"](GET|POST|PUT|DELETE)[\'"]', "jquery_ajax", None),
            (r'XMLHttpRequest.*open\s*\(\s*[\'"](GET|POST|PUT|DELETE)[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]', "xhr", None)
        ]
        for pat, src, default in pats:
            for match in re.finditer(pat, clean, re.IGNORECASE | re.DOTALL):
                if src == "fetch" and default:
                    endpoint, method = match.group(1), default
                elif src == "fetch_with_method":
                    endpoint, method = match.groups()
                elif src == "axios":
                    method, endpoint = match.groups()
                elif src == "jquery_ajax":
                    endpoint, method = match.groups()
                elif src == "xhr":
                    method, endpoint = match.groups()
                else:
                    continue
                full = urljoin(base, endpoint)
                calls.append({
                    "endpoint": full,
                    "method": method.upper() if method else "GET",
                    "source": src,
                    "original": endpoint
                })
        return calls

# -------------------- AuthFlowAnalyzer --------------------
class AuthFlowAnalyzer(BaseAnalyzer):
    """تحليل نقاط المصادقة في الصفحة."""
    AUTH_PATTERNS = {
        "login_form": [r'<form[^>]*action=["\'](.*login.*|.*signin.*)["\']', r'<input[^>]*name=["\'](password|passwd|pwd)["\']'],
        "register_form": [r'<form[^>]*action=["\'](.*register.*|.*signup.*)["\']'],
        "forgot_password": [r'<a[^>]*href=["\'](.*forgot.*|.*reset.*)["\']', r'<form[^>]*action=["\'](.*forgot.*|.*reset.*)["\']'],
        "logout": [r'<a[^>]*href=["\'](.*logout.*)["\']'],
        "oauth": [r'oauth', r'openid', r'login with (google|facebook|github)'],
        "jwt": [r'jwt', r'token', r'authorization: bearer'],
        "basic_auth": [r'www-authenticate', r'basic realm'],
    }

    def __init__(self):
        super().__init__("auth")

    def analyze(self, asset: Asset, context: ScanContext) -> Dict[str, Any]:
        results = []
        if not asset.alive or asset.ssl_issue:
            return {"findings": []}

        # تحقق من رأس WWW-Authenticate
        if 'www-authenticate' in asset.headers:
            results.append({
                "type": "basic_auth",
                "detail": "Basic authentication detected via header",
                "confidence": "high"
            })

        # تحقق من وجود cookies
        set_cookie = asset.headers.get('set-cookie', '')
        if 'session' in set_cookie.lower() or 'auth' in set_cookie.lower():
            results.append({
                "type": "session_cookie",
                "detail": "Session cookie detected",
                "confidence": "medium"
            })

        # تحقق من HTML
        html = asset.content_sample
        cache_key = f"html:{asset.url}"
        cached_html = context.cache.get(cache_key)
        if cached_html:
            html = cached_html
        if html:
            html_lower = html.lower()
            for auth_type, patterns in self.AUTH_PATTERNS.items():
                for pat in patterns:
                    if re.search(pat, html_lower, re.IGNORECASE):
                        results.append({
                            "type": auth_type,
                            "detail": f"Pattern '{pat}' matched",
                            "confidence": "low" if auth_type in ["oauth", "jwt"] else "medium"
                        })
                        break

        # إزالة التكرار
        unique = []
        seen = set()
        for r in results:
            key = (r['type'], r['detail'])
            if key not in seen:
                seen.add(key)
                unique.append(r)
        return {"findings": unique}

# -------------------- ScoringEngine (معدل - Feature-based) --------------------
class ScoringEngine:
    """محرك تسجيل متقدم يعتمد على الميزات (Features) بدلاً من الإشارات العامة."""
    CATEGORY_WEIGHTS = {
        "surface": 0.25,
        "structural": 0.5,
        "behavioral": 0.25
    }

    # تعريف قواعد التسجيل: كل قاعدة تحدد اسم الميزة، الفئة، الوزن، وشرط اختياري
    RULES = [
        # سطحية
        {"feature": "status_protected", "category": "surface", "weight": 2.0},
        {"feature": "status_200", "category": "surface", "weight": 1.0},
        {"feature": "status_warning", "category": "surface", "weight": 0.5},
        {"feature": "status_valid", "category": "surface", "weight": 0.8},
        {"feature": "is_json_xml", "category": "surface", "weight": 2.0},
        {"feature": "login_page", "category": "surface", "weight": 2.0},
        {"feature": "admin_page", "category": "surface", "weight": 2.0},
        {"feature": "error_page", "category": "surface", "weight": -1.0},

        # هيكلية
        {"feature": "dev_environment", "category": "structural", "weight": 2.0},
        {"feature": "admin_panel_path", "category": "structural", "weight": 3.0},
        {"feature": "api_endpoint", "category": "structural", "weight": 2.0},
        {"feature": "backup_asset", "category": "structural", "weight": 2.0},
        {"feature": "missing_security_header", "category": "structural", "weight": 1.0},  # لكل header
        {"feature": "insecure_security_header", "category": "structural", "weight": 0.5},
        {"feature": "hidden_file_found", "category": "structural", "weight": 2.0},
        {"feature": "sensitive_hidden_file", "category": "structural", "weight": 4.0},
        {"feature": "auth_finding", "category": "structural", "weight": 2.0},  # لكل finding
        {"feature": "ssl_issue", "category": "structural", "weight": 2.0},

        # سلوكية
        {"feature": "url_parameters", "category": "behavioral", "weight": 1.0},  # لكل معامل (حتى 3)
        {"feature": "low_latency", "category": "behavioral", "weight": 1.0},
        {"feature": "normal_latency", "category": "behavioral", "weight": 0.2},
    ]

    # مضاعفات سياقية (تعتمد على الميزات أيضاً)
    CONTEXT_MULTIPLIERS = [
        ("protected_api", lambda f: f.get("status_protected") and f.get("api_endpoint"), 1.5),
        ("fast_protected", lambda f: f.get("status_protected") and f.get("low_latency"), 1.3),
        ("small_200", lambda f: f.get("status_200") and f.get("small_content"), 0.7),
    ]

    @classmethod
    def compute(cls, asset: Asset) -> Tuple[float, List[str]]:
        # تجميع الدرجات حسب الفئة
        category_scores = {"surface": 0.0, "structural": 0.0, "behavioral": 0.0}
        factors = []

        features = asset.features

        # تطبيق القواعد على الميزات
        for rule in cls.RULES:
            feat_name = rule["feature"]
            if feat_name in features:
                val = features[feat_name]
                # إذا كانت القيمة عددية (مثل عدد headers المفقودة) نضرب الوزن بعددها
                if isinstance(val, (int, float)) and not isinstance(val, bool):
                    score = rule["weight"] * val
                else:
                    # قيمة منطقية أو أي شيء آخر - نضيف الوزن مرة واحدة إذا كانت موجودة وصحيحة
                    if val:
                        score = rule["weight"]
                    else:
                        continue
                category_scores[rule["category"]] += score
                # نضيف عامل 설명
                if isinstance(val, (int, float)) and val > 1:
                    factors.append(f"{feat_name} (x{val}) (+{score})")
                else:
                    factors.append(f"{feat_name} (+{score})")

        # حساب الدرجة الخام بضرب كل فئة بوزنها
        raw_score = (
            category_scores["surface"] * cls.CATEGORY_WEIGHTS["surface"] +
            category_scores["structural"] * cls.CATEGORY_WEIGHTS["structural"] +
            category_scores["behavioral"] * cls.CATEGORY_WEIGHTS["behavioral"]
        )

        # تطبيق المضاعفات السياقية
        multiplier = 1.0
        for name, condition, mult in cls.CONTEXT_MULTIPLIERS:
            if condition(features):
                multiplier *= mult
                factors.append(f"{name} (x{mult})")

        final_score = raw_score * multiplier

        # تطبيع (تقدير max possible)
        max_surface = sum(r["weight"] for r in cls.RULES if r["category"] == "surface" and r["weight"] > 0)
        max_structural = sum(r["weight"] for r in cls.RULES if r["category"] == "structural")
        max_behavioral = sum(r["weight"] for r in cls.RULES if r["category"] == "behavioral")
        max_possible = (
            max_surface * cls.CATEGORY_WEIGHTS["surface"] +
            max_structural * cls.CATEGORY_WEIGHTS["structural"] +
            max_behavioral * cls.CATEGORY_WEIGHTS["behavioral"]
        ) * 1.2

        if max_possible > 0:
            norm_score = min(round((final_score / max_possible) * 100, 1), 100)
        else:
            norm_score = 0.0

        return norm_score, factors

# -------------------- TargetValidator (معدل - يسجل الميزات اللازمة) --------------------
class TargetValidator:
    """التحقق من حياة الهدف وجمع المعلومات الأساسية باستخدام HttpClient."""
    @staticmethod
    def validate(subdomain: str, ctx: ScanContext) -> Asset:
        asset = Asset(f"https://{subdomain}")  # سنحاول https أولاً
        for scheme in ["https://", "http://"]:
            url = scheme + subdomain
            try:
                start = time.perf_counter()
                http = ctx.http_client
                resp = http.get(url, allow_redirects=True)
                total_time = time.perf_counter() - start
                if not resp:
                    continue

                # تعبئة بيانات Asset
                asset.url = resp.url
                asset.status = resp.status_code
                asset.server = resp.headers.get("Server", "")
                asset.content_type = resp.headers.get("Content-Type", "").lower()
                asset.headers = dict(resp.headers)
                asset.alive = True
                asset.total_time = total_time
                asset.content_length = len(resp.content)
                asset.content_sample = resp.text[:200] + "..." if len(resp.text) > 200 else resp.text
                asset.title = extract_title(resp.text)

                # تسجيل الميزات الأساسية
                asset.features["status_valid"] = is_valid_status(asset.status)
                asset.features["status_warning"] = is_warning_status(asset.status)
                asset.features["status_protected"] = is_protected_status(asset.status)
                if asset.status == 200:
                    asset.features["status_200"] = True
                asset.is_api = 'json' in asset.content_type or 'xml' in asset.content_type
                if asset.is_api:
                    asset.features["is_json_xml"] = True
                    asset.features["content_type_json"] = True
                if asset.content_length > 0 and asset.content_length < SMALL_CONTENT_LENGTH:
                    asset.features["small_content"] = True

                # ميزات العنوان
                if asset.title:
                    low = asset.title.lower()
                    if any(k in low for k in ['login', 'signin']):
                        asset.features["login_page"] = True
                    elif any(k in low for k in ['admin', 'dashboard']):
                        asset.features["admin_page"] = True
                    elif any(k in low for k in ['error', '404']):
                        asset.features["error_page"] = True

                # تحليل الرؤوس الأمنية
                headers_analyzer = SecurityHeadersAnalyzer()
                asset.security_headers = headers_analyzer.analyze(asset, ctx)
                # تحويل نتائج headers إلى ميزات
                missing_count = len(asset.security_headers.get('missing', []))
                if missing_count > 0:
                    asset.features["missing_security_header"] = missing_count
                insecure_count = len(asset.security_headers.get('insecure', []))
                if insecure_count > 0:
                    asset.features["insecure_security_header"] = insecure_count

                # تحليل المصادقة
                auth_analyzer = AuthFlowAnalyzer()
                auth_result = auth_analyzer.analyze(asset, ctx)
                asset.auth_findings = auth_result.get("findings", [])
                if asset.auth_findings:
                    asset.features["auth_finding"] = len(asset.auth_findings)

                # ميزة requires_auth (إذا وجدت مصادقة أو الحماية)
                if asset.auth_findings or asset.status_protected:
                    asset.features["requires_auth"] = True

                # ميزة is_admin_path / admin_panel_path من URL
                if any(k in asset.url.lower() for k in ['admin', 'administrator', 'panel']):
                    asset.features["is_admin_path"] = True
                    asset.features["admin_panel_path"] = True

                # ميزة has_numeric_param: فحص وجود معاملات رقمية في URL
                parsed = urlparse(asset.url)
                if parsed.query:
                    params = parse_qs(parsed.query)
                    for values in params.values():
                        if any(v.isdigit() for v in values if isinstance(v, str)):
                            asset.features["has_numeric_param"] = True
                            break

                # تخزين HTML في cache للاستفادة لاحقًا
                ctx.cache.set(f"html:{asset.url}", resp.text)

                return asset

            except requests.exceptions.SSLError as e:
                ctx.logger.debug(f"SSL error for {url}: {e}")
                asset.ssl_issue = True
                asset.error = f"SSL Error: {e}"
                asset.features["ssl_issue"] = True
                continue
            except Exception as e:
                ctx.logger.debug(f"Request error for {url}: {e}")
                continue

        asset.alive = False
        asset.error = "No response"
        return asset

# -------------------- ScanOrchestrator (معدل - يستخدم should_deep_scan و Hybrid Ranking) --------------------
class ScanOrchestrator:
    def __init__(self, config: ScanConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.rate_limiter = RateLimiter(config.max_concurrent, config.rate_limit)
        self.cache = CacheManager()
        self.start_time = time.time()
        self.global_deadline = self.start_time + config.global_timeout

        # إنشاء HttpClient وتمريره للـ Context
        self.ctx = ScanContext(config, self.logger, self.rate_limiter, self.cache, self.global_deadline)
        self.http_client = HttpClient(self.ctx)
        self.ctx.http_client = self.http_client

        # تسجيل المحللات
        self.registry = AnalyzerRegistry()
        self.registry.register(SecurityHeadersAnalyzer())
        self.registry.register(HiddenFilesAnalyzer())
        self.registry.register(JavaScriptAnalyzer())
        self.registry.register(AuthFlowAnalyzer())

    def run(self):
        self.logger.info("بدء عملية الفحص")
        # 1. الاكتشاف
        raw_subs = TargetDiscovery.discover(self.config.domain, self.config.delay)
        in_scope = {s for s in raw_subs if is_in_scope(f"http://{s}", self.config.allowed_domains)}
        self.logger.info(f"تم العثور على {len(in_scope)} نطاق فرعي ضمن النطاق المسموح")
        if not in_scope:
            self.logger.warning("لا توجد نطاقات للفحص")
            return

        # 2. التحقق الأساسي بالتوازي (يستخدم TargetValidator المعدل الذي يرجع Asset)
        assets = []
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            future_to_sub = {executor.submit(TargetValidator.validate, sub, self.ctx): sub for sub in in_scope}
            remaining = max(0, self.global_deadline - time.time())
            try:
                for future in as_completed(future_to_sub, timeout=remaining if remaining > 0 else None):
                    sub = future_to_sub[future]
                    try:
                        asset = future.result()
                        assets.append(asset)
                    except Exception as e:
                        self.logger.error(f"خطأ في فحص {sub}: {e}", exc_info=True)
            except FuturesTimeoutError:
                self.logger.warning("تجاوز المهلة الزمنية الإجمالية أثناء الفحص الأساسي")
                executor.shutdown(wait=False, cancel_futures=True)

        # تصفية الأحياء
        live_assets = [a for a in assets if a.alive or a.ssl_issue]
        self.logger.info(f"تم العثور على {len(live_assets)} نطاق حي (بما في ذلك مشكلات SSL)")

        # 3. تحليل عميق وتسجيل المخاطر
        for asset in live_assets:
            if time.time() > self.global_deadline:
                self.logger.warning("تجاوز المهلة، إيقاف التحليل العميق")
                break

            # التحليل العميق فقط إذا كان الهدف يستحق ذلك
            if asset.alive and not asset.ssl_issue and asset.status_valid and should_deep_scan(asset):
                # تشغيل المحللات المسموح بها
                analyzer_results = self.registry.run_all(asset, self.ctx, self.config.enabled_analyzers)
                # دمج النتائج في asset
                if "hidden" in analyzer_results:
                    asset.hidden_files = analyzer_results["hidden"].get("found", [])
                if "js" in analyzer_results:
                    asset.js_endpoints = set(analyzer_results["js"].get("endpoints", []))
                    asset.js_api_calls = analyzer_results["js"].get("api_calls", [])
                # auth_findings موجودة بالفعل من TargetValidator، لا حاجة لدمجها مرة أخرى
            else:
                self.logger.debug(f"Skipping deep scan for {asset.url} (low priority)")

            # تقييم المخاطر باستخدام ScoringEngine (يتم دائماً، حتى بدون تحليل عميق)
            score, factors = ScoringEngine.compute(asset)
            asset.score = score
            asset.factors = factors
            if asset.score >= self.config.threshold_high:
                asset.risk = "High"
            elif asset.score >= self.config.threshold_medium:
                asset.risk = "Medium"
            else:
                asset.risk = "Low"

        # حساب final_priority لكل asset (hybrid score) – هنا نفترض وجود احتمالية IDOR في vuln_probabilities
        for asset in live_assets:
            idor_prob = asset.vuln_probabilities.get("idor", 0.0)
            original_score = asset.score
            # دمج: 60% original score, 40% IDOR probability (محول إلى مقياس 0-100)
            asset.final_priority = (original_score * 0.6) + ((idor_prob * 100) * 0.4)

        # 4. الترتيب حسب final_priority (بدلاً من score)
        live_assets.sort(key=lambda a: a.final_priority, reverse=True)

        # 5. التقرير النهائي
        self._generate_report(live_assets, len(in_scope), len(live_assets))

        # 6. حفظ النتائج
        self._save_results(live_assets, len(in_scope), len(live_assets))

        # إغلاق الجلسة
        self.http_client.close()

    def _generate_report(self, assets: List[Asset], total_subs, live_count):
        print("\n" + "="*80)
        print("🔍 التقرير النهائي - الأصول مصنفة حسب الأولوية")
        print("="*80)
        print(f"\n📊 إحصائيات عامة:")
        print(f"   - إجمالي النطاقات الفرعية: {total_subs}")
        print(f"   - النطاقات الحية: {live_count}")
        hidden_count = sum(len(a.hidden_files) for a in assets)
        auth_count = sum(len(a.auth_findings) for a in assets)
        ssl_count = sum(1 for a in assets if a.ssl_issue)
        if hidden_count:
            print(f"   - ملفات مخفية مكتشفة: {hidden_count}")
        if auth_count:
            print(f"   - نقاط مصادقة مكتشفة: {auth_count}")
        if ssl_count:
            print(f"   - مشكلات SSL: {ssl_count}")

        high = [a for a in assets if a.risk == "High"]
        print("\n" + "🔥"*40)
        print(f"🚨 الأصول عالية القيمة (Score ≥ {self.config.threshold_high})")
        print("🔥"*40)
        if high:
            for a in high[:10]:
                ssl_warn = " (SSL Issue!)" if a.ssl_issue else ""
                prot = " (Protected)" if a.status_protected else ""
                idor_prob = a.vuln_probabilities.get("idor", 0.0)
                print(f"\n   • 🌐 {a.url} [{a.risk}] Score: {a.score} | Priority: {a.final_priority:.1f} | IDOR: {idor_prob:.2f}{ssl_warn}{prot}")
                if a.factors:
                    for f in a.factors[:3]:
                        print(f"       - {f}")
                if a.hidden_files:
                    print(f"       ⚠️  ملفات مخفية: {len(a.hidden_files)}")
                if a.auth_findings:
                    print(f"       🔐 نقاط مصادقة: {len(a.auth_findings)}")
        else:
            print("   لا توجد أصول عالية القيمة.")
        print("\n💡 توصيات: ركز على الأصول عالية القيمة أولاً، ثم تحقق من الملفات المخفية ونقاط المصادقة.")

    def _save_results(self, assets: List[Asset], total_subs, live_count):
        data = {
            "target_domain": self.config.domain,
            "allowed_domains": self.config.allowed_domains,
            "thresholds": {"high": self.config.threshold_high, "medium": self.config.threshold_medium},
            "statistics": {
                "total_subdomains": total_subs,
                "live_subdomains": live_count,
                "scored_targets": len(assets)
            },
            "results": [a.to_dict() for a in assets]
        }
        try:
            with open(self.config.output, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False, default=str)
            print(f"\n[+] تم حفظ النتائج في {self.config.output}")
        except Exception as e:
            self.logger.error(f"فشل حفظ النتائج: {e}")

# -------------------- الوظيفة الرئيسية --------------------
def main():
    parser = argparse.ArgumentParser(description="السكربت المعاد هيكلته - Analyzer Registry")
    parser.add_argument("-d", "--domain", required=True)
    parser.add_argument("--allowed", nargs='+')
    parser.add_argument("--delay", type=float, default=DEFAULT_REQUEST_DELAY)
    parser.add_argument("--output", default="results_final.json")
    parser.add_argument("--no-js", action="store_true")
    parser.add_argument("--no-hidden", action="store_true")
    parser.add_argument("--hidden-scan", action="store_true")
    parser.add_argument("--no-auth", action="store_true")
    parser.add_argument("--threshold-high", type=int, default=DEFAULT_SCORE_THRESHOLD_HIGH)
    parser.add_argument("--threshold-medium", type=int, default=DEFAULT_SCORE_THRESHOLD_MEDIUM)
    parser.add_argument("--max-js-domains", type=int, default=0)
    parser.add_argument("--max-concurrent", type=int, default=DEFAULT_MAX_CONCURRENT_REQUESTS)
    parser.add_argument("--rate-limit", type=int, default=DEFAULT_RATE_LIMIT)
    parser.add_argument("--global-timeout", type=int, default=DEFAULT_GLOBAL_TIMEOUT)
    parser.add_argument("--insecure", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--log-file", type=str)
    args = parser.parse_args()

    logger = setup_logging(args.debug, args.log_file)
    config = ScanConfig(args)
    logger.info(f"بدء الفحص على النطاق {config.domain}")
    if config.insecure:
        logger.warning("التحقق من SSL معطل! غير آمن.")

    orchestrator = ScanOrchestrator(config)
    try:
        orchestrator.run()
    except KeyboardInterrupt:
        logger.info("تم الإيقاف بواسطة المستخدم.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"خطأ غير متوقع: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
