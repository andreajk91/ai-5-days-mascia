"""
FastAPI web server for ADK Playground UI and A2A Protocol endpoints.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from google.adk.cli.fast_api import get_fastapi_app
from app.agent import root_agent

app = get_fastapi_app(agent=root_agent)
