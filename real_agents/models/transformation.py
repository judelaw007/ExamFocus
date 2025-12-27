"""
Data models for chapter transformation (Agent 4.1 and 4.2 output).
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ContentAction(str, Enum):
    KEEP = "keep"
    REMOVE = "remove"
    MODIFY = "modify"
    CONVERT = "convert"


class SyllabusRequirements(BaseModel):
    """Syllabus requirements for a topic."""

    topic_code: str = Field(..., description="Topic code (e.g., 'I.A')")
    topic_description: str = Field(..., description="Topic description")
    section: str = Field(..., description="Section name")
    level: int = Field(..., ge=1, le=3, description="Depth level 1-3")
    min_words: int = Field(..., description="Minimum word count")
    max_words: int = Field(..., description="Maximum word count")


class ContentToKeep(BaseModel):
    """Content identified to keep from existing chapter."""

    section: str = Field(..., description="Current section reference")
    description: str = Field(..., description="Content description")
    reason: str = Field(..., description="Why to keep")
    modifications: Optional[str] = Field(None, description="Any modifications needed")


class ContentToRemove(BaseModel):
    """CheatBook element identified for removal."""

    element_type: str = Field(..., description="Type of element")
    location: str = Field(..., description="Location in chapter")
    replacement_strategy: str = Field(..., description="How to handle removal")


class StructuralMapping(BaseModel):
    """Mapping from current to new structure."""

    current_heading: str = Field(..., description="Current heading")
    new_heading: str = Field(..., description="New heading with numbering")
    notes: str = Field("", description="Transformation notes")


class OldNotesIntegration(BaseModel):
    """Content from old notes to integrate."""

    content: str = Field(..., description="Content from old notes")
    relevance: str = Field(..., description="High/Medium/Low")
    integration_location: str = Field(..., description="Where and how to use")


class ContentGap(BaseModel):
    """Content gap identified that needs filling."""

    gap: str = Field(..., description="Missing topic")
    syllabus_requirement: str = Field(..., description="What syllabus requires")
    research_needed: bool = Field(False, description="Whether research is needed")
    priority: str = Field(..., description="High/Medium/Low")


class WordCountStrategy(BaseModel):
    """Strategy for meeting word count targets."""

    target_min: int = Field(..., description="Target minimum words")
    target_max: int = Field(..., description="Target maximum words")
    current_count: int = Field(..., description="Current word count")
    difference: int = Field(..., description="Difference from target")
    strategy: str = Field(..., description="How to expand/reduce")
    areas_to_develop: list[str] = Field(default_factory=list, description="Areas to expand")
    areas_to_trim: list[str] = Field(default_factory=list, description="Areas to reduce")


class TransformationPlan(BaseModel):
    """
    Complete transformation plan for a chapter.
    Output of Agent 4.1: Transformation Planner.
    """

    topic_code: str = Field(..., description="Topic code")
    topic_description: str = Field(..., description="Topic description")
    syllabus_requirements: SyllabusRequirements = Field(..., description="Syllabus requirements")

    # Syllabus alignment
    scope_gaps: list[str] = Field(default_factory=list, description="Gaps in scope coverage")
    scope_excess: list[str] = Field(default_factory=list, description="Excess content to remove")

    # Content decisions
    content_to_keep: list[ContentToKeep] = Field(
        default_factory=list, description="Content to retain"
    )
    content_to_remove: list[ContentToRemove] = Field(
        default_factory=list, description="CheatBook elements to remove"
    )

    # Structure
    structural_mapping: list[StructuralMapping] = Field(
        default_factory=list, description="Current to new structure mapping"
    )
    proposed_outline: str = Field("", description="New outline in markdown")

    # Old notes
    old_notes_available: bool = Field(False, description="Whether old notes exist")
    old_notes_integration: list[OldNotesIntegration] = Field(
        default_factory=list, description="Old notes content to integrate"
    )

    # Gaps
    content_gaps: list[ContentGap] = Field(
        default_factory=list, description="Content gaps to fill"
    )

    # Exam references
    subtle_exam_references: list[dict[str, str]] = Field(
        default_factory=list, description="Planned exam references"
    )

    # Word count
    word_count_strategy: WordCountStrategy = Field(..., description="Word count strategy")

    # Checklist
    transformation_checklist: list[str] = Field(
        default_factory=list, description="Items for Agent 4.2 to verify"
    )

    # Special instructions
    special_instructions: str = Field("", description="Topic-specific guidance")


class TransformedChapter(BaseModel):
    """
    Complete transformed chapter.
    Output of Agent 4.2: Chapter Transformer.
    """

    topic_code: str = Field(..., description="Topic code")
    topic_description: str = Field(..., description="Topic description")
    chapter_number: str = Field(..., description="Chapter number")
    content: str = Field(..., description="Full markdown content")
    word_count: int = Field(..., description="Final word count")
    within_target: bool = Field(..., description="Whether word count is within target")

    # Verification
    cheatbook_elements_removed: bool = Field(True, description="All CheatBook elements removed")
    hierarchical_numbering_correct: bool = Field(True, description="Numbering format correct")
    exam_references_count: int = Field(0, description="Number of subtle exam references")
    old_notes_integrated: bool = Field(False, description="Old notes integrated if available")
    content_gaps_filled: bool = Field(False, description="Content gaps addressed")

    def summary(self) -> str:
        """Return a brief summary."""
        return f"""
Topic: {self.topic_code} - {self.topic_description}
Chapter: {self.chapter_number}
Word Count: {self.word_count} (within target: {self.within_target})
Exam References: {self.exam_references_count}
CheatBook Elements Removed: {self.cheatbook_elements_removed}
"""
