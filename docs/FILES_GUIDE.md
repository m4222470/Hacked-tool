# 📁 دليل الملفات الشامل

## 📊 خريطة الهيكل

```
Hacked-tool/
│
├── 📂 src/                          # كود المشروع الرئيسي
│   ├── 📂 core/                     # النظام الأساسي
│   │   ├── engine.py               # محرك التنسيق الرئيسي
│   │   ├── logger.py               # نظام السجلات
│   │   ├── config_manager.py       # مدير الإعدادات
│   │   ├── task_manager.py         # مدير المهام
│   │   ├── module_loader.py        # محمل الوحدات
│   │   ├── session_manager.py      # مدير الجلسات
│   │   └── __init__.py             # تهيئة الحزمة
│   │
│   ├── 📂 modules/                  # الوحدات الوظيفية
│   │   ├── 📂 reconnaissance/       # وحدات الاستطلاع
│   │   │   ├── fingerprinting.py   # كشف التقنيات
│   │   │   └── __init__.py
│   │   ├── 📂 scanning/             # وحدات المسح
│   │   │   ├── port_scanner.py     # فحص المنافذ
│   │   │   └── __init__.py
│   │   ├── 📂 analysis/             # وحدات التحليل
│   │   │   ├── vulnerability_mapper.py  # خريطة الثغرات
│   │   │   └── __init__.py
│   │   ├── 📂 integrations/         # وحدات التكاملات
│   │   │   ├── external_connector.py    # الموصلات الخارجية
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── 📂 plugins/                  # نظام الإضافات
│   │   ├── base_plugin.py          # الفئة الأساسية للإضافات
│   │   ├── plugin_manager.py       # مدير الإضافات
│   │   └── __init__.py
│   │
│   ├── 📂 utils/                    # الدوال المساعدة
│   │   ├── parser.py               # محلل الأوامر
│   │   ├── url_utils.py            # أدوات URL
│   │   ├── validators.py           # مدققات الصحة
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── 📂 config/                       # ملفات الإعدادات
│   ├── settings.yaml               # الإعدادات العامة
│   ├── modules.yaml                # إعدادات الوحدات
│   └── logging.yaml                # إعدادات السجلات
│
├── 📂 data/                         # البيانات الثابتة
│   └── 📂 fingerprints/
│       └── technologies.json       # قاعدة بيانات التقنيات
│
├── 📂 tests/                        # الاختبارات
│   ├── test_core_engine.py         # اختبارات النظام الأساسي
│   ├── test_modules.py             # اختبارات الوحدات
│   ├── test_utils.py               # اختبارات الأدوات
│   └── __init__.py
│
├── 📂 docs/                         # التوثيق
│   ├── INDEX.md                    # فهرس التوثيق
│   ├── ARCHITECTURE.md             # وثيقة المعمارية
│   ├── DETAILED_ANALYSIS.md        # التحليل المفصل
│   ├── IMPLEMENTATION_CHECKLIST.md # قائمة التحقق
│   ├── USAGE_GUIDE.md              # دليل الاستخدام
│   └── DEVELOPER_ROADMAP.md        # خريطة الطريق
│
├── 📂 output/                       # مخرجات المسح
│   ├── 📂 logs/                     # ملفات السجلات
│   ├── 📂 results/                  # نتائج المسح
│   ├── 📂 reports/                  # التقارير
│   └── 📂 exports/                  # الملفات المصدرة
│
├── main.py                          # نقطة الدخول الرئيسية
├── requirements.txt                 # المكتبات المطلوبة
├── README.md                        # دليل المشروع الأساسي
├── README_NEW.md                    # نسخة محدثة من README
└── .gitignore                       # ملف تجاهل Git
```

---

## 📄 شرح الملفات الرئيسية

### Core System (src/core/)

#### engine.py
- **الوصف**: محرك التنسيق الرئيسي للنظام
- **الفئات**: `Engine`
- **الدوال الرئيسية**:
  - `initialize()` - تهيئة المحرك والمكونات
  - `run_scan(target)` - تشغيل عملية مسح
  - `shutdown()` - إيقاف النظام بشكل آمن
- **الحجم**: ~60 سطر
- **الاستخدام**: نقطة الانطلاق الرئيسية للتطبيق

#### logger.py
- **الوصف**: نظام Singleton للسجلات
- **الفئات**: `LoggerManager`
- **الميزات**:
  - سجل على الملف والشاشة معاً
  - ترميز UTF-8
  - مستويات مختلفة (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **الحجم**: ~64 سطر
- **الاستخدام**: `logger.info("رسالة")`

#### config_manager.py
- **الوصف**: مدير الإعدادات الِقائم على YAML
- **الفئات**: `ConfigManager`
- **الميزات**:
  - تحميل من ملفات YAML
  - Singleton pattern
  - دعم أقسام متعددة
- **الحجم**: ~85 سطر
- **الملفات**: `config/settings.yaml`, `config/modules.yaml`, `config/logging.yaml`

#### task_manager.py
- **الوصف**: مدير دورة حياة المهام
- **الفئات**: `Task`, `TaskManager`
- **الحالات**: PENDING, RUNNING, COMPLETED, FAILED, CANCELLED
- **الميزات**:
  - تتبع التقدم
  - إدارة الأخطاء
  - آمن من التزامن (Thread-safe)
- **الحجم**: ~170 سطر

#### module_loader.py
- **الوصف**: محمّل الوحدات الديناميكي
- **الفئات**: `ModuleLoader`
- **الميزات**:
  - اكتشاف الوحدات تلقائياً
  - التحميل الديناميكي (importlib)
  - معالجة الأخطاء
- **الحجم**: ~85 سطر

#### session_manager.py
- **الوصف**: مدير الجلسات والحالة
- **الفئات**: `Session`, `SessionManager`
- **الحالات**: INITIALIZED, RUNNING, COMPLETED, FAILED
- **الميزات**:
  - تتبع الجلسات بـ UUID
  - حفظ النتائج والأخطاء
  - تتبع البيانات الوصفية
- **الحجم**: ~155 سطر

---

### Modules (src/modules/)

#### reconnaissance/fingerprinting.py
- **الوظيفة**: كشف التقنيات المستخدمة
- **يكتشف**:
  - أنظمة إدارة المحتوى (WordPress, Drupal, Joomla)
  - أطر العمل (Django, Laravel, .NET)
  - خوادم الويب (Apache, Nginx)
  - لغات البرمجة (PHP, Node.js, Python)
- **المصدر**: `data/fingerprints/technologies.json`

#### scanning/port_scanner.py
- **الوظيفة**: فحص المنافذ والخدمات
- **الميزات**:
  - Scanning متوازي
  - اكتشاف الخدمات
  - جمع معلومات Banner

#### analysis/vulnerability_mapper.py
- **الوظيفة**: خريطة الثغرات والعيوب الأمنية
- **يربط**:
  - CVEs
  - نقاط الضعف
  - Exploits
  - درجات المخاطر

#### integrations/external_connector.py
- **الوظيفة**: التكامل مع الخدمات الخارجية
- **يدعم**:
  - Shodan API
  - Censys API
  - URLhaus
  - واجهات خارجية أخرى

---

### Plugin System (src/plugins/)

#### base_plugin.py
- **الوصف**: الفئة الأساسية المجردة للإضافات
- **الدوال الإجبارية**:
  - `execute(target, options)` - تنفيذ الإضافة
  - `initialize()` - التهيئة
  - `shutdown()` - الإغلاق
- **الدوال الاختيارية**:
  - `get_info()` - معلومات الإضافة
  - `validate_config()` - تحقق من الإعدادات
  - `get_requirements()` - المتطلبات

#### plugin_manager.py
- **الوصف**: مدير دورة حياة الإضافات
- **الدوال الرئيسية**:
  - `discover_plugins()` - اكتشاف الإضافات
  - `load_plugin()` - تحميل إضافة معينة
  - `execute_plugin()` - تنفيذ إضافة
  - `enable_plugin()` / `disable_plugin()` - التفعيل
  - `list_plugins()` - قائمة الإضافات

---

### Utilities (src/utils/)

#### parser.py
- **الوصف**: محلل الأوامر السطرية
- **الخيارات**:
  - `-d, --domain` - النطاق المستهدف
  - `--allowed` - قائمة النطاقات المسموحة
  - `--delay` - التأخير بين الطلبات
  - `--max-concurrent` - الحد الأقصى للطلبات المتزامنة
  - `--timeout` - مهلة زمنية
  - `--output` - ملف الإخراج

#### url_utils.py
- **الوصف**: أدوات معالجة URLs
- **الدوال**:
  - `extract_domain()` - استخراج النطاق
  - `extract_path()` - استخراج المسار
  - `extract_parameters()` - استخراج المعاملات
  - `normalize_url()` - تطبيع URL
  - `is_same_domain()` - التحقق من نفس النطاق

#### validators.py
- **الوصف**: مدققات صحة الإدخال
- **الفئات**:
  - `URLValidator` - التحقق من URLs
  - `ParameterValidator` - التحقق من المعاملات

---

### Configuration (config/)

#### settings.yaml
```yaml
scan:
  threads: 10              # عدد الخيوط
  timeout: 30              # المهلة الزمنية
  rate_limit: 10           # حد معدل الطلبات
  max_concurrent: 5        # الحد الأقصى للتزامن
  verify_ssl: true         # التحقق من SSL
  output_format: json      # صيغة الإخراج
```

#### modules.yaml
```yaml
modules:
  reconnaissance:
    enabled: true
    fingerprinting:
      enabled: true
  scanning:
    enabled: true
    port_scanner:
      enabled: true
  analysis:
    enabled: true
  integrations:
    enabled: false
```

#### logging.yaml
```yaml
logging:
  level: INFO
  format: "[%(asctime)s] %(levelname)s: %(message)s"
  file: output/logs/scan.log
  max_file_size: 10485760    # 10MB
  backup_count: 5
```

---

### Tests (tests/)

#### test_core_engine.py
- **اختبارات**:
  - تهيئة المحرك
  - السجلات
  - مدير الإعدادات
  - مدير المهام
  - مدير الجلسات

#### test_modules.py
- **اختبارات**:
  - اكتشاف الوحدات
  - تحميل الوحدات
  - نظام الإضافات
  - الإضافات الأساسية

#### test_utils.py
- **اختبارات**:
  - أدوات URLs
  - التحقق من URLs
  - التحقق من المعاملات

---

### Documentation (docs/)

#### ARCHITECTURE.md
- شرح المعمارية الكاملة
- رسم بياني لتدفق البيانات
- شرح الطبقات الأربع
- 210+ سطر

#### DETAILED_ANALYSIS.md
- تحليل 9 المشاكل المعمارية
- قبل وبعد المقارنة
- أمثلة من الكود
- نقاط الضعف والحلول
- 400+ سطر

#### IMPLEMENTATION_CHECKLIST.md
- قائمة تحقق من التطبيقات
- 9/9 مشاكل محلولة
- 32/32 ملف مُنشأ
- 25+ اختبار موجود

#### USAGE_GUIDE.md
- دليل الاستخدام السريع
- أمثلة عملية
- كيفية إضافة Plugins
- كيفية إضافة Modules

#### DEVELOPER_ROADMAP.md
- خريطة الطريق الكاملة
- 4 مراحل للتطوير
- قائمة مهام مفصلة
- معايير الجودة

---

## 📊 إحصائيات الملفات

| الفئة | العدد | الأسطر | الغرض |
|-------|-------|--------|--------|
| Core Files | 7 | ~600 | النظام الأساسي |
| Module Files | 9 | ~450 | الوحدات الوظيفية |
| Plugin Files | 3 | ~200 | نظام الإضافات |
| Utility Files | 4 | ~300 | الدوال المساعدة |
| Test Files | 3 | ~500 | الاختبارات |
| Config Files | 3 | ~100 | الإعدادات |
| Docs Files | 5 | ~1500 | التوثيق |
| **الإجمالي** | **37** | **~3650** | |

---

## 🔗 المراجع والروابط

### الملفات المرتبطة بـ engine.py
```
engine.py
├── يستخدم: logger.py
├── يستخدم: config_manager.py
├── يستخدم: task_manager.py
├── يستخدم: module_loader.py
└── يستخدم: session_manager.py
```

### الملفات المرتبطة بـ plugin_manager.py
```
plugin_manager.py
├── يثقل: base_plugin.py
├── يحمل: src/modules/**/*.py
└── يسجل: logger.py
```

### الملفات المرتبطة بـ module_loader.py
```
module_loader.py
├── يكتشف: src/modules/
├── يحمل: plugin_manager.py
└── يسجل: logger.py
```

---

## 💾 إنشاء / تعديل الملفات

### لإضافة Plugins جديد
1. أنشئ ملفاً في `src/plugins/`
2. ورّث من `BasePlugin`
3. طبّق `execute()`
4. أضف اختبار في `tests/`

### لإضافة Module جديد
1. أنشئ مجلد في `src/modules/`
2. أنشئ `module_name.py`
3. ورّث من `BasePlugin`
4. أضف في إعدادات `config/modules.yaml`

### لإضافة Utility جديد
1. أنشئ ملفاً في `src/utils/`
2. أضف دوالاً مفيدة
3. اكتب اختبارات
4. وثّق في README

---

## 🎯 ملخص سريع

**اكتفِ بـ**:
- ✅ 32 ملف مُنشأ ومنظم
- ✅ 7 ملفات Core فقط
- ✅ 4 وحدات منطقية
- ✅ 25+ اختبار شامل
- ✅ معمارية احترافية

