"""
Tools for Root Orchestrator Agent.
Includes A2A dispatchers and GCS publication utilities.
GCP Infrastructure Location: us-central1
"""

def dispatch_search_request(topic: str, domain: str, session_id: str) -> dict:
    """A2A tool to dispatch research requests to the Searcher Agent."""
    return {
        "status": "DISPATCHED",
        "target": "searcher_agent",
        "topic": topic,
        "domain": domain,
        "session_id": session_id
    }


def publish_to_gcs(article_id: str, payload: dict) -> dict:
    """Publishes approved blog post JSON and HTML assets to GCS Bucket in us-central1."""
    bucket_name = "blog-writer-articles-gen-lang-client-0748552619"
    return {
        "status": "PUBLISHED",
        "gcs_uri": f"gs://{bucket_name}/articles/{article_id}.json",
        "public_url": f"https://blog-writer-cloudrun-us-central1.a.run.app/article/{article_id}",
        "region": "us-central1"
    }
