"""
Politics Writer Agent.
Domain expert in Political Science, Geopolitics, and Public Policy.
Configured with permissive safety settings for objective political commentary.
"""

from google.adk.agents import Agent
from src.common.safety_config import get_permissive_safety_config, on_model_error_fallback
from .tools import generate_political_hero_image, format_politics_markdown


politics_writer_agent = Agent(
    name="politics_writer_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    on_model_error_callback=on_model_error_fallback,
    instruction="""You are the Politics Writer Agent, an expert political analyst and investigative journalist.
Responsibilities:
1. Synthesize 3-4 political news articles provided by the Searcher Agent into objective geopolitical analysis.
2. Structure the article with a Catchy Title, Hero Image Data URI, Introduction, Body Sections, and Conclusion.
""",
    tools=[generate_political_hero_image, format_politics_markdown]
)
