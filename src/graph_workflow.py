"""
ADK 2.0 Graph Workflow API Implementation.
Defines explicit workflow graph nodes, directed edges, conditional branching,
and Human-in-the-Loop (HITL) review logic for the Automated Blog Writer Platform.
"""

from typing import Dict, Any, Literal
from src.agents import (
    root_orchestrator_agent,
    searcher_agent,
    politics_writer_agent,
    economics_writer_agent,
    science_writer_agent,
    judge_agent,
)


class BlogWriterGraphWorkflow:
    """ADK 2.0 Graph Workflow orchestrating multi-agent state transitions."""

    def __init__(self):
        self.nodes = {
            "root_node": root_orchestrator_agent,
            "searcher_node": searcher_agent,
            "politics_writer_node": politics_writer_agent,
            "economics_writer_node": economics_writer_agent,
            "science_writer_node": science_writer_agent,
            "judge_node": judge_agent,
        }

    def route_writer_node(self, domain: str):
        """Dynamic graph routing edge to domain-specific writer node."""
        domain_clean = domain.lower()
        if "politic" in domain_clean:
            return self.nodes["politics_writer_node"]
        elif "economic" in domain_clean or "financ" in domain_clean:
            return self.nodes["economics_writer_node"]
        elif "science" in domain_clean or "tech" in domain_clean:
            return self.nodes["science_writer_node"]
        else:
            raise ValueError(f"Unsupported domain routing for: {domain}")

    def evaluate_judge_conditional_edge(self, judgment_result: Dict[str, Any]) -> Literal["human_review_node", "retry_writer_edge"]:
        """ADK 2.0 conditional edge evaluating Judge Agent outcome."""
        decision = judgment_result.get("decision", "REJECTED")
        if decision == "APPROVED":
            return "human_review_node"
        return "retry_writer_edge"
