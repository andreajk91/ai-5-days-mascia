"""
Root Orchestrator Agent.
Serves as the primary entry point registered with Gemini Enterprise.
Interacts with journalists, dispatches research and writing via A2A,
handles human-in-the-loop approval, and triggers GCS publication.
"""

from google.adk.agents import Agent
from .tools import generate_blog_post, dispatch_search_request, publish_to_gcs


root_orchestrator_agent = Agent(
    name="root_orchestrator_agent",
    model="gemini-3.6-flash",
    instruction="""You are the Root Orchestrator Agent for the Automated Blog Writer Platform.
Your responsibilities:
1. When a user or journalist asks to write, generate, or produce a blog post on any topic, determine the domain ("Politicals", "Economics", or "Science") and IMMEDIATELY call the `generate_blog_post` tool with the topic and domain.
2. Present the returned article to the journalist in a clean, professional, publication-ready Markdown layout including:
   - Catchy Title
   - Hero Image URL
   - Introduction
   - Section Headings and Body
   - Conclusion
   - Editorial Commentary
   - GCS Asset Link and Judge Audit Confirmation
""",
    tools=[generate_blog_post, dispatch_search_request, publish_to_gcs]
)
