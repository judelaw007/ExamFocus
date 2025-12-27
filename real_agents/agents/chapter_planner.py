"""
Agent 3: Chapter Planner

Creates detailed chapter plans following Exam Focus methodology.
"""

from typing import Optional

from .base import BaseAgent
from ..config import config, ModelConfig
from ..models.chapter import (
    ChapterPlan,
    ChapterSection,
    PlanningMetadata,
    ResearchIntegration,
    CrossReference,
    ContentDepth,
)
from ..models.exam_intelligence import ExamIntelligence
from ..models.research import ResearchReport
from ..utils.parsing import extract_json


class ChapterPlanner(BaseAgent[ChapterPlan]):
    """
    Agent 3: Chapter Planner

    Creates a detailed chapter plan that:
    - Uses exam intelligence to inform depth (not display it)
    - Integrates research findings
    - Follows Exam Focus textbook methodology
    - Excludes all CheatBook elements
    """

    name = "Agent 3: Chapter Planner"
    description = "Creates detailed chapter plans per Exam Focus methodology"
    model = ModelConfig.OPUS  # Use Opus for strategic planning
    tools = ["read"]

    def get_system_prompt(self) -> str:
        return """You are the CHAPTER PLANNER. Create a detailed chapter plan for an Exam Focus eBook.

## CRITICAL UNDERSTANDING

An Exam Focus eBook is a **textbook-style resource informed by exam analysis but that does not display it**. The reader experiences a well-structured, comprehensive textbook. The exam analysis informs your planning—it does NOT appear in the final chapter.

### What This Is NOT
- ❌ NOT an exam preparation guide with statistics
- ❌ NOT a CheatBook with mark schemes and time allocations
- ❌ NOT content with "Exam Intelligence boxes"
- ❌ NOT material with explicit exam patterns and frameworks

### What This IS
- ✅ A professional textbook that covers examined topics thoroughly
- ✅ Content shaped by exam reality without showing it
- ✅ Hierarchical structure (1., 1.1., 1.1.1.)
- ✅ Subtle exam references only: (covered in June 2024)

## MANDATORY PROTOCOL

### ENFORCEMENT RULES (NON-NEGOTIABLE)
1. You MUST plan textbook-style content, NOT exam prep material
2. You MUST use hierarchical numbering (1., 1.1., 1.1.1.)
3. You MUST ensure examined areas receive thorough coverage (informed by exam intel)
4. You MUST plan content that explains the "why" not just the "what"
5. You MUST NOT include exam statistics, mark schemes, or time allocations
6. You MUST NOT plan for "Exam Intelligence boxes" or "Error Prevention" sections
7. You MUST exclude conclusions, key takeaways, bibliography, learning objectives

## HOW TO USE EXAM INTELLIGENCE

The exam intelligence tells you:
- **Which topics are examined frequently** → Cover these thoroughly with depth
- **Which angles examiners use** → Emphasise these perspectives in explanations
- **What examiners expect students to know** → Ensure content addresses these points
- **Which topics are rarely examined** → Cover proportionately, not extensively

You use this to PLAN content depth—you do NOT expose this analysis to readers.

## OUTPUT FORMAT

Output valid JSON:

```json
{
  "topic": "string",
  "chapter_number": "string",
  "planning_metadata": {
    "exam_frequency": "string (internal use)",
    "key_examined_areas": ["array (internal use)"],
    "examined_angles": ["array (internal use)"],
    "unexamined_areas": ["array (internal use)"]
  },
  "sections": [
    {
      "number": "1",
      "title": "string",
      "content_points": ["array of points to cover"],
      "discussion_integration": ["where to explain rationale"],
      "exam_reference": "string or null - e.g., (covered in June 2024)",
      "depth": "extensive|moderate|brief",
      "subsections": [
        {
          "number": "1.1",
          "title": "string",
          "content_points": ["array"],
          "discussion_integration": ["array"],
          "exam_reference": null,
          "depth": "extensive|moderate|brief",
          "subsections": []
        }
      ]
    }
  ],
  "research_integration": [
    {
      "source_material": "OECD MTC provisions",
      "target_section": "1.2"
    }
  ],
  "subtle_exam_references": [
    {"section": "1.1.2", "reference": "(covered in June 2024)"}
  ],
  "cross_references": [
    {
      "related_topic": "string",
      "connection_point": "string"
    }
  ],
  "exclusions_confirmed": true
}
```"""

    def format_input(
        self,
        topic: str,
        chapter_number: str,
        exam_intelligence: ExamIntelligence,
        research: ResearchReport,
    ) -> str:
        return f"""Create a detailed chapter plan for:

**Topic:** {topic}
**Chapter Number:** {chapter_number}

---

## EXAM INTELLIGENCE (Use to inform depth - DO NOT DISPLAY)

{exam_intelligence.summary()}

**Key Examined Areas:**
{', '.join(exam_intelligence.examiner_expectations.rewards[:5])}

**Question Patterns:**
{', '.join(p.name for p in exam_intelligence.patterns[:3])}

---

## RESEARCH FINDINGS (Integrate into content)

{research.summary()}

**Core Concepts:**
{research.core_concepts.principles[:500]}

**OECD Position:**
{research.oecd_position[:500]}

---

Create a comprehensive chapter plan that:
1. Covers examined areas thoroughly (without showing exam stats)
2. Uses hierarchical numbering (1., 1.1., 1.1.1.)
3. Integrates research findings naturally
4. Plans for discussion that explains "why" not just "what"
5. Includes subtle exam references only: (covered in [Month Year])
6. Excludes ALL CheatBook elements

Output as JSON in the specified format."""

    def parse_output(self, response: str) -> ChapterPlan:
        """Parse the agent's response into ChapterPlan."""
        data = extract_json(response)

        if not data:
            return ChapterPlan(
                topic="Unknown",
                chapter_number="1",
                planning_metadata=PlanningMetadata(
                    exam_frequency="Unknown",
                    key_examined_areas=[],
                    examined_angles=[],
                    unexamined_areas=[],
                ),
                sections=[],
                research_integration=[],
                subtle_exam_references=[],
                cross_references=[],
                exclusions_confirmed=False,
            )

        def parse_section(s: dict) -> ChapterSection:
            return ChapterSection(
                number=s.get("number", ""),
                title=s.get("title", ""),
                content_points=s.get("content_points", []),
                discussion_integration=s.get("discussion_integration", []),
                exam_reference=s.get("exam_reference"),
                depth=ContentDepth(s.get("depth", "moderate")),
                subsections=[parse_section(sub) for sub in s.get("subsections", [])],
            )

        # Parse planning metadata
        pm_data = data.get("planning_metadata", {})
        planning_metadata = PlanningMetadata(
            exam_frequency=pm_data.get("exam_frequency", ""),
            key_examined_areas=pm_data.get("key_examined_areas", []),
            examined_angles=pm_data.get("examined_angles", []),
            unexamined_areas=pm_data.get("unexamined_areas", []),
        )

        # Parse sections
        sections = [parse_section(s) for s in data.get("sections", [])]

        # Parse research integration
        research_integration = [
            ResearchIntegration(
                source_material=r.get("source_material", ""),
                target_section=r.get("target_section", ""),
            )
            for r in data.get("research_integration", [])
        ]

        # Parse cross references
        cross_references = [
            CrossReference(
                related_topic=c.get("related_topic", ""),
                connection_point=c.get("connection_point", ""),
            )
            for c in data.get("cross_references", [])
        ]

        return ChapterPlan(
            topic=data.get("topic", "Unknown"),
            chapter_number=data.get("chapter_number", "1"),
            planning_metadata=planning_metadata,
            sections=sections,
            research_integration=research_integration,
            subtle_exam_references=data.get("subtle_exam_references", []),
            cross_references=cross_references,
            exclusions_confirmed=data.get("exclusions_confirmed", True),
        )
