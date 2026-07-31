"""
Tools for Science Writer Agent.
Generates real renderable hero images and formats science articles safely.
"""

from typing import Any
from src.common.image_generator import generate_domain_hero_image


def generate_science_hero_image(prompt: str) -> dict:
    """Generates a high-quality hero image for science articles returning a renderable image URI."""
    image_url = generate_domain_hero_image(prompt, "Science")
    return {
        "prompt": prompt,
        "image_url": image_url,
        "status": "GENERATED"
    }


def format_science_markdown(title: str, intro: str, body: Any, conclusion: str) -> str:
    """Formats science article sections into clean Markdown safely handling lists of dicts or strings."""
    formatted_body = []
    if isinstance(body, list):
        for i, item in enumerate(body, 1):
            if isinstance(item, dict):
                heading = item.get("heading", f"Section {i}")
                content = item.get("content", str(item))
                formatted_body.append(f"### {heading}\n{content}")
            elif isinstance(item, str):
                formatted_body.append(f"### Key Section {i}\n{item}")
            else:
                formatted_body.append(str(item))
    elif isinstance(body, str):
        formatted_body.append(body)
    else:
        formatted_body.append(str(body))
        
    sections = "\n\n".join(formatted_body)
    return f"# {title}\n\n{intro}\n\n{sections}\n\n### Conclusion\n{conclusion}"
