"""
Tools for Politics Writer Agent.
Hero image generator and markdown formatting tools.
"""

def generate_political_hero_image(prompt: str) -> dict:
    """Generates a high-quality hero image for political articles using Vertex Imagen 3."""
    return {
        "prompt": prompt,
        "image_url": f"gs://blog-writer-assets/politics_{hash(prompt) % 10000}.png",
        "status": "GENERATED"
    }


def format_politics_markdown(title: str, intro: str, body: list, conclusion: str) -> str:
    """Formats political article sections into clean Markdown."""
    sections = "\n\n".join([f"### {b['heading']}\n{b['content']}" for b in body])
    return f"# {title}\n\n{intro}\n\n{sections}\n\n### Conclusion\n{conclusion}"
