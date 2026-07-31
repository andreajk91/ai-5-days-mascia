"""
Specialized Image Generator Agent.
Responsible for crafting topic-tailored, visually stunning, eye-catching hero images for all blog articles.
Uploads hero images to GCS in us-central1 and returns control to root_orchestrator_agent.
"""

from google.adk.agents import Agent
from src.common.safety_config import (
    get_permissive_safety_config,
    before_model_sanitize_callback,
)
from .tools import generate_bespoke_hero_image


image_generator_agent = Agent(
    name="image_generator_agent",
    model="gemini-2.5-flash-lite",
    generate_content_config=get_permissive_safety_config(),

    before_model_callback=before_model_sanitize_callback,
    instruction="""You are the Image Generator Agent responsible for visual media design.

Instructions:
1. Examine the provided article title, domain, and summary.
2. Call `generate_bespoke_hero_image` with the title, domain, and summary.
3. Return the generated hero image result to root_orchestrator_agent.
""",
    tools=[generate_bespoke_hero_image]
)

