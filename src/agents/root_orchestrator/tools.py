"""
Tools for Root Orchestrator Agent.
Includes A2A dispatchers and GCS publication utilities.
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
    """Publishes approved blog post JSON and HTML assets to GCS Bucket."""
    return {
        "status": "PUBLISHED",
        "gcs_uri": f"gs://blog-writer-public-bucket/articles/{article_id}.json",
        "public_url": f"https://blog-writer-cloudrun.a.run.app/article/{article_id}"
    }
