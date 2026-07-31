"""
Judge Agent.
Quality gatekeeper for the Automated Blog Writer Platform.
Configured with ADK before_model_callback sanitization.
"""

from google.adk.agents import Agent
from src.common.safety_config import (
    get_permissive_safety_config,
    before_model_sanitize_callback,
    on_model_error_fallback,
)
from .tools import evaluate_coherence_and_form, log_and_record_judgment


judge_agent = Agent(
    name="judge_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    before_model_callback=before_model_sanitize_callback,
    on_model_error_callback=on_model_error_fallback,
    instruction="""You are the Judge Agent, the chief editorial gatekeeper.
Responsibilities:
1. Evaluate candidate drafts for coherence, sentence fluency, and structural completeness.
2. MANDATORY: Persistently record 100% of evaluation decisions, rubric scores, critiques, detailed considerations, and draft snapshots using `log_and_record_judgment`.
""",
    tools=[evaluate_coherence_and_form, log_and_record_judgment]
)
