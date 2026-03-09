# 🚀 دليل الاستخدام السريع - المعمارية الجديدة

## التثبيت والتشغيل

### 1. التثبيت
```bash
cd /workspaces/Hacked-tool
pip install -r requirements.txt pyyaml pytest
```

### 2. تشغيل الاختبارات
```bash
# تشغيل جميع الاختبارات
pytest tests/

# تشغيل اختبار محدد
pytest tests/test_core_engine.py

# مع التفاصيل
pytest tests/ -v
```

### 3. استخدام المحرك
```python
from src.core.engine import engine

# تهيئة
engine.initialize()

# تشغيل مسح
results = engine.run_scan('example.com')

# إيقاف
engine.shutdown()
```

---

## البنية المعمارية الجديدة

### مثال: إضافة Plugin جديد

#### الخطوة 1: إنشاء الملف
```python
# src/plugins/my_plugin.py

from src.plugins import BasePlugin
from typing import Dict, Any

class MyPlugin(BasePlugin):
    name = "My Plugin"
    version = "1.0.0"
    author = "Your Name"
    description = "What it does"
    
    def execute(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the plugin"""
        return {
            'target': target,
            'result': 'success',
            'data': []
        }
```

#### الخطوة 2: تحميل واستخدام
```python
from src.plugins.plugin_manager import plugin_manager

# تحميل
plugin_manager.load_plugin('my_plugin')

# التشغيل
result = plugin_manager.execute_plugin('my_plugin', 'example.com')

# قائمة
plugins = plugin_manager.list_plugins()
```

---

## مثال: إضافة Module جديد

### الهيكل
```
src/modules/reconnaissance/
├── __init__.py
├── fingerprinting.py
└── my_new_analyzer.py
```

### الكود
```python
# src/modules/reconnaissance/my_new_analyzer.py

from src.plugins import BasePlugin

class MyAnalyzerModule(BasePlugin):
    name = "My Analyzer"
    
    def execute(self, target, options=None):
        # Implementation
        return {'target': target, 'findings': []}
```

---

## مثال: استخدام Config Manager

```python
from src.core.config_manager import config_manager

# الحصول على إعدادات
settings = config_manager.get('settings')
timeout = config_manager.get('settings', 'timeout')  # 30

# تعديل الإعدادات (Loading من YAML)
modules_config = config_manager.get('modules')
```

---

## مثال: استخدام Task Manager

```python
from src.core.task_manager import task_manager, TaskStatus

# إنشاء task
task = task_manager.create_task('scan-001', 'Scan', 'scanner', {})

# تحديث الحالة
task_manager.update_task_status('scan-001', TaskStatus.RUNNING)
task_manager.update_task_progress('scan-001', 50)

# النتيجة
task_manager.set_task_result('scan-001', {'result': 'data'})
task_manager.update_task_status('scan-001', TaskStatus.COMPLETED)

# عرض
task = task_manager.get_task('scan-001')
print(task.to_dict())
```

---

## مثال: استخدام Session Manager

```python
from src.core.session_manager import session_manager

# إنشاء جلسة
session = session_manager.create_session('example.com', {})
session_id = session.session_id

# بدء الجلسة
session_manager.start_session(session_id)

# إضافة نتائج
session_manager.add_result(session_id, 'technologies', ['WordPress', 'Apache'])

# إكمال الجلسة
session_manager.complete_session(session_id)

# عرض الجلسة
session = session_manager.get_session(session_id)
print(session.to_dict())
```

---

## مثال: استخدام Module Loader

```python
from src.core.module_loader import module_loader

# اكتشاف الوحدات
modules = module_loader.discover_modules()
print(f"Found modules: {modules}")

# تحميل وحدة محددة
module_loader.load_module('reconnaissance.fingerprinting')

# تحميل جميع الوحدات
count = module_loader.load_all_modules()
print(f"Loaded {count} modules")

# استخدام الوحدة
fingerprinting_module = module_loader.get_module('reconnaissance.fingerprinting')
```

---

## مثال: استخدام Logging

```python
from src.core.logger import logger

logger.info("Application started")
logger.debug("Debug information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical error")

# يتم حفظه في: output/logs/scan_YYYYMMDD.log
# وطباعته على الشاشة
```

---

## معايير الترميز

### Type Hints
```python
from typing import Dict, List, Optional, Any

def process_target(target: str, options: Dict[str, Any]) -> List[Dict]:
    """Process target.
    
    Args:
        target: Target domain
        options: Configuration options
        
    Returns:
        List of findings
    """
    pass
```

### Docstrings
```python
def execute(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
    """Execute plugin against target.
    
    Long description here...
    
    Args:
        target: Target domain or IP
        options: Optional configuration
        
    Returns:
        Dictionary with results
        
    Raises:
        ValueError: If target is invalid
    """
    pass
```

### Error Handling
```python
try:
    result = plugin.execute(target)
except ValueError as e:
    logger.error(f"Invalid target: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

---

## اختبار الكود الجديد

### كتابة اختبار
```python
# tests/test_my_feature.py

import unittest
from src.plugins.my_plugin import MyPlugin

class TestMyPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = MyPlugin()
    
    def test_execute(self):
        result = self.plugin.execute('example.com')
        self.assertIn('target', result)
    
    def test_plugin_info(self):
        info = self.plugin.get_info()
        self.assertEqual(info['name'], 'My Plugin')

if __name__ == '__main__':
    unittest.main()
```

### تشغيل الاختبار
```bash
pytest tests/test_my_feature.py -v
```

---

## الهيكل الملخص

```
hacked-tool/
├── src/core/              ← النظام الأساسي (Engine)
├── src/modules/           ← الوحدات المنطقية
├── src/plugins/           ← نظام الإضافات
├── src/utils/             ← الدوال المساعدة
├── config/                ← الإعدادات YAML
├── data/                  ← البيانات الثابتة
├── tests/                 ← الاختبارات
├── docs/                  ← التوثيق
├── output/                ← المخرجات
├── main.py                ← نقطة الدخول
└── requirements.txt       ← المكتبات
```

---

## الأوامر الشائعة

```bash
# تشغيل جميع الاختبارات
pytest tests/

# تشغيل مع التفاصيل
pytest tests/ -v -s

# تشغيل ملف اختبار واحد
pytest tests/test_core_engine.py

# تشغيل اختبار واحد
pytest tests/test_core_engine.py::TestEngine::test_engine_initialization

# المراقبة (reload on change)
pytest-watch tests/

# بتقرير التغطية
pytest tests/ --cov=src/

# تشغيل البرنامج
python main.py -d example.com

# مع الـ Debug
python main.py -d example.com --debug
```

---

## حل المشاكل الشائعة

### "ModuleNotFoundError"
```python
# ✅ الحل:
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.engine import engine
```

### "Config not found"
```python
# ✅ تحقق من وجود config/settings.yaml
ls config/

# إنشاء من جديد إذا لزم
from src.core.config_manager import config_manager
config_manager = ConfigManager()  # ستُنشئ الإعدادات الافتراضية
```

### "Plugin not loading"
```python
# ✅ تحقق من inherit من BasePlugin
class MyPlugin(BasePlugin):  # ✅ صحيح
    pass

# ❌ خطأ:
class MyPlugin:             # ❌ تابع من object
    pass
```

---

**الآن أنت مستعد لاستخدام المعمارية الجديدة!** 🎉
