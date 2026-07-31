"""
Root Orchestrator Agent.
Serves as the primary entry point registered with Gemini Enterprise.
Interacts with journalists, dispatches research and writing via A2A,
handles human-in-the-loop approval, and triggers GCS publication.
"""

from google.adk.agents import Agent
from .tools import dispatch_search_request, publish_to_gcs


root_orchestrator_agent = Agent(
    name="root_orchestrator_agent",
    model="gemini-3.6-flash",
    instruction="""You are the Root Orchestrator Agent for the Automated Blog Writer Platform.
Your responsibilities:
1. Receive topics and domain selections (Politicals, Economics, Science) from journalists.
2. Communicate with specialized sub-agents (Searcher, Domain Writers, Judge) using the A2A protocol.
3. Present Judge-approved article candidates to human journalists for final review.
4. Upon human approval, trigger publication to Google Cloud Storage (GCS) and log execution stats.
""",
    tools=[dispatch_search_request, publish_to_gcs]
)
