"""
Economics Writer Agent.
Domain expert in Macroeconomics, Global Markets, Fiscal Policy, and Trade Disruption.
Configured with permissive safety settings for objective economic commentary.
"""

from google.adk.agents import Agent
from src.common.safety_config import get_permissive_safety_config, on_model_error_fallback
from .tools import generate_economics_hero_image, format_economics_markdown


economics_writer_agent = Agent(
    name="economics_writer_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    on_model_error_callback=on_model_error_fallback,
    instruction="""You are the Economics Writer Agent, a senior financial analyst and economic journalist.
Responsibilities:
1. Synthesize 3-4 economic/financial news articles into objective macroeconomic and market impact analysis.
2. Structure the article with a Catchy Title, Hero Image Data URI, Introduction, Body Sections, and Conclusion.
""",
    tools=[generate_economics_hero_image, format_economics_markdown]
)
