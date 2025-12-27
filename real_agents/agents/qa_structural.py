"""
Agent 5c: Structural Refinement

Removes educational scaffolding while preserving substantive content.
"""

from typing import Optional

from .base import BaseAgent
from ..config import ModelConfig
from ..models.qa import (
    StructuralReport,
    ScaffoldingRemoval,
)
from ..utils.parsing import extract_json


class StructuralRefinement(BaseAgent[StructuralReport]):
    """
    Agent 5c: Structural Refinement

    Removes educational scaffolding elements that don't add
    knowledge value while preserving all substantive content.
    """

    name = "Agent 5c: Structural Refinement"
    description = "Removes scaffolding, preserves substance"
    model = ModelConfig.HAIKU  # Fast model for simple pattern-based work
    tools = ["read"]

    def get_system_prompt(self) -> str:
        return """You are the STRUCTURAL REFINEMENT agent. Remove educational scaffolding while preserving all substantive content.

## WHAT TO REMOVE (Scaffolding)

These add no knowledge value:
- Learning objectives ("In this chapter, you will learn...")
- Time indicators ("Allow 30 minutes for this section")
- Progress markers ("Now that we've covered X, let's move to Y")
- Section summaries ("In summary, we have seen that...")
- Meta-commentary ("This is important because...")
- Reader addresses ("You should note that...")
- Study tips ("For exam success, remember...")

## WHAT TO PRESERVE (Substantive)

NEVER remove:
- Actual content and explanations
- Examples and illustrations
- Technical definitions
- Legal provisions and citations
- Worked examples
- Discussion that explains "why"
- Answer frameworks
- All exam-related methodology content

## DELETION RULES

**DO:**
- Remove only true scaffolding
- Make clean deletions
- Preserve paragraph flow after deletions
- Keep all substantive content

**DO NOT:**
- Remove any content that teaches something
- Remove examples or illustrations
- Remove methodology components
- Change meaning or emphasis

## OUTPUT FORMAT

Output valid JSON:

```json
{
  "scaffolding_removed": [
    {
      "element_type": "learning_objective|time_indicator|progress_marker|summary|meta_commentary|reader_address|study_tip",
      "location": "string",
      "removed_text": "string"
    }
  ],
  "substantive_content_preserved": true,
  "worked_examples_intact": true,
  "answer_frameworks_intact": true,
  "refined_chapter": "full chapter with scaffolding removed"
}
```"""

    def format_input(self, chapter_content: str, topic: str) -> str:
        return f"""Refine this chapter on **{topic}** by removing scaffolding:

---

{chapter_content}

---

## TASKS

Remove ONLY scaffolding elements:
- Learning objectives
- Time indicators
- Progress markers
- Section summaries
- Meta-commentary
- Reader addresses
- Study tips

PRESERVE all substantive content, examples, and methodology.

Output as JSON with the refined chapter."""

    def parse_output(self, response: str) -> StructuralReport:
        """Parse the agent's response into StructuralReport."""
        data = extract_json(response)

        if not data:
            return StructuralReport(
                scaffolding_removed=[],
                substantive_content_preserved=True,
                worked_examples_intact=True,
                answer_frameworks_intact=True,
                refined_chapter="Parsing failed - original content unchanged",
            )

        # Parse scaffolding removed
        scaffolding_removed = []
        for s in data.get("scaffolding_removed", []):
            try:
                scaffolding_removed.append(ScaffoldingRemoval(
                    element_type=s.get("element_type", ""),
                    location=s.get("location", ""),
                    removed_text=s.get("removed_text", ""),
                ))
            except (ValueError, KeyError):
                pass

        return StructuralReport(
            scaffolding_removed=scaffolding_removed,
            substantive_content_preserved=data.get("substantive_content_preserved", True),
            worked_examples_intact=data.get("worked_examples_intact", True),
            answer_frameworks_intact=data.get("answer_frameworks_intact", True),
            refined_chapter=data.get("refined_chapter", ""),
        )
