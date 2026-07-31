"""
Specialized Image Generator Agent.
Responsible for crafting topic-tailored, visually stunning, eye-catching hero images for all blog articles.
Configured with ADK before_model_callback sanitization.
"""

from google.adk.agents import Agent
from src.common.safety_config import (
    get_permissive_safety_config,
    before_model_sanitize_callback,
    on_model_error_fallback,
)
from .tools import generate_bespoke_hero_image


image_generator_agent = Agent(
    name="image_generator_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    before_model_callback=before_model_sanitize_callback,
    on_model_error_callback=on_model_error_fallback,
    instruction="""You are the Specialized Image Generator Agent, a master visual designer and creative director.

Your sole duty is to design and produce bespoke, eye-catching, high-impact hero images tailored specifically to the article topic:
1. Examine the article title, domain, and summary.
2. Formulate a rich visual design concept reflecting the core subject (e.g., oncology/DNA metaphors for medical science, Italian governance motifs for Italian policy reforms, financial chart/shipping corridors for macroeconomics).
3. Invoke `generate_bespoke_hero_image` with the title, domain, and summary to produce the final renderable hero image Data URI.
""",
    tools=[generate_bespoke_hero_image]
)
