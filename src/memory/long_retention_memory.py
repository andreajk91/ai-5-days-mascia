"""
Long Retention Memory Bank Client.
Stores long-term contextual memory across sessions including editorial style preferences,
historical topic coverage to prevent duplication, and Judge feedback patterns.
GCP Infrastructure Location: us-central1
"""

from typing import Dict, Any, List, Optional


class LongRetentionMemoryBank:
    """ADK Memory Bank interface for long-term agent persistence in us-central1."""

    def __init__(self, storage_path: str = "gs://blog-writer-memory-gen-lang-client-0748552619"):
        self.storage_path = storage_path
        self._editorial_preferences: Dict[str, Any] = {
            "tone": "Authoritative yet accessible journalism",
            "formatting": "Include catching title, hero image, clear section headings",
            "prohibited_phrases": ["In conclusion", "As an AI", "In this fast-paced world"]
        }
        self._covered_topics: List[Dict[str, Any]] = []

    def check_topic_duplication(self, topic: str, domain: str) -> bool:
        """Check if topic was recently covered to prevent duplication."""
        for item in self._covered_topics:
            if item["domain"] == domain and topic.lower() in item["topic"].lower():
                return True
        return False

    def record_published_topic(self, topic: str, domain: str, article_id: str):
        """Record published topic into long-term memory bank."""
        self._covered_topics.append({
            "topic": topic,
            "domain": domain,
            "article_id": article_id
        })

    def get_editorial_preferences(self) -> Dict[str, Any]:
        return self._editorial_preferences
