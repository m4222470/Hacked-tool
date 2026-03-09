"""
Plugin manager - Load, manage and execute plugins
"""

import importlib
from pathlib import Path
from typing import Dict, Any, List, Type
from .base_plugin import BasePlugin

class PluginManager:
    """Manage plugin loading and execution"""
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_classes: Dict[str, Type[BasePlugin]] = {}
        self.plugins_dir = Path('src/plugins')
    
    def discover_plugins(self) -> Dict[str, str]:
        """Discover all available plugins"""
        plugins = {}
        
        if not self.plugins_dir.exists():
            return plugins
        
        for plugin_file in self.plugins_dir.glob('*.py'):
            if plugin_file.name in ['base_plugin.py', 'plugin_manager.py', '__init__.py']:
                continue
            
            plugin_name = plugin_file.stem
            plugins[plugin_name] = str(plugin_file)
        
        return plugins
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Load a single plugin"""
        try:
            if plugin_name in self.plugins:
                return True
            
            plugins = self.discover_plugins()
            if plugin_name not in plugins:
                return False
            
            # Import plugin module
            module_path = f"src.plugins.{plugin_name}"
            module = importlib.import_module(module_path)
            
            # Find BasePlugin subclass
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr != BasePlugin:
                    plugin_instance = attr()
                    self.plugins[plugin_name] = plugin_instance
                    self.plugin_classes[plugin_name] = attr
                    plugin_instance.initialize()
                    return True
            
            return False
        except Exception as e:
            print(f"Failed to load plugin {plugin_name}: {e}")
            return False
    
    def load_all_plugins(self) -> int:
        """Load all plugins"""
        plugins = self.discover_plugins()
        count = 0
        
        for plugin_name in plugins:
            if self.load_plugin(plugin_name):
                count += 1
        
        return count
    
    def get_plugin(self, plugin_name: str) -> BasePlugin:
        """Get plugin instance"""
        return self.plugins.get(plugin_name)
    
    def execute_plugin(self, plugin_name: str, target: str, 
                      options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            return plugin.execute(target, options)
        return {'error': f'Plugin {plugin_name} not found'}
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins"""
        return [
            {
                'name': name,
                'info': plugin.get_info(),
                'enabled': plugin.enabled,
            }
            for name, plugin in self.plugins.items()
        ]
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.enabled = True
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.enabled = False
            return True
        return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.shutdown()
            del self.plugins[plugin_name]
            return True
        return False
    
    def unload_all_plugins(self):
        """Unload all plugins"""
        for plugin_name in list(self.plugins.keys()):
            self.unload_plugin(plugin_name)

# Global instance
plugin_manager = PluginManager()
