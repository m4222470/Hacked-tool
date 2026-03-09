"""
Core engine unit tests
"""

import unittest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.engine import engine
from core.logger import logger
from core.config_manager import config_manager
from core.task_manager import task_manager, TaskStatus
from core.module_loader import module_loader
from core.session_manager import session_manager

class TestEngine(unittest.TestCase):
    """Test Engine class"""
    
    def test_engine_initialization(self):
        """Test engine can initialize"""
        engine.initialize()
        self.assertIsNotNone(engine.logger)
        self.assertIsNotNone(engine.config)
    
    def test_logger(self):
        """Test logger works"""
        logger.info("Test message")
        self.assertIsNotNone(logger)
    
    def test_config_manager(self):
        """Test config manager"""
        self.assertIsNotNone(config_manager)
        settings = config_manager.get('settings')
        self.assertIsNotNone(settings)

class TestTaskManager(unittest.TestCase):
    """Test TaskManager class"""
    
    def test_create_task(self):
        """Test creating a task"""
        task = task_manager.create_task('test-1', 'Test Task', 'test_module', {})
        self.assertEqual(task.task_id, 'test-1')
        self.assertEqual(task.status, TaskStatus.PENDING)
    
    def test_update_task_status(self):
        """Test updating task status"""
        task = task_manager.create_task('test-2', 'Test', 'test', {})
        task_manager.update_task_status('test-2', TaskStatus.RUNNING)
        self.assertEqual(task.status, TaskStatus.RUNNING)

class TestModuleLoader(unittest.TestCase):
    """Test ModuleLoader class"""
    
    def test_module_discovery(self):
        """Test module discovery"""
        modules = module_loader.discover_modules()
        self.assertIsInstance(modules, dict)

class TestSessionManager(unittest.TestCase):
    """Test SessionManager class"""
    
    def test_create_session(self):
        """Test creating a session"""
        session = session_manager.create_session('example.com', {})
        self.assertEqual(session.target, 'example.com')
        self.assertIsNotNone(session.session_id)
    
    def test_session_workflow(self):
        """Test session state transitions"""
        session = session_manager.create_session('test.com', {})
        session_id = session.session_id
        
        session_manager.start_session(session_id)
        self.assertEqual(session.status.value, 'running')
        
        session_manager.complete_session(session_id)
        self.assertEqual(session.status.value, 'completed')

if __name__ == '__main__':
    unittest.main()
