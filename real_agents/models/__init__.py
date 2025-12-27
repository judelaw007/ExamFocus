"""
Data models for the ExamFocus multi-agent pipeline.
"""

from .exam_intelligence import ExamIntelligence, QuestionPattern, WorkedExample
from .research import ResearchReport, SearchResult, SourceInfo
from .treaty_research import TreatyResearchReport, ActivationCheck, TreatyProvision
from .chapter import ChapterPlan, ChapterDraft, ChapterSection
from .transformation import TransformationPlan, TransformedChapter, SyllabusRequirements
from .qa import (
    AccuracyReport,
    ConsistencyReport,
    StructuralReport,
    DiscussionReport,
    Correction,
)

__all__ = [
    # Exam Intelligence (Agent 1)
    "ExamIntelligence",
    "QuestionPattern",
    "WorkedExample",
    # Research (Agent 2)
    "ResearchReport",
    "SearchResult",
    "SourceInfo",
    # Treaty Research (Agent 2b)
    "TreatyResearchReport",
    "ActivationCheck",
    "TreatyProvision",
    # Chapter Planning & Drafting (Agents 3 & 4)
    "ChapterPlan",
    "ChapterDraft",
    "ChapterSection",
    # Transformation (Agents 4.1 & 4.2)
    "TransformationPlan",
    "TransformedChapter",
    "SyllabusRequirements",
    # Quality Assurance (Agents 5a-5d)
    "AccuracyReport",
    "ConsistencyReport",
    "StructuralReport",
    "DiscussionReport",
    "Correction",
]
