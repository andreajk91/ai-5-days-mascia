"""
Tools for Politics Writer Agent.
Generates real renderable hero images and formats political articles.
"""

from src.common.image_generator import generate_domain_hero_image


def generate_political_hero_image(prompt: str) -> dict:
    """Generates a high-quality hero image for political articles returning a renderable image URI."""
    image_url = generate_domain_hero_image(prompt, "Politicals")
    return {
        "prompt": prompt,
        "image_url": image_url,
        "status": "GENERATED"
    }


def format_politics_markdown(title: str, intro: str, body: list, conclusion: str) -> str:
    """Formats political article sections into clean Markdown."""
    sections = "\n\n".join([f"### {b['heading']}\n{b['content']}" for b in body])
    return f"# {title}\n\n{intro}\n\n{sections}\n\n### Conclusion\n{conclusion}"
