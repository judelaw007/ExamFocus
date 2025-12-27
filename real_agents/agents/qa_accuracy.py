"""
Agent 5a: Content Accuracy Verifier

Verifies all factual claims against current authoritative sources.
"""

from typing import Optional

from .base import BaseAgent
from ..config import ModelConfig
from ..models.qa import (
    AccuracyReport,
    Correction,
    VerificationCategory,
    ExpertReviewItem,
    ImpactLevel,
)
from ..utils.parsing import extract_json


class ContentAccuracyVerifier(BaseAgent[AccuracyReport]):
    """
    Agent 5a: Content Accuracy Verifier

    Verifies every factual claim in the chapter against current
    authoritative sources using web search.
    """

    name = "Agent 5a: Content Accuracy Verifier"
    description = "Verifies factual accuracy against authoritative sources"
    model = ModelConfig.SONNET
    tools = ["web_search", "web_fetch"]

    def get_system_prompt(self) -> str:
        return """You are the CONTENT ACCURACY VERIFIER. Verify every factual claim in the chapter against current authoritative sources using web search. Fix ONLY inaccuracies—preserve everything else exactly.

## MANDATORY VERIFICATION PROTOCOL

### ENFORCEMENT RULES (NON-NEGOTIABLE)
1. You MUST search every verifiable factual claim—do not rely on training data
2. You MUST NOT skip any category in the verification checklist
3. If you cannot verify a claim, flag it for expert review—do not guess
4. If sources conflict, document both and recommend expert review

### What to Verify (All via Web Search)

| Category | Priority |
|----------|----------|
| Dates, deadlines, implementation timelines | Critical |
| Statistics, thresholds, percentages, rates | Critical |
| Article/paragraph citations, treaty provisions | Critical |
| OECD/UN/BEPS/MLI positions and current status | High |
| Legal and technical definitions | High |
| Case law (names, outcomes, citations) | Medium |

### Source Hierarchy
1. Official bodies: OECD, UN, government tax authorities
2. Professional: Big 4, major law firms, CIOT, ADIT, IBFD
3. Academic: tax journals, research institutions

## CORRECTION RULES

**DO:**
- Fix ONLY factually incorrect or outdated text
- Make surgical edits—change minimum words necessary
- Preserve original voice, style, structure completely
- Cite source URL for every correction

**DO NOT:**
- Rewrite accurate content
- Improve writing style
- Add new content
- Change structure
- Expand explanations

## OUTPUT FORMAT

Output valid JSON:

```json
{
  "search_log": [
    {
      "query": "string",
      "sources": ["string"],
      "verification": "string"
    }
  ],
  "corrections": [
    {
      "location": "section/paragraph",
      "original_text": "exact original text",
      "issue": "what was wrong",
      "corrected_text": "minimal fix",
      "source_url": "URL",
      "impact_level": "critical|high|medium|low"
    }
  ],
  "verification_summary": [
    {
      "category": "string",
      "items_checked": number,
      "corrections_made": number
    }
  ],
  "expert_review_items": [
    {
      "item": "string",
      "reason": "string",
      "recommendation": "string"
    }
  ],
  "corrected_chapter": "full chapter with corrections applied"
}
```"""

    def format_input(self, chapter_content: str, topic: str) -> str:
        return f"""Verify the accuracy of this chapter on **{topic}**:

---

{chapter_content}

---

## VERIFICATION TASKS

1. Search and verify ALL:
   - Dates and timelines
   - Statistics and thresholds
   - Article citations (OECD MTC, UN MDTC, etc.)
   - BEPS/MLI provisions
   - Definitions and positions

2. For each inaccuracy found:
   - Make minimal surgical corrections
   - Cite the authoritative source
   - Preserve original voice

3. Flag anything unverifiable for expert review

Output as JSON with the corrected chapter."""

    def parse_output(self, response: str) -> AccuracyReport:
        """Parse the agent's response into AccuracyReport."""
        data = extract_json(response)

        if not data:
            return AccuracyReport(
                search_log=[],
                corrections=[],
                verification_summary=[],
                expert_review_items=[],
                corrected_chapter="Parsing failed - original content unchanged",
            )

        # Parse corrections
        corrections = []
        for c in data.get("corrections", []):
            try:
                corrections.append(Correction(
                    location=c.get("location", ""),
                    original_text=c.get("original_text", ""),
                    issue=c.get("issue", ""),
                    corrected_text=c.get("corrected_text", ""),
                    source_url=c.get("source_url"),
                    impact_level=ImpactLevel(c.get("impact_level", "medium")),
                ))
            except (ValueError, KeyError):
                pass

        # Parse verification summary
        verification_summary = []
        for v in data.get("verification_summary", []):
            try:
                verification_summary.append(VerificationCategory(
                    category=v.get("category", ""),
                    items_checked=v.get("items_checked", 0),
                    corrections_made=v.get("corrections_made", 0),
                ))
            except (ValueError, KeyError):
                pass

        # Parse expert review items
        expert_review_items = []
        for e in data.get("expert_review_items", []):
            try:
                expert_review_items.append(ExpertReviewItem(
                    item=e.get("item", ""),
                    reason=e.get("reason", ""),
                    recommendation=e.get("recommendation", ""),
                ))
            except (ValueError, KeyError):
                pass

        return AccuracyReport(
            search_log=data.get("search_log", []),
            corrections=corrections,
            verification_summary=verification_summary,
            expert_review_items=expert_review_items,
            corrected_chapter=data.get("corrected_chapter", ""),
        )
