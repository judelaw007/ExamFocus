"""
Data models for treaty and case law research (Agent 2b output).
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ActivationCheck(BaseModel):
    """Check whether Agent 2b should be activated."""

    treaty_articles: bool = Field(False, description="Does topic involve specific treaty articles?")
    commentary_provisions: bool = Field(False, description="Are there significant Commentary provisions?")
    major_cases: bool = Field(False, description="Are there major international cases?")
    cfa_reports: bool = Field(False, description="Are there key OECD CFA reports?")

    @property
    def should_proceed(self) -> bool:
        return any([
            self.treaty_articles,
            self.commentary_provisions,
            self.major_cases,
            self.cfa_reports,
        ])


class TreatyProvision(BaseModel):
    """A treaty provision from OECD MTC or UN MTDC."""

    article: str = Field(..., description="Article number (e.g., 'Art 5')")
    model: str = Field(..., description="Model type: 'OECD MTC' or 'UN MTDC'")
    key_provisions: str = Field(..., description="Summary of key provisions")
    exam_relevance: str = Field(..., description="Why it matters for exams")


class CommentaryParagraph(BaseModel):
    """A Commentary paragraph reference."""

    article: str = Field(..., description="Article number")
    paragraph: str = Field(..., description="Paragraph number(s)")
    guidance: str = Field(..., description="Key guidance provided")
    source: str = Field("OECD", description="Source: 'OECD' or 'UN'")


class CFAReport(BaseModel):
    """An OECD Committee on Fiscal Affairs report."""

    name: str = Field(..., description="Report name")
    date: str = Field(..., description="Publication date")
    key_points: str = Field(..., description="Summary of key points")
    exam_relevance: str = Field(..., description="Application to exams")


class InternationalCase(BaseModel):
    """A major international tax case."""

    name: str = Field(..., description="Case name")
    jurisdiction: str = Field(..., description="Country/jurisdiction")
    year: str = Field(..., description="Year of decision")
    key_principle: str = Field(..., description="Key principle established")


class IntegrationNotes(BaseModel):
    """Notes on how this research integrates with Agent 2."""

    confirms: list[str] = Field(default_factory=list, description="What this confirms from Agent 2")
    adds: list[str] = Field(default_factory=list, description="New information not in Agent 2")
    clarifies: list[str] = Field(default_factory=list, description="Areas with additional detail")


class TreatyResearchReport(BaseModel):
    """
    Complete treaty and case law research report.
    Output of Agent 2b: Treaty & Case Law Researcher.
    """

    topic: str = Field(..., description="Topic name")
    activation_check: ActivationCheck = Field(..., description="Activation check results")
    skipped: bool = Field(False, description="Whether research was skipped")
    skip_reason: Optional[str] = Field(None, description="Reason for skipping if skipped")

    oecd_mtc_provisions: list[TreatyProvision] = Field(
        default_factory=list, description="OECD MTC provisions"
    )
    un_mtdc_differences: list[TreatyProvision] = Field(
        default_factory=list, description="UN MTDC differences"
    )
    oecd_commentary: list[CommentaryParagraph] = Field(
        default_factory=list, description="OECD Commentary analysis"
    )
    un_commentary_differences: list[CommentaryParagraph] = Field(
        default_factory=list, description="UN Commentary differences"
    )
    cfa_reports: list[CFAReport] = Field(
        default_factory=list, description="OECD CFA reports"
    )
    major_cases: list[InternationalCase] = Field(
        default_factory=list, description="Major international cases"
    )
    integration_notes: IntegrationNotes = Field(
        default_factory=IntegrationNotes, description="Integration with Agent 2"
    )

    def summary(self) -> str:
        """Return a brief summary."""
        if self.skipped:
            return f"Topic: {self.topic}\nStatus: Skipped - {self.skip_reason}"

        return f"""
Topic: {self.topic}
OECD MTC Provisions: {len(self.oecd_mtc_provisions)}
UN MTDC Differences: {len(self.un_mtdc_differences)}
Commentary Paragraphs: {len(self.oecd_commentary) + len(self.un_commentary_differences)}
CFA Reports: {len(self.cfa_reports)}
Major Cases: {len(self.major_cases)}
"""
