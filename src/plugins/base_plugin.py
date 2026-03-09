"""
Base plugin class - All plugins must inherit from this
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BasePlugin(ABC):
    """Abstract base class for all plugins"""
    
    # Plugin metadata
    name: str = "Unknown Plugin"
    version: str = "1.0.0"
    author: str = "Unknown"
    description: str = "No description"
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize plugin"""
        self.config = config or {}
        self.enabled = True
        self.results = {}
    
    @abstractmethod
    def execute(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the plugin logic - Must be implemented by subclasses"""
        pass
    
    def initialize(self):
        """Called when plugin is loaded"""
        pass
    
    def shutdown(self):
        """Called when plugin is unloaded"""
        pass
    
    def get_info(self) -> Dict[str, str]:
        """Get plugin information"""
        return {
            'name': self.name,
            'version': self.version,
            'author': self.author,
            'description': self.description,
        }
    
    def validate_config(self) -> bool:
        """Validate plugin configuration"""
        return True
    
    def get_requirements(self) -> List[str]:
        """Get list of required packages"""
        return []
