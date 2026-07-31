"""
Shared Session Memory Client.
Provides persistent, database-backed short-term session state sharing and async I/O across agents.
Database Storage Path: app/.adk/session_persistence.db (SQLite)
"""

import sqlite3
import json
import time
import asyncio
from typing import Dict, Any, Optional
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/.adk/session_persistence.db"))
_GLOBAL_SESSIONS: Dict[str, Dict[str, Any]] = {}


def _init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("""
        CREATE TABLE IF NOT EXISTS session_store (
            session_id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


_init_db()


class SharedSessionMemory:
    """Persistent SQLite database and in-memory session state manager shared across agents."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._memory_cache = _GLOBAL_SESSIONS

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Synchronously retrieve active session data from memory cache or SQLite database."""
        if session_id in self._memory_cache:
            return self._memory_cache[session_id]

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT data FROM session_store WHERE session_id = ?", (session_id,))
        row = c.fetchone()
        conn.close()

        if row:
            session_data = json.loads(row[0])
            self._memory_cache[session_id] = session_data
            return session_data

        now = time.time()
        new_session = {
            "created_at": now,
            "updated_at": now,
            "topic": "",
            "domain": "",
            "task_id": "",
            "research_bundle": None,
            "current_draft": None,
            "judge_critiques": [],
            "iteration_count": 0,
            "status": "INIT"
        }
        self._memory_cache[session_id] = new_session

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO session_store (session_id, data, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                data = excluded.data,
                updated_at = excluded.updated_at
        """, (session_id, json.dumps(new_session), now, now))
        conn.commit()
        conn.close()

        return new_session

    async def get_session_async(self, session_id: str) -> Dict[str, Any]:
        """Asynchronously retrieve active session data."""
        return await asyncio.to_thread(self.get_session, session_id)

    def update_session(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronously update session data and commit to persistent SQLite database."""
        session = self.get_session(session_id)
        session.update(updates)
        now = time.time()
        session["updated_at"] = now
        self._memory_cache[session_id] = session

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        created_at = session.get("created_at", now)
        c.execute("""
            INSERT INTO session_store (session_id, data, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                data = excluded.data,
                updated_at = excluded.updated_at
        """, (session_id, json.dumps(session), created_at, now))
        conn.commit()
        conn.close()
        return session

    async def update_session_async(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Asynchronously update session data and commit to persistent database."""
        return await asyncio.to_thread(self.update_session, session_id, updates)
