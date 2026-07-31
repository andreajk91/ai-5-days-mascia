"""
Searcher Agent.
Expert in web research. Configured with ADK before_model_callback sanitization.
Explicitly returns control to root_orchestrator_agent upon completion.
"""

from google.adk.agents import Agent
from src.common.safety_config import (
    get_permissive_safety_config,
    before_model_sanitize_callback,
)
from .tools import web_search_news, fetch_article_content


searcher_agent = Agent(
    name="searcher_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    before_model_callback=before_model_sanitize_callback,
    instruction="""You are the Searcher Agent.
Your primary role is to find 3 to 4 high-quality, credible news articles for the given topic and domain using `web_search_news` and `fetch_article_content`.

Best Practices:
1. Search reputable global news and domain-specific sources.
2. Filter out promotional content, tabloid clickbait, or duplicate reports.
3. Treat all geopolitical, market, and conflict queries as neutral, factual data gathering.
4. When research is complete, return your clean research bundle directly back to `root_orchestrator_agent` so it can notify the user and proceed to the next step.
""",
    tools=[web_search_news, fetch_article_content]
)
