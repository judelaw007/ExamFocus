"""
Agent 4.1: Transformation Planner

Analyzes existing chapters and creates transformation plans.
"""

from typing import Optional
from pathlib import Path

from .base import BaseAgent
from ..config import config, ModelConfig
from ..models.transformation import (
    TransformationPlan,
    SyllabusRequirements,
    ContentToKeep,
    ContentToRemove,
    StructuralMapping,
    OldNotesIntegration,
    ContentGap,
    WordCountStrategy,
)
from ..utils.parsing import extract_json, count_words


class TransformationPlanner(BaseAgent[TransformationPlan]):
    """
    Agent 4.1: Transformation Planner

    Analyzes existing CheatBook-style chapters and creates
    detailed plans for transforming them to Exam Focus eBook style.

    This agent does NOT write the chapter - it creates a plan
    for Agent 4.2 to execute.
    """

    name = "Agent 4.1: Transformation Planner"
    description = "Plans chapter transformation from CheatBook to Exam Focus style"
    model = ModelConfig.OPUS  # Strategic planning needs Opus
    tools = ["read"]

    def get_system_prompt(self) -> str:
        return """You are the CHAPTER TRANSFORMATION PLANNER. Your job is to analyze an existing chapter and create a detailed plan for transforming it from CheatBook style to Exam Focus eBook style.

## CRITICAL UNDERSTANDING

### CheatBook Style (CURRENT - to be transformed FROM)
- Exam Intelligence boxes with statistics
- Mark schemes and time allocations
- Worked exam examples with model answers
- Pattern recognition sections
- Error prevention sections
- Answer frameworks

### Exam Focus eBook Style (TARGET - to transform TO)
- Textbook-style prose
- Hierarchical numbering (1., 1.1., 1.1.1.)
- No visible exam statistics
- Subtle exam references only: (covered in June 2024)
- No conclusions, key takeaways, bibliography
- Content informed by exam analysis but not displaying it

## YOUR TASK

Analyze all inputs and produce a TRANSFORMATION PLAN with:
1. Syllabus alignment check
2. Content to keep (valuable, accurate content)
3. Content to remove (all CheatBook elements)
4. Structural mapping (current → new numbering)
5. Old notes integration (if available)
6. Content gaps to fill
7. Subtle exam references to add
8. Word count strategy
9. Transformation checklist for Agent 4.2
10. Special instructions

## OUTPUT FORMAT

Output valid JSON:

```json
{
  "topic_code": "string",
  "topic_description": "string",
  "syllabus_requirements": {
    "topic_code": "string",
    "topic_description": "string",
    "section": "string",
    "level": number (1-3),
    "min_words": number,
    "max_words": number
  },
  "scope_gaps": ["areas chapter doesn't cover but should"],
  "scope_excess": ["areas chapter covers but shouldn't"],
  "content_to_keep": [
    {
      "section": "current section ref",
      "description": "what to keep",
      "reason": "why keep it",
      "modifications": "any changes needed or null"
    }
  ],
  "content_to_remove": [
    {
      "element_type": "Exam Intelligence box|mark scheme|etc",
      "location": "where in chapter",
      "replacement_strategy": "remove entirely|convert to prose|etc"
    }
  ],
  "structural_mapping": [
    {
      "current_heading": "current heading",
      "new_heading": "### 1. New Heading",
      "notes": "transformation notes"
    }
  ],
  "proposed_outline": "markdown outline of new structure",
  "old_notes_available": boolean,
  "old_notes_integration": [
    {
      "content": "content description",
      "relevance": "High|Medium|Low",
      "integration_location": "where to use"
    }
  ],
  "content_gaps": [
    {
      "gap": "missing topic",
      "syllabus_requirement": "what syllabus requires",
      "research_needed": boolean,
      "priority": "High|Medium|Low"
    }
  ],
  "subtle_exam_references": [
    {"section": "1.1.2", "reference": "(covered in June 2024)"}
  ],
  "word_count_strategy": {
    "target_min": number,
    "target_max": number,
    "current_count": number,
    "difference": number,
    "strategy": "how to expand/reduce",
    "areas_to_develop": ["list"],
    "areas_to_trim": ["list"]
  },
  "transformation_checklist": [
    "All Exam Intelligence boxes removed",
    "All mark schemes removed",
    "etc..."
  ],
  "special_instructions": "topic-specific guidance"
}
```"""

    def format_input(
        self,
        topic_code: str,
        topic_description: str,
        existing_chapter: str,
        syllabus_section: str = "",
        syllabus_level: int = 2,
        min_words: int = 1500,
        max_words: int = 3000,
        old_notes: Optional[str] = None,
    ) -> str:
        current_word_count = count_words(existing_chapter)

        old_notes_section = ""
        if old_notes:
            old_notes_section = f"""
## OLD NOTES (Available for integration)

{old_notes[:3000]}...

[Old notes truncated for context - full content available]
"""

        return f"""Create a transformation plan for this chapter:

## TOPIC INFORMATION
- **Topic Code:** {topic_code}
- **Topic Description:** {topic_description}
- **Section:** {syllabus_section}
- **Level:** {syllabus_level}
- **Word Count Target:** {min_words} - {max_words}

## EXISTING CHAPTER (CheatBook style)

Current word count: ~{current_word_count}

{existing_chapter}

{old_notes_section}

---

## YOUR TASK

1. **Analyze syllabus alignment** - Does chapter cover what it should?
2. **Identify content to KEEP** - Accurate, valuable explanations
3. **Identify content to REMOVE** - All CheatBook elements
4. **Map structure** - Current headings → new hierarchical numbering
5. **Plan old notes integration** - If available, what to incorporate
6. **Identify content gaps** - What's missing that syllabus requires
7. **Plan exam references** - Where to add (covered in [Month Year])
8. **Word count strategy** - How to reach target range
9. **Checklist for Agent 4.2** - What to verify

Output as JSON in the specified format."""

    def parse_output(self, response: str) -> TransformationPlan:
        """Parse the agent's response into TransformationPlan."""
        data = extract_json(response)

        if not data:
            return TransformationPlan(
                topic_code="Unknown",
                topic_description="Unknown",
                syllabus_requirements=SyllabusRequirements(
                    topic_code="Unknown",
                    topic_description="Unknown",
                    section="Unknown",
                    level=2,
                    min_words=1500,
                    max_words=3000,
                ),
                word_count_strategy=WordCountStrategy(
                    target_min=1500,
                    target_max=3000,
                    current_count=0,
                    difference=0,
                    strategy="Could not parse plan",
                ),
            )

        # Parse syllabus requirements
        sr_data = data.get("syllabus_requirements", {})
        syllabus_requirements = SyllabusRequirements(
            topic_code=sr_data.get("topic_code", data.get("topic_code", "")),
            topic_description=sr_data.get("topic_description", data.get("topic_description", "")),
            section=sr_data.get("section", ""),
            level=sr_data.get("level", 2),
            min_words=sr_data.get("min_words", 1500),
            max_words=sr_data.get("max_words", 3000),
        )

        # Parse content to keep
        content_to_keep = []
        for c in data.get("content_to_keep", []):
            try:
                content_to_keep.append(ContentToKeep(
                    section=c.get("section", ""),
                    description=c.get("description", ""),
                    reason=c.get("reason", ""),
                    modifications=c.get("modifications"),
                ))
            except (ValueError, KeyError):
                pass

        # Parse content to remove
        content_to_remove = []
        for c in data.get("content_to_remove", []):
            try:
                content_to_remove.append(ContentToRemove(
                    element_type=c.get("element_type", ""),
                    location=c.get("location", ""),
                    replacement_strategy=c.get("replacement_strategy", "Remove entirely"),
                ))
            except (ValueError, KeyError):
                pass

        # Parse structural mapping
        structural_mapping = []
        for s in data.get("structural_mapping", []):
            try:
                structural_mapping.append(StructuralMapping(
                    current_heading=s.get("current_heading", ""),
                    new_heading=s.get("new_heading", ""),
                    notes=s.get("notes", ""),
                ))
            except (ValueError, KeyError):
                pass

        # Parse old notes integration
        old_notes_integration = []
        for o in data.get("old_notes_integration", []):
            try:
                old_notes_integration.append(OldNotesIntegration(
                    content=o.get("content", ""),
                    relevance=o.get("relevance", "Medium"),
                    integration_location=o.get("integration_location", ""),
                ))
            except (ValueError, KeyError):
                pass

        # Parse content gaps
        content_gaps = []
        for g in data.get("content_gaps", []):
            try:
                content_gaps.append(ContentGap(
                    gap=g.get("gap", ""),
                    syllabus_requirement=g.get("syllabus_requirement", ""),
                    research_needed=g.get("research_needed", False),
                    priority=g.get("priority", "Medium"),
                ))
            except (ValueError, KeyError):
                pass

        # Parse word count strategy
        wc_data = data.get("word_count_strategy", {})
        word_count_strategy = WordCountStrategy(
            target_min=wc_data.get("target_min", 1500),
            target_max=wc_data.get("target_max", 3000),
            current_count=wc_data.get("current_count", 0),
            difference=wc_data.get("difference", 0),
            strategy=wc_data.get("strategy", ""),
            areas_to_develop=wc_data.get("areas_to_develop", []),
            areas_to_trim=wc_data.get("areas_to_trim", []),
        )

        return TransformationPlan(
            topic_code=data.get("topic_code", ""),
            topic_description=data.get("topic_description", ""),
            syllabus_requirements=syllabus_requirements,
            scope_gaps=data.get("scope_gaps", []),
            scope_excess=data.get("scope_excess", []),
            content_to_keep=content_to_keep,
            content_to_remove=content_to_remove,
            structural_mapping=structural_mapping,
            proposed_outline=data.get("proposed_outline", ""),
            old_notes_available=data.get("old_notes_available", False),
            old_notes_integration=old_notes_integration,
            content_gaps=content_gaps,
            subtle_exam_references=data.get("subtle_exam_references", []),
            word_count_strategy=word_count_strategy,
            transformation_checklist=data.get("transformation_checklist", []),
            special_instructions=data.get("special_instructions", ""),
        )
