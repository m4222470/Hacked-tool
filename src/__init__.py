"""
Hacked-tool - Main package

All source code is organized in the src/ directory.
"""

from .core import (
    engine,
    logger,
    config_manager,
    task_manager,
    module_loader,
    session_manager,
    AdaptiveRateLimiter,
    Engine,
    LoggerManager,
    ConfigManager,
    Task,
    TaskManager,
    TaskStatus,
    Session,
    SessionManager,
    ModuleLoader,
)

from .utils import (
    create_parser,
    URLUtils,
    URLValidator,
    ParameterValidator,
)

from .plugins import (
    BasePlugin,
    plugin_manager,
)

from .evasion import (
    HeaderRandomizer,
)

__all__ = [
    # Core singletons
    'engine',
    'logger',
    'config_manager',
    'task_manager',
    'module_loader',
    'session_manager',
    
    # Core classes
    'Engine',
    'LoggerManager',
    'ConfigManager',
    'Task',
    'TaskManager',
    'TaskStatus',
    'Session',
    'SessionManager',
    'ModuleLoader',
    'AdaptiveRateLimiter',
    
    # Utils
    'create_parser',
    'URLUtils',
    'URLValidator',
    'ParameterValidator',
    
    # Plugins
    'BasePlugin',
    'plugin_manager',
    
    # Evasion
    'HeaderRandomizer',
]
