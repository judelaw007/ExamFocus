"""
Data models for QA agents (Agent 5a-5d output).
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ImpactLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Correction(BaseModel):
    """A single correction made by a QA agent."""

    location: str = Field(..., description="Section/paragraph location")
    original_text: str = Field(..., description="Original text")
    issue: str = Field(..., description="What was wrong")
    corrected_text: str = Field(..., description="Corrected text")
    source_url: Optional[str] = Field(None, description="Source URL for verification")
    impact_level: ImpactLevel = Field(..., description="Impact level of correction")


class ExpertReviewItem(BaseModel):
    """Item flagged for expert review."""

    item: str = Field(..., description="Item description")
    reason: str = Field(..., description="Why it needs review")
    recommendation: str = Field(..., description="Recommended action")


class VerificationCategory(BaseModel):
    """Verification stats for a category."""

    category: str = Field(..., description="Category name")
    items_checked: int = Field(..., description="Items checked")
    corrections_made: int = Field(..., description="Corrections made")

    @property
    def accuracy_rate(self) -> float:
        if self.items_checked == 0:
            return 1.0
        return 1 - (self.corrections_made / self.items_checked)


class AccuracyReport(BaseModel):
    """
    Content accuracy verification report.
    Output of Agent 5a: Content Accuracy Verifier.
    """

    search_log: list[dict[str, str]] = Field(
        default_factory=list, description="Searches conducted"
    )
    corrections: list[Correction] = Field(default_factory=list, description="Corrections made")
    verification_summary: list[VerificationCategory] = Field(
        default_factory=list, description="Verification stats by category"
    )
    expert_review_items: list[ExpertReviewItem] = Field(
        default_factory=list, description="Items for expert review"
    )
    corrected_chapter: str = Field(..., description="Chapter with corrections applied")

    @property
    def total_corrections(self) -> int:
        return len(self.corrections)

    @property
    def overall_accuracy(self) -> float:
        total_checked = sum(v.items_checked for v in self.verification_summary)
        total_corrections = sum(v.corrections_made for v in self.verification_summary)
        if total_checked == 0:
            return 1.0
        return 1 - (total_corrections / total_checked)


class TerminologyFix(BaseModel):
    """A terminology standardization fix."""

    original: str = Field(..., description="Original term")
    standardized: str = Field(..., description="Standardized term")
    occurrences: int = Field(..., description="Number of occurrences fixed")


class RedundancyRemoval(BaseModel):
    """A redundancy that was removed."""

    location: str = Field(..., description="Location in chapter")
    removed_text: str = Field(..., description="Text that was removed")
    reason: str = Field(..., description="Why it was redundant")


class ConsistencyReport(BaseModel):
    """
    Consistency and flow check report.
    Output of Agent 5b: Consistency & Flow Checker.
    """

    terminology_fixes: list[TerminologyFix] = Field(
        default_factory=list, description="Terminology standardizations"
    )
    redundancies_removed: list[RedundancyRemoval] = Field(
        default_factory=list, description="Redundancies removed"
    )
    cross_references_validated: int = Field(0, description="Cross-references validated")
    contradictions_resolved: list[str] = Field(
        default_factory=list, description="Contradictions resolved"
    )
    corrected_chapter: str = Field(..., description="Chapter with fixes applied")

    @property
    def total_fixes(self) -> int:
        return len(self.terminology_fixes) + len(self.redundancies_removed)


class ScaffoldingRemoval(BaseModel):
    """A scaffolding element that was removed."""

    element_type: str = Field(..., description="Type of scaffolding")
    location: str = Field(..., description="Location in chapter")
    removed_text: str = Field(..., description="Text removed")


class StructuralReport(BaseModel):
    """
    Structural refinement report.
    Output of Agent 5c: Structural Refinement.
    """

    scaffolding_removed: list[ScaffoldingRemoval] = Field(
        default_factory=list, description="Scaffolding elements removed"
    )
    substantive_content_preserved: bool = Field(True, description="Core content untouched")
    worked_examples_intact: bool = Field(True, description="Examples preserved")
    answer_frameworks_intact: bool = Field(True, description="Frameworks preserved")
    refined_chapter: str = Field(..., description="Refined chapter content")

    @property
    def total_removals(self) -> int:
        return len(self.scaffolding_removed)


class DiscussionAddition(BaseModel):
    """Discussion prose added to the chapter."""

    location: str = Field(..., description="Where discussion was added")
    content: str = Field(..., description="Discussion content added")
    word_count: int = Field(..., description="Words added")
    purpose: str = Field(..., description="Purpose of this discussion")


class DiscussionReport(BaseModel):
    """
    Discussion enhancement report.
    Output of Agent 5d: Discussion Enhancement.
    """

    additions: list[DiscussionAddition] = Field(
        default_factory=list, description="Discussion additions"
    )
    total_words_added: int = Field(0, description="Total words added")
    discussion_percentage: float = Field(0.0, description="Percentage of chapter that is discussion")
    voice_consistent: bool = Field(True, description="Voice consistency maintained")
    existing_content_preserved: bool = Field(True, description="No existing content changed")
    enhanced_chapter: str = Field(..., description="Enhanced chapter content")
