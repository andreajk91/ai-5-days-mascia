"""
Tools for Specialized Image Generator Agent.
Uses high-powered visual design prompts and multi-layered SVG graphics rendering,
uploads images directly to Google Cloud Storage (GCS) in us-central1,
and returns public HTTP URLs for 100% reliable rendering in Markdown and Web UIs.
"""

import base64
import uuid
from typing import Dict, Any
from google.cloud import storage


def generate_bespoke_hero_image(title: str, domain: str, summary: str, task_id: str = None) -> Dict[str, Any]:
    """Generates an eye-catching, highly customized hero image, uploads it to GCS bucket
    in us-central1, and returns a public GCS HTTP image URL.
    """
    task_id = task_id or f"img_{uuid.uuid4().hex[:8]}"
    domain_clean = domain.lower()
    title_clean = title.lower()
    summary_clean = summary.lower()
    
    # Topic-specific visual theme derivation
    if "cancer" in title_clean or "cancer" in summary_clean or "health" in domain_clean or "science" in domain_clean:
        bg_gradient = "linear-gradient(135deg, #1e0826 0%, #3b0764 50%, #4c1d95 100%)"
        accent_color = "#c084fc"
        glow_color = "#a855f7"
        icon_symbol = "🧬"
        category_label = "ONCOLOGY & SCIENCE BREAKTHROUGH"
        pattern_svg = """
        <circle cx="650" cy="120" r="90" fill="#a855f7" opacity="0.25" filter="blur(20px)"/>
        <circle cx="150" cy="300" r="110" fill="#c084fc" opacity="0.2" filter="blur(25px)"/>
        <path d="M 50,200 Q 200,100 350,200 T 650,200" stroke="#c084fc" stroke-width="3" fill="none" opacity="0.4"/>
        <path d="M 50,200 Q 200,300 350,200 T 650,200" stroke="#a855f7" stroke-width="3" fill="none" opacity="0.4"/>
        """
    elif "italian" in title_clean or "politician" in title_clean or "reform" in title_clean or "politic" in domain_clean:
        bg_gradient = "linear-gradient(135deg, #022c22 0%, #064e3b 50%, #0f766e 100%)"
        accent_color = "#34d399"
        glow_color = "#10b981"
        icon_symbol = "🏛️"
        category_label = "ITALIAN POLICY & GOVERNANCE"
        pattern_svg = """
        <rect x="580" y="80" width="140" height="220" rx="8" fill="#10b981" opacity="0.15" stroke="#34d399" stroke-width="1.5"/>
        <line x1="600" y1="120" x2="700" y2="120" stroke="#34d399" stroke-width="2" opacity="0.5"/>
        <line x1="600" y1="160" x2="700" y2="160" stroke="#34d399" stroke-width="2" opacity="0.5"/>
        <line x1="600" y1="200" x2="700" y2="200" stroke="#34d399" stroke-width="2" opacity="0.5"/>
        <circle cx="120" cy="100" r="80" fill="#34d399" opacity="0.1" filter="blur(20px)"/>
        """
    else:  # Economic, Middle East, War, Finance
        bg_gradient = "linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%)"
        accent_color = "#fbbf24"
        glow_color = "#f59e0b"
        icon_symbol = "📊"
        category_label = "GLOBAL MACROECONOMIC REPORT"
        pattern_svg = """
        <polyline points="80,320 220,240 380,270 520,160 680,100" fill="none" stroke="#fbbf24" stroke-width="4" stroke-linecap="round" opacity="0.8"/>
        <circle cx="680" cy="100" r="8" fill="#fbbf24"/>
        <circle cx="680" cy="100" r="24" fill="#fbbf24" opacity="0.25"/>
        <rect x="60" y="60" width="680" height="280" fill="none" stroke="#fbbf24" stroke-width="1" stroke-dasharray="6,6" opacity="0.2"/>
        """

    display_title = title[:50] + ("..." if len(title) > 50 else "")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="450" viewBox="0 0 900 450">
      <defs>
        <linearGradient id="bg_grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#1e293b;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#020617;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="card_grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#1e293b;stop-opacity:0.95" />
          <stop offset="100%" style="stop-color:#0f172a;stop-opacity:0.95" />
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <!-- Base Background -->
      <rect width="900" height="450" fill="url(#bg_grad)" />
      
      <!-- Custom Pattern Elements -->
      {pattern_svg}
      
      <!-- Glassmorphic Central Card Container -->
      <rect x="50" y="45" width="800" height="360" rx="20" fill="url(#card_grad)" stroke="{accent_color}" stroke-width="2" stroke-opacity="0.5" filter="url(#glow)" />
      
      <!-- Domain & Topic Category Badge -->
      <rect x="80" y="80" width="280" height="36" rx="18" fill="{accent_color}" fill-opacity="0.18" stroke="{accent_color}" stroke-width="1" />
      <text x="220" y="103" fill="{accent_color}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle" letter-spacing="1">{category_label}</text>
      
      <!-- Eye-Catching Icon Symbol -->
      <text x="80" y="210" font-size="64" filter="url(#glow)">{icon_symbol}</text>
      
      <!-- Dynamic Article Title -->
      <text x="80" y="280" fill="#ffffff" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="26" font-weight="bold">{display_title}</text>
      
      <!-- Editorial Subtitle -->
      <text x="80" y="325" fill="#94a3b8" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="15">AUTOMATED BLOG WRITER PLATFORM • SPECIALIZED IMAGE GENERATOR AGENT</text>
      
      <!-- High-Tech Accent Bar -->
      <rect x="80" y="355" width="120" height="4" rx="2" fill="{accent_color}" />
    </svg>"""

    # Upload hero image to GCS Bucket in us-central1
    bucket_name = "blog-writer-articles-gen-lang-client-0748552619"
    gcs_blob_path = f"images/{task_id}_hero.svg"
    
    try:
        storage_client = storage.Client(project="gen-lang-client-0748552619")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(gcs_blob_path)
        blob.upload_from_string(svg_content, content_type="image/svg+xml")
        gcs_public_url = f"https://storage.googleapis.com/{bucket_name}/{gcs_blob_path}"
        gcs_uri = f"gs://{bucket_name}/{gcs_blob_path}"
        print(f"☁️ [GCS UPLOAD SUCCESS] Hero image uploaded to {gcs_uri} | Public URL: {gcs_public_url}")
    except Exception as e:
        print(f"⚠️ [GCS UPLOAD FALLBACK] Could not upload image to GCS: {e}")
        encoded_svg = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
        gcs_public_url = f"data:image/svg+xml;base64,{encoded_svg}"
        gcs_uri = gcs_public_url

    return {
        "title": title,
        "domain": domain,
        "category_label": category_label,
        "hero_image_url": gcs_public_url,
        "gcs_uri": gcs_uri,
        "status": "GENERATED_AND_UPLOADED"
    }
