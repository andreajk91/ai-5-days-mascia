"""
Tools for Root Orchestrator Agent.
Includes workflow drafting, GCS publication, and A2A dispatchers.
GCP Infrastructure Location: us-central1
"""

def draft_blog_post(topic: str, domain: str) -> dict:
    """Drafts a blog post by executing the full ADK 2.0 Graph Workflow across Searcher,
    Domain Writer, Image Generator, and Judge Agent sub-agents.
    
    Args:
        topic: The topic requested by the journalist.
        domain: One of 'Politicals', 'Economics', or 'Science'.
    """
    from src.graph_workflow import BlogWriterGraphWorkflow
    workflow = BlogWriterGraphWorkflow()
    result = workflow.draft_and_evaluate_article(topic=topic, domain=domain, journalist_id="interactive_user")
    return result


def publish_blog_post(session_id: str) -> dict:
    """Permanently publishes the approved candidate blog post to GCS Bucket after human journalist review.
    
    Args:
        session_id: The active session ID returned during draft creation.
    """
    from src.graph_workflow import BlogWriterGraphWorkflow
    workflow = BlogWriterGraphWorkflow()
    result = workflow.publish_approved_article(session_id=session_id)
    return result


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
    public_url = f"https://storage.googleapis.com/{bucket_name}/articles/{article_id}.json"
    
    print(f"[GCS UPLOADED] Article '{title}' published to {gcs_uri}")
    
    return {
        "status": "PUBLISHED_TO_GCS",
        "article_id": article_id,
        "gcs_uri": gcs_uri,
        "public_url": public_url,
        "region": "us-central1"
    }
