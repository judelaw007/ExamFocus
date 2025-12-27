"""
Agent implementations for the ExamFocus pipeline.
"""

from .base import BaseAgent, AgentOutput
from .past_paper_analyzer import PastPaperAnalyzer
from .topic_researcher import TopicResearcher
from .treaty_researcher import TreatyResearcher
from .chapter_planner import ChapterPlanner
from .chapter_drafter import ChapterDrafter
from .transformation_planner import TransformationPlanner
from .chapter_transformer import ChapterTransformer
from .qa_accuracy import ContentAccuracyVerifier
from .qa_consistency import ConsistencyFlowChecker
from .qa_structural import StructuralRefinement
from .qa_discussion import DiscussionEnhancement

__all__ = [
    "BaseAgent",
    "AgentOutput",
    # Content Creation Pipeline
    "PastPaperAnalyzer",       # Agent 1
    "TopicResearcher",         # Agent 2
    "TreatyResearcher",        # Agent 2b (conditional)
    "ChapterPlanner",          # Agent 3
    "ChapterDrafter",          # Agent 4
    # Transformation Pipeline
    "TransformationPlanner",   # Agent 4.1
    "ChapterTransformer",      # Agent 4.2
    # Quality Assurance
    "ContentAccuracyVerifier", # Agent 5a
    "ConsistencyFlowChecker",  # Agent 5b
    "StructuralRefinement",    # Agent 5c
    "DiscussionEnhancement",   # Agent 5d
]
