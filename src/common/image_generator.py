"""
Common Image Generator Helper.
Bridge helper for domain-specific writer agent hero image tools.
"""

from src.agents.image_generator_agent.tools import generate_bespoke_hero_image


def generate_domain_hero_image(prompt: str, domain: str) -> str:
    """Generates a high-quality SVG hero image URI for the requested domain and prompt."""
    res = generate_bespoke_hero_image(title=prompt, domain=domain, summary=prompt, task_id="hero_common")
    return res.get("hero_image_url", "https://storage.googleapis.com/blog-writer-articles-gen-lang-client-0748552619/images/hero_common.svg")
