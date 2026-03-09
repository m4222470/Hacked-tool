# 🔗 Professional Integration Layer
## Multi-Tool Orchestration Framework

---

## Overview

The **Integration Layer** provides a unified, standardized interface for orchestrating multiple security tools (Metasploit, Nuclei, Nmap, OpenVAS, etc.) as interchangeable components. This enables tool-agnostic workflows while maintaining extensibility.

---

## Architecture

```python
┌────────────────────────────────────────────────────────────┐
│  Application Layer                                         │
│  (Workflows, Reporting, UI)                               │
└────────────────────────┬─────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
┌────────────────────┐          ┌────────────────────┐
│  Unified API       │          │  Abstract Interfaces│
│  ├── standardize() │          │  ├── Scanner       │
│  ├── execute()     │          │  ├── Exploiter     │
│  ├── results()     │          │  ├── PostModule    │
│  └── cleanup()     │          │  └── Reporter      │
└────────────┬───────┘          └────────────────────┘
             │
             ▼
   ┌─────────────────────────┐
   │  Tool Registry          │
   │  ├── Tool Config        │
   │  ├── Connection Pool    │
   │  └── Health Monitor     │
   └──────────┬──────────────┘
              │
    ┌─────────┼─────────┬──────────┐
    │         │         │          │
    ▼         ▼         ▼          ▼
┌───────┐ ┌──────┐ ┌──────┐ ┌────────┐
│  MSF  │ │Nuclei│ │ Nmap │ │OpenVAS │
│ Conn. │ │ Conn.│ │ Conn.│ │ Conn.  │
└───────┘ └──────┘ └──────┘ └────────┘
```

---

## Abstract Interfaces

### 1. ToolConnector Base

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ToolConfig:
    """Standardized tool configuration."""
    name: str
    type: str                  # scanner, exploiter, analyzer, reporter
    version: str
    host: str
    port: int
    username: str = None
    password: str = None
    api_key: str = None
    verify_ssl: bool = True
    timeout: int = 60
    max_retries: int = 3
    options: Dict[str, Any] = None

class ToolConnector(ABC):
    """Abstract base class for all tool connectors."""
    
    def __init__(self, config: ToolConfig):
        self.config = config
        self.is_connected = False
        self.last_error = None
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to tool."""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Close connection."""
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """Verify tool is operational."""
        pass
    
    @abstractmethod
    def execute(self, operation: str, params: dict) -> Dict[str, Any]:
        """Execute operation on tool."""
        pass
    
    @abstractmethod
    def get_results(self, job_id: str) -> Dict[str, Any]:
        """Retrieve results."""
        pass
    
    @abstractmethod
    def normalize_output(self, raw_output: Any) -> Dict[str, Any]:
        """Convert tool output to standard format."""
        pass
```

### 2. Scanner Interface

```python
class ScannerInterface(ToolConnector):
    """Interface for vulnerability scanning tools."""
    
    @abstractmethod
    def scan_host(self, target: str, 
                  scan_type: str = 'comprehensive') -> str:
        """
        Scan target for vulnerabilities.
        
        Args:
            target: IP, CIDR, or hostname
            scan_type: quick, standard, comprehensive, aggressive
            
        Returns:
            job_id for async retrieval
        """
        pass
    
    @abstractmethod
    def get_vulnerabilities(self, job_id: str) -> List[dict]:
        """Get discovered vulnerabilities."""
        pass
    
    @abstractmethod
    def get_services(self, job_id: str) -> List[dict]:
        """Get service discovery results."""
        pass
    
    @abstractmethod
    def cancel_scan(self, job_id: str) -> bool:
        """Cancel running scan."""
        pass

# Standard vulnerability output format
@dataclass
class StandardVulnerability:
    """Normalized vulnerability record."""
    scanner_name: str
    cve_id: str
    severity: str              # critical, high, medium, low
    service: str               # http, ssh, smb
    version: str
    description: str
    remediation: str
    cvss_score: float
```

### 3. Exploiter Interface

```python
class ExploiterInterface(ToolConnector):
    """Interface for exploitation tools."""
    
    @abstractmethod
    def search_modules(self, criteria: dict) -> List[dict]:
        """
        Search for exploitation modules.
        
        criteria can include:
        {
            'cve': 'CVE-2021-44228',
            'software': 'Apache',
            'version': '2.4.49',
            'platform': 'linux'
        }
        """
        pass
    
    @abstractmethod
    def check_vulnerability(self, module: str, 
                           target: str, 
                           options: dict) -> bool:
        """Non-destructive test if vulnerability exists."""
        pass
    
    @abstractmethod
    def execute_exploit(self, module: str, 
                       target: str, 
                       options: dict,
                       payload: dict = None) -> str:
        """Execute exploit, return session/result ID."""
        pass
    
    @abstractmethod
    def get_exploit_results(self, session_id: str) -> dict:
        """Get exploitation results."""
        pass

@dataclass
class StandardExploitation:
    """Normalized exploitation result."""
    tool_name: str
    target: str
    module_name: str
    status: str                # success, partial, failed
    session_type: str          # shell, meterpreter, etc.
    session_id: str
    execution_time: float
    artifacts: List[str]       # Files/data collected
```

### 4. PostModule Interface

```python
class PostModuleInterface(ToolConnector):
    """Interface for post-exploitation modules."""
    
    @abstractmethod
    def run_post_module(self, session_id: str, 
                       module: str, 
                       options: dict) -> str:
        """Execute post-exploitation module."""
        pass
    
    @abstractmethod
    def get_post_results(self, job_id: str) -> dict:
        """Get post-module execution results."""
        pass
    
    @abstractmethod
    def list_available_post_modules(self, 
                                    session_type: str,
                                    category: str = None) -> List[dict]:
        """List available post-exploitation modules."""
        pass

@dataclass
class PostModuleResult:
    """Normalized post-module result."""
    tool_name: str
    session_id: str
    module_name: str
    category: str              # credentials, network, system
    data: Dict[str, Any]
    timestamp: datetime
```

---

## Tool Registry

```python
class ToolRegistry:
    """Central registry and management for all tools."""
    
    def __init__(self):
        self.tools = {}           # name -> ToolConnector
        self.configs = {}         # name -> ToolConfig
        self.health_status = {}   # name -> bool
    
    def register_tool(self, name: str, 
                     tool_class: type, 
                     config: ToolConfig) -> bool:
        """
        Register and initialize tool.
        
        Example:
            registry.register_tool(
                'msf1',
                MSFConnector,
                ToolConfig(
                    name='Metasploit',
                    host='localhost',
                    port=55552,
                    username='msf_user',
                    password='msf_pass'
                )
            )
        """
        pass
    
    def get_tool(self, name: str) -> Optional[ToolConnector]:
        """Get registered tool by name."""
        pass
    
    def get_tools_by_type(self, tool_type: str) -> List[ToolConnector]:
        """Get all tools of specific type (scanner, exploiter)."""
        pass
    
    def list_registered_tools(self) -> List[str]:
        """List all registered tool names."""
        pass
    
    def unregister_tool(self, name: str) -> bool:
        """Unregister and disconnect tool."""
        pass
    
    def health_check_all(self) -> Dict[str, bool]:
        """Check health of all registered tools."""
        pass
    
    def get_primary_tool(self, tool_type: str) -> Optional[ToolConnector]:
        """Get primary/default tool for type."""
        pass
    
    def get_backup_tool(self, tool_type: str) -> Optional[ToolConnector]:
        """Get backup tool if primary fails."""
        pass
```

---

## Unified API Layer

```python
class UnifiedToolAPI:
    """Single API for orchestrating all tools."""
    
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
    
    # ============= SCANNING =============
    
    def scan_target(self, target: str, 
                   scanner_preference: str = 'nmap',
                   scan_type: str = 'comprehensive') -> str:
        """Execute vulnerability scan."""
        pass
    
    def get_scan_results(self, scan_id: str) -> Dict[str, Any]:
        """Retrieve scan results in standard format."""
        pass
    
    def normalize_vulnerabilities(self, raw_vulns: List) -> List[StandardVulnerability]:
        """Convert any scanner output to standard format."""
        pass
    
    # ============= EXPLOITATION =============
    
    def find_exploits(self, vulnerability: StandardVulnerability) -> List[dict]:
        """Find available exploits for vulnerability."""
        pass
    
    def test_vulnerability(self, vulnerability: StandardVulnerability,
                          exploiter: str = 'msf') -> bool:
        """Non-destructive check if exploitable."""
        pass
    
    def exploit_target(self, vulnerability: StandardVulnerability,
                      exploiter: str = 'msf',
                      options: dict = None) -> StandardExploitation:
        """Execute exploit."""
        pass
    
    # ============= POST-EXPLOITATION =============
    
    def run_post_exploitation(self, session: str,
                             modules: List[str] = None) -> List[PostModuleResult]:
        """Execute post-exploitation modules."""
        pass
    
    def harvest_credentials(self, session: str) -> List[dict]:
        """Extract credentials from session."""
        pass
    
    def harvest_system_info(self, session: str) -> dict:
        """Extract system information."""
        pass
    
    # ============= CLEANUP =============
    
    def cleanup_session(self, session: str) -> bool:
        """Clean up artifacts from session."""
        pass
    
    def close_all_sessions(self) -> bool:
        """Close all active sessions."""
        pass
```

---

## Tool Implementations

### MSFConnector Implementation

```python
class MSFConnector(ExploiterInterface, PostModuleInterface):
    """Implementation of MSF RPC connector."""
    
    def __init__(self, config: ToolConfig):
        super().__init__(config)
        self.rpc = None
    
    def connect(self) -> bool:
        """Connect to msfrpcd."""
        # See MSF_CONNECTOR_DESIGN.md for details
        pass
    
    def normalize_output(self, raw_output: Any) -> Dict[str, Any]:
        """Convert MSF output to standard format."""
        pass
```

### NmapScanner Implementation

```python
class NmapConnector(ScannerInterface):
    """Implementation of Nmap scanner connector."""
    
    def __init__(self, config: ToolConfig):
        super().__init__(config)
    
    def scan_host(self, target: str, 
                  scan_type: str = 'comprehensive') -> str:
        """Run Nmap scan."""
        pass
    
    def get_vulnerabilities(self, job_id: str) -> List[dict]:
        """Extract vulnerabilities from Nmap results."""
        pass
    
    def normalize_output(self, raw_output: Any) -> Dict[str, Any]:
        """Convert Nmap XML to standard format."""
        pass
```

### NucleiConnector Implementation

```python
class NucleiConnector(ScannerInterface):
    """Implementation of Nuclei scanner connector."""
    
    def __init__(self, config: ToolConfig):
        super().__init__(config)
    
    def scan_host(self, target: str, 
                  scan_type: str = 'comprehensive') -> str:
        """Run Nuclei scan."""
        pass
    
    def get_vulnerabilities(self, job_id: str) -> List[dict]:
        """Extract vulnerabilities from Nuclei results."""
        pass
    
    def normalize_output(self, raw_output: Any) -> Dict[str, Any]:
        """Convert Nuclei JSON to standard format."""
        pass
```

---

## Failover & Redundancy

```python
class FailoverManager:
    """Handle tool failures and provide redundancy."""
    
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.failover_config = {}
    
    def set_failover(self, primary: str, backup: str):
        """Specify backup tool if primary fails."""
        pass
    
    def execute_with_failover(self, tool_type: str, 
                             operation: str, 
                             params: dict) -> Dict[str, Any]:
        """
        Execute operation with automatic failover.
        
        If primary fails, retry with backup tool.
        """
        pass
    
    def automatic_health_monitoring(self, check_interval: int = 60):
        """Periodically check tool health and trigger failover if needed."""
        pass
```

---

## Configuration Management

```python
# config.yaml
integration_layer:
  version: "1.0"
  
  tools:
    metasploit:
      type: exploiter
      class: MSFConnector
      config:
        host: localhost
        port: 55552
        username: msf_user
        password: ${MSF_PASSWORD}
    
    nmap:
      type: scanner
      class: NmapConnector
      config:
        binary_path: /usr/bin/nmap
    
    nuclei:
      type: scanner
      class: NucleiConnector
      config:
        binary_path: /usr/local/bin/nuclei
    
    openvas:
      type: scanner
      class: OpenVASConnector
      config:
        host: openvas.internal
        port: 9392
        username: admin
        password: ${OPENVAS_PASSWORD}
  
  failover:
    scanner:
      primary: nmap
      backup: nuclei
    exploiter:
      primary: metasploit
      backup: null
  
  timeouts:
    scan: 3600
    exploit: 600
    post_module: 300
```

---

## Usage Example

```python
from integration_layer import (
    ToolRegistry, ToolConfig, UnifiedToolAPI,
    MSFConnector, NmapConnector, NucleiConnector
)
import yaml

# Load configuration
with open('config.yaml') as f:
    config = yaml.safe_load(f)

# Initialize registry
registry = ToolRegistry()

# Register tools from config
for tool_name, tool_config in config['integration_layer']['tools'].items():
    if tool_config['type'] == 'scanner':
        tool_class = globals()[tool_config['class']]
        registry.register_tool(
            tool_name,
            tool_class,
            ToolConfig(**tool_config['config'])
        )

# Initialize unified API
api = UnifiedToolAPI(registry)

# ===== SCANNING =====
print("[*] Scanning target...")
scan_id = api.scan_target('192.168.1.100', scanner_preference='nmap')
vulnerabilities = api.get_scan_results(scan_id)

# ===== EXPLOITATION =====
for vuln in vulnerabilities:
    print(f"\n[*] Exploiting {vuln.cve_id}...")
    
    # Check if exploitable
    if api.test_vulnerability(vuln):
        result = api.exploit_target(vuln, exploiter='msf')
        if result.status == 'success':
            print(f"    [+] Session {result.session_id} opened!")
            
            # ===== POST-EXPLOITATION =====
            post_results = api.run_post_exploitation(result.session_id)
            for post_result in post_results:
                print(f"    [+] {post_result.module_name}: {len(post_result.data)} items")
```

---

## Benefits

1. **Tool-Agnostic** - Swap tools without workflow changes
2. **Standardized** - Common interface for all tools
3. **Extensible** - Add new tools by implementing interfaces
4. **Resilient** - Failover support for tool failures
5. **Observable** - Unified logging and monitoring
6. **Maintainable** - Single code path for each operation type

---

## Adding New Tool

```python
# Step 1: Implement interface
class NewToolConnector(ScannerInterface):
    def connect(self) -> bool:
        pass
    
    def scan_host(self, target: str, scan_type: str) -> str:
        pass
    
    # ... implement other methods

# Step 2: Register tool
registry.register_tool(
    'newtool',
    NewToolConnector,
    ToolConfig(name='NewTool', host='...')
)

# Step 3: Use unified API
api.scan_target('target', scanner_preference='newtool')
```

---

This integration layer enables professional multi-tool orchestration with minimal coupling between tools and workflows.
