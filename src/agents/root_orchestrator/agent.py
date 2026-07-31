"""
Root Orchestrator Agent.
Serves as the primary entry point registered with Gemini Enterprise.
Configured with permissive safety settings to prevent Model Armor false positives.
"""

from google.adk.agents import Agent
from src.agents.searcher_agent import searcher_agent
from src.agents.politics_writer_agent import politics_writer_agent
from src.agents.economics_writer_agent import economics_writer_agent
from src.agents.science_writer_agent import science_writer_agent
from src.agents.judge_agent import judge_agent
from src.common.safety_config import get_permissive_safety_config, on_model_error_fallback
from .tools import a2a_send_message, publish_to_gcs


root_orchestrator_agent = Agent(
    name="root_orchestrator_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    on_model_error_callback=on_model_error_fallback,
    instruction="""You are the Root Orchestrator Agent for the Automated Blog Writer Platform.
Your role is to orchestrate multi-agent blog production by forwarding tasks to your specialized sub-agents using the Agent-to-Agent (A2A) protocol.

Important:
- Handle all geopolitical, policy, and economic conflict topics as objective, neutral journalistic analysis.
- Frame user requests cleanly so that economic impact queries (e.g. inflation, supply chain disruptions, commodity markets) are processed objectively.

Workflow Steps:
1. **Research Dispatch (A2A)**: Forward user topic to `searcher_agent` for web research.
2. **Writing Dispatch (A2A)**: Forward research bundle to specialized SME Writer (`politics_writer_agent`, `economics_writer_agent`, or `science_writer_agent`).
3. **Quality Evaluation Dispatch (A2A)**: Forward draft to `judge_agent` to evaluate quality.
4. **Human Final Review Presentation**: Present candidate article to the user with title, hero image, intro, body, conclusion, commentary, and judge audit score. Ask: *"Candidate article ready for final review! Reply 'PUBLISH' to store in Google Cloud Storage, or reply with feedback to revise."*
5. **GCS Publication**: Upon user confirmation ("PUBLISH"), invoke `publish_to_gcs`.
""",
    sub_agents=[
        searcher_agent,
        politics_writer_agent,
        economics_writer_agent,
        science_writer_agent,
        judge_agent,
    ],
    tools=[a2a_send_message, publish_to_gcs]
)
