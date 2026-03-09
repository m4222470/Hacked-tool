"""
Configuration manager - Load and manage all configurations
Handles both YAML files and default Python constants
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Centralized configuration management with defaults"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Load configurations from config directory"""
        self.config = {}
        self.config_dir = Path(__file__).parent.parent.parent / 'config'
        
        # Apply default constants first
        self._set_defaults()
        
        # Create default config if doesn't exist
        if not self.config_dir.exists():
            self.config_dir.mkdir(exist_ok=True, parents=True)
            self._create_default_configs()
        
        # Load YAML files (overrides defaults if present)
        self._load_all_configs()
    
    def _set_defaults(self):
        """Set all default configuration constants"""
        self.config = {
            # Request settings
            'REQUEST_TIMEOUT': 10,
            'MAX_CONCURRENT_REQUESTS': 20,
            'DEFAULT_REQUEST_DELAY': 1,
            'DEFAULT_RATE_LIMIT': 10,
            'DEFAULT_MAX_CONCURRENT': 5,
            
            # Crawling settings
            'CRAWL_DEPTH': 3,
            'MAX_CRAWLED_PAGES': 50,
            'MAX_JS_DOMAINS': 0,
            'MAX_HIDDEN_CHECKS': 100,
            
            # Retry settings
            'RETRY_COUNT': 2,
            'RETRY_BACKOFF': 0.5,
            
            # SSL settings
            'VERIFY_SSL_DEFAULT': True,
            'SSL_ISSUE_SCORE': 2,
            
            # Logging
            'LOG_LEVEL': 'INFO',
            'LOG_FILE': 'output/logs/scan.log',
            'OUTPUT_FORMAT': 'json',
            'OUTPUT_FILE': 'output/reports/results_final.json',
            
            # Scoring settings
            'DEFAULT_SCORE_THRESHOLD_HIGH': 70,
            'DEFAULT_SCORE_THRESHOLD_MEDIUM': 40,
            'SMALL_CONTENT_LENGTH': 500,
            'LOW_LATENCY_THRESHOLD': 0.3,
            
            # Scoring weights
            'SURFACE_WEIGHT': 0.25,
            'STRUCTURAL_WEIGHT': 0.5,
            'BEHAVIORAL_WEIGHT': 0.25,
            
            # Timeout settings
            'DEFAULT_GLOBAL_TIMEOUT': 600,
            'CONNECTION_TIMEOUT': 10,
            
            # Size settings
            'MAX_HTML_SIZE': 300000,
            'MAX_JS_FILE_SIZE': 200000,
            'MAX_CACHE_SIZE': 1000,
            
            # Security settings
            'RANDOMIZE_HEADERS': True,
            'ROTATE_USER_AGENTS': True,
            'USE_ADAPTIVE_THROTTLING': True,
            'ADAPTIVE_DELAY_ON_429': 0.5,
            
            # Tool info
            'TOOL_VERSION': '2.0.0',
            'TOOL_NAME': 'Hacked-tool (Professional Reconnaissance Scanner)',
            'AUTHOR': 'Security Research Team',
            'DESCRIPTION': 'أداة متقدمة للكشف عن الأصول والثغرات في سطح الهجوم',
            
            # Common parameters
            'COMMON_PARAMETERS': [
                'id', 'user_id', 'admin', 'debug', 'internal', 'token', 'api_key',
                'secret', 'password', 'email', 'role', 'group', 'permission',
                'version', 'env', 'test', 'stage', 'prod', 'verbose', 'output',
                'format', 'callback', 'redirect', 'url', 'fetch', 'load', 'query'
            ],
            
            # HTTP status codes
            'VALID_STATUS_CODES': {200, 201, 202, 204, 301, 302, 307, 308, 401, 403, 405, 406, 409, 410, 415, 429, 500, 501, 502, 503},
            'WARNING_STATUS_CODES': {301, 302, 307, 308, 429, 500, 501, 502, 503},
            'PROTECTED_STATUS_CODES': {401, 403, 405},
        }
    
    def _create_default_configs(self):
        """Create default configuration files"""
        # Default settings
        settings_yaml = {
            'scan_threads': 10,
            'timeout': 30,
            'log_level': 'INFO',
            'rate_limit': 10,
            'max_concurrent': 5,
        }
        
        # Default modules
        modules_yaml = {
            'reconnaissance': {'enabled': True},
            'scanning': {'enabled': True},
            'analysis': {'enabled': True},
            'fingerprinting': {'enabled': True},
        }
        
        # Default logging
        logging_yaml = {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': 'output/logs/scan.log',
        }
        
        # Write defaults
        self._write_yaml(self.config_dir / 'settings.yaml', settings_yaml)
        self._write_yaml(self.config_dir / 'modules.yaml', modules_yaml)
        self._write_yaml(self.config_dir / 'logging.yaml', logging_yaml)
    
    
    def _load_all_configs(self):
        """Load all configuration files and merge with defaults"""
        if self.config_dir.exists():
            for yaml_file in self.config_dir.glob('*.yaml'):
                section = yaml_file.stem
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        yaml_config = yaml.safe_load(f) or {}
                        if section == 'settings':
                            # Merge settings into root config
                            self.config.update(yaml_config)
                        else:
                            # Keep other sections separate
                            self.config[section] = yaml_config
                        logger.debug(f"Loaded config from {yaml_file}")
                except Exception as e:
                    logger.error(f"Error loading {yaml_file}: {e}")
    
    @staticmethod
    def _write_yaml(filepath: Path, data: Dict[str, Any]):
        """Write YAML file"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return self.config.get(key, default)
    
    def get_section(self, section: str, key: str = None, default: Any = None) -> Any:
        """Get configuration from a specific section"""
        if section not in self.config:
            return default
        
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configurations"""
        return self.config.copy()
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value


# Global instance
_config_manager_instance = None


def get_config_manager() -> ConfigManager:
    """Get or create the global config manager instance"""
    global _config_manager_instance
    if _config_manager_instance is None:
        _config_manager_instance = ConfigManager()
    return _config_manager_instance


# For backward compatibility - create the global instance
config_manager = get_config_manager()


# Export commonly used functions
def get_config(key: str, default: Any = None) -> Any:
    """Get a config value (shorthand)"""
    return get_config_manager().get(key, default)


# For backward compatibility - expose constants as module-level exports
_cm = get_config_manager()

# Tool info (commonly imported)
TOOL_VERSION = _cm.get('TOOL_VERSION')
TOOL_NAME = _cm.get('TOOL_NAME')
DESCRIPTION = _cm.get('DESCRIPTION')
AUTHOR = _cm.get('AUTHOR')

# Request settings
DEFAULT_REQUEST_DELAY = _cm.get('DEFAULT_REQUEST_DELAY')
DEFAULT_MAX_CONCURRENT = _cm.get('DEFAULT_MAX_CONCURRENT')
DEFAULT_RATE_LIMIT = _cm.get('DEFAULT_RATE_LIMIT')
DEFAULT_GLOBAL_TIMEOUT = _cm.get('DEFAULT_GLOBAL_TIMEOUT')
DEFAULT_SCORE_THRESHOLD_HIGH = _cm.get('DEFAULT_SCORE_THRESHOLD_HIGH')
DEFAULT_SCORE_THRESHOLD_MEDIUM = _cm.get('DEFAULT_SCORE_THRESHOLD_MEDIUM')
