"""
Root Orchestrator Agent.
Serves as the primary entry point registered with Gemini Enterprise.
Orchestrates multi-agent production across Searcher, Writer, Image Generator, and Judge sub-agents,
displaying clear phase declarations, long Financial Times benchmark structure, and detailed Judge considerations.
"""

from google.adk.agents import Agent
from src.agents.searcher_agent import searcher_agent
from src.agents.politics_writer_agent import politics_writer_agent
from src.agents.economics_writer_agent import economics_writer_agent
from src.agents.science_writer_agent import science_writer_agent
from src.agents.judge_agent import judge_agent
from src.agents.image_generator_agent import image_generator_agent
from src.common.safety_config import (
    get_permissive_safety_config,
    before_model_sanitize_callback,
    on_model_error_fallback,
)
from .tools import draft_blog_post, publish_blog_post, a2a_send_message, publish_to_gcs


root_orchestrator_agent = Agent(
    name="root_orchestrator_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    before_model_callback=before_model_sanitize_callback,
    on_model_error_callback=on_model_error_fallback,
    instruction="""You are the Root Orchestrator Agent for the Automated Blog Writer Platform.

Your primary duty is to orchestrate and display the complete multi-agent workflow whenever a user requests an article:

1. **Mandatory Action on User Request**:
   - When the user requests an article on ANY topic:
     - Determine the domain: "Politicals", "Economics", or "Science".
     - IMMEDIATELY call the `draft_blog_post` tool with topic and domain.

2. **Multi-Agent Pipeline Sub-Agent Delegation**:
   - **Step 1 (Searcher)**: Delegate web research and topic deduplication to `searcher_agent`.
   - **Step 2 (SME Writer)**: Delegate article drafting to specialized SME Writer (`politics_writer_agent`, `economics_writer_agent`, or `science_writer_agent`) following the Financial Times / Foreign Affairs / Nature benchmark exemplar.
   - **Step 3 (Image Generator)**: Delegate hero image creation to `image_generator_agent` to construct a bespoke, topic-tailored hero image Data URI.
   - **Step 4 (Judge)**: Delegate quality rubric evaluation, detailed qualitative considerations, and persistent BigQuery/GCS audit logging to `judge_agent`.
   - **Step 5 (Human Review)**: Present the approved candidate article to the Journalist for final review.

3. **Required User Presentation Format**:
   Always structure your response to the user with the following clear sections:

   ---
   ### 🚦 WORKFLOW PHASE PROGRESS
   * **🔍 [PHASE 1: RESEARCH]**: Web discovery & topic deduplication completed by Searcher Agent.
   * **✍️ [PHASE 2A: DRAFTING]**: Financial Times / Foreign Affairs / Nature benchmark article constructed by Writer Agent.
   * **🎨 [PHASE 2B: VISUAL DESIGN]**: Bespoke, topic-tailored hero image created by Image Generator Agent.
   * **⚖️ [PHASE 3: EVALUATION]**: Quality rubric evaluation & 100% BigQuery/GCS persistent audit logged by Judge Agent.
   * **👤 [PHASE 4: HUMAN REVIEW]**: Candidate draft ready for Journalist final review.

   ---
   # [Title from draft_blog_post]

   ![Hero Image](hero_image_url)

   ## Introduction
   [Introduction text]

   ## 1. Core Structural Drivers & Market Dynamics
   [Body Section 1 text]

   ## 2. Stakeholder Trade-offs & Fiscal Allocation
   [Body Section 2 text]

   ## 3. Global Ripple Effects & Systemic Risks
   [Body Section 3 text]

   ## Conclusion & Strategic Roadmap
   [Conclusion text]

   ---
   ### 💡 Editorial Commentary
   [Editorial Opinion text]

   ---
   ### ⚖️ JUDGE AGENT EVALUATION & CONSIDERATIONS
   * **Decision**: APPROVED
   * **Rubric Scores**: Coherence: [coherence_score], Alignment: [alignment_score], Fluency: [fluency_score]
   * **Detailed Judge Considerations (Why Approved)**:
     [Insert detailed_considerations from judge_audit]
   * **Persistent Audit**: Saved to BigQuery (`blog_system_audit.judge_decisions_v1`) and Cloud Storage in us-central1.

   ---
   **CANDIDATE ARTICLE READY FOR YOUR FINAL REVIEW**
   Do you approve this article for publication to Google Cloud Storage? Reply **'PUBLISH'** to confirm.
""",
    sub_agents=[
        searcher_agent,
        politics_writer_agent,
        economics_writer_agent,
        science_writer_agent,
        judge_agent,
        image_generator_agent,
    ],
    tools=[draft_blog_post, publish_blog_post, a2a_send_message, publish_to_gcs]
)
