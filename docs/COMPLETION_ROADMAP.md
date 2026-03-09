# 🛣️ خطة الإكمال - Hacked-tool v2.0.0

## 📋 ملخص سريع

البنية المعمارية الأساسية جاهزة بنسبة 90%. الخطوة التالية هي **استخراج الـ classes من main.py وتنظيمها في الوحدات المتخصصة** ثم تكاملها.

**الوقت المتوقع:** 2-3 ساعات للبرمجة الماهرة
**الصعوبة:** متوسطة (copy-paste + تحديث imports)

---

## 🎯 الأهداف المرحلية

### المرحلة 1: استخراج Analyzers ⏳ (الأولوية: عالية جداً)

#### 1.1 استخراج BaseAnalyzer و AnalyzerRegistry
**الملف المصدر:** `main.py` (lines ~100-300)
**الوجهة:** `core/scanner.py`

```python
# ما يجب نقله:
- class BaseAnalyzer(ABC)
- class AnalyzerRegistry
- class ScanOrchestrator

# يجب استيراده من:
from config import *
from utils.logger import logger
from core.rate_limiter import AdaptiveRateLimiter
```

#### 1.2 استخراج HttpClient
**الملف المصدر:** `main.py` (lines ~400-500)
**الوجهة:** `core/request_manager.py`

```python
# ما يجب نقله:
- class HttpClient
- class CacheManager

# يجب استيراده من:
from config import *
from evasion.header_randomizer import get_random_headers
from core.rate_limiter import AdaptiveRateLimiter
```

#### 1.3 استخراج نماذج البيانات
**الملف المصدر:** `main.py` (lines ~50-150)
**الوجهة:** `core/models.py`

```python
# ما يجب نقله:
- class Asset
- class Endpoint
- class VulnProbabilities (struct تقريباً)

# لا يحتاج استيرادات معقدة
```

### المرحلة 2: استخراج Analyzers المتخصصة ⏳ (الأولوية: عالية)

#### 2.1 إنشاء modules/fingerprinting.py
```python
# ما يجب نقله:
- class SecurityHeadersAnalyzer(BaseAnalyzer)
- class AuthFlowAnalyzer(BaseAnalyzer)
- class TechDetectionAnalyzer(BaseAnalyzer)  # جديد

# استيرادات مطلوبة:
from core.scanner import BaseAnalyzer
from config import TECH_FINGERPRINTS
from utils.logger import logger
from data.fingerprints import load_technology_database()
```

#### 2.2 إنشاء modules/endpoint_discovery.py
```python
# ما يجب نقله:
- class HiddenFilesAnalyzer(BaseAnalyzer)
- class JavaScriptAnalyzer(BaseAnalyzer)
- class ParameterDiscoveryAnalyzer(BaseAnalyzer)

# استيرادات مطلوبة:
from core.scanner import BaseAnalyzer
from core.request_manager import HttpClient
from utils.logger import logger
```

#### 2.3 إنشاء modules/subdomain_takeover.py
```python
# ما يجب نقله:
- class SubdomainTakeoverAnalyzer(BaseAnalyzer)

# استيرادات مطلوبة:
from core.scanner import BaseAnalyzer
from core.request_manager import HttpClient
from utils.logger import logger
```

#### 2.4 إنشاء modules/crawler.py
```python
# ما يجب نقله:
- class SmartCrawler(BaseAnalyzer)

# استيرادات مطلوبة:
from core.scanner import BaseAnalyzer
from core.request_manager import HttpClient
from utils.logger import logger
```

### المرحلة 3: استخراج محركات الـ scoring والتحليل ⏳ (الأولوية: متوسطة)

#### 3.1 إنشاء modules/scoring.py
```python
# ما يجب نقله:
- class ScoringEngine
- class FeatureScorer

# استيرادات مطلوبة:
from config import *
from utils.logger import logger
```

#### 3.2 إنشاء modules/graph_builder.py
```python
# ما يجب نقله:
- class EndpointGraph
- class CorrelationEngine

# استيرادات مطلوبة:
from core.models import Endpoint
from utils.logger import logger
```

### المرحلة 4: التكامل والاختبار ⏳ (الأولوية: متوسطة)

#### 4.1 تحديث main_launcher.py
```python
# يجب أن يقوم بـ:
from core.scanner import ScanOrchestrator
from core.request_manager import HttpClient
from modules.fingerprinting import SecurityHeadersAnalyzer, TechDetectionAnalyzer
from modules.endpoint_discovery import HiddenFilesAnalyzer, ParameterDiscoveryAnalyzer
from modules.subdomain_takeover import SubdomainTakeoverAnalyzer
from modules.crawler import SmartCrawler
from modules.scoring import ScoringEngine

# المنطق:
1. Parser arguments
2. Initialize logger
3. Create registry
4. Register analyzers
5. Create orchestrator
6. Run scan
7. Output results
```

#### 4.2 تحديث main.py أو استبداله
```python
# الخيار 1: احتفظ بـ main.py كـ legacy
# الخيار 2: جعل main.py يستدعي main_launcher.py

if __name__ == "__main__":
    from main_launcher import main
    main()
```

---

## 📝 قائمة المهام التفصيلية

### Task 1: استخراج core/scanner.py
- [ ] نسخ BaseAnalyzer من main.py
- [ ] نسخ AnalyzerRegistry من main.py
- [ ] نسخ ScanOrchestrator من main.py
- [ ] تحديث جميع الـ imports
- [ ] اختبار import: `from core.scanner import BaseAnalyzer`

### Task 2: استخراج core/request_manager.py
- [ ] نسخ HttpClient من main.py
- [ ] نسخ CacheManager من main.py
- [ ] تحديث جميع الـ imports
- [ ] إضافة استيراد AdaptiveRateLimiter
- [ ] إضافة استيراد get_random_headers
- [ ] اختبار import: `from core.request_manager import HttpClient`

### Task 3: استخراج core/models.py
- [ ] نسخ class Asset من main.py
- [ ] نسخ class Endpoint من main.py
- [ ] نسخ class VulnProbabilities من main.py
- [ ] تحديث جميع الـ imports
- [ ] اختبار import: `from core.models import Asset`

### Task 4: استخراج modules/fingerprinting.py
- [ ] نسخ SecurityHeadersAnalyzer من main.py
- [ ] نسخ AuthFlowAnalyzer من main.py
- [ ] إضافة TechDetectionAnalyzer (جديد إن لزم)
- [ ] تحديث جميع الـ imports
- [ ] اختبار import: `from modules.fingerprinting import SecurityHeadersAnalyzer`

### Task 5: استخراج modules/endpoint_discovery.py
- [ ] نسخ HiddenFilesAnalyzer من main.py
- [ ] نسخ JavaScriptAnalyzer من main.py
- [ ] نسخ ParameterDiscoveryAnalyzer من main.py
- [ ] تحديث جميع الـ imports
- [ ] اختبار import: `from modules.endpoint_discovery import HiddenFilesAnalyzer`

### Task 6: استخراج modules/subdomain_takeover.py
- [ ] نسخ SubdomainTakeoverAnalyzer من main.py
- [ ] تحديث جميع الـ imports
- [ ] اختبار import: `from modules.subdomain_takeover import SubdomainTakeoverAnalyzer`

### Task 7: استخراج modules/crawler.py
- [ ] نسخ SmartCrawler من main.py
- [ ] تحديث جميع الـ imports
- [ ] اختبار import: `from modules.crawler import SmartCrawler`

### Task 8: استخراج modules/scoring.py
- [ ] نسخ ScoringEngine من main.py
- [ ] نسخ FeatureScorer من main.py
- [ ] تحديث جميع الـ imports
- [ ] اختبار import: `from modules.scoring import ScoringEngine`

### Task 9: استخراج modules/graph_builder.py
- [ ] نسخ EndpointGraph من main.py
- [ ] نسخ CorrelationEngine من main.py
- [ ] تحديث جميع الـ imports
- [ ] اختبار import: `from modules.graph_builder import EndpointGraph`

### Task 10: تحديث main_launcher.py
- [ ] استيراد جميع الوحدات الجديدة
- [ ] تحديث منطق الـ main function
- [ ] اختبار التشغيل: `python main_launcher.py --help`

### Task 11: تحديث main.py
- [ ] اجعله يستدعي main_launcher.py
- [ ] أو احتفظ بـ legacy script

### Task 12: الاختبار النهائي
- [ ] اختبر جميع الـ imports
- [ ] اختبر التشغيل: `python main_launcher.py -d example.com`
- [ ] تحقق من النتائج
- [ ] تحقق من الـ logs

---

## 🔧 خطوات التنفيذ العملية

### الخطوة 1: فهم الهيكل الحالي لـ main.py

```bash
# العد على عدد الـ classes والدوال
grep -n "^class " /workspaces/Hacked-tool/main.py
grep -n "^def " /workspaces/Hacked-tool/main.py
```

### الخطوة 2: استخراج كل class بشكل منفصل

```python
# مثال: استخراج BaseAnalyzer
# 1. افتح main.py
# 2. ابحث عن "class BaseAnalyzer"
# 3. انسخ الـ class بالكامل مع docstring
# 4. الصقه في الملف الجديد
# 5. حدّث الـ imports
# 6. اختبر import: python -c "from core.scanner import BaseAnalyzer; print('OK')"
```

### الخطوة 3: التحقق من الـ imports

```python
# في كل ملف جديد، أضف في الأعلى:
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ثم اختبر:
python -c "from core.scanner import BaseAnalyzer; print('Imports OK')"
```

### الخطوة 4: الاختبار المرحلي

```bash
# بعد كل استخراج جديد:
python -c "import core.scanner; print('core.scanner: OK')"
python -c "import core.request_manager; print('core.request_manager: OK')"
python -c "import modules.fingerprinting; print('modules.fingerprinting: OK')"
# ... وهكذا
```

---

## ✅ معايير الإكمال

سيعتبر المشروع **مكتملاً بنسبة 100%** عند:

- [ ] جميع 12 مهمة أعلاه مكتملة
- [ ] جميع الـ imports تعمل بدون أخطاء
- [ ] `python main_launcher.py --help` يعمل
- [ ] `python main_launcher.py -d example.com` يعمل (مع domain اختباري)
- [ ] جميع الـ logs تظهر بشكل صحيح
- [ ] النتائج تُحفظ بشكل صحيح
- [ ] التوثيق محدّث

---

## 🚀 التسريع المحتمل

يمكنك تسريع العملية بـ:

1. **استخدام editor macros** لاستبدال الـ imports الدفعي
2. **استخدام git bisect** للتحقق من الكود الأصلي
3. **کتابة script Python** لاستخراج الـ classes تلقائياً
4. **العمل بالتوازي** على ملفات مختلفة

### Script مقترح للاستخراج السريع:

```python
# extract_classes.py
import re
import sys

def extract_class(filename, class_name):
    with open(filename, 'r') as f:
        content = f.read()
    
    # استخراج class مع محتوياته
    pattern = rf'^class {class_name}.*?(?=^class |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        return match.group(0)
    return None

# الاستخدام:
if __name__ == "__main__":
    code = extract_class('main.py', 'BaseAnalyzer')
    if code:
        print(code)
```

---

## 📊 متابعة التقدم

| المرحلة | المهام | المكتمل | النسبة |
|--------|--------|---------|--------|
| المرحلة 1 | 3 | 0 | 0% |
| المرحلة 2 | 4 | 0 | 0% |
| المرحلة 3 | 2 | 0 | 0% |
| المرحلة 4 | 3 | 0 | 0% |
| **الإجمالي** | **12** | **0** | **0%** |

---

## 🔗 الروابط المهمة

- [README.md](README.md) - التوثيق الشامل
- [ARCHITECTURE.html](ARCHITECTURE.html) - الرسم المعماري
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - حالة المشروع
- [config.py](config.py) - الإعدادات المركزية
- [main.py](main.py) - الملف الأصلي (مصدر الاستخراج)

---

## ⚠️ ملاحظات مهمة

1. **لا تحذف main.py** - احتفظ به كـ reference ونسخة احتياطية
2. **احدّث الـ imports تدريجياً** - لا تحاول الكل مرة واحدة
3. **اختبر كل ملف جديد** - بعد كتابته مباشرة
4. **احتفظ بـ git history** - حتى تتمكن من الرجوع للخلف إذا لزم الأمر
5. **وثّق أي تغييرات كبيرة** - في docstrings والـ README

---

**تم إنشاء هذه الخطة بواسطة نظام التخطيط المتقدم**
