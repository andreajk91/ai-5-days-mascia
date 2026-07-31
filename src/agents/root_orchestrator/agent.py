"""
Root Orchestrator Agent.
Serves as the primary entry point registered with Gemini Enterprise.
Orchestrates multi-agent production by delegating step-by-step to specialized sub-agents
(Searcher, Domain Writers, Judge) via ADK native sub-agent delegation.
"""

from google.adk.agents import Agent
from src.agents.searcher_agent import searcher_agent
from src.agents.politics_writer_agent import politics_writer_agent
from src.agents.economics_writer_agent import economics_writer_agent
from src.agents.science_writer_agent import science_writer_agent
from src.agents.judge_agent import judge_agent
from .tools import publish_to_gcs


root_orchestrator_agent = Agent(
    name="root_orchestrator_agent",
    model="gemini-3.6-flash",
    instruction="""You are the Root Orchestrator Agent for the Automated Blog Writer Platform.
Your role is to orchestrate multi-agent blog production by delegating tasks step-by-step to your specialized sub-agents:

1. **Research Delegation**: Forward the user's topic and requested domain to `searcher_agent` to find 3-4 news articles.
2. **Writing Delegation**: Forward the research bundle from `searcher_agent` to the specialized domain writer sub-agent:
   - For Politicals -> delegate to `politics_writer_agent`
   - For Economics -> delegate to `economics_writer_agent`
   - For Science -> delegate to `science_writer_agent`
3. **Quality Evaluation Delegation**: Forward the draft created by the Writer Agent to `judge_agent` to evaluate quality, coherence, and form.
   - If `judge_agent` rejects with feedback -> forward the critique back to the Writer Agent to rewrite until approved.
4. **Human Final Review Presentation**: Once `judge_agent` approves, present the candidate article directly to the user/journalist for review. Display:
   - Catchy Title
   - Rendered Hero Image (`![Hero Image](hero_image_url)`)
   - Introduction, Body Sections, and Conclusion
   - Editorial Commentary
   - Judge Quality Score & Evaluation
   Ask the user: *"Candidate article ready for final review! Reply 'PUBLISH' to store in Google Cloud Storage, or reply with feedback to revise."*
5. **GCS Publication**: When the user explicitly confirms approval (e.g. says "PUBLISH" or "OK to publish"), invoke the `publish_to_gcs` tool to upload the article to GCS bucket `gs://blog-writer-articles-gen-lang-client-0748552619` and share the public link.
""",
    sub_agents=[
        searcher_agent,
        politics_writer_agent,
        economics_writer_agent,
        science_writer_agent,
        judge_agent,
    ],
    tools=[publish_to_gcs]
)
