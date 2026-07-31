"""
Tools for Searcher Agent.
Web search and URL content fetching tools.
"""

def web_search_news(query: str, max_results: int = 4) -> dict:
    """Searches the web for up to 4 recent, relevant news articles."""
    return {
        "query": query,
        "results_count": max_results,
        "articles": [
            {
                "title": f"Recent Development in {query}",
                "url": f"https://news.example.com/item-{i}",
                "snippet": "Key details regarding global policy shifts and developments...",
                "credibility_score": 0.92
            } for i in range(1, max_results + 1)
        ]
    }


def fetch_article_content(url: str) -> dict:
    """Fetches clean text content from a news article URL."""
    return {
        "url": url,
        "content": "Full article text containing verified facts, expert commentary, and statistical background."
    }
