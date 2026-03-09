# 🛠️ دليل المطورين - Hacked-tool v2.0.0

## 🎯 مرحباً بالمطورين!

هذا الدليل يساعدك على المساهمة في تطوير Hacked-tool بفعالية.

---

## ⚡ البدء السريع

### 1. استنساخ وإعداد المشروع

```bash
# استنساخ المشروع
cd /workspaces
git clone <repository-url> Hacked-tool
cd Hacked-tool

# إنشاء virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows

# تثبيت المكتبات
pip install -r requirements_new.txt

# تثبيت أدوات التطوير
pip install pytest pylint black flake8 sphinx
```

### 2. فهم البنية الحالية

```bash
# عرض هيكل الملفات
tree -L 2 -I '__pycache__|*.pyc'

# فهم الملفات الرئيسية
cat config.py          # الإعدادات المركزية
cat core/rate_limiter.py  # مثال على module
cat utils/logger.py    # مثال على utility
```

### 3. اختبر التثبيت

```bash
# اختبر الاستيراد
python -c "from config import *; print('Config OK')"
python -c "from utils.logger import logger; print('Logger OK')"
python -c "from core.rate_limiter import AdaptiveRateLimiter; print('RateLimiter OK')"

# اختبر المشروع
python main.py --help
```

---

## 📚 فهم المعمارية

### الهيكل المعماري

```
Hacked-tool
├── config.py                 # الثوابت والإعدادات
├── main.py                   # Entry point الأصلي (Legacy)
├── main_launcher.py          # Entry point الجديد (Modern)
│
├── core/                     # محرك المسح الأساسي
│   ├── scanner.py           # ScanOrchestrator (قادم)
│   ├── request_manager.py   # HttpClient (قادم)
│   ├── rate_limiter.py      # ✅ مكتمل
│   ├── async_engine.py      # (قادم)
│   └── models.py            # (قادم)
│
├── modules/                  # وحدات متخصصة
│   ├── fingerprinting.py    # (قادم) - Tech Detection
│   ├── endpoint_discovery.py # (قادم) - Hidden Files
│   ├── subdomain_takeover.py # (قادم) - Subdomain Analysis
│   ├── crawler.py           # (قادم) - Smart Crawling
│   ├── scoring.py           # (قادم) - Risk Scoring
│   └── graph_builder.py     # (قادم) - Endpoint Graph
│
├── evasion/                  # تقنيات التخفي
│   ├── header_randomizer.py # ✅ مكتمل
│   └── (ملفات أخرى قادمة)
│
├── utils/                    # دوال مساعدة
│   ├── logger.py            # ✅ مكتمل
│   ├── parser.py            # ✅ مكتمل
│   ├── validators.py        # ✅ مكتمل
│   └── url_utils.py         # ✅ مكتمل
│
└── data/                     # ملفات البيانات
    └── fingerprints.json    # ✅ مكتمل
```

---

## 🎯 المهام الحالية

### المرحلة 1: استخراج الـ Analyzers (الأولوية: عالية جداً)

#### Task 1.1: استخراج core/scanner.py

**الملف المصدر:** `main.py` (lines ~100-300)
**الهدف:** استخراج `BaseAnalyzer` و `AnalyzerRegistry` و `ScanOrchestrator`

```python
# يجب أن يحتوي على:
class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, asset):
        pass

class AnalyzerRegistry:
    def register(self, analyzer):
        pass
    def get_analyzers(self):
        pass

class ScanOrchestrator:
    def scan(self, target):
        pass
```

**الاعتماديات:**
```python
from config import *
from utils.logger import logger
from core.rate_limiter import AdaptiveRateLimiter
# ... إلخ
```

**الاختبار:**
```bash
python -c "from core.scanner import BaseAnalyzer, AnalyzerRegistry, ScanOrchestrator; print('OK')"
```

#### Task 1.2: استخراج core/request_manager.py

**الملف المصدر:** `main.py` (lines ~400-500)

```python
# يجب أن يحتوي على:
class HttpClient:
    def request(self, url):
        pass

class CacheManager:
    def get(self, key):
        pass
    def set(self, key, value):
        pass
```

#### Task 1.3: استخراج core/models.py

```python
# يجب أن يحتوي على:
class Asset:
    domain: str
    score: float
    technologies: List[str]
    # ... إلخ

class Endpoint:
    url: str
    status: int
    # ... إلخ
```

---

## 🔧 معايير الكود

### Python Code Style

```python
# استخدم PEP 8
# 4 spaces للـ indentation
# max line length: 100 characters
# استخدم triple quotes للـ docstrings

def analyze_domain(domain: str) -> Dict[str, Any]:
    """
    تحليل النطاق وإرجاع النتائج
    
    Args:
        domain: النطاق المراد تحليله
        
    Returns:
        dict: النتائج المفصلة
        
    Raises:
        ValueError: إذا كان النطاق غير صحيح
    """
    if not domain:
        raise ValueError("Domain cannot be empty")
    
    return {"analyzed": True}
```

### Naming Conventions

```python
# Classes: PascalCase
class SecurityHeadersAnalyzer:
    pass

# Functions/Methods: snake_case
def analyze_headers(headers):
    return {}

# Constants: UPPER_CASE
DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3

# Private: _starting_with_underscore
_private_variable = "secret"

# Protected: _double_underscore_not_recommended
```

### Docstrings

```python
class MyAnalyzer(BaseAnalyzer):
    """تحليل الرؤوس الأمنية
    
    يفحص وجود رؤوس أمان مهمة مثل HSTS و CSP.
    
    Attributes:
        name (str): اسم المحلل
        priority (int): أولوية التنفيذ
    """
    
    def analyze(self, asset: Asset) -> AnalysisResult:
        """تحليل أصل
        
        Args:
            asset: الأصل المراد تحليله
            
        Returns:
            AnalysisResult: النتائج
            
        Raises:
            NetworkError: عند فشل الاتصال
        """
        pass
```

---

## 🧪 الاختبار

### أنواع الاختبارات

```bash
# اختبار الوحدة (Unit Tests)
pytest tests/test_validators.py -v

# اختبار التكامل (Integration Tests)
pytest tests/integration/ -v

# اختبار الأداء (Performance Tests)
pytest tests/performance/ --benchmark

# تغطية الاختبار (Coverage)
pytest --cov=. --cov-report=html
```

### كتابة اختبار جديد

```python
# tests/test_validators.py
import pytest
from utils.validators import URLValidator

class TestURLValidator:
    """اختبارات URL Validator"""
    
    def test_valid_domain(self):
        """اختبار نطاق صحيح"""
        assert URLValidator.is_valid_domain("example.com") == True
    
    def test_invalid_domain(self):
        """اختبار نطاق غير صحيح"""
        assert URLValidator.is_valid_domain("invalid..com") == False
    
    def test_normalize_domain(self):
        """اختبار تطبيع النطاق"""
        result = URLValidator.normalize_domain("www.Example.COM")
        assert result == "example.com"
    
    @pytest.mark.parametrize("domain", [
        "google.com",
        "github.com",
        "stackoverflow.com"
    ])
    def test_multiple_domains(self, domain):
        """اختبار نطاقات متعددة"""
        assert URLValidator.is_valid_domain(domain) == True
```

---

## 📝 عملية الـ Commit

### معايير رسائل الـ Commit

```bash
# الصيغة:
[TYPE] subject - description

# Types:
# feat - ميزة جديدة
# fix - إصلاح bug
# docs - تحديث توثيق
# refactor - إعادة تنظيم كود
# test - إضافة tests
# perf - تحسين أداء

# الأمثلة:
git commit -m "[feat] Add tech detection analyzer"
git commit -m "[fix] Rate limiter not handling 429 correctly"
git commit -m "[docs] Update README with examples"
```

### Commit Checklist

- [ ] الكود يتبع معايير Style
- [ ] أضفت tests إن لزم
- [ ] أضفت docstrings
- [ ] الـ imports منـظمة بشكل صحيح
- [ ] لا توجد typos أو errors
- [ ] الـ commit message واضح

---

## 🔄 سير العمل

### الخطوات الموصى بها

```
1. ابدأ من issue/task
2. أنشئ فرع جديد
   git checkout -b feature/thing-name

3. طور الميزة
   - اكتب الكود
   - أضف tests
   - أضف docs

4. اختبر محلياً
   pytest
   python -m pylint core/scanner.py
   python -m black --check .

5. اجعل الكود منسقاً
   python -m black .
   python -m pylint core/scanner.py --fix

6. اجعل commit صحيح
   git add -A
   git commit -m "[type] message"

7. ادفع للخادم وأنشئ PR
   git push origin feature/thing-name
```

---

## 🚀 أفكار للمساهمات المختلفة

### للمبتدئين

- [ ] إضافة المزيد من التكنولوجيات إلى `data/fingerprints.json`
- [ ] تحسين التعليقات والـ docstrings
- [ ] إصلاح الـ typos والـ grammar
- [ ] إضافة unit tests للـ utilities الموجودة

### للمتوسطين

- [ ] استخراج `modules/fingerprinting.py`
- [ ] تحسين `utils/validators.py`
- [ ] إضافة المزيد من evasion techniques
- [ ] تحسين نظام الـ logging

### للمتقدمين

- [ ] إنشاء `core/async_engine.py`
- [ ] تطوير `modules/graph_builder.py`
- [ ] تحسين الأداء (profiling + optimization)
- [ ] إضافة دعم الـ plugins

---

## 🐛 Find and Fix Bugs

### طرق اكتشاف الأخطاء

```bash
# استخدم pylint للتحليل الثابت
pylint core/rate_limiter.py

# استخدم flake8 للأسلوب
flake8 utils/

# استخدم mypy للـ type checking
mypy core/

# استخدم pytest للاختبارات
pytest tests/ -v
```

### الإبلاغ عن Bug

عند اكتشاف خطأ:

```markdown
## Bug Report

**الوصف:**
أصف المشكلة بوضوح

**خطوات التكرار:**
1. افعل الخطوة الأولى
2. افعل الخطوة الثانية
3. الخطأ يحدث بعد ذلك

**السلوك المتوقع:**
ماذا يجب أن يحدث

**السلوك الفعلي:**
ماذا يحدث فعلاً

**معلومات الإصدار:**
- Python: 3.9.1
- OS: Ubuntu 20.04
- Platform: Linux
```

---

## 📊 Profiling والأداء

### مثال على profiling

```python
import cProfile
import pstats
from io import StringIO

# الكود الذي تريد profiling
def expensive_function():
    result = 0
    for i in range(1000000):
        result += i
    return result

# تشغيل profiler
profiler = cProfile.Profile()
profiler.enable()

expensive_function()

profiler.disable()

# عرض النتائج
stats = pstats.Stats(profiler, stream=StringIO())
stats.sort_stats('cumulative')
print(stats.rstrip())
```

### معايير الأداء

```
مقاييس الأداء المطلوبة:
- 1000 URLs في أقل من 20 ثانية
- استهلاك ذاكرة < 500 MB
- CPU usage < 80%
- Response time < 100ms (لكل request)
```

---

## 🎓 موارد التعلم

### قراءة موصى بها

- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)

### مشاريع مشابهة

- [OWASP ZAP](https://www.zaproxy.org/)
- [Nuclei](https://github.com/projectdiscovery/nuclei)
- [Amass](https://github.com/OWASP/Amass)

---

## 🎯 الخطوات التالية

### المهام الحالية (الأسبوع القادم)

```
Priority: CRITICAL
[ ] استخراج core/scanner.py
[ ] استخراج core/request_manager.py
[ ] استخراج core/models.py

Priority: HIGH
[ ] استخراج modules/fingerprinting.py
[ ] استخراج modules/endpoint_discovery.py
[ ] تحديث main_launcher.py

Priority: MEDIUM
[ ] إضافة unit tests شاملة
[ ] تحسين التوثيق
[ ] تحسين الأداء
```

---

## 📞 للمساعدة

### إذا احتجت مساعدة

1. اقرأ التوثيق الموجودة
2. ابحث في issues الموجودة
3. اسأل في discussions
4. أنشئ issue جديدة إن لزم

---

## 🎉 شكراً للمساهمة!

شهادة تقدير لكل من يساهم في تحسين Hacked-tool.

---

**آخر تحديث:** 8 مارس 2025

👉 **ابدأ الآن:** اختر مهمة من المهام أعلاه وابدأ العمل

الكود جميل، والمساهمة سهلة!
