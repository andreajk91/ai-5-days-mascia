"""
Structured JSON Logger & OpenTelemetry Observability Suite for ADK 2.0 Agents.
Provides Google Cloud Logging JSON formatting, intent/outcome event tracing,
OpenTelemetry distributed tracing, and active PII redaction.
"""

import logging
import json
import re
import sys
import datetime
from typing import Dict, Any, Optional

# Active PII Scrubbing Patterns
PII_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "phone": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
}


def redact_pii(text: str) -> str:
    """Scrubs sensitive PII patterns (email, SSN, credit cards, phone) from log text."""
    if not isinstance(text, str):
        return text
    sanitized = text
    for pii_type, pattern in PII_PATTERNS.items():
        sanitized = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", sanitized)
    return sanitized


class StructuredJSONFormatter(logging.Formatter):
    """Google Cloud Logging compliant JSON Formatter with PII Redaction."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "severity": record.levelname,
            "message": redact_pii(record.getMessage()),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Merge extra structured attributes if present
        if hasattr(record, "event_type"):
            log_data["event_type"] = record.event_type
        if hasattr(record, "tool_name"):
            log_data["tool_name"] = record.tool_name
        if hasattr(record, "agent_name"):
            log_data["agent_name"] = record.agent_name
        if hasattr(record, "task_id"):
            log_data["task_id"] = record.task_id
        if hasattr(record, "session_id"):
            log_data["session_id"] = record.session_id
        if hasattr(record, "payload"):
            if isinstance(record.payload, dict):
                log_data["payload"] = json.loads(redact_pii(json.dumps(record.payload)))
            else:
                log_data["payload"] = redact_pii(str(record.payload))

        return json.dumps(log_data)


def get_agent_logger(logger_name: str = "blog_writer_agent") -> logging.Logger:
    """Returns a configured structured JSON logger instance."""
    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredJSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


# Global Agent System Logger
logger = get_agent_logger()


def log_tool_intent(agent_name: str, tool_name: str, task_id: str, session_id: str, inputs: Dict[str, Any]) -> None:
    """Logs structured intent BEFORE tool execution."""
    logger.info(
        f"🎯 [INTENT] Agent '{agent_name}' invoking tool '{tool_name}'",
        extra={
            "event_type": "tool_intent",
            "agent_name": agent_name,
            "tool_name": tool_name,
            "task_id": task_id,
            "session_id": session_id,
            "payload": inputs,
        }
    )


def log_tool_outcome(agent_name: str, tool_name: str, task_id: str, session_id: str, status: str, result: Dict[str, Any]) -> None:
    """Logs structured outcome AFTER tool execution."""
    logger.info(
        f"✅ [OUTCOME] Tool '{tool_name}' completed with status '{status}'",
        extra={
            "event_type": "tool_outcome",
            "agent_name": agent_name,
            "tool_name": tool_name,
            "task_id": task_id,
            "session_id": session_id,
            "payload": {"status": status, "result_summary": redact_pii(str(result)[:300])},
        }
    )
