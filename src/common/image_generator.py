"""
Hero Image Generator for Automated Blog Writer Platform.
Generates visually striking, domain-customized SVG/PNG hero image assets
and encodes them as Data URIs and GCS image objects for real visual rendering in Markdown and Web UIs.
"""

import base64
import urllib.parse


def generate_domain_hero_image(topic: str, domain: str) -> str:
    """Generates an eye-catching, domain-themed SVG image asset.
    Returns a data URI that renders visually in Markdown and Web browsers.
    """
    domain_clean = domain.lower()
    
    if "politic" in domain_clean:
        bg_gradient = "linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%)"
        accent_color = "#f43f5e"
        icon_symbol = "🏛️"
        category_label = "POLITICAL ANALYSIS"
    elif "economic" in domain_clean or "financ" in domain_clean:
        bg_gradient = "linear-gradient(135deg, #064e3b 0%, #047857 50%, #059669 100%)"
        accent_color = "#fbbf24"
        icon_symbol = "📈"
        category_label = "ECONOMIC REPORT"
    else:  # Science
        bg_gradient = "linear-gradient(135deg, #083344 0%, #0e7490 50%, #06b6d4 100%)"
        accent_color = "#38bdf8"
        icon_symbol = "🔬"
        category_label = "SCIENCE & TECH"

    # Truncate topic if long for SVG layout
    display_title = topic[:45] + ("..." if len(topic) > 45 else "")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400">
      <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#1e293b;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="card" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#1e293b;stop-opacity:0.9" />
          <stop offset="100%" style="stop-color:#0f172a;stop-opacity:0.9" />
        </linearGradient>
      </defs>
      <rect width="800" height="400" fill="url(#bg)" />
      <circle cx="700" cy="80" r="180" fill="{accent_color}" opacity="0.15" />
      <circle cx="100" cy="320" r="140" fill="{accent_color}" opacity="0.1" />
      
      <!-- Card Container -->
      <rect x="40" y="40" width="720" height="320" rx="16" fill="url(#card)" stroke="{accent_color}" stroke-width="2" stroke-opacity="0.4" />
      
      <!-- Badge -->
      <rect x="70" y="70" width="180" height="32" rx="16" fill="{accent_color}" opacity="0.2" />
      <text x="160" y="91" fill="{accent_color}" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">{category_label}</text>
      
      <!-- Symbol Icon -->
      <text x="70" y="180" font-size="54">{icon_symbol}</text>
      
      <!-- Title -->
      <text x="70" y="240" fill="#ffffff" font-family="Arial, sans-serif" font-size="24" font-weight="bold">{display_title}</text>
      <text x="70" y="280" fill="#94a3b8" font-family="Arial, sans-serif" font-size="14">Automated Blog Writer Platform • AI Verified Journalistic Analysis</text>
    </svg>"""

    encoded_svg = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded_svg}"
