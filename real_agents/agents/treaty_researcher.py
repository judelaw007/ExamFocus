"""
Agent 2b: Treaty & Case Law Researcher

Supplements Agent 2 with comprehensive treaty and case law research.
This is a CONDITIONAL agent - only activates when relevant.
"""

from typing import Optional

from .base import BaseAgent
from ..config import ModelConfig
from ..models.treaty_research import (
    TreatyResearchReport,
    ActivationCheck,
    TreatyProvision,
    CommentaryParagraph,
    CFAReport,
    InternationalCase,
    IntegrationNotes,
)
from ..models.research import ResearchReport
from ..utils.parsing import extract_json


class TreatyResearcher(BaseAgent[TreatyResearchReport]):
    """
    Agent 2b: Treaty & Case Law Researcher

    Supplements Agent 2 by ensuring comprehensive coverage of:
    - OECD MTC/UN MTDC provisions
    - Commentaries
    - OECD CFA reports
    - Major international cases

    This is a CONDITIONAL agent - only runs when the topic involves
    specific treaty articles, commentary, cases, or CFA reports.
    """

    name = "Agent 2b: Treaty & Case Law Researcher"
    description = "Researches treaty provisions, commentary, and case law"
    model = ModelConfig.SONNET
    tools = ["web_search", "web_fetch"]

    def get_system_prompt(self) -> str:
        return """You are the TREATY & CASE LAW RESEARCHER. You supplement the Topic Researcher (Agent 2) by ensuring comprehensive coverage of OECD MTC/UN MTDC provisions, Commentaries, OECD CFA reports, and major international cases.

## ACTIVATION CHECK

Before proceeding, you MUST determine if this research is relevant:
- Does this topic involve specific treaty articles? [Y/N]
- Are there significant Commentary provisions? [Y/N]
- Are there major international cases on this topic? [Y/N]
- Are there key OECD CFA reports? [Y/N]

If ALL answers are N → Output a skip response.
If ANY answer is Y → PROCEED with full research.

## WHEN TO SKIP

Skip this research if:
- Topic is purely domestic law
- Topic is historical/institutional (e.g., League of Nations history)
- Topic is conceptual without treaty provisions (e.g., tax policy theory)
- Agent 2 research already covers treaty provisions adequately

## MANDATORY RESEARCH AREAS (If Proceeding)

### 1. OECD Model Tax Convention Provisions
- Relevant article text (current version)
- Key paragraphs within the article
- Cross-references to other articles

### 2. UN Model Double Taxation Convention Provisions
- How UN MTDC differs from OECD MTC
- UN-specific provisions (Art 12A, Art 12B, Art 5A)
- Developing country perspectives

### 3. OECD Commentary Analysis
- Key Commentary paragraphs for relevant articles
- Significant interpretive guidance
- Reservations and observations

### 4. UN Commentary Differences
- Where UN Commentary differs from OECD
- Additional developing country guidance

### 5. OECD CFA Reports
- Relevant BEPS Action reports
- Transfer pricing guidelines (if applicable)
- Pillar One/Two documents (if applicable)

### 6. Major International Cases
- Leading cases by jurisdiction
- Key principles established
- Recent significant decisions

## OUTPUT FORMAT

Output valid JSON:

```json
{
  "topic": "string",
  "activation_check": {
    "treaty_articles": boolean,
    "commentary_provisions": boolean,
    "major_cases": boolean,
    "cfa_reports": boolean
  },
  "skipped": boolean,
  "skip_reason": "string or null",
  "oecd_mtc_provisions": [
    {
      "article": "Art X",
      "model": "OECD MTC",
      "key_provisions": "string",
      "exam_relevance": "string"
    }
  ],
  "un_mtdc_differences": [
    {
      "article": "Art X",
      "model": "UN MTDC",
      "key_provisions": "string",
      "exam_relevance": "string"
    }
  ],
  "oecd_commentary": [
    {
      "article": "Art X",
      "paragraph": "Para Y",
      "guidance": "string",
      "source": "OECD"
    }
  ],
  "un_commentary_differences": [...],
  "cfa_reports": [
    {
      "name": "string",
      "date": "string",
      "key_points": "string",
      "exam_relevance": "string"
    }
  ],
  "major_cases": [
    {
      "name": "string",
      "jurisdiction": "string",
      "year": "string",
      "key_principle": "string"
    }
  ],
  "integration_notes": {
    "confirms": ["what this confirms from Agent 2"],
    "adds": ["new information"],
    "clarifies": ["additional detail"]
  }
}
```"""

    def format_input(
        self,
        topic: str,
        agent2_research: Optional[ResearchReport] = None,
    ) -> str:
        context = ""
        if agent2_research:
            context = f"""
## AGENT 2 RESEARCH SUMMARY

{agent2_research.summary()}

Key provisions already covered:
{agent2_research.oecd_position[:500] if agent2_research.oecd_position else 'None'}
"""

        return f"""Research treaty and case law for topic: **{topic}**
{context}
## ACTIVATION CHECK

First, determine if this research is needed by answering:
1. Does this topic involve specific OECD/UN treaty articles?
2. Are there significant Commentary provisions?
3. Are there major international cases?
4. Are there key OECD CFA reports?

If ALL answers are NO, skip and explain why.
If ANY answer is YES, proceed with full research.

## IF PROCEEDING

Use web_search and web_fetch to gather:
1. OECD MTC article text and provisions
2. UN MTDC differences
3. Commentary paragraphs (cite specific numbers)
4. CFA reports (cite dates)
5. Major cases (cite jurisdiction and year)

Output as JSON in the specified format."""

    def parse_output(self, response: str) -> TreatyResearchReport:
        """Parse the agent's response into TreatyResearchReport."""
        data = extract_json(response)

        if not data:
            return TreatyResearchReport(
                topic="Unknown",
                activation_check=ActivationCheck(),
                skipped=True,
                skip_reason="Could not parse response",
            )

        # Check if skipped
        if data.get("skipped", False):
            return TreatyResearchReport(
                topic=data.get("topic", "Unknown"),
                activation_check=ActivationCheck(**data.get("activation_check", {})),
                skipped=True,
                skip_reason=data.get("skip_reason", "Not relevant for this topic"),
            )

        # Parse activation check
        ac_data = data.get("activation_check", {})
        activation_check = ActivationCheck(
            treaty_articles=ac_data.get("treaty_articles", False),
            commentary_provisions=ac_data.get("commentary_provisions", False),
            major_cases=ac_data.get("major_cases", False),
            cfa_reports=ac_data.get("cfa_reports", False),
        )

        # Parse OECD MTC provisions
        oecd_provisions = []
        for p in data.get("oecd_mtc_provisions", []):
            try:
                oecd_provisions.append(TreatyProvision(
                    article=p.get("article", ""),
                    model=p.get("model", "OECD MTC"),
                    key_provisions=p.get("key_provisions", ""),
                    exam_relevance=p.get("exam_relevance", ""),
                ))
            except (ValueError, KeyError):
                pass

        # Parse UN MTDC differences
        un_differences = []
        for p in data.get("un_mtdc_differences", []):
            try:
                un_differences.append(TreatyProvision(
                    article=p.get("article", ""),
                    model=p.get("model", "UN MTDC"),
                    key_provisions=p.get("key_provisions", ""),
                    exam_relevance=p.get("exam_relevance", ""),
                ))
            except (ValueError, KeyError):
                pass

        # Parse OECD commentary
        oecd_commentary = []
        for c in data.get("oecd_commentary", []):
            try:
                oecd_commentary.append(CommentaryParagraph(
                    article=c.get("article", ""),
                    paragraph=c.get("paragraph", ""),
                    guidance=c.get("guidance", ""),
                    source=c.get("source", "OECD"),
                ))
            except (ValueError, KeyError):
                pass

        # Parse UN commentary differences
        un_commentary = []
        for c in data.get("un_commentary_differences", []):
            try:
                un_commentary.append(CommentaryParagraph(
                    article=c.get("article", ""),
                    paragraph=c.get("paragraph", ""),
                    guidance=c.get("guidance", ""),
                    source=c.get("source", "UN"),
                ))
            except (ValueError, KeyError):
                pass

        # Parse CFA reports
        cfa_reports = []
        for r in data.get("cfa_reports", []):
            try:
                cfa_reports.append(CFAReport(
                    name=r.get("name", ""),
                    date=r.get("date", ""),
                    key_points=r.get("key_points", ""),
                    exam_relevance=r.get("exam_relevance", ""),
                ))
            except (ValueError, KeyError):
                pass

        # Parse major cases
        major_cases = []
        for c in data.get("major_cases", []):
            try:
                major_cases.append(InternationalCase(
                    name=c.get("name", ""),
                    jurisdiction=c.get("jurisdiction", ""),
                    year=c.get("year", ""),
                    key_principle=c.get("key_principle", ""),
                ))
            except (ValueError, KeyError):
                pass

        # Parse integration notes
        int_data = data.get("integration_notes", {})
        integration_notes = IntegrationNotes(
            confirms=int_data.get("confirms", []),
            adds=int_data.get("adds", []),
            clarifies=int_data.get("clarifies", []),
        )

        return TreatyResearchReport(
            topic=data.get("topic", "Unknown"),
            activation_check=activation_check,
            skipped=False,
            oecd_mtc_provisions=oecd_provisions,
            un_mtdc_differences=un_differences,
            oecd_commentary=oecd_commentary,
            un_commentary_differences=un_commentary,
            cfa_reports=cfa_reports,
            major_cases=major_cases,
            integration_notes=integration_notes,
        )
