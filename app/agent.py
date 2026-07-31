"""
App Agent Entrypoint for agents-cli playground and ADK serving.
Bridges to the Root Orchestrator Agent and ADK 2.0 Graph Workflow.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents import root_orchestrator_agent

agent = root_orchestrator_agent
