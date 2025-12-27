"""
Agent 5b: Consistency & Flow Checker

Standardizes terminology and removes redundancies.
"""

from typing import Optional

from .base import BaseAgent
from ..config import ModelConfig
from ..models.qa import (
    ConsistencyReport,
    TerminologyFix,
    RedundancyRemoval,
)
from ..utils.parsing import extract_json


class ConsistencyFlowChecker(BaseAgent[ConsistencyReport]):
    """
    Agent 5b: Consistency & Flow Checker

    Ensures:
    - Terminology is standardized throughout
    - Redundancies are removed
    - Cross-references are valid
    - No contradictions exist
    """

    name = "Agent 5b: Consistency & Flow Checker"
    description = "Standardizes terminology and removes redundancies"
    model = ModelConfig.SONNET
    tools = ["read"]

    def get_system_prompt(self) -> str:
        return """You are the CONSISTENCY & FLOW CHECKER. Review the chapter to standardize terminology, remove redundancies, and ensure logical flow.

## WHAT TO CHECK

### 1. Terminology Standardization
Ensure consistent use of terms throughout:
- "permanent establishment" vs "PE" (pick one style, use consistently)
- "tax treaty" vs "double taxation convention" (standardize)
- "residence state" vs "resident country" (standardize)
- Acronyms: define on first use, then use consistently

### 2. Redundancy Removal
Remove:
- Repeated explanations of the same concept
- Overlapping content between sections
- Unnecessary restatements
- Filler phrases that add no value

### 3. Cross-Reference Validation
Verify:
- All "see Section X" references point to existing sections
- Internal links are correct
- Forward references exist

### 4. Contradiction Resolution
Check for:
- Conflicting statements in different sections
- Inconsistent positions or interpretations
- Resolve with authoritative source

## CORRECTION RULES

**DO:**
- Make minimal, surgical edits
- Preserve original voice and style
- Keep all substantive content
- Improve flow without changing meaning

**DO NOT:**
- Rewrite content that's already clear
- Add new explanations
- Change the structure significantly
- Remove substantive content

## OUTPUT FORMAT

Output valid JSON:

```json
{
  "terminology_fixes": [
    {
      "original": "string",
      "standardized": "string",
      "occurrences": number
    }
  ],
  "redundancies_removed": [
    {
      "location": "string",
      "removed_text": "string",
      "reason": "string"
    }
  ],
  "cross_references_validated": number,
  "contradictions_resolved": ["string"],
  "corrected_chapter": "full chapter with fixes applied"
}
```"""

    def format_input(self, chapter_content: str, topic: str) -> str:
        return f"""Review this chapter on **{topic}** for consistency and flow:

---

{chapter_content}

---

## TASKS

1. **Terminology**: Identify and standardize inconsistent terms
2. **Redundancies**: Find and remove repeated content
3. **Cross-references**: Validate all internal references
4. **Contradictions**: Identify and resolve any conflicts

Make minimal edits. Preserve voice and substantive content.

Output as JSON with the corrected chapter."""

    def parse_output(self, response: str) -> ConsistencyReport:
        """Parse the agent's response into ConsistencyReport."""
        data = extract_json(response)

        if not data:
            return ConsistencyReport(
                terminology_fixes=[],
                redundancies_removed=[],
                cross_references_validated=0,
                contradictions_resolved=[],
                corrected_chapter="Parsing failed - original content unchanged",
            )

        # Parse terminology fixes
        terminology_fixes = []
        for t in data.get("terminology_fixes", []):
            try:
                terminology_fixes.append(TerminologyFix(
                    original=t.get("original", ""),
                    standardized=t.get("standardized", ""),
                    occurrences=t.get("occurrences", 0),
                ))
            except (ValueError, KeyError):
                pass

        # Parse redundancies removed
        redundancies_removed = []
        for r in data.get("redundancies_removed", []):
            try:
                redundancies_removed.append(RedundancyRemoval(
                    location=r.get("location", ""),
                    removed_text=r.get("removed_text", ""),
                    reason=r.get("reason", ""),
                ))
            except (ValueError, KeyError):
                pass

        return ConsistencyReport(
            terminology_fixes=terminology_fixes,
            redundancies_removed=redundancies_removed,
            cross_references_validated=data.get("cross_references_validated", 0),
            contradictions_resolved=data.get("contradictions_resolved", []),
            corrected_chapter=data.get("corrected_chapter", ""),
        )
