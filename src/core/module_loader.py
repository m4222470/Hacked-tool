"""
Module loader - Dynamically load and manage modules
"""

import importlib
import sys
from pathlib import Path
from typing import Dict, Any, Type
import inspect

class ModuleLoader:
    """Dynamic module loading system"""
    
    def __init__(self):
        self.loaded_modules: Dict[str, Any] = {}
        self.module_classes: Dict[str, Type] = {}
        self.modules_dir = Path('src/modules')
    
    def discover_modules(self) -> Dict[str, str]:
        """Discover all available modules"""
        modules = {}
        
        if not self.modules_dir.exists():
            return modules
        
        for module_file in self.modules_dir.rglob('*.py'):
            if module_file.name.startswith('_'):
                continue
            
            relative_path = module_file.relative_to(self.modules_dir)
            module_name = str(relative_path.with_suffix(''))
            module_path = f"src.modules.{module_name.replace('/', '.')}"
            
            modules[module_name.replace('/', '.')] = module_path
        
        return modules
    
    def load_module(self, module_name: str) -> bool:
        """Load a specific module"""
        try:
            if module_name in self.loaded_modules:
                return True
            
            modules = self.discover_modules()
            if module_name not in modules:
                return False
            
            module_path = modules[module_name]
            module = importlib.import_module(module_path)
            self.loaded_modules[module_name] = module
            
            return True
        except Exception as e:
            print(f"Failed to load module {module_name}: {e}")
            return False
    
    def load_all_modules(self) -> int:
        """Load all discovered modules"""
        modules = self.discover_modules()
        count = 0
        
        for module_name in modules:
            if self.load_module(module_name):
                count += 1
        
        return count
    
    def get_module(self, module_name: str) -> Any:
        """Get loaded module"""
        return self.loaded_modules.get(module_name)
    
    def get_module_class(self, module_name: str, class_name: str) -> Type:
        """Get class from module"""
        try:
            module = self.get_module(module_name)
            if module and hasattr(module, class_name):
                return getattr(module, class_name)
            return None
        except Exception:
            return None
    
    def list_loaded_modules(self) -> Dict[str, Any]:
        """List all loaded modules"""
        return self.loaded_modules.copy()

# Global instance
module_loader = ModuleLoader()
