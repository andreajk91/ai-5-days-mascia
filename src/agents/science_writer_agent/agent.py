"""
Science Writer Agent.
Domain expert in Technological Innovation, AI, Space, Medicine, and Research.
Configured with permissive safety settings for objective science commentary.
"""

from google.adk.agents import Agent
from src.common.safety_config import get_permissive_safety_config, on_model_error_fallback
from .tools import generate_science_hero_image, format_science_markdown


science_writer_agent = Agent(
    name="science_writer_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    on_model_error_callback=on_model_error_fallback,
    instruction="""You are the Science Writer Agent, a prominent science journalist and technology commentator.
Responsibilities:
1. Synthesize 3-4 scientific/technological news articles into objective science journalism.
2. Structure the article with a Catchy Title, Hero Image Data URI, Introduction, Body Sections, and Conclusion.
""",
    tools=[generate_science_hero_image, format_science_markdown]
)
