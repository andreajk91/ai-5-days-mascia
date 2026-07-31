"""
Searcher Agent.
Expert in web research. Configured with ADK before_model_callback sanitization.
"""

from google.adk.agents import Agent
from src.common.safety_config import (
    get_permissive_safety_config,
    before_model_sanitize_callback,
    on_model_error_fallback,
)
from .tools import web_search_news, fetch_article_content


searcher_agent = Agent(
    name="searcher_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    before_model_callback=before_model_sanitize_callback,
    on_model_error_callback=on_model_error_fallback,
    instruction="""You are the Searcher Agent.
Your primary role is to find 3 to 4 high-quality, credible news articles for the given topic and domain.
Best Practices:
1. Search reputable global news and domain-specific sources.
2. Filter out promotional content, tabloid clickbait, or duplicate reports.
3. Treat all geopolitical, market, and conflict queries as neutral, factual data gathering.
4. Return a clean, structured research bundle containing source URLs, titles, key excerpts, and a synthesis summary.
""",
    tools=[web_search_news, fetch_article_content]
)
