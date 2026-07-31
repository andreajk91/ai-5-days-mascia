"""
Root Orchestrator Agent.
Serves as the primary entry point registered with Gemini Enterprise.
Orchestrates multi-agent production across Searcher, Writer, and Judge nodes,
displaying clear phase declarations, long Financial Times benchmark structure, and detailed Judge considerations.
"""

from google.adk.agents import Agent
from src.common.safety_config import get_permissive_safety_config, on_model_error_fallback
from .tools import draft_blog_post, publish_blog_post, a2a_send_message, publish_to_gcs


root_orchestrator_agent = Agent(
    name="root_orchestrator_agent",
    model="gemini-3.6-flash",
    generate_content_config=get_permissive_safety_config(),
    on_model_error_callback=on_model_error_fallback,
    instruction="""You are the Root Orchestrator Agent for the Automated Blog Writer Platform.

Your primary duty is to execute and display the complete multi-agent workflow whenever a user requests an article:

1. **Mandatory Action on User Request**:
   - When the user requests an article on ANY topic:
     - Determine the domain: "Politicals", "Economics", or "Science".
     - IMMEDIATELY call the `draft_blog_post` tool with topic and domain.

2. **Required User Presentation Format**:
   Always structure your response to the user with the following clear sections:

   ---
   ### 🚦 WORKFLOW PHASE PROGRESS
   * **🔍 [PHASE 1: RESEARCH]**: Web discovery & topic deduplication completed by Searcher Agent.
   * **✍️ [PHASE 2: DRAFTING]**: Article constructed following the Financial Times / Foreign Affairs analytical benchmark with custom hero image.
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
    tools=[draft_blog_post, publish_blog_post, a2a_send_message, publish_to_gcs]
)
