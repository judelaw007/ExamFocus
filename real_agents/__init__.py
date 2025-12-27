"""
ExamFocus Multi-Agent Content Pipeline

A production-ready multi-agent system for creating exam-focused educational content.
"""

__version__ = "1.0.0"

from .pipeline.orchestrator import ContentPipeline
from .agents.base import BaseAgent, AgentOutput

__all__ = ["ContentPipeline", "BaseAgent", "AgentOutput"]
