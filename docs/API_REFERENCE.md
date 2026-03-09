# 📚 مرجع الـ API الكامل - Hacked-tool v2.0.0

## 🎯 مقدمة

هذا المرجع يحتوي على وثائق شاملة لجميع الكلاسات والدوال الرئيسية في Hacked-tool v2.0.0.

---

## 📦 الـ Modules الرئيسية

### 1. `config.py` - الإعدادات المركزية

**الغرض:** تخزين جميع الثوابت والإعدادات الافتراضية

**الثوابت الرئيسية:**

```python
# التوقيتات (بالثواني)
DEFAULT_REQUEST_DELAY = 1
MAX_THREADS = 10
TIMEOUT = 10
DEFAULT_GLOBAL_TIMEOUT = 600

# عتبات الدرجات (0-100)
DEFAULT_SCORE_THRESHOLD_HIGH = 70
DEFAULT_SCORE_THRESHOLD_MEDIUM = 40
SSL_ISSUE_SCORE = 2

# حدود الحجم
MAX_HTML_SIZE = 300000  # 300 KB

# الوزن لـ Scoring
SURFACE_WEIGHT = 0.25
STRUCTURAL_WEIGHT = 0.5
BEHAVIORAL_WEIGHT = 0.25
```

**مسارات الإدارة المشبوهة:**

```python
ADMIN_PATHS = [
    "admin", "panel", "dashboard", "backend", "manage", 
    "control", "console", "administrator", "cp", "wp-admin",
    # ... 10 مسارات إضافية
]
```

**بصمات التكنولوجيات:**

```python
TECH_FINGERPRINTS = {
    "wordpress": ["wp-content", "wp-includes", ...],
    "laravel": ["laravel", "app/", ...],
    # ... تكنولوجيات أخرى
}
```

**الاستخدام:**

```python
from config import DEFAULT_SCORE_THRESHOLD_HIGH, ADMIN_PATHS

threshold = DEFAULT_SCORE_THRESHOLD_HIGH
for path in ADMIN_PATHS:
    print(path)
```

---

### 2. `utils/logger.py` - نظام التسجيل

**الغرض:** توفير نظام تسجيل مركزي مع Singleton pattern

**الكلاس الرئيسي:**

```python
class Logger:
    """نظام التسجيل المركزي - Singleton pattern"""
    
    # Methods:
    get_logger(name: str) -> logging.Logger
    set_log_file(filepath: str) -> None
    set_level(level: int) -> None
```

**الاستخدام:**

```python
from utils.logger import logger

# تسجيل رسائل مختلفة
logger.info("بدء الفحص")
logger.warning("تحذير: الخادم بطيء")
logger.error("خطأ: الاتصال فشل")
logger.debug("معلومات التصحيح")
```

---

### 3. `utils/validators.py` - التحقق من الصحة

**الكلاسات الرئيسية:**

#### 3.1 URLValidator

```python
class URLValidator:
    """التحقق من صحة URLs والنطاقات"""
    
    @staticmethod
    def is_valid_domain(domain: str) -> bool
        """هل النطاق صحيح؟"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool
        """هل الـ URL صحيح؟"""
    
    @staticmethod
    def normalize_domain(domain: str) -> str
        """تطبيع النطاق (إزالة www, toLowerCase)"""
    
    @staticmethod
    def is_subdomain(domain: str, parent: str) -> bool
        """هل هو subdomain من النطاق الأب؟"""
```

**الاستخدام:**

```python
from utils.validators import URLValidator

# التحقق من النطاق
if URLValidator.is_valid_domain("example.com"):
    print("نطاق صحيح")

# تطبيع النطاق
normalized = URLValidator.normalize_domain("www.Example.COM")
# النتيجة: "example.com"

# التحقق من الـ URL
if URLValidator.is_valid_url("https://example.com/api"):
    print("URL صحيح")
```

#### 3.2 ParameterValidator

```python
class ParameterValidator:
    """التحقق من معاملات محتملة للثغرات"""
    
    @staticmethod
    def is_suspicious_parameter(param_name: str) -> bool
        """هل اسم المعامل يشير إلى ثغرة؟"""
    
    @staticmethod
    def score_parameter(param_name: str) -> float
        """إعطاء درجة للتعرض للخطر (0-100)"""
```

**الاستخدام:**

```python
from utils.validators import ParameterValidator

suspicious_params = ["id", "user_id", "file", "path", "admin"]

for param in suspicious_params:
    if ParameterValidator.is_suspicious_parameter(param):
        score = ParameterValidator.score_parameter(param)
        print(f"{param}: درجة الخطر = {score}")
```

---

### 4. `utils/url_utils.py` - عمليات الـ URLs

**الكلاسات الرئيسية:**

#### 4.1 URLUtils

```python
class URLUtils:
    """عمليات معالجة الـ URLs"""
    
    @staticmethod
    def extract_domain(url: str) -> str
        """استخراج النطاق من URL"""
    
    @staticmethod
    def extract_path(url: str) -> str
        """استخراج المسار من URL"""
    
    @staticmethod
    def extract_query_params(url: str) -> Dict[str, str]
        """استخراج معاملات البحث (Query parameters)"""
    
    @staticmethod
    def normalize_urls(urls: List[str]) -> List[str]
        """إزالة التكرار وتطبيع URLs"""
    
    @staticmethod
    def extract_parameters(html: str) -> Set[str]
        """استخراج جميع المعاملات من HTML"""
```

**الاستخدام:**

```python
from utils.url_utils import URLUtils

url = "https://api.example.com/v1/users?id=123&filter=active"

domain = URLUtils.extract_domain(url)
# النتيجة: "api.example.com"

path = URLUtils.extract_path(url)
# النتيجة: "/v1/users"

params = URLUtils.extract_query_params(url)
# النتيجة: {"id": "123", "filter": "active"}

# تطبيع URLs وإزالة التكرار
urls = ["https://example.com", "http://example.com", "https://example.com/"]
normalized = URLUtils.normalize_urls(urls)
```

#### 4.2 PathUtils

```python
class PathUtils:
    """عمليات المسارات الشائعة"""
    
    @staticmethod
    def get_common_paths() -> List[str]
        """الحصول على المسارات الشائعة"""
    
    @staticmethod
    def has_numeric_parameter(path: str) -> bool
        """هل يحتوي المسار على معامل رقمي؟"""
    
    @staticmethod
    def get_api_endpoints() -> List[str]
        """الحصول على نقاط API الشائعة"""
```

**الاستخدام:**

```python
from utils.url_utils import PathUtils

# الحصول على مسارات شائعة
paths = PathUtils.get_common_paths()
# النتيجة: ["/admin", "/login", "/api", ...]

# التحقق من معاملات رقمية
if PathUtils.has_numeric_parameter("/user/123/profile"):
    print("يحتوي على معامل رقمي")

# الحصول على نقاط API
api_endpoints = PathUtils.get_api_endpoints()
# النتيجة: ["/api", "/api/v1", "/api/v2", ...]
```

---

### 5. `utils/parser.py` - معالج الوسائط

**الدالة الرئيسية:**

```python
def create_parser() -> argparse.ArgumentParser:
    """إنشاء معالج الوسائط بجميع الخيارات"""
```

**الخيارات المتاحة:**

```
-d, --domain        [مطلوب] النطاق المراد فحصه
--allowed           [اختياري] النطاقات المسموح بها
--max-concurrent    [اختياري] عدد الطلبات المتزامنة (الافتراضي: 5)
--rate-limit        [اختياري] معدل الطلبات (الافتراضي: 10)
--threshold-high    [اختياري] عتبة الخطورة العالية (الافتراضي: 70)
--threshold-medium  [اختياري] عتبة الخطورة المتوسطة (الافتراضي: 40)
-o, --output        [اختياري] ملف الإخراج
--debug             [اختياري] وضع التصحيح
```

**الاستخدام:**

```python
from utils.parser import create_parser

# إنشاء المحلل
parser = create_parser()

# تحليل الوسائط
args = parser.parse_args()

# استخدام الوسائط
domain = args.domain
max_concurrent = args.max_concurrent
threshold = args.threshold_high
```

---

### 6. `core/rate_limiter.py` - محدد المعدل المتكيف

**الكلاس الرئيسي:**

```python
class AdaptiveRateLimiter:
    """محدد معدل متكيف - يتكيف تلقائياً مع استجابة الخادم"""
    
    def __init__(self, base_rate: float = 10, min_rate: float = 1, 
                 max_rate: float = 100):
        """
        Args:
            base_rate: المعدل الافتراضي (طلب/ثانية)
            min_rate: أقل معدل مسموح
            max_rate: أعلى معدل مسموح
        """
    
    def record_429(self) -> None:
        """تسجيل رد Too Many Requests (يقلل المعدل)"""
    
    def record_success(self) -> None:
        """تسجيل نجاح الطلب (يزيد المعدل قليلاً)"""
    
    def wait_for_rate(self) -> None:
        """الانتظار قبل الطلب التالي"""
    
    def get_stats(self) -> Dict:
        """الحصول على إحصائيات المعدل الحالية"""
```

**المنطق:**

- عند رد 429: تقليل المعدل بـ 30%
- عند نجاح الطلب: زيادة المعدل بـ 5%
- يتراوح بين `min_rate` و `max_rate`

**الاستخدام:**

```python
from core.rate_limiter import AdaptiveRateLimiter

# إنشاء محدد معدل
limiter = AdaptiveRateLimiter(base_rate=10)

# في حلقة الطلبات:
for request in requests:
    limiter.wait_for_rate()  # انتظر قبل الطلب
    
    try:
        response = make_request()
        if response.status_code == 429:
            limiter.record_429()  # خفض المعدل
        else:
            limiter.record_success()  # رفع المعدل قليلاً
    except Exception as e:
        limiter.record_429()  # أيضاً عند الأخطاء

# عرض الإحصائيات
print(limiter.get_stats())
# النتيجة: {'current_rate': 9.5, '429_count': 2, 'success_count': 50}
```

---

### 7. `evasion/header_randomizer.py` - عشوائية الرؤوس

**الكلاس الرئيسي:**

```python
class HeaderRandomizer:
    """توليد رؤوس عشوائية لتجنب الكشف"""
    
    @staticmethod
    def get_random_headers() -> Dict[str, str]
        """الحصول على مجموعة رؤوس عشوائية"""
    
    @staticmethod
    def get_random_user_agent() -> str
        """الحصول على User-Agent عشوائي"""
    
    @staticmethod
    def get_random_accept_language() -> str
        """الحصول على لغة قبول عشوائية"""
    
    @staticmethod
    def get_random_cache_control() -> str
        """الحصول على سياسة cache عشوائية"""
```

**الاستخدام:**

```python
from evasion.header_randomizer import get_random_headers, get_random_user_agent

# الحصول على رؤوس عشوائية كاملة
headers = get_random_headers()
# النتيجة: مثال
# {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Cache-Control': 'max-age=0',
#     'Accept': 'text/html,application/xhtml+xml,...'
# }

# استخدامها في طلب HTTP
import requests

response = requests.get("https://example.com", headers=headers)

# أو الحصول على User-Agent فقط
user_agent = get_random_user_agent()
```

---

### 8. `core/models.py` - نماذج البيانات (قادم)

**سيحتوي على:**

```python
class Asset:
    """تمثيل أصل (domain/host)"""
    domain: str
    score: float
    technologies: List[str]
    endpoints: List['Endpoint']
    vulnerabilities: List['Vulnerability']

class Endpoint:
    """تمثيل نقطة نهائية (URL)"""
    url: str
    method: str
    status: int
    response_time: float
    technologies: List[str]

class Vulnerability:
    """تمثيل ثغرة"""
    type: str
    severity: str
    description: str
    endpoint: Optional[Endpoint]
```

---

### 9. `core/scanner.py` - محرك الفحص (قادم)

**الكلاسات الرئيسية:**

```python
class BaseAnalyzer(ABC):
    """الكلاس الأساسي لجميع محللات الفحص"""
    
    @abstractmethod
    def analyze(self, asset: Asset) -> AnalysisResult:
        """تحليل الأصل"""
    
    def get_name(self) -> str:
        """الحصول على اسم المحلل"""

class AnalyzerRegistry:
    """سجل جميع المحللات المتاحة"""
    
    def register(self, analyzer: BaseAnalyzer) -> None:
        """تسجيل محلل جديد"""
    
    def get_analyzers(self) -> List[BaseAnalyzer]:
        """الحصول على جميع المحللات"""

class ScanOrchestrator:
    """المنظم الرئيسي للفحص"""
    
    def scan(self, target: str, depth: int = 1) -> ScanResult:
        """إجراء فحص كامل على الهدف"""
```

---

### 10. `modules/fingerprinting.py` - تحديد التكنولوجيات (قادم)

**المحللات:**

```python
class SecurityHeadersAnalyzer(BaseAnalyzer):
    """تحليل رؤوس الأمان (HSTS, CSP, X-Frame-Options)"""

class TechDetectionAnalyzer(BaseAnalyzer):
    """تحديد التكنولوجيات المستخدمة"""

class AuthFlowAnalyzer(BaseAnalyzer):
    """تحليل آليات المصادقة"""
```

---

### 11. `modules/endpoint_discovery.py` - اكتشاف النقاط (قادم)

**المحللات:**

```python
class HiddenFilesAnalyzer(BaseAnalyzer):
    """البحث عن ملفات مخفية وأوراق احتياطية"""

class JavaScriptAnalyzer(BaseAnalyzer):
    """تحليل ملفات JavaScript لاستخراج endpoints"""

class ParameterDiscoveryAnalyzer(BaseAnalyzer):
    """اكتشاف جميع المعاملات (GET, POST, header)"""
```

---

### 12. `modules/subdomain_takeover.py` - كشف الاستيلاء (قادم)

**المحللات:**

```python
class SubdomainTakeoverAnalyzer(BaseAnalyzer):
    """كشف الـ subdomains القابلة للاستيلاء عليها"""
```

---

### 13. `modules/scoring.py` - نقاط التقييم (قادم)

**الكلاسات:**

```python
class ScoringEngine:
    """حساب درجة الخطورة (0-100) لكل أصل"""
    
    def calculate_score(self, features: Dict[str, float]) -> float:
        """حساب الدرجة النهائية"""
    
    def get_severity(self, score: float) -> str:
        """الحصول على مستوى الخطورة"""
```

---

### 14. `modules/graph_builder.py` - بناء الرسم البياني (قادم)

**الكلاسات:**

```python
class EndpointGraph:
    """رسم بياني لعلاقات النقاط النهائية"""
    
    def add_endpoint(self, endpoint: Endpoint) -> None
    def find_related_endpoints(self, endpoint: Endpoint) -> List[Endpoint]

class CorrelationEngine:
    """ربط النتائج من مصادر مختلفة"""
    
    def correlate(self, results: List[AnalysisResult]) -> CorrelatedResult
```

---

## 🎯 أمثلة عملية

### مثال 1: استخدام الـ API برمجياً

```python
#!/usr/bin/env python3
# scenario: scan.py - فحص موقع برمجياً

from config import DEFAULT_SCORE_THRESHOLD_HIGH
from core.scanner import ScanOrchestrator, AnalyzerRegistry
from modules.fingerprinting import SecurityHeadersAnalyzer, TechDetectionAnalyzer
from modules.endpoint_discovery import HiddenFilesAnalyzer
from utils.logger import logger

# إنشاء registry
registry = AnalyzerRegistry()

# تسجيل المحللات
registry.register(SecurityHeadersAnalyzer())
registry.register(TechDetectionAnalyzer())
registry.register(HiddenFilesAnalyzer())

# إنشاء المنظم
orchestrator = ScanOrchestrator(
    registry=registry,
    threshold=DEFAULT_SCORE_THRESHOLD_HIGH
)

# تنفيذ الفحص
results = orchestrator.scan("example.com")

# طباعة النتائج
for asset in results.assets:
    logger.info(f"الأصل: {asset.domain}")
    logger.info(f"الدرجة: {asset.score}")
    logger.info(f"التكنولوجيات: {asset.technologies}")
```

### مثال 2: استخدام معالج الوسائط

```python
#!/usr/bin/env python3
# scenario: main.py - نقطة الدخول الرئيسية

from utils.parser import create_parser
from utils.logger import logger
from core.scanner import ScanOrchestrator
import json

# إنشاء محلل الوسائط
parser = create_parser()
args = parser.parse_args()

# إعداد التسجيل
if args.debug:
    logger.set_level(logging.DEBUG)

# بناء النتائج
results = ScanOrchestrator(threshold=args.threshold_high).scan(args.domain)

# حفظ النتائج
if args.output:
    with open(args.output, 'w') as f:
        json.dump(results.to_dict(), f, indent=2)
else:
    print(json.dumps(results.to_dict(), indent=2))
```

---

## 🔗 الاعتماديات بين الـ Modules

```
config.py
    ↓
    ├─→ utils/logger.py
    ├─→ utils/validators.py
    ├─→ utils/url_utils.py
    ├─→ utils/parser.py
    │
    ├─→ core/models.py
    │
    ├─→ core/rate_limiter.py
    │
    ├─→ core/request_manager.py (يعتمد على: rate_limiter, evasion/header_randomizer)
    │
    ├─→ evasion/header_randomizer.py
    │
    ├─→ core/scanner.py (يعتمد على: models, rate_limiter, request_manager)
    │
    ├─→ modules/fingerprinting.py (يعتمد على: core/scanner)
    ├─→ modules/endpoint_discovery.py (يعتمد على: core/scanner, core/request_manager)
    ├─→ modules/subdomain_takeover.py (يعتمد على: core/scanner)
    ├─→ modules/crawler.py (يعتمد على: core/scanner, core/request_manager)
    │
    ├─→ modules/scoring.py (يعتمد على: config)
    │
    └─→ modules/graph_builder.py (يعتمد على: models)
```

---

## 📊 مقارنة الـ API القديم والجديد

| الشيء | النسخة القديمة | النسخة الجديدة |
|------|--------------|--------------|
| Entry point | `main.py` | `main_launcher.py` |
| Logging | متفرقة | `utils/logger.py` |
| Config | مشتتة | `config.py` |
| HTTP Requests | `HttpClient` مدمج | `core/request_manager.py` |
| Analyzers | كلاسات عديدة | `modules/fingerprinting.py` etc |
| Rate Limiting | `RateLimiter` بسيط | `core/rate_limiter.py` متقدم |
| Models | نماذج معرفة قديمة | `core/models.py` حديثة |

---

**تم إنشاء هذا المرجع لتسهيل الاستخدام والتطوير**
