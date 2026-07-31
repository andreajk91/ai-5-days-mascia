"""
Searcher Agent.
Expert in web research. Finds 3-4 news articles for a given topic,
evaluates source credibility, checks for anti-duplication, and formats a research bundle.
"""

from google.adk.agents import Agent
from .tools import web_search_news, fetch_article_content


searcher_agent = Agent(
    name="searcher_agent",
    model="gemini-3.6-flash",
    instruction="""You are the Searcher Agent.
Your primary role is to find 3 to 4 high-quality, credible news articles for the given topic and domain.
Best Practices:
1. Search reputable global news and domain-specific sources.
2. Filter out promotional content, tabloid clickbait, or duplicate reports.
3. Return a clean, structured research bundle containing source URLs, titles, key excerpts, and a synthesis summary.
4. Use A2A to deliver the research bundle directly to the specialized Writer Agent.
""",
    tools=[web_search_news, fetch_article_content]
)
