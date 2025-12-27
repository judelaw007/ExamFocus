"""
Data models for research (Agent 2 output).
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import date


class SourceReliability(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SourceType(str, Enum):
    OECD = "oecd"
    UN = "un"
    GOVERNMENT = "government"
    BIG4 = "big4"
    LAW_FIRM = "law_firm"
    PROFESSIONAL_BODY = "professional_body"
    ACADEMIC = "academic"
    OTHER = "other"


class SearchResult(BaseModel):
    """Result from a single web search."""

    query: str = Field(..., description="Search query used")
    source_type: SourceType = Field(..., description="Type of source")
    key_findings: str = Field(..., description="Key findings from this search")


class SourceInfo(BaseModel):
    """Information about a source."""

    name: str = Field(..., description="Source name")
    url: str = Field(..., description="Source URL")
    date_accessed: date = Field(..., description="Date accessed")
    reliability: SourceReliability = Field(..., description="Reliability rating")


class CoreConcepts(BaseModel):
    """Core concepts for the topic."""

    principles: str = Field(..., description="Fundamental principles")
    key_provisions: dict[str, str] = Field(
        default_factory=dict, description="Key provisions (article: description)"
    )
    terminology: dict[str, str] = Field(
        default_factory=dict, description="Essential terminology (term: definition)"
    )


class OECDUNComparison(BaseModel):
    """Comparison between OECD and UN Model provisions."""

    aspect: str = Field(..., description="Aspect being compared")
    oecd_position: str = Field(..., description="OECD Model position")
    un_position: str = Field(..., description="UN Model position")


class BEPSMLIInfo(BaseModel):
    """BEPS and MLI related information."""

    relevant_actions: list[str] = Field(default_factory=list, description="Relevant BEPS Actions")
    mli_provisions: list[str] = Field(default_factory=list, description="MLI articles affecting topic")
    implementation_status: str = Field("", description="Current implementation status")


class ResearchReport(BaseModel):
    """
    Complete research report for a topic.
    Output of Agent 2: Topic Researcher.
    """

    topic: str = Field(..., description="Topic name")
    search_log: list[SearchResult] = Field(default_factory=list, description="All searches conducted")
    core_concepts: CoreConcepts = Field(..., description="Core concepts")
    oecd_position: str = Field(..., description="Current OECD position (2-3 paragraphs)")
    un_differences: list[OECDUNComparison] = Field(
        default_factory=list, description="OECD vs UN differences"
    )
    beps_mli: BEPSMLIInfo = Field(default_factory=BEPSMLIInfo, description="BEPS/MLI developments")
    current_developments: list[str] = Field(
        default_factory=list, description="Current developments 2024-2025"
    )
    examiner_insights: str = Field("", description="Insights from examiner reports")
    practical_considerations: list[str] = Field(
        default_factory=list, description="Practical challenges"
    )
    sources: list[SourceInfo] = Field(default_factory=list, description="Sources used")
    research_gaps: list[str] = Field(default_factory=list, description="Areas with no info found")

    def summary(self) -> str:
        """Return a brief summary for use by other agents."""
        return f"""
Topic: {self.topic}
Searches Conducted: {len(self.search_log)}
Key OECD Position: {self.oecd_position[:200]}...
UN Differences: {len(self.un_differences)} aspects compared
Current Developments: {len(self.current_developments)} items
Research Gaps: {', '.join(self.research_gaps) if self.research_gaps else 'None'}
"""
