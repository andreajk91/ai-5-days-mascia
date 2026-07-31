"""
Tools for Science Writer Agent.
Generates real renderable hero images and formats science articles.
"""

from src.common.image_generator import generate_domain_hero_image


def generate_science_hero_image(prompt: str) -> dict:
    """Generates a high-quality hero image for science articles returning a renderable image URI."""
    image_url = generate_domain_hero_image(prompt, "Science")
    return {
        "prompt": prompt,
        "image_url": image_url,
        "status": "GENERATED"
    }


def format_science_markdown(title: str, intro: str, body: list, conclusion: str) -> str:
    """Formats science article sections into clean Markdown."""
    sections = "\n\n".join([f"### {b['heading']}\n{b['content']}" for b in body])
    return f"# {title}\n\n{intro}\n\n{sections}\n\n### Conclusion\n{conclusion}"
