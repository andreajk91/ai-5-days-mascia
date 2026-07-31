"""
A2A (Agent-to-Agent) Protocol Core Definitions and Messaging Client.
Ensures standardized communication across all specialized agents in the system.
"""

from typing import Dict, Any, List, Optional, Literal
from pydantic import BaseModel, Field
import datetime
import httpx


class AgentCard(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    domain: Optional[str] = None
    endpoint_url: str
    capabilities: List[str] = Field(default_factory=list)


class A2AMessage(BaseModel):
    protocol: str = "A2A/1.0"
    sender: str
    recipient: str
    task_id: str
    session_id: str
    payload_type: str
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    body: Dict[str, Any]


class ArticleDraft(BaseModel):
    title: str
    domain: Literal["Politicals", "Economics", "Science"]
    hero_image_url: str
    introduction: str
    body_sections: List[Dict[str, str]]
    conclusion: str
    editorial_opinion: str


class ResearchBundle(BaseModel):
    topic: str
    domain: Literal["Politicals", "Economics", "Science"]
    articles: List[Dict[str, Any]]
    research_summary: str


class JudgmentRecord(BaseModel):
    judgment_id: str
    task_id: str
    session_id: str
    timestamp: str
    domain: Literal["Politicals", "Economics", "Science"]
    writer_agent_id: str
    iteration_number: int
    decision: Literal["APPROVED", "REJECTED"]
    article_snapshot: ArticleDraft
    rubric_scores: Dict[str, float]
    critique: str
    required_revisions: List[str]


class A2AClient:
    """Client for sending A2A protocol messages between agent endpoints."""

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout

    async def send_message(self, target_endpoint: str, message: A2AMessage) -> Dict[str, Any]:
        """Send an A2A message payload to a recipient agent endpoint."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{target_endpoint}/a2a/message",
                json=message.model_dump(),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
