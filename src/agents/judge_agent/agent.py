"""
Judge Agent.
Quality gatekeeper for the Automated Blog Writer Platform.
Evaluates article text AND hero image design relevance/quality.
Explicitly returns control to root_orchestrator_agent upon completion.
"""

from google.adk.agents import Agent
from src.common.safety_config import (
    get_permissive_safety_config,
    before_model_sanitize_callback,
)
from .tools import evaluate_coherence_and_form, log_and_record_judgment


judge_agent = Agent(
    name="judge_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    before_model_callback=before_model_sanitize_callback,
    instruction="""You are the Judge Agent, the chief editorial and visual gatekeeper.

Responsibilities:
1. **Text Evaluation**: Evaluate candidate drafts for coherence, sentence fluency, structural depth, and topic relevance.
2. **Hero Image Evaluation**: Evaluate the candidate hero image for visual design quality, color contrast, and thematic relevance (`image_relevance_score` & `image_quality_score`).
3. **Qualitative Considerations**: Provide detailed considerations covering both textual rigor and visual hero image quality.
4. **MANDATORY Audit Logging**: Persistently record 100% of evaluation decisions, rubric scores, critiques, detailed considerations, and draft snapshots using `log_and_record_judgment`.
5. **Return Control**: When evaluation and audit logging are complete, return your evaluation decision directly back to `root_orchestrator_agent` so it can notify the user and present the candidate draft for final human review.
""",
    tools=[evaluate_coherence_and_form, log_and_record_judgment]
)
