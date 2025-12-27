"""
Data models for exam intelligence (Agent 1 output).
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TrendDirection(str, Enum):
    INCREASING = "increasing"
    STABLE = "stable"
    DECREASING = "decreasing"


class QuestionFormat(str, Enum):
    FULL_QUESTION = "full_question"
    SUB_PART = "sub_part"
    BOTH = "both"


class QuestionPattern(BaseModel):
    """A recurring question pattern identified in past papers."""

    name: str = Field(..., description="Name of the pattern")
    trigger_words: list[str] = Field(default_factory=list, description="Words that trigger this pattern")
    structure: str = Field(..., description="Typical structure of this question type")
    example_reference: str = Field(..., description="Reference to an example (e.g., 'June 2024 Q5')")


class WorkedExample(BaseModel):
    """A candidate worked example from past papers."""

    exam_sitting: str = Field(..., description="Exam sitting (e.g., 'June 2024 Q7')")
    marks: int = Field(..., description="Mark allocation")
    question_text: str = Field(..., description="Verbatim question text")
    aspects_tested: list[str] = Field(default_factory=list, description="Key aspects tested")
    selection_rationale: str = Field(..., description="Why this example was selected")


class FrequencyData(BaseModel):
    """Frequency analysis of topic appearances."""

    appearances: int = Field(..., description="Number of times topic appeared")
    total_papers: int = Field(..., description="Total papers analyzed")
    percentage: float = Field(..., description="Appearance percentage")
    sittings: list[str] = Field(default_factory=list, description="List of exam sittings")
    trend: TrendDirection = Field(..., description="Trend direction")


class MarkAllocation(BaseModel):
    """Mark allocation data."""

    range_min: int = Field(..., description="Minimum marks")
    range_max: int = Field(..., description="Maximum marks")
    average: float = Field(..., description="Average marks")
    format: QuestionFormat = Field(..., description="Question format")


class PartDistribution(BaseModel):
    """Distribution between Part A and Part B questions."""

    part_a: int = Field(0, description="Part A (Theory) count")
    part_b: int = Field(0, description="Part B (Scenario) count")
    combined: int = Field(0, description="Combined count")


class ExaminerExpectations(BaseModel):
    """What examiners expect from candidates."""

    rewards: list[str] = Field(default_factory=list, description="What earns marks")
    frameworks: list[str] = Field(default_factory=list, description="Expected answer frameworks")
    common_errors: list[str] = Field(default_factory=list, description="Common candidate errors")


class ExamIntelligence(BaseModel):
    """
    Complete exam intelligence report for a topic.
    Output of Agent 1: Past Paper Analyzer.
    """

    topic: str = Field(..., description="Topic name")
    frequency: FrequencyData = Field(..., description="Frequency analysis")
    marks: MarkAllocation = Field(..., description="Mark allocation data")
    part_distribution: PartDistribution = Field(..., description="Part A/B distribution")
    patterns: list[QuestionPattern] = Field(default_factory=list, description="Question patterns")
    question_evolution: str = Field("", description="How questions have evolved over time")
    worked_examples: list[WorkedExample] = Field(default_factory=list, description="Candidate worked examples")
    examiner_expectations: ExaminerExpectations = Field(
        default_factory=ExaminerExpectations, description="Examiner expectations"
    )
    pass_rate: Optional[str] = Field(None, description="Pass rate data if available")
    strategic_priority: int = Field(..., ge=1, le=5, description="Priority rating 1-5")
    priority_rationale: str = Field(..., description="Rationale for priority rating")

    def get_priority_stars(self) -> str:
        """Return star rating string."""
        return "★" * self.strategic_priority + "☆" * (5 - self.strategic_priority)

    def summary(self) -> str:
        """Return a brief summary for use by other agents."""
        return f"""
Topic: {self.topic}
Frequency: {self.frequency.appearances}/{self.frequency.total_papers} ({self.frequency.percentage:.1f}%)
Marks: {self.marks.range_min}-{self.marks.range_max} (avg: {self.marks.average})
Priority: {self.get_priority_stars()}
Key Patterns: {', '.join(p.name for p in self.patterns[:3])}
"""
