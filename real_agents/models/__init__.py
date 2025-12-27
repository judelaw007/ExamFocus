"""
Data models for the ExamFocus multi-agent pipeline.
"""

from .exam_intelligence import ExamIntelligence, QuestionPattern, WorkedExample
from .research import ResearchReport, SearchResult, SourceInfo
from .chapter import ChapterPlan, ChapterDraft, ChapterSection
from .qa import (
    AccuracyReport,
    ConsistencyReport,
    StructuralReport,
    DiscussionReport,
    Correction,
)

__all__ = [
    "ExamIntelligence",
    "QuestionPattern",
    "WorkedExample",
    "ResearchReport",
    "SearchResult",
    "SourceInfo",
    "ChapterPlan",
    "ChapterDraft",
    "ChapterSection",
    "AccuracyReport",
    "ConsistencyReport",
    "StructuralReport",
    "DiscussionReport",
    "Correction",
]
