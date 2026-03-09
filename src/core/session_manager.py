"""
Session manager - Manage scanning sessions and state
"""

from typing import Dict, List, Any
from datetime import datetime
from enum import Enum
import threading
import uuid

class SessionStatus(Enum):
    """Session status"""
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Session:
    """Represents a scanning session"""
    
    def __init__(self, session_id: str, target: str, config: Dict[str, Any]):
        self.session_id = session_id
        self.target = target
        self.config = config
        self.status = SessionStatus.INITIALIZED
        self.created_at = datetime.now()
        self.started_at = None
        self.ended_at = None
        self.results: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.metadata: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary"""
        return {
            'session_id': self.session_id,
            'target': self.target,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'errors_count': len(self.errors),
        }

class SessionManager:
    """Manage scanning sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.active_session: Session = None
        self.lock = threading.Lock()
    
    def create_session(self, target: str, config: Dict[str, Any]) -> Session:
        """Create a new scanning session"""
        session_id = str(uuid.uuid4())
        session = Session(session_id, target, config)
        
        with self.lock:
            self.sessions[session_id] = session
            self.active_session = session
        
        return session
    
    def get_session(self, session_id: str) -> Session:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def get_active_session(self) -> Session:
        """Get active session"""
        with self.lock:
            return self.active_session
    
    def start_session(self, session_id: str):
        """Start a session"""
        session = self.get_session(session_id)
        if session:
            session.status = SessionStatus.RUNNING
            session.started_at = datetime.now()
    
    def pause_session(self, session_id: str):
        """Pause a session"""
        session = self.get_session(session_id)
        if session:
            session.status = SessionStatus.PAUSED
    
    def resume_session(self, session_id: str):
        """Resume a paused session"""
        session = self.get_session(session_id)
        if session and session.status == SessionStatus.PAUSED:
            session.status = SessionStatus.RUNNING
    
    def complete_session(self, session_id: str):
        """Mark session as completed"""
        session = self.get_session(session_id)
        if session:
            session.status = SessionStatus.COMPLETED
            session.ended_at = datetime.now()
    
    def fail_session(self, session_id: str, error: str):
        """Mark session as failed"""
        session = self.get_session(session_id)
        if session:
            session.status = SessionStatus.FAILED
            session.ended_at = datetime.now()
            session.errors.append(error)
    
    def add_result(self, session_id: str, key: str, value: Any):
        """Add result to session"""
        session = self.get_session(session_id)
        if session:
            session.results[key] = value
    
    def add_error(self, session_id: str, error: str):
        """Add error to session"""
        session = self.get_session(session_id)
        if session:
            session.errors.append(error)
    
    def get_all_sessions(self) -> List[Session]:
        """Get all sessions"""
        return list(self.sessions.values())
    
    def get_active_sessions(self) -> List[Session]:
        """Get all active sessions"""
        return [s for s in self.sessions.values() if s.status == SessionStatus.RUNNING]
    
    def clear_completed(self):
        """Clear completed sessions"""
        with self.lock:
            to_remove = [sid for sid, session in self.sessions.items()
                        if session.status in [SessionStatus.COMPLETED, SessionStatus.FAILED]]
            for sid in to_remove:
                del self.sessions[sid]

# Global instance
session_manager = SessionManager()
