# 🧩 Plugin System Architecture
## Dynamic Module Loading & Extension Framework

---

## Overview

The **Plugin System** enables dynamic loading of security modules (scanners, exploiters, analyzers, reporters) without modifying core code, providing extensibility while maintaining safety and stability.

---

## Architecture

```python
┌────────────────────────────────────────────────────────────┐
│  Core Application                                          │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │  Plugin System Manager         │
        │  ├── Discovery                 │
        │  ├── Loading                   │
        │  ├── Validation                │
        │  └── Lifecycle                 │
        └────────────┬───────────────────┘
                     │
        ┌────────────┴─────────┬─────────────┬─────────────┐
        │                      │             │             │
        ▼                      ▼             ▼             ▼
   ┌─────────┐         ┌──────────┐   ┌──────────┐   ┌──────────┐
   │ Scanner │         │Exploiter │   │ Analyzer │   │ Reporter │
   │ Plugins │         │ Plugins  │   │ Plugins  │   │ Plugins  │
   └─────────┘         └──────────┘   └──────────┘   └──────────┘
        │                      │             │             │
        ▼                      ▼             ▼             ▼
   ┌─────────┐         ┌──────────┐   ┌──────────┐   ┌──────────┐
   │ Registry│         │Registry  │   │ Registry │   │ Registry │
   └─────────┘         └──────────┘   └──────────┘   └──────────┘
        │                      │             │             │
        └──────────────────────┴─────────────┴──────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Plugin Database     │
                    │ ├── Metadata        │
                    │ ├── Dependencies    │
                    │ └── Configuration   │
                    └─────────────────────┘
```

---

## Plugin Structure

### Standard Plugin Directory Layout

```
plugins/
├── scanners/
│   ├── nmap_scanner/
│   │   ├── __init__.py
│   │   ├── plugin.yaml
│   │   ├── scanner.py           # Main code
│   │   ├── requirements.txt
│   │   └── README.md
│   └── nuclei_scanner/
│       ├── __init__.py
│       ├── plugin.yaml
│       ├── scanner.py
│       └── ...
│
├── exploiters/
│   ├── msf_exploiter/
│   │   ├── __init__.py
│   │   ├── plugin.yaml
│   │   ├── exploiter.py
│   │   └── ...
│
├── analyzers/
│   ├── credential_analyzer/
│   │   ├── __init__.py
│   │   ├── plugin.yaml
│   │   ├── analyzer.py
│   │   └── ...
│
└── reporters/
    ├── pdf_reporter/
    ├── json_reporter/
    └── ...
```

### Plugin Manifest (plugin.yaml)

```yaml
# plugins/scanners/nmap_scanner/plugin.yaml

metadata:
  name: "Nmap Scanner"
  version: "1.0.0"
  author: "Security Team"
  description: "Port and service scanning using Nmap"
  category: "scanner"
  
  # Plugin stability indicator
  stability: "stable"                  # stable, beta, experimental
  
  # Minimum required versions
  requires:
    python: "3.9+"
    core: "1.0.0+"

# Required dependencies
dependencies:
  - libnmap
  - python-nmap

# Plugin interface
interface:
  base_class: "ScannerInterface"
  module: "scanner"
  entry_point: "NmapScanner"

# Configuration schema
config:
  schema:
    binary_path:
      type: "string"
      default: "/usr/bin/nmap"
      description: "Path to Nmap executable"
    
    timeout:
      type: "integer"
      default: 3600
      description: "Scan timeout in seconds"
    
    aggressiveness:
      type: "enum"
      choices: [1, 2, 3, 4, 5]
      default: 3
      description: "Nmap -T flag (1-5)"

# Capabilities and features
capabilities:
  - port_scanning
  - service_detection
  - os_detection
  - vulnerability_detection

# Permissions required
permissions:
  - network_access
  - execute_system_commands
  - read_result_files

# Security sandbox rules
sandbox:
  allowed_system_calls:
    - execute_nmap
    - read_nmap_config
  
  blocked_operations:
    - accessing_credentials
    - modifying_core_files
  
  network_isolation: false

# Healthcheck
healthcheck:
  enabled: true
  interval: 300                      # Check every 5 minutes
  command: "nmap_scanner:healthcheck"
```

---

## Core Components

### 1. PluginLoader

```python
class PluginLoader:
    """Discover and load plugins dynamically."""
    
    def __init__(self, plugin_directories: List[str] = None):
        """
        Initialize plugin loader.
        
        Args:
            plugin_directories: Paths to search for plugins
        """
        self.plugin_dirs = plugin_directories or ['./plugins']
        self.loaded_plugins = {}
    
    def discover_plugins(self, plugin_type: str = None) -> List[dict]:
        """
        Discover available plugins.
        
        Args:
            plugin_type: 'scanner', 'exploiter', 'analyzer', 'reporter' or None for all
            
        Returns:
            List of plugin metadata
        """
        pass
    
    def load_plugin(self, plugin_name: str, 
                   plugin_type: str) -> bool:
        """
        Load specific plugin.
        
        Process:
        1. Find plugin directory
        2. Load plugin.yaml
        3. Validate manifest
        4. Check dependencies
        5. Import module
        6. Instantiate class
        7. Register plugin
        """
        pass
    
    def load_all_plugins(self, plugin_type: str = None) -> Dict[str, bool]:
        """Load all discovered plugins."""
        pass
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload running plugin."""
        pass
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """Reload plugin (for development)."""
        pass
```

### 2. PluginValidator

```python
class PluginValidator:
    """Validate plugin safety and correctness."""
    
    def __init__(self):
        pass
    
    def validate_manifest(self, manifest: dict) -> bool:
        """Verify plugin.yaml has required fields."""
        pass
    
    def validate_dependencies(self, dependencies: List[str]) -> bool:
        """Check all dependencies installed."""
        pass
    
    def validate_interface_compliance(self, plugin_class, 
                                     base_interface) -> bool:
        """Verify plugin implements required interface."""
        pass
    
    def security_scan(self, plugin_path: str) -> List[str]:
        """
        Scan plugin for security issues.
        
        Checks:
        - No hardcoded credentials
        - No eval()/exec() calls
        - No unauthorized file access
        - No network access outside sandbox
        - Check for known vulnerabilities
        """
        pass
    
    def check_permissions(self, plugin_path: str, 
                         requested_permissions: List[str]) -> bool:
        """Verify plugin doesn't exceed requested permissions."""
        pass
```

### 3. PluginRegistry

```python
class PluginRegistry:
    """Central registry of all plugins."""
    
    def __init__(self):
        self.plugins = {}           # name -> plugin instance
        self.plugin_metadata = {}   # name -> metadata
        self.plugin_types = {}      # type -> [plugin names]
    
    def register_plugin(self, name: str, 
                       plugin_instance: object, 
                       metadata: dict):
        """Register loaded plugin."""
        pass
    
    def get_plugin(self, name: str) -> object:
        """Retrieve plugin by name."""
        pass
    
    def get_plugins_by_type(self, plugin_type: str) -> List[object]:
        """Get all plugins of specific type."""
        pass
    
    def list_plugins(self, plugin_type: str = None, 
                    include_disabled: bool = False) -> List[dict]:
        """List all plugins with metadata."""
        pass
    
    def get_plugin_capabilities(self, name: str) -> List[str]:
        """Get capabilities of plugin."""
        pass
    
    def plugin_supports(self, name: str, 
                       capability: str) -> bool:
        """Check if plugin supports capability."""
        pass
    
    def disable_plugin(self, name: str) -> bool:
        """Temporarily disable plugin."""
        pass
    
    def enable_plugin(self, name: str) -> bool:
        """Re-enable disabled plugin."""
        pass
```

### 4. DependencyManager

```python
class DependencyManager:
    """Manage plugin dependencies."""
    
    def __init__(self):
        self.dependency_graph = {}
    
    def add_dependency(self, plugin_a: str, depends_on_plugin_b: str):
        """Track dependency between plugins."""
        pass
    
    def resolve_dependencies(self, plugin_name: str) -> List[str]:
        """Return ordered list of plugins to load first."""
        pass
    
    def detect_circular_dependencies(self) -> List[Tuple[str, str]]:
        """Find circular dependency issues."""
        pass
    
    def check_version_compatibility(self, plugin_name: str) -> bool:
        """Verify plugin version compatible with core."""
        pass
    
    def get_dependency_tree(self, plugin_name: str) -> dict:
        """Visualize dependency tree."""
        pass
```

### 5. PluginConfiguration

```python
class PluginConfiguration:
    """Manage plugin-specific configuration."""
    
    def __init__(self, config_file: str = 'plugins.json'):
        self.config_file = config_file
        self.configs = self._load()
    
    def set_config(self, plugin_name: str, 
                  settings: dict) -> bool:
        """Configure plugin."""
        pass
    
    def get_config(self, plugin_name: str) -> dict:
        """Retrieve plugin configuration."""
        pass
    
    def validate_config(self, plugin_name: str, 
                       config: dict) -> List[str]:
        """Verify configuration matches schema."""
        pass
    
    def reset_config(self, plugin_name: str) -> bool:
        """Reset to default configuration."""
        pass
    
    def save(self):
        """Persist configurations."""
        pass
```

### 6. PluginLifecycleManager

```python
class PluginLifecycleManager:
    """Manage plugin startup/shutdown lifecycle."""
    
    def __init__(self):
        self.plugin_states = {}     # name -> state
    
    def initialize(self, plugin_name: str) -> bool:
        """Call plugin.initialize() method."""
        pass
    
    def start(self, plugin_name: str) -> bool:
        """Call plugin.start() method."""
        pass
    
    def stop(self, plugin_name: str) -> bool:
        """Call plugin.stop() method."""
        pass
    
    def shutdown(self, plugin_name: str) -> bool:
        """Call plugin.shutdown() method for cleanup."""
        pass
    
    def get_state(self, plugin_name: str) -> str:
        """Get plugin state: uninitialized, initialized, running, stopped"""
        pass
    
    def wait_until_ready(self, plugin_name: str, 
                        timeout: int = 30) -> bool:
        """Wait for plugin to become ready."""
        pass
```

---

## Base Plugin Classes

### Scanner Plugin

```python
class ScannerPlugin(ScannerInterface):
    """Base class for scanner plugins."""
    
    def __init__(self, config: ToolConfig):
        super().__init__(config)
    
    # Lifecycle methods plugins override
    def initialize(self):
        """Plugin initialization."""
        pass
    
    def start(self):
        """Plugin startup."""
        pass
    
    def stop(self):
        """Plugin shutdown."""
        pass
    
    def healthcheck(self) -> bool:
        """Verify plugin is operational."""
        pass
    
    # Required interface methods
    def scan_host(self, target: str, scan_type: str) -> str:
        raise NotImplementedError()
    
    def get_vulnerabilities(self, job_id: str) -> List[dict]:
        raise NotImplementedError()

# Example concrete implementation
class CustomNmapScanner(ScannerPlugin):
    def scan_host(self, target: str, scan_type: str) -> str:
        # Implementation
        pass
```

### Exploiter Plugin

```python
class ExploiterPlugin(ExploiterInterface):
    """Base class for exploiter plugins."""
    
    def initialize(self):
        pass
    
    def start(self):
        pass
    
    def stop(self):
        pass
    
    def healthcheck(self) -> bool:
        pass
    
    # Required interface methods
    def execute_exploit(self, module: str, target: str, 
                       options: dict, payload: dict = None) -> str:
        raise NotImplementedError()
```

### Analyzer Plugin

```python
class AnalyzerPlugin(ABC):
    """Base class for analyzer plugins."""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
    
    def initialize(self):
        pass
    
    def analyze(self, data: dict) -> dict:
        """Analyze data and return insights."""
        raise NotImplementedError()
    
    def get_analytics(self) -> dict:
        """Return analysis results."""
        raise NotImplementedError()

# Example: Credential analyzer
class CredentialAnalyzerPlugin(AnalyzerPlugin):
    def analyze(self, credentials: List[dict]) -> dict:
        """Analyze credentials for strength, patterns, etc."""
        pass
```

### Reporter Plugin

```python
class ReporterPlugin(ABC):
    """Base class for reporter plugins."""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
    
    def generate_report(self, results: dict, 
                       output_path: str) -> bool:
        """Generate report in specific format."""
        raise NotImplementedError()

# Example: PDF reporter
class PDFReporterPlugin(ReporterPlugin):
    def generate_report(self, results: dict, output_path: str) -> bool:
        """Generate PDF report."""
        pass
```

---

## Plugin Discovery & Loading

```python
# Typical plugin loading flow
from plugin_system import PluginSystem

# Initialize system
plugin_system = PluginSystem(['./plugins', '/usr/local/lib/hackedtool'])

# Discover plugins
print("Discovering plugins...")
plugins = plugin_system.discover_plugins()

# Load specific plugin
print("Loading Nmap scanner...")
plugin_system.load_plugin('nmap_scanner', 'scanner')

# Get plugin instance
nmap = plugin_system.get_plugin('nmap_scanner')

# Use plugin through unified interface
config = ToolConfig(host='localhost', port=22)
results = nmap.scan_host('192.168.1.0/24')
```

---

## Plugin Sandbox & Security

```python
class PluginSandbox:
    """Execute plugins in restricted environment."""
    
    def __init__(self, plugin_name: str, 
                 allowed_operations: List[str] = None):
        self.plugin_name = plugin_name
        self.allowed_ops = allowed_operations or []
    
    def execute_plugin_method(self, method: str, 
                             *args, **kwargs) -> Any:
        """
        Execute plugin method in sandbox.
        
        Restrictions:
        - File system access limited
        - Network access controlled
        - System commands restricted
        - Resource limits enforced
        """
        pass
    
    def set_resource_limits(self, memory_mb: int = 512, 
                           cpu_cores: int = 2):
        """Limit plugin resource consumption."""
        pass
    
    def enable_audit_logging(self):
        """Log all plugin operations."""
        pass
```

---

## Plugin Configuration

```yaml
# plugins_config.yaml

plugins:
  enabled:
    - nmap_scanner
    - nuclei_scanner
    - msf_exploiter
    - credential_analyzer
    - pdf_reporter
  
  disabled:
    - experimental_scanner
  
  plugin_settings:
    nmap_scanner:
      timeout: 3600
      aggressiveness: 3
      enabled: true
    
    nuclei_scanner:
      timeout: 1800
      templates_path: /usr/local/nuclei-templates
      enabled: true
    
    msf_exploiter:
      timeout: 600
      payload_format: meterpreter
      enabled: true

  # Resource limits
  sandbox:
    memory_limit_mb: 512
    cpu_limit: 2
    network_allow_all: false
    file_access: restricted
```

---

## Creating Custom Plugin

```python
# plugins/scanners/custom_scanner/scanner.py

from plugin_system import ScannerPlugin, ToolConfig
from typing import List

class CustomScanner(ScannerPlugin):
    """Custom vulnerability scanner plugin."""
    
    def initialize(self):
        """Initialize scanner."""
        print(f"Initializing {self.config.name}")
    
    def start(self):
        """Start scanner."""
        print("Scanner started")
    
    def scan_host(self, target: str, 
                  scan_type: str = 'standard') -> str:
        """Execute scan."""
        # Implementation
        return "SCAN-001"
    
    def get_vulnerabilities(self, job_id: str) -> List[dict]:
        """Get scan results."""
        return [{
            'cve': 'CVE-2021-44228',
            'severity': 'critical',
            'service': 'http'
        }]
    
    def healthcheck(self) -> bool:
        """Verify operational."""
        return True
```

---

## Benefits

1. **Extensibility** - Add features without modifying core
2. **Modularity** - Each tool is self-contained
3. **Safety** - Sandboxed execution with permissions
4. **Maintainability** - Easier to maintain independent plugins
5. **Version Control** - Each plugin has own versioning
6. **Hot Reload** - Update plugins without restart (optional)

---

This plugin system provides a professional, secure framework for extending Hacked-tool with custom security modules while maintaining stability and safety.
