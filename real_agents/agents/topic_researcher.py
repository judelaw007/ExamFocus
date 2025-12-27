"""
Agent 2: Topic Researcher

Conducts comprehensive web research on the specified topic.
"""

from typing import Optional
from datetime import date

from .base import BaseAgent
from ..config import ModelConfig
from ..models.research import (
    ResearchReport,
    SearchResult,
    SourceInfo,
    CoreConcepts,
    OECDUNComparison,
    BEPSMLIInfo,
    SourceType,
    SourceReliability,
)
from ..utils.parsing import extract_json


class TopicResearcher(BaseAgent[ResearchReport]):
    """
    Agent 2: Topic Researcher

    Conducts web research to gather:
    - Core concepts and definitions
    - OECD position
    - UN Model differences
    - BEPS/MLI developments
    - Current developments
    - Examiner insights
    """

    name = "Agent 2: Topic Researcher"
    description = "Researches authoritative sources for topic information"
    model = ModelConfig.SONNET
    tools = ["web_search", "web_fetch"]

    def get_system_prompt(self) -> str:
        return """You are the TOPIC RESEARCHER. Conduct comprehensive web research on the specified topic, focusing on information relevant to how this topic is examined.

## MANDATORY PROTOCOL

### ENFORCEMENT RULES (NON-NEGOTIABLE)
1. You MUST conduct minimum 5 searches (scale up for complex topics)
2. You MUST prioritize authoritative sources (OECD, UN, government, Big 4)
3. You MUST cite specifically—article numbers, paragraph references, dates
4. You MUST focus on exam-relevant information
5. You MUST note research gaps clearly
6. If information conflicts between sources, document both and flag

## MANDATORY SEARCHES (Minimum 5)

| # | Focus | Query Pattern |
|---|-------|---------------|
| 1 | OECD Current Position | "[topic] OECD Model Tax Convention 2024 2025" |
| 2 | UN Model Differences | "[topic] UN Model Double Taxation differences" |
| 3 | BEPS/MLI Impact | "[topic] BEPS MLI implementation" |
| 4 | Recent Developments | "[topic] international tax developments 2024 2025" |
| 5 | Examiner Reports | "[topic] ADIT examiner report" |

## SOURCE HIERARCHY

| Priority | Source Type |
|----------|-------------|
| 1 | OECD official publications |
| 2 | UN Tax Committee publications |
| 3 | Government tax authorities |
| 4 | Examiner reports (ADIT, CTA, etc.) |
| 5 | Big 4 / major law firms |
| 6 | Professional bodies (CIOT, ADIT, IBFD) |
| 7 | Academic journals |

## OUTPUT FORMAT

You MUST output valid JSON:

```json
{
  "topic": "string",
  "search_log": [
    {
      "query": "string",
      "source_type": "oecd|un|government|big4|law_firm|professional_body|academic|other",
      "key_findings": "string"
    }
  ],
  "core_concepts": {
    "principles": "string (fundamental principles)",
    "key_provisions": {"article_name": "description"},
    "terminology": {"term": "definition"}
  },
  "oecd_position": "string (2-3 paragraphs with specific references)",
  "un_differences": [
    {
      "aspect": "string",
      "oecd_position": "string",
      "un_position": "string"
    }
  ],
  "beps_mli": {
    "relevant_actions": ["string"],
    "mli_provisions": ["string"],
    "implementation_status": "string"
  },
  "current_developments": ["string (with dates and sources)"],
  "examiner_insights": "string",
  "practical_considerations": ["string"],
  "sources": [
    {
      "name": "string",
      "url": "string",
      "date_accessed": "YYYY-MM-DD",
      "reliability": "high|medium|low"
    }
  ],
  "research_gaps": ["string"]
}
```

Use web_search and web_fetch tools to gather authoritative information."""

    def format_input(self, topic: str, exam_intelligence_summary: str = "") -> str:
        context = ""
        if exam_intelligence_summary:
            context = f"""
## Exam Intelligence Context
Use this to focus your research on what's actually tested:

{exam_intelligence_summary}
"""

        return f"""Research the topic: **{topic}**
{context}
Conduct at least 5 searches covering:
1. OECD current position
2. UN Model differences
3. BEPS/MLI impact
4. Recent developments (2024-2025)
5. Examiner reports/insights

Output your research as JSON in the specified format."""

    def parse_output(self, response: str) -> ResearchReport:
        """Parse the agent's response into ResearchReport."""
        data = extract_json(response)

        if not data:
            return ResearchReport(
                topic="Unknown",
                search_log=[],
                core_concepts=CoreConcepts(
                    principles="Research parsing failed",
                    key_provisions={},
                    terminology={},
                ),
                oecd_position="",
                un_differences=[],
                beps_mli=BEPSMLIInfo(),
                current_developments=[],
                examiner_insights="",
                practical_considerations=[],
                sources=[],
                research_gaps=["Research could not be parsed"],
            )

        # Parse search log
        search_log = []
        for s in data.get("search_log", []):
            try:
                search_log.append(SearchResult(
                    query=s.get("query", ""),
                    source_type=SourceType(s.get("source_type", "other")),
                    key_findings=s.get("key_findings", ""),
                ))
            except (ValueError, KeyError):
                pass

        # Parse core concepts
        cc_data = data.get("core_concepts", {})
        core_concepts = CoreConcepts(
            principles=cc_data.get("principles", ""),
            key_provisions=cc_data.get("key_provisions", {}),
            terminology=cc_data.get("terminology", {}),
        )

        # Parse UN differences
        un_differences = []
        for u in data.get("un_differences", []):
            try:
                un_differences.append(OECDUNComparison(
                    aspect=u.get("aspect", ""),
                    oecd_position=u.get("oecd_position", ""),
                    un_position=u.get("un_position", ""),
                ))
            except (ValueError, KeyError):
                pass

        # Parse BEPS/MLI
        beps_data = data.get("beps_mli", {})
        beps_mli = BEPSMLIInfo(
            relevant_actions=beps_data.get("relevant_actions", []),
            mli_provisions=beps_data.get("mli_provisions", []),
            implementation_status=beps_data.get("implementation_status", ""),
        )

        # Parse sources
        sources = []
        for s in data.get("sources", []):
            try:
                sources.append(SourceInfo(
                    name=s.get("name", ""),
                    url=s.get("url", ""),
                    date_accessed=date.fromisoformat(s.get("date_accessed", str(date.today()))),
                    reliability=SourceReliability(s.get("reliability", "medium")),
                ))
            except (ValueError, KeyError):
                pass

        return ResearchReport(
            topic=data.get("topic", "Unknown"),
            search_log=search_log,
            core_concepts=core_concepts,
            oecd_position=data.get("oecd_position", ""),
            un_differences=un_differences,
            beps_mli=beps_mli,
            current_developments=data.get("current_developments", []),
            examiner_insights=data.get("examiner_insights", ""),
            practical_considerations=data.get("practical_considerations", []),
            sources=sources,
            research_gaps=data.get("research_gaps", []),
        )
