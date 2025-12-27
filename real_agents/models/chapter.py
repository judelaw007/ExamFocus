"""
Data models for chapter planning and drafting (Agent 3 & 4 output).
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ContentDepth(str, Enum):
    EXTENSIVE = "extensive"
    MODERATE = "moderate"
    BRIEF = "brief"


class ChapterSection(BaseModel):
    """A section within a chapter."""

    number: str = Field(..., description="Section number (e.g., '1.1')")
    title: str = Field(..., description="Section title")
    content_points: list[str] = Field(default_factory=list, description="Content points to cover")
    discussion_integration: list[str] = Field(
        default_factory=list, description="Where to explain rationale"
    )
    exam_reference: Optional[str] = Field(None, description="Subtle exam reference if applicable")
    depth: ContentDepth = Field(..., description="Content depth level")
    subsections: list["ChapterSection"] = Field(
        default_factory=list, description="Nested subsections"
    )


class PlanningMetadata(BaseModel):
    """Internal planning metadata (not for publication)."""

    exam_frequency: str = Field(..., description="Exam frequency from Agent 1")
    key_examined_areas: list[str] = Field(default_factory=list, description="Frequently examined areas")
    examined_angles: list[str] = Field(default_factory=list, description="How examiners approach this")
    unexamined_areas: list[str] = Field(default_factory=list, description="Rarely examined areas")


class ResearchIntegration(BaseModel):
    """How research should be integrated."""

    source_material: str = Field(..., description="Source material type")
    target_section: str = Field(..., description="Where to use this material")


class CrossReference(BaseModel):
    """Cross-reference to related topic."""

    related_topic: str = Field(..., description="Related topic name")
    connection_point: str = Field(..., description="How it connects")


class ChapterPlan(BaseModel):
    """
    Complete chapter plan.
    Output of Agent 3: Chapter Planner.
    """

    topic: str = Field(..., description="Topic name")
    chapter_number: str = Field(..., description="Chapter number")
    planning_metadata: PlanningMetadata = Field(..., description="Internal planning metadata")
    sections: list[ChapterSection] = Field(default_factory=list, description="Chapter sections")
    research_integration: list[ResearchIntegration] = Field(
        default_factory=list, description="Research integration points"
    )
    subtle_exam_references: list[dict[str, str]] = Field(
        default_factory=list, description="Planned exam references"
    )
    cross_references: list[CrossReference] = Field(
        default_factory=list, description="Cross-references"
    )
    exclusions_confirmed: bool = Field(True, description="CheatBook elements excluded")

    def get_outline(self) -> str:
        """Return a formatted outline of the chapter."""
        lines = [f"## Chapter {self.chapter_number}: {self.topic}\n"]
        for section in self.sections:
            lines.append(f"### {section.number}. {section.title}")
            for subsection in section.subsections:
                lines.append(f"#### {subsection.number}. {subsection.title}")
        return "\n".join(lines)


class ChapterDraft(BaseModel):
    """
    Complete drafted chapter.
    Output of Agent 4: Chapter Drafter.
    """

    topic: str = Field(..., description="Topic name")
    chapter_number: str = Field(..., description="Chapter number")
    content: str = Field(..., description="Full markdown content")
    word_count: int = Field(..., description="Word count")
    sections_count: int = Field(..., description="Number of sections")
    exam_references: list[str] = Field(
        default_factory=list, description="Subtle exam references included"
    )
    cheatbook_elements_excluded: bool = Field(True, description="CheatBook elements excluded")

    def summary(self) -> str:
        """Return a brief summary."""
        return f"""
Chapter {self.chapter_number}: {self.topic}
Word Count: {self.word_count}
Sections: {self.sections_count}
Exam References: {len(self.exam_references)}
"""
