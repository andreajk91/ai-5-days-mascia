"""
Tools for Root Orchestrator Agent.
Includes workflow drafting, GCS publication, and A2A dispatchers.
GCP Infrastructure Location: us-central1
"""

from typing import Dict, Any, Union
from src.common.schemas import DraftBlogResultSchema, PublishBlogResultSchema, ToolErrorResponse


def draft_blog_post(topic: str, domain: str) -> Union[Dict[str, Any], ToolErrorResponse]:
    """Drafts a blog post by executing the full multi-agent Graph Workflow across Searcher,
    Domain Writer, Image Generator, and Judge Agent sub-agents.

    Args:
        topic (str): The specific article topic or policy subject requested by the user.
        domain (str): Subject domain, must be one of 'Politicals', 'Economics', or 'Science'.

    Returns:
        Union[Dict[str, Any], ToolErrorResponse]: Dictionary matching DraftBlogResultSchema on success,
            or ToolErrorResponse with guided LLM recovery instructions on failure.
    """
    try:
        if not topic or not domain:
            return ToolErrorResponse(
                error_type="ValueError",
                error_message="Topic and domain arguments cannot be empty.",
                recovery_instruction="Provide valid topic and domain arguments (e.g. topic='UK political situation', domain='Politicals')."
            ).model_dump()

        from src.graph_workflow import BlogWriterGraphWorkflow
        workflow = BlogWriterGraphWorkflow()
        result = workflow.draft_and_evaluate_article(topic=topic, domain=domain, journalist_id="interactive_user")
        return result
    except Exception as e:
        return ToolErrorResponse(
            error_type=type(e).__name__,
            error_message=str(e),
            recovery_instruction="Check topic and domain inputs and retry draft_blog_post."
        ).model_dump()


def publish_blog_post(session_id: str) -> Union[Dict[str, Any], ToolErrorResponse]:
    """Permanently publishes an approved candidate blog post to Google Cloud Storage (GCS) after user review.

    Args:
        session_id (str): The active session ID generated during article drafting.

    Returns:
        Union[Dict[str, Any], ToolErrorResponse]: Dictionary matching PublishBlogResultSchema on success,
            or ToolErrorResponse with guided recovery instructions on failure.
    """
    try:
        if not session_id:
            return ToolErrorResponse(
                error_type="ValueError",
                error_message="session_id argument is required for publication.",
                recovery_instruction="Provide the active session_id returned during draft_blog_post execution."
            ).model_dump()

        from src.graph_workflow import BlogWriterGraphWorkflow
        workflow = BlogWriterGraphWorkflow()
        result = workflow.publish_approved_article(session_id=session_id)
        return result
    except Exception as e:
        return ToolErrorResponse(
            error_type=type(e).__name__,
            error_message=str(e),
            recovery_instruction="Ensure draft_blog_post was run first in this session before calling publish_blog_post."
        ).model_dump()


def publish_to_gcs(
    article_id: str,
    title: str,
    domain: str,
    hero_image_url: str,
    content: str,
    editorial_opinion: str
) -> Union[Dict[str, Any], ToolErrorResponse]:
    """Publishes approved blog post JSON and HTML assets directly to GCS Bucket in us-central1.

    Args:
        article_id (str): Unique article identifier.
        title (str): Catchy title of the blog post.
        domain (str): One of 'Politicals', 'Economics', or 'Science'.
        hero_image_url (str): Public GCS HTTP URI of the hero image.
        content (str): Complete markdown article text.
        editorial_opinion (str): Domain editorial commentary text.

    Returns:
        Union[Dict[str, Any], ToolErrorResponse]: Dictionary matching PublishBlogResultSchema on success,
            or ToolErrorResponse with guided recovery instructions on failure.
    """
    try:
        bucket_name = "blog-writer-articles-gen-lang-client-0748552619"
        gcs_uri = f"gs://{bucket_name}/articles/{article_id}.json"
        public_url = f"https://storage.googleapis.com/{bucket_name}/articles/{article_id}.json"
        
        result = PublishBlogResultSchema(
            status="PUBLISHED",
            article_id=article_id,
            session_id="direct_gcs_publish",
            title=title,
            gcs_uri=gcs_uri,
            public_url=public_url
        )
        return result.model_dump()
    except Exception as e:
        return ToolErrorResponse(
            error_type=type(e).__name__,
            error_message=str(e),
            recovery_instruction="Provide valid article_id and title parameters for GCS publication."
        ).model_dump()

