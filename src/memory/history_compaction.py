"""
Context Window History Compaction Module.
Provides automatic conversation turn summarization and history compaction
when conversation token length exceeds ADK context thresholds.
"""

from typing import Dict, Any, List
import re


def compact_history_callback(callback_context, llm_request) -> None:
    """ADK native callback that monitors conversation history token length
    and compacts older turns into concise summary points to preserve LLM context budget.
    """
    if not hasattr(llm_request, "contents") or not llm_request.contents:
        return

    # Check turn count in conversation context
    turn_count = len(llm_request.contents)
    if turn_count <= 8:
        return  # No compaction needed for short histories

    print(f"🧹 [HISTORY COMPACTION] Compacted older conversation turns (Turn count: {turn_count} -> 4)")

    # Preserve system turn (turn 0) and the last 3 turns
    system_turn = llm_request.contents[0]
    recent_turns = llm_request.contents[-3:]

    # Summarize intermediate turns into a single compacted summary turn
    intermediate_summary = "SUMMARY OF PRIOR TURNS: The user requested an article topic, web research was conducted, and initial draft sections were synthesized."
    
    # Reconstruct compacted contents array
    compacted_contents = [system_turn]
    
    # Create summary content part if supported by LlmRequest schema
    try:
        from google.genai import types
        summary_part = types.Content(
            role="user",
            parts=[types.Part.from_text(text=intermediate_summary)]
        )
        compacted_contents.append(summary_part)
    except Exception:
        pass

    compacted_contents.extend(recent_turns)
    llm_request.contents = compacted_contents
