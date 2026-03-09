"""
Main application engine - Orchestrates the entire scanning process
"""

from typing import Dict, Any
from .logger import logger
from .config_manager import config_manager
from .task_manager import task_manager, TaskStatus
from .module_loader import module_loader
from .session_manager import session_manager

class Engine:
    """Main application engine"""
    
    def __init__(self):
        self.config = config_manager.get_all()
        self.logger = logger
        self.task_manager = task_manager
        self.module_loader = module_loader
        self.session_manager = session_manager
    
    def initialize(self):
        """Initialize engine"""
        self.logger.info("Initializing Hacked-tool engine...")
        
        # Load modules
        count = self.module_loader.load_all_modules()
        self.logger.info(f"Loaded {count} modules")
    
    def run_scan(self, target: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a complete scan"""
        try:
            # Create session
            session = self.session_manager.create_session(target, config or {})
            self.logger.info(f"Started session {session.session_id} for {target}")
            
            # Start session
            self.session_manager.start_session(session.session_id)
            
            # Execute tasks
            # This will be expanded with actual module execution
            
            # Complete session
            self.session_manager.complete_session(session.session_id)
            self.logger.info(f"Completed session {session.session_id}")
            
            return session.to_dict()
        
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")
            if session:
                self.session_manager.fail_session(session.session_id, str(e))
            raise
    
    def shutdown(self):
        """Shutdown engine"""
        self.logger.info("Shutting down engine...")
        self.session_manager.clear_completed()
        self.task_manager.clear_completed()

# Global instance
engine = Engine()
