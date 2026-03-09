# Project Structure and Architecture

## Directory Organization

```
hacked-tool/
├── src/                      # Source code
│   ├── core/                 # Core engine components
│   │   ├── engine.py        # Main application engine
│   │   ├── logger.py        # Logging system (Singleton)
│   │   ├── config_manager.py# Configuration management
│   │   ├── task_manager.py  # Task orchestration
│   │   ├── module_loader.py # Dynamic module loading
│   │   └── session_manager.py# Session state management
│   │
│   ├── modules/              # Scanning modules
│   │   ├── reconnaissance/   # Reconnaissance phase
│   │   │   └── fingerprinting.py
│   │   ├── scanning/         # Scanning phase
│   │   │   └── port_scanner.py
│   │   ├── analysis/         # Analysis phase
│   │   │   └── vulnerability_mapper.py
│   │   └── integrations/     # External integrations
│   │       └── external_connector.py
│   │
│   ├── plugins/              # Plugin system
│   │   ├── base_plugin.py   # Abstract plugin class
│   │   ├── plugin_manager.py# Plugin orchestration
│   │   └── __init__.py
│   │
│   └── utils/                # Utilities
│       ├── parser.py        # CLI argument parsing
│       ├── url_utils.py     # URL manipulation
│       ├── validators.py    # Input validation
│       └── __init__.py
│
├── config/                   # Configuration files
│   ├── settings.yaml        # Main settings
│   ├── modules.yaml         # Module configuration
│   └── logging.yaml         # Logging configuration
│
├── data/                     # Data files
│   ├── fingerprints/        # Technology fingerprints
│   │   └── technologies.json
│   └── patterns/            # Detection patterns
│
├── output/                   # Output directory
│   ├── logs/                # Log files
│   ├── reports/             # Scan reports
│   ├── graphs/              # Visualization data
│   └── exports/             # Data exports
│
├── tests/                    # Test suite
│   ├── test_core_engine.py  # Core engine tests
│   ├── test_modules.py      # Module tests
│   ├── test_utils.py        # Utility tests
│   └── __init__.py
│
├── docs/                     # Documentation
│   ├── architecture.md      # This file
│   ├── index.md             # Documentation index
│   └── *.md                 # Other docs
│
├── main.py                   # Legacy entry point
├── README.md                # Project readme
├── requirements.txt          # Dependencies
└── requirements_new.txt      # New dependencies
```

## Architecture Layers

### 1. Core Engine Layer (`src/core/`)
**Responsibility**: Central application control

- **engine.py**: Main orchestrator, coordinates all components
- **logger.py**: Centralized Singleton logging  
- **config_manager.py**: YAML-based configuration loading
- **task_manager.py**: Task creation, state management, tracking
- **module_loader.py**: Dynamic module discovery and loading
- **session_manager.py**: Session lifecycle and state tracking

### 2. Modules Layer (`src/modules/`)
**Responsibility**: Feature implementation

- **reconnaissance/**: Information gathering phase
- **scanning/**: Port and service scanning
- **analysis/**: Vulnerability and exploit mapping
- **integrations/**: External tool integration

### 3. Plugin System (`src/plugins/`)
**Responsibility**: Extensibility framework

- **base_plugin.py**: Abstract plugin interface
- **plugin_manager.py**: Plugin lifecycle management
- Modules can be loaded as plugins for better isolation

### 4. Utilities Layer (`src/utils/`)
**Responsibility**: Helper functions

- **parser.py**: CLI argument parsing
- **url_utils.py**: URL manipulation and normalization
- **validators.py**: Input validation

## Data Flow

```
User Input (CLI)
    ↓
Parser (src/utils/parser.py)
    ↓
Engine (src/core/engine.py)
    ↓
Config Manager (src/core/config_manager.py)
    ↓
Module Loader (src/core/module_loader.py)
    ↓
Plugin System (src/plugins/plugin_manager.py)
    ↓
Modules (src/modules/*/*)
    ↓
Task Manager (src/core/task_manager.py)
    ↓
Session Manager (src/core/session_manager.py)
    ↓
Output & Logging
```

## Configuration System

### YAML-Based Configuration

```yaml
# config/settings.yaml
scan_threads: 10
timeout: 30
log_level: INFO

# config/modules.yaml
reconnaissance:
  enabled: true
  modules:
    - fingerprinting
    - subdomain_analysis

# config/logging.yaml
level: INFO
format: '%(asctime)s - %(levelname)s - %(message)s'
file: output/logs/scan.log
```

## Plugin Architecture

### Plugin Lifecycle

1. **Discovery**: PluginManager scans `src/plugins/` for plugins
2. **Loading**: Dynamically imports plugins at runtime
3. **Validation**: Checks plugin meets BasePlugin interface
4. **Initialization**: Calls plugin.initialize()
5. **Execution**: Engine calls plugin.execute(target, options)
6. **Shutdown**: Calls plugin.shutdown() for cleanup

### Creating a Plugin

```python
from src.plugins import BasePlugin

class MyPlugin(BasePlugin):
    name = "My Plugin"
    version = "1.0.0"
    author = "Your Name"
    description = "What it does"
    
    def execute(self, target: str, options: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation
        return {'result': 'data'}
```

## Module Loading

### Dynamic Module Discovery

```
src/modules/
├── reconnaissance/
│   ├── __init__.py
│   └── fingerprinting.py     → reconnaissance.fingerprinting
├── scanning/
│   ├── __init__.py
│   └── port_scanner.py       → scanning.port_scanner
└── analysis/
    ├── __init__.py
    └── vulnerability_mapper.py → analysis.vulnerability_mapper
```

## Task Management

### Task Lifecycle

```
PENDING → RUNNING → COMPLETED/FAILED/CANCELLED

Task Properties:
- task_id: Unique identifier
- name: Human-readable name  
- module_name: Associated module
- status: Current status enum
- progress: 0-100 percentage
- result: Task output
- error: Error message if failed
- timestamps: start_time, end_time
```

## Session Management

### Session Lifecycle

```
INITIALIZED → RUNNING → PAUSED/COMPLETED/FAILED/CANCELLED

Session Properties:
- session_id: UUID
- target: Scanning target
- status: Current status
- results: Collected data
- errors: List of errors
- metadata: Custom data
- timestamps: created_at, started_at, ended_at
```

## Benefits of This Architecture

✅ **Modularity**: Clear separation of concerns
✅ **Extensibility**: Plugin system allows easy enhancement  
✅ **Maintainability**: Organized structure is easier to navigate
✅ **Scalability**: Components can scale independently
✅ **Testability**: Each component is independently testable
✅ **Reusability**: Utilities and plugins can be reused
✅ **Configuration**: YAML-based, no code changes needed
✅ **Logging**: Centralized Singleton logging throughout
✅ **Thread Safety**: Thread-safe managers with locking
✅ **Error Handling**: Proper exception handling at each layer
