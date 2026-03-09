"""
Task manager - Orchestrate scanning tasks
"""

from typing import List, Dict, Any, Callable
from enum import Enum
from datetime import datetime
import threading

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Task:
    """Represents a single task"""
    
    def __init__(self, task_id: str, name: str, module_name: str, 
                 config: Dict[str, Any], callback: Callable = None):
        self.task_id = task_id
        self.name = name
        self.module_name = module_name
        self.config = config
        self.callback = callback
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None
        self.progress = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            'id': self.task_id,
            'name': self.name,
            'module': self.module_name,
            'status': self.status.value,
            'progress': self.progress,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'error': self.error,
        }

class TaskManager:
    """Manage scanning tasks"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.running_tasks: List[str] = []
        self.lock = threading.Lock()
    
    def create_task(self, task_id: str, name: str, module_name: str,
                   config: Dict[str, Any]) -> Task:
        """Create a new task"""
        task = Task(task_id, name, module_name, config)
        with self.lock:
            self.tasks[task_id] = task
        return task
    
    def get_task(self, task_id: str) -> Task:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: TaskStatus):
        """Update task status"""
        task = self.get_task(task_id)
        if task:
            task.status = status
            if status == TaskStatus.RUNNING:
                task.start_time = datetime.now()
                with self.lock:
                    self.running_tasks.append(task_id)
            elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                task.end_time = datetime.now()
                with self.lock:
                    if task_id in self.running_tasks:
                        self.running_tasks.remove(task_id)
    
    def update_task_progress(self, task_id: str, progress: int):
        """Update task progress (0-100)"""
        task = self.get_task(task_id)
        if task:
            task.progress = min(100, max(0, progress))
    
    def set_task_result(self, task_id: str, result: Any):
        """Set task result"""
        task = self.get_task(task_id)
        if task:
            task.result = result
    
    def set_task_error(self, task_id: str, error: str):
        """Set task error"""
        task = self.get_task(task_id)
        if task:
            task.error = error
    
    def get_running_tasks(self) -> List[Task]:
        """Get all running tasks"""
        return [self.tasks[tid] for tid in self.running_tasks if tid in self.tasks]
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return list(self.tasks.values())
    
    def cancel_task(self, task_id: str):
        """Cancel a task"""
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
    
    def clear_completed(self):
        """Clear completed/failed tasks"""
        with self.lock:
            to_remove = [tid for tid, task in self.tasks.items()
                        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]]
            for tid in to_remove:
                del self.tasks[tid]

# Global instance
task_manager = TaskManager()
