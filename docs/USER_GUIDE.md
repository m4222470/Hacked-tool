# 🎓 دليل المستخدم الشامل - Hacked-tool v2.0.0

## 📖 مقدمة

**Hacked-tool** هي أداة متقدمة لاستطلاع الأصول (Asset Reconnaissance) واكتشاف الثغرات الأمنية على سطح الهجوم (Attack Surface). تجمع بين تقنيات المسح المتقدمة والذكاء الاصطناعي للكشف عن نقاط الضعف.

---

## ⚙️ التثبيت والإعداد

### 1. المتطلبات الأساسية
```bash
# Python 3.8+
python --version

# pip (package manager)
pip --version
```

### 2. تثبيت المكتبات
```bash
# استخدم requirements_new.txt للبنية الجديدة
pip install -r requirements_new.txt

# أو use requirements.txt للملف الأصلي
pip install -r requirements.txt
```

### 3. التحقق من التثبيت
```bash
# اختبر الاستيراد الأساسي
python -c "import requests; print('OK')"

# اختبر وحدات المشروع
python -c "from config import *; print('Config: OK')"
python -c "from utils.logger import logger; print('Logger: OK')"
```

---

## 🚀 طرق التشغيل

### الطريقة 1: الملف الأصلي (Legacy)
```bash
python main.py -d target.com
```

### الطريقة 2: البنية الجديدة (Modular) - قريباً
```bash
python main_launcher.py -d target.com
```

### الطريقة 3: استخدام الـ API برمجياً
```python
from core.scanner import ScanOrchestrator
from config import DEFAULT_SCORE_THRESHOLD_HIGH

orchestrator = ScanOrchestrator(threshold=DEFAULT_SCORE_THRESHOLD_HIGH)
results = orchestrator.scan("target.com")
```

---

## 📋 خيارات سطر الأوامر

### الخيارات الأساسية

```
-d, --domain DOMAIN (مطلوب)
    النطاق المراد فحصه
    مثال: target.com

--allowed DOMAIN (اختياري)
    النطاقات المسموح بفحصها
    مثال: target.com,api.target.com
    الافتراضي: نطاق واحد فقط

--max-concurrent NUMBER (اختياري)
    عدد الطلبات المتزامنة
    القيم: 1-50
    الافتراضي: 5
    ملاحظة: زيادة = أسرع لكن قد تزيد من الحمل

--rate-limit REQUESTS_PER_SECOND (اختياري)
    عدد الطلبات في الثانية
    القيم: 1-100
    الافتراضي: 10
```

### خيارات العتبات (Thresholds)

```
--threshold-high NUMBER (اختياري)
    عتبة الخطورة العالية (0-100)
    الافتراضي: 70
    مثال: --threshold-high 75

--threshold-medium NUMBER (اختياري)
    عتبة الخطورة المتوسطة (0-100)
    الافتراضي: 40
```

### خيارات الإخراج (Output)

```
-o, --output FILE (اختياري)
    ملف الإخراج (JSON)
    مثال: --output results.json
    الافتراضي: stdout

-f, --format FORMAT (اختياري)
    تنسيق الإخراج
    الخيارات: json, csv, html, txt
    الافتراضي: json
```

### خيارات التصحيح (Debug)

```
--debug
    تفعيل وضع التصحيح (verbose)
    يطبع معلومات تفصيلية حول كل خطوة

-v, --verbose
    إخراج مفصل أكثر

-q, --quiet
    إخراج محدود (errors فقط)
```

---

## 💡 أمثلة الاستخدام

### مثال 1: فحص بسيط
```bash
python main.py -d example.com
```

### مثال 2: فحص مع معايير مشددة
```bash
python main.py -d example.com \
  --threshold-high 80 \
  --threshold-medium 50 \
  --max-concurrent 10
```

### مثال 3: فحص نطاقات متعددة
```bash
python main.py -d example.com \
  --allowed example.com,api.example.com,admin.example.com
```

### مثال 4: فحص مع حد معدل منخفض (للخوادم الحساسة)
```bash
python main.py -d example.com \
  --rate-limit 2 \
  --max-concurrent 2
```

### مثال 5: فحص مع إخراج مفصل
```bash
python main.py -d example.com \
  --output results.json \
  --debug \
  --verbose
```

### مثال 6: فحص سريع (أقل جودة، أسرع)
```bash
python main.py -d example.com \
  --max-concurrent 20 \
  --rate-limit 50
```

---

## 📊 فهم النتائج

### بنية الإخراج JSON

```json
{
  "target": "example.com",
  "scan_date": "2025-03-08T12:34:56Z",
  "assets": [
    {
      "domain": "example.com",
      "score": 85,
      "severity": "HIGH",
      "technologies": ["WordPress", "Apache"],
      "endpoints": [
        {
          "url": "https://example.com/admin",
          "status": 403,
          "is_interesting": true,
          "score": 75
        }
      ],
      "vulnerabilities": [
        {
          "type": "ADMIN_PANEL_DETECTED",
          "severity": "MEDIUM",
          "description": "Admin panel accessible but protected",
          "url": "https://example.com/admin"
        }
      ]
    }
  ],
  "summary": {
    "total_assets": 5,
    "high_severity": 3,
    "medium_severity": 2,
    "low_severity": 1
  }
}
```

### شرح الحقول

| الحقل | المعنى | الأمثلة |
|------|--------|--------|
| `score` | درجة الخطورة (0-100) | 85 (خطير جداً) |
| `severity` | مستوى الخطورة | HIGH, MEDIUM, LOW |
| `technologies` | التكنولوجيات المكتشفة | WordPress, Apache, PHP |
| `status` | رمز الحالة HTTP | 200, 403, 500 |
| `is_interesting` | هل تستحق المزيد من الاهتمام؟ | true, false |

### تفسير الدرجات

| النطاق | التصنيف | الإجراء المقترح |
|--------|---------|-----------------|
| 80-100 | 🔴 حرج جداً | فحص فوري، إصلاح عاجل |
| 60-79 | 🟠 عالي | فحص تفصيلي، إصلاح قريب |
| 40-59 | 🟡 متوسط | فحص، إصلاح مخطط |
| 20-39 | 🟢 منخفض | راقب، إصلاح عند التحديث |
| 0-19 | ⚪ ضئيل جداً | توثيق، عادة آمن |

---

## 🔍 المميزات الرئيسية

### 1. المسح السريع (Fast Scanning)
- **التقنية:** ThreadPoolExecutor مع 20 عامل
- **الأداء:** 1000 URL في ~15 ثانية
- **الفائدة:** 40x أسرع من التسلسلي

### 2. التخفي (Traffic Camouflage)
- **التقنية:** User-Agent randomization + header shuffling
- **7 User-Agents مختلفة**
- **الفائدة:** تجنب الكشف من طرف WAF/IDS

### 3. اكتشاف التكنولوجيات (Technology Detection)
- **يكتشف:** WordPress, Laravel, Django, React, Node.js, وغيرها
- **المصادر:** HTTP headers, HTML patterns, JavaScript analysis
- **الفائدة:** تضييق نطاق البحث عن الثغرات

### 4. اكتشاف استيلاء Subdomains (Subdomain Takeover)
- **يكتشف:** هل Subdomain متروك وقابل للاستيلاء عليه؟
- **الخدمات:** GitHub, Heroku, AWS S3, Azure, وغيرها
- **الفائدة:** اكتشاف مشاكل الأمان الشديدة

### 5. اكتشاف Endpoints المخفية
- **يفحص:** admin panels, debug pages, backup files
- **يستخدم:** Smart crawling + regex analysis
- **الفائدة:** الكشف عن نقاط دخول غير متوقعة

### 6. اكتشاف المعاملات (Parameter Discovery)
- **يكتشف:** GET/POST/header parameters
- **يحلل:** JavaScript files و forms
- **الفائدة:** اكتشاف injection points محتملة

---

## 📁 هيكل المشروع المعماري

```
/workspaces/Hacked-tool/
├── main.py                    # Entry point الأصلي
├── main_launcher.py           # Entry point الجديد
├── config.py                  # الإعدادات المركزية
│
├── core/                      # محرك الفحص الأساسي
│   ├── scanner.py            # ScanOrchestrator, BaseAnalyzer
│   ├── request_manager.py    # HttpClient, CacheManager
│   ├── async_engine.py       # Async scanning engine
│   ├── rate_limiter.py       # Adaptive rate limiting
│   └── models.py             # Data models
│
├── modules/                   # وحدات الفحص المتخصصة
│   ├── fingerprinting.py     # Technology detection
│   ├── endpoint_discovery.py # Admin/hidden file detection
│   ├── subdomain_takeover.py # Subdomain takeover detection
│   ├── crawler.py            # Smart crawling engine
│   ├── scoring.py            # Scoring engine
│   └── graph_builder.py      # Endpoint graph & correlation
│
├── evasion/                   # تقنيات التخفي
│   ├── header_randomizer.py  # Header randomization
│   ├── user_agent_rotator.py # User-Agent rotation
│   └── proxy_manager.py      # Proxy management
│
├── utils/                     # دوال مساعدة
│   ├── logger.py             # Logging system
│   ├── parser.py             # CLI argument parsing
│   ├── validators.py         # URL/Parameter validation
│   └── url_utils.py          # URL manipulation
│
├── data/                      # ملفات البيانات
│   ├── fingerprints.json     # Technology signatures
│   ├── subdomains_patterns.json
│   └── user_agents.txt
│
└── output/                    # نتائج الفحص
    ├── reports/
    ├── graphs/
    └── logs/
```

---

## 🔧 تخصيص السلوك

### تغيير الإعدادات الافتراضية

**الملف:** `config.py` (سطور 1-50)

```python
# يمكنك تغيير:
DEFAULT_REQUEST_DELAY = 1  # التأخير بين الطلبات
MAX_THREADS = 10  # عدد الخيوط
TIMEOUT = 10  # مهلة الطلب
MAX_HTML_SIZE = 300000  # حد أقصى لحجم HTML
ADMIN_PATHS = [...]  # مسارات الإدارة المشبوهة
```

### إضافة தकनولوجيات جديدة

**الملف:** `data/fingerprints.json`

```json
{
  "my_custom_tech": {
    "headers": ["X-Custom-Header"],
    "patterns": ["<div class='my-app'>"],
    "score": 50
  }
}
```

---

## 🐛 استكشاف الأخطاء

### المشكلة: الأداة بطيئة جداً

**الحل:**
```bash
# زيادة الطلبات المتزامنة
python main.py -d example.com --max-concurrent 20

# زيادة معدل الطلبات
python main.py -d example.com --rate-limit 50

# الجمع بين الاثنين
python main.py -d example.com --max-concurrent 20 --rate-limit 50
```

### المشكلة: يتم حظر الطلبات

**الحل:**
```bash
# تقليل معدل الطلبات
python main.py -d example.com --rate-limit 5 --max-concurrent 2

# استخدام خيارات التخفي (قيد التطوير)
# python main.py -d example.com --use-proxy

# إضافة تأخيرات عشوائية (مدمج بالفعل)
```

### المشكلة: SSL certificate error

**الحل:** (تطبيق مضمون في الكود)
```python
# البرنامج يختبر SSL تلقائياً ويعطي درجات أقل للأخطاء
# لا تحتاج لتغيير شيء - البرنامج يتعامل معها
```

### المشكلة: نتائج غير دقيقة جداً

**الحل:**
```bash
# استخدم عتبات أعلى
python main.py -d example.com --threshold-high 80 --threshold-medium 60

# أعد المحاولة باستخدام أوقات مختلفة
```

---

## 📝 التسجيل في الملفات

### الملفات المُنتجة

```
logs/                         # مجلد الـ logs
├── scan_2025-03-08.log      # ملف log يومي
└── errors_2025-03-08.log    # أخطاء فقط
```

### قراءة الـ logs

```bash
# عرض آخر 50 سطر
tail -50 logs/scan_2025-03-08.log

# البحث عن أخطاء
grep "ERROR" logs/scan_2025-03-08.log

# تتبع عملية محددة
grep "example.com" logs/scan_2025-03-08.log
```

---

## 🔐 اعتبارات الأمان

### قبل الاستخدام

⚠️ **تأكد من:**
1. ✅ لديك إذن من صاحب النظام
2. ✅ استخدمت NDA/اتفاقية سرية إن لزم
3. ✅ تفهم التشريعات المحلية
4. ✅ وثقت جميع النشاطات

### أثناء الاستخدام

⚠️ **لا تفعل:**
1. ❌ لا تفحص شبكات لا تملكها
2. ❌ لا تخزن بيانات حساسة
3. ❌ لا تضغط بقوة على الخادم
4. ❌ لا تستخدمها لأغراض ضارة

---

## 📞 الدعم والموارد

### معلومات إضافية

- [README.md](README.md) - التوثيق الفني
- [ARCHITECTURE.html](ARCHITECTURE.html) - الرسم المعماري
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - حالة المشروع
- [COMPLETION_ROADMAP.md](COMPLETION_ROADMAP.md) - خطة الإكمال

### الأخطاء الشائعة

| الخطأ | السبب | الحل |
|------|------|------|
| `ModuleNotFoundError` | مكتبة مفقودة | `pip install -r requirements.txt` |
| `ConnectionError` | لا يوجد إنترنت | تحقق من الاتصال |
| `Timeout Error` | الخادم بطيء | زيادة timeout في config |
| `Permission Denied` | لا تملك الإذن | اطلب الإذن من الإدارة |

---

**تم إنشاء هذا الدليل لتسهيل استخدام Hacked-tool بفعالية وأمان**
