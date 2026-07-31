"""
Multi-Agent Registry for Automated Blog Writer Platform.
Exposes all 6 specialized agents configured with A2A protocol communication.
"""

from .root_orchestrator import root_orchestrator_agent
from .searcher_agent import searcher_agent
from .politics_writer_agent import politics_writer_agent
from .economics_writer_agent import economics_writer_agent
from .science_writer_agent import science_writer_agent
from .judge_agent import judge_agent

__all__ = [
    "root_orchestrator_agent",
    "searcher_agent",
    "politics_writer_agent",
    "economics_writer_agent",
    "science_writer_agent",
    "judge_agent",
]
