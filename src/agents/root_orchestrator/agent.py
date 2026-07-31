"""
Root Orchestrator Agent.
Serves as the primary entry point registered with Gemini Enterprise.
Orchestrates multi-agent production natively across Searcher, Writer, Image Generator, and Judge sub-agents,
displaying explicit sub-agent hand-off notifications, GCS public image URLs, Financial Times benchmark structure, and detailed Judge considerations.
"""

from google.adk.agents import Agent
from src.agents.searcher_agent import searcher_agent
from src.agents.politics_writer_agent import politics_writer_agent
from src.agents.economics_writer_agent import economics_writer_agent
from src.agents.science_writer_agent import science_writer_agent
from src.agents.judge_agent import judge_agent
from src.agents.image_generator_agent import image_generator_agent
from src.common.safety_config import (
    get_permissive_safety_config,
    before_model_sanitize_callback,
)
from .tools import draft_blog_post, publish_blog_post, publish_to_gcs


root_orchestrator_agent = Agent(
    name="root_orchestrator_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    before_model_callback=before_model_sanitize_callback,
    instruction="""You are the Root Orchestrator Agent for the Automated Blog Writer Platform.

Your primary duty is to coordinate article creation across specialized domain sub-agents and tools.

Workflow Instructions:
1. When a user requests an article or blog post on any topic:
   - Identify the primary domain: "Politicals", "Economics", or "Science".
   - Call the `draft_blog_post` tool with the topic and domain.
2. Structure your response clearly to present:
   - The sub-agent workflow hand-off notifications.
   - The full article title, hero image, introduction, analytical sections, and conclusion.
   - The editorial commentary and Judge Agent evaluation scores.
3. When the user confirms with 'PUBLISH', call `publish_blog_post` with the session ID.
""",
    sub_agents=[
        searcher_agent,
        politics_writer_agent,
        economics_writer_agent,
        science_writer_agent,
        judge_agent,
        image_generator_agent,
    ],
    tools=[draft_blog_post, publish_blog_post, publish_to_gcs]
)

