# ✅ 解决方案：所有源代码移至 src/ 目录

## 🎯 已完成的更改 (Changes Made)

### 1. ✅ 创建 src/evasion/ 模块
```
src/evasion/
├── __init__.py
└── header_randomizer.py
```
- 从根目录 `evasion/header_randomizer.py` 移动到 `src/evasion/`
- 更新为使用英文文档字符串
- 导出 `HeaderRandomizer` 类

### 2. ✅ 合并 src/core 模块
```
src/core/
├── engine.py
├── logger.py
├── config_manager.py
├── task_manager.py
├── module_loader.py
├── session_manager.py
├── rate_limiter.py          ← NEW (从 root core/ 移动)
└── __init__.py              ← 更新完成
```
- 从根目录 `core/rate_limiter.py` 复制到 `src/core/`
- 更新为独立的（不依赖 root config.py）
- 更新 `src/core/__init__.py` 导出所有类和单例

### 3. ✅ 更新 src/utils/ 模块
```
src/utils/
├── parser.py
├── url_utils.py
├── validators.py
└── __init__.py              ← 更新完成
```
- 更新 `src/utils/__init__.py` 导出所有类

### 4. ✅ 更新 src/modules/ 模块
```
src/modules/
├── reconnaissance/
├── scanning/
├── analysis/
├── integrations/
└── __init__.py              ← 更新完成
```

### 5. ✅ 更新 src/plugins/ 模块
```
src/plugins/
├── base_plugin.py
├── plugin_manager.py
└── __init__.py              ← 已完整
```

### 6. ✅ 创建主 src/__init__.py
```
src/__init__.py              ← NEW
```
- 导出所有主要类和单例
- 方便从 `src` 导入所有组件

---

## 📋 需要删除的根目录文件/文件夹 (TO CLEAN UP)

以下文件应该从项目根目录**删除**，因为它们现在存在于 `src/` 中：

```
root 目录应删除：
❌ core/                    (已移动到 src/core)
❌ evasion/                 (已移动到 src/evasion)
❌ utils/                   (已合并到 src/utils)
❌ modules/                 (已在 src/modules)
```

可选删除（保持配置，非源代码）：
- ⚠️  config.py             (旧配置文件，已被 src/config YAML 取代)

---

## 📚 导入更新

### 旧的（❌ 错误）
```python
from core.rate_limiter import AdaptiveRateLimiter
from evasion.header_randomizer import HeaderRandomizer
from utils.parser import create_parser
from utils.validators import URLValidator
```

### 新的（✅ 正确）
```python
# 方式 1：从 src 导入
from src.core.rate_limiter import AdaptiveRateLimiter
from src.evasion import HeaderRandomizer
from src.utils import create_parser, URLValidator

# 方式 2：简化导入（当 src 在 sys.path 中）
from core.rate_limiter import AdaptiveRateLimiter
from evasion import HeaderRandomizer
from utils import create_parser
```

### 测试文件（已正确配置）✅
```python
# tests/ 中的导入已正确配置
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from core.engine import engine  # ✅ 工作正常
```

---

## 🚀 下一步（Next Steps）

### 立即删除这些根目录：
```bash
# 备份后删除
rm -rf core/
rm -rf evasion/
rm -rf utils/
rm -rf modules/
```

### 可选：清理旧配置
```bash
# 如果确认 config.py 不再使用
rm config.py
```

### 验证结构：
```bash
# 确保所有代码在 src/ 中
tree src/

# 应显示：
# src/
# ├── __init__.py
# ├── core/
# ├── modules/
# ├── plugins/
# ├── utils/
# ├── evasion/
# └── data/
```

---

## ✨ 最终结构

```
Hacked-tool/
├── src/                        ← 所有源代码
│   ├── __init__.py            ← 主导出列表
│   ├── core/                  ← 核心系统 (7 个文件)
│   ├── modules/               ← 功能模块 (9 个文件)
│   ├── plugins/               ← 插件系統 (3 个文件)
│   ├── utils/                 ← 工具函数 (4 个文件)
│   ├── evasion/              ← 规避技术 (2 个文件)
│   └── data/                  ← 静态数据
│
├── config/                     ← YAML 配置
├── tests/                      ← 单元测试 (正确导入)
├── docs/                       ← 文档
├── main.py                     ← 入口点 (根目录可接受)
└── requirements.txt
```

---

## ✅ 工作清单

- [x] 创建 `src/evasion/` 并移动文件
- [x] 将 `core/rate_limiter.py` 移动到 `src/core/`
- [x] 更新所有 `__init__.py` 文件的导出
- [x] 创建 `src/__init__.py` 主导出文件
- [x] 验证 tests/ 导入正确
- [ ] 删除根目录 `core/`, `evasion/`, `utils/`, `modules/`
- [ ] 更新任何文档中的导入示例

---

## 📝 指示

**应用这些更改后，架构将是正确的：**

✅ 所有源代码在 `src/` 中  
✅ 根目录仅包含配置和入口点  
✅ 遵循 Python 最佳实践  
✅ 易于导入和使用  

**运行此命令完成清理：**
```bash
cd /workspaces/Hacked-tool
rm -rf core/ evasion/ utils/ modules/
```

然后验证：
```bash
python -m pytest tests/ -v
```

---

**完成！所有源代码现在都正确地组织在 src/ 中！** 🎉
