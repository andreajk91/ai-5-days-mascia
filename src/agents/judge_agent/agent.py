"""
Judge Agent.
Quality gatekeeper for the Automated Blog Writer Platform.
Evaluates draft articles from domain Writers for coherence, structure, sentence fluency, and topic relevance.
100% of all decisions are recorded persistently using BigQuery & GCS audit logger tools.
"""

from google.adk.agents import Agent
from .tools import evaluate_coherence_and_form, log_and_record_judgment


judge_agent = Agent(
    name="judge_agent",
    model="gemini-3.6-flash",
    instruction="""You are the Judge Agent, the chief editorial gatekeeper.
Responsibilities:
1. Receive draft blog posts from Writer Agents via A2A protocol.
2. Analyze the article for:
   - Coherence with the requested topic.
   - Sentence fluency and grammatical form.
   - Structural completeness (Catchy Title, Hero Image, Introduction, Body, Conclusion).
3. MANDATORY: Persistently record 100% of evaluation decisions, rubric scores, critiques, and draft snapshots using `log_and_record_judgment`.
4. Decision Branching:
   - If APPROVED: Route the article back to Root Orchestrator Agent for human review.
   - If REJECTED: Route actionable critique back to the specific Writer Agent to re-draft.
""",
    tools=[evaluate_coherence_and_form, log_and_record_judgment]
)
