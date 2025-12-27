"""
Agent 5d: Discussion Enhancement

Ensures ~15% of chapter content is integrated prose discussion.
"""

from typing import Optional

from .base import BaseAgent
from ..config import ModelConfig
from ..models.qa import (
    DiscussionReport,
    DiscussionAddition,
)
from ..utils.parsing import extract_json, count_words


class DiscussionEnhancement(BaseAgent[DiscussionReport]):
    """
    Agent 5d: Discussion Enhancement

    Ensures the chapter has sufficient integrated prose discussion
    that explains the "why" behind rules, not just the "what".
    """

    name = "Agent 5d: Discussion Enhancement"
    description = "Adds integrated discussion to explain 'why'"
    model = ModelConfig.OPUS  # Use Opus for quality writing
    tools = ["read"]

    def get_system_prompt(self) -> str:
        return """You are the DISCUSSION ENHANCEMENT agent. Ensure ~15% of the chapter is integrated prose discussion that explains the "why" behind rules.

## WHAT IS DISCUSSION?

Discussion is prose that:
- Explains WHY a rule exists (not just WHAT it is)
- Provides context and background
- Connects concepts to broader principles
- Discusses practical implications
- Offers analysis and insight

## DISCUSSION TARGET

Approximately 15% of chapter word count should be discussion.

Calculate:
- Current word count
- Current discussion percentage (estimate)
- Words of discussion needed

## WHERE TO ADD DISCUSSION

Good places for discussion:
- Before introducing a complex rule (context)
- After stating a provision (implications)
- Between related sections (connections)
- Where concepts might seem arbitrary (rationale)

## DISCUSSION STYLE

**Voice:** Expert teacher explaining to intelligent adults
**Tone:** Authoritative but accessible
**Focus:** Understanding, not memorization

**Example:**
```
This distinction between residence and source taxation reflects a fundamental
tension in international tax policy. Residence countries argue they have the
right to tax their residents' worldwide income because residency implies
access to public services and infrastructure. Source countries counter that
economic activity within their borders justifies taxation regardless of the
taxpayer's residence. The compromise embedded in most tax treaties—shared
taxing rights with relief mechanisms—attempts to balance these competing claims.
```

## RULES

**DO:**
- Add discussion that provides genuine insight
- Weave discussion naturally into existing content
- Maintain consistent voice
- Focus on the "why"

**DO NOT:**
- Change existing content
- Add padding or filler
- Duplicate information
- Add exam-focused content

## OUTPUT FORMAT

Output valid JSON:

```json
{
  "additions": [
    {
      "location": "after section 1.2",
      "content": "discussion text added",
      "word_count": number,
      "purpose": "explains why X exists"
    }
  ],
  "total_words_added": number,
  "discussion_percentage": number,
  "voice_consistent": true,
  "existing_content_preserved": true,
  "enhanced_chapter": "full chapter with discussion added"
}
```"""

    def format_input(self, chapter_content: str, topic: str) -> str:
        word_count = count_words(chapter_content)
        target_discussion = int(word_count * 0.15)

        return f"""Enhance this chapter on **{topic}** with integrated discussion:

---

{chapter_content}

---

## ANALYSIS

- Current word count: ~{word_count}
- Target discussion: ~{target_discussion} words (15%)

## TASKS

1. Identify where discussion would add value
2. Write discussion that explains "why" behind rules
3. Weave discussion naturally into the chapter
4. Maintain consistent expert teacher voice
5. Preserve all existing content

Add discussion that provides genuine insight and understanding.

Output as JSON with the enhanced chapter."""

    def parse_output(self, response: str) -> DiscussionReport:
        """Parse the agent's response into DiscussionReport."""
        data = extract_json(response)

        if not data:
            return DiscussionReport(
                additions=[],
                total_words_added=0,
                discussion_percentage=0.0,
                voice_consistent=True,
                existing_content_preserved=True,
                enhanced_chapter="Parsing failed - original content unchanged",
            )

        # Parse additions
        additions = []
        for a in data.get("additions", []):
            try:
                additions.append(DiscussionAddition(
                    location=a.get("location", ""),
                    content=a.get("content", ""),
                    word_count=a.get("word_count", 0),
                    purpose=a.get("purpose", ""),
                ))
            except (ValueError, KeyError):
                pass

        return DiscussionReport(
            additions=additions,
            total_words_added=data.get("total_words_added", 0),
            discussion_percentage=data.get("discussion_percentage", 0.0),
            voice_consistent=data.get("voice_consistent", True),
            existing_content_preserved=data.get("existing_content_preserved", True),
            enhanced_chapter=data.get("enhanced_chapter", ""),
        )
