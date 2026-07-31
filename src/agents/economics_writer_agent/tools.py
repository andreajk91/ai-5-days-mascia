"""
Tools for Economics Writer Agent.
Generates real renderable hero images and formats economic articles.
"""

from src.common.image_generator import generate_domain_hero_image


def generate_economics_hero_image(prompt: str) -> dict:
    """Generates a high-quality hero image for economics articles returning a renderable image URI."""
    image_url = generate_domain_hero_image(prompt, "Economics")
    return {
        "prompt": prompt,
        "image_url": image_url,
        "status": "GENERATED"
    }


def format_economics_markdown(title: str, intro: str, body: list, conclusion: str) -> str:
    """Formats economic article sections into clean Markdown."""
    sections = "\n\n".join([f"### {b['heading']}\n{b['content']}" for b in body])
    return f"# {title}\n\n{intro}\n\n{sections}\n\n### Conclusion\n{conclusion}"
