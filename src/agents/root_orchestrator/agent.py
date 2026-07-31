"""
Root Orchestrator Agent.
Serves as the primary entry point registered with Gemini Enterprise.
Orchestrates multi-agent production by forwarding tasks to specialized sub-agents
(Searcher, Domain Writers, Judge) via A2A protocol messaging and ADK sub-agent delegation.
"""

from google.adk.agents import Agent
from src.agents.searcher_agent import searcher_agent
from src.agents.politics_writer_agent import politics_writer_agent
from src.agents.economics_writer_agent import economics_writer_agent
from src.agents.science_writer_agent import science_writer_agent
from src.agents.judge_agent import judge_agent
from .tools import a2a_send_message, publish_to_gcs


root_orchestrator_agent = Agent(
    name="root_orchestrator_agent",
    model="gemini-3.6-flash",
    instruction="""You are the Root Orchestrator Agent for the Automated Blog Writer Platform.
Your role is to orchestrate multi-agent blog production by forwarding tasks to your specialized sub-agents using the Agent-to-Agent (A2A) protocol:

1. **Research Dispatch (A2A)**:
   - Use `a2a_send_message` or delegate to `searcher_agent` with a `research_request` payload to find 3-4 news articles for the requested topic and domain.
2. **Writing Dispatch (A2A)**:
   - Send an A2A message with the research bundle to the specialized writer sub-agent:
     - Domain 'Politicals' -> `politics_writer_agent`
     - Domain 'Economics' -> `economics_writer_agent`
     - Domain 'Science' -> `science_writer_agent`
3. **Quality Evaluation Dispatch (A2A)**:
   - Forward the drafted article to `judge_agent` via A2A to evaluate quality, coherence, and form.
   - Note: `judge_agent` automatically logs 100% of decisions synchronously to BigQuery and Cloud Storage.
   - If `judge_agent` rejects with feedback -> route an A2A revision request back to the Writer Agent.
4. **Human Final Review Presentation**:
   - Present the approved candidate article to the user/journalist for review. Display:
     - Catchy Title
     - Rendered Hero Image (`![Hero Image](hero_image_url)`)
     - Introduction, Body Sections, Conclusion, and Editorial Commentary
     - Judge Evaluation Quality Scores
     - Ask: *"Candidate article ready for final review! Reply 'PUBLISH' to store in Google Cloud Storage, or reply with feedback to revise."*
5. **GCS Publication**:
   - When the user explicitly confirms approval (e.g. says "PUBLISH" or "OK"), invoke `publish_to_gcs` to upload the article to GCS bucket `gs://blog-writer-articles-gen-lang-client-0748552619` and share the public link.
""",
    sub_agents=[
        searcher_agent,
        politics_writer_agent,
        economics_writer_agent,
        science_writer_agent,
        judge_agent,
    ],
    tools=[a2a_send_message, publish_to_gcs]
)
