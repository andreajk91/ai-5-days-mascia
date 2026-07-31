"""
Long Retention Memory Bank Client.
Stores persistent contextual memory across sessions including editorial style preferences,
historical topic coverage to prevent duplication, and Judge feedback patterns.
GCP Infrastructure Location: us-central1
Database Storage Path: app/.adk/session_persistence.db (SQLite)
"""

import sqlite3
import json
import time
import asyncio
import os
from typing import Dict, Any, List, Optional

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/.adk/session_persistence.db"))


def _init_memory_bank_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS covered_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            domain TEXT NOT NULL,
            article_id TEXT NOT NULL,
            published_at REAL NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS editorial_preferences (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


_init_memory_bank_db()


class LongRetentionMemoryBank:
    """ADK Memory Bank interface with SQLite persistence and async I/O in us-central1."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._default_editorial_preferences = {
            "tone": "Authoritative yet accessible journalism",
            "formatting": "Include catching title, hero image, clear section headings",
            "prohibited_phrases": ["In conclusion", "As an AI", "In this fast-paced world"]
        }

    def check_topic_duplication(self, topic: str, domain: str) -> bool:
        """Synchronously check if topic was recently published to prevent duplication."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT topic FROM covered_topics WHERE domain = ?", (domain,))
        rows = c.fetchall()
        conn.close()

        topic_clean = topic.lower().strip()
        for (past_topic,) in rows:
            if topic_clean in past_topic.lower():
                return True
        return False

    async def check_topic_duplication_async(self, topic: str, domain: str) -> bool:
        """Asynchronously check if topic was recently published."""
        return await asyncio.to_thread(self.check_topic_duplication, topic, domain)

    def record_published_topic(self, topic: str, domain: str, article_id: str):
        """Synchronously record published topic into long-term memory database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO covered_topics (topic, domain, article_id, published_at)
            VALUES (?, ?, ?, ?)
        """, (topic, domain, article_id, time.time()))
        conn.commit()
        conn.close()

    async def record_published_topic_async(self, topic: str, domain: str, article_id: str):
        """Asynchronously record published topic into long-term memory database."""
        await asyncio.to_thread(self.record_published_topic, topic, domain, article_id)

    def get_editorial_preferences(self) -> Dict[str, Any]:
        """Synchronously retrieve editorial style preferences."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT key, value FROM editorial_preferences")
        rows = c.fetchall()
        conn.close()

        prefs = dict(self._default_editorial_preferences)
        for key, val in rows:
            try:
                prefs[key] = json.loads(val)
            except Exception:
                prefs[key] = val
        return prefs

    async def get_editorial_preferences_async(self) -> Dict[str, Any]:
        """Asynchronously retrieve editorial style preferences."""
        return await asyncio.to_thread(self.get_editorial_preferences)

    def set_editorial_preference(self, key: str, value: Any):
        """Synchronously set editorial style preference."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        val_str = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        c.execute("""
            INSERT INTO editorial_preferences (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
        """, (key, val_str, time.time()))
        conn.commit()
        conn.close()

    async def set_editorial_preference_async(self, key: str, value: Any):
        """Asynchronously set editorial style preference."""
        await asyncio.to_thread(self.set_editorial_preference, key, value)
