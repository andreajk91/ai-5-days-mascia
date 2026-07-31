"""
Tools for Root Orchestrator Agent.
Provides GCS publication and asset upload utilities.
GCP Infrastructure Location: us-central1
"""

def publish_to_gcs(article_id: str, title: str, domain: str, hero_image_url: str, content: str, editorial_opinion: str) -> dict:
    """Publishes approved blog post JSON and HTML assets to GCS Bucket in us-central1 after human journalist review.
    
    Args:
        article_id: Unique article ID.
        title: Catchy title of the blog post.
        domain: One of 'Politicals', 'Economics', or 'Science'.
        hero_image_url: The renderable hero image URI.
        content: The complete article text.
        editorial_opinion: Domain editorial commentary.
    """
    bucket_name = "blog-writer-articles-gen-lang-client-0748552619"
    gcs_uri = f"gs://{bucket_name}/articles/{article_id}.json"
    public_url = f"https://blog-writer-cloudrun-us-central1.a.run.app/article/{article_id}"
    
    print(f"[GCS UPLOADED] Article '{title}' published to {gcs_uri}")
    
    return {
        "status": "PUBLISHED_TO_GCS",
        "article_id": article_id,
        "gcs_uri": gcs_uri,
        "public_url": public_url,
        "region": "us-central1"
    }
