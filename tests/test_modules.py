"""
Module loading and plugin system tests
"""

import unittest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.module_loader import module_loader
from plugins.plugin_manager import plugin_manager
from plugins.base_plugin import BasePlugin

class TestModuleLoader(unittest.testCase):
    """Test ModuleLoader functionality"""
    
    def test_discover_modules(self):
        """Test module discovery"""
        modules = module_loader.discover_modules()
        self.assertIsInstance(modules, dict)
    
    def test_load_module(self):
        """Test loading a module"""
        # Should not fail even if module doesn't exist
        result = module_loader.load_module('non_existent')
        self.assertIsInstance(result, bool)

class TestPluginManager(unittest.TestCase):
    """Test PluginManager functionality"""
    
    def test_discover_plugins(self):
        """Test plugin discovery"""
        plugins = plugin_manager.discover_plugins()
        self.assertIsInstance(plugins, dict)
    
    def test_list_plugins(self):
        """Test listing plugins"""
        plugins_list = plugin_manager.list_plugins()
        self.assertIsInstance(plugins_list, list)

class TestBasePlugin(unittest.TestCase):
    """Test BasePlugin functionality"""
    
    class DummyPlugin(BasePlugin):
        """Test plugin"""
        name = "Dummy"
        
        def execute(self, target, options=None):
            return {'target': target, 'result': 'success'}
    
    def test_plugin_creation(self):
        """Test creating a plugin"""
        plugin = self.DummyPlugin()
        self.assertEqual(plugin.name, 'Dummy')
    
    def test_plugin_execution(self):
        """Test executing a plugin"""
        plugin = self.DummyPlugin()
        result = plugin.execute('test.com')
        self.assertEqual(result['target'], 'test.com')
    
    def test_plugin_info(self):
        """Test plugin info retrieval"""
        plugin = self.DummyPlugin()
        info = plugin.get_info()
        self.assertEqual(info['name'], 'Dummy')

if __name__ == '__main__':
    unittest.main()
