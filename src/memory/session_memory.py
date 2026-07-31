"""
Shared Session Memory Client.
Provides short-term session state sharing across agents during article generation.
"""

from typing import Dict, Any, Optional
import time


class SharedSessionMemory:
    """In-memory and persistent session state manager shared across agents."""

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def get_session(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "created_at": time.time(),
                "topic": "",
                "domain": "",
                "research_bundle": None,
                "current_draft": None,
                "judge_critiques": [],
                "iteration_count": 0,
                "status": "INIT"
            }
        return self._sessions[session_id]

    def update_session(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        session = self.get_session(session_id)
        session.update(updates)
        session["updated_at"] = time.time()
        return session
