"""
Agent 4: Chapter Drafter

Writes complete, publication-ready chapters following the plan.
"""

from typing import Optional

from .base import BaseAgent
from ..config import config, ModelConfig
from ..models.chapter import ChapterPlan, ChapterDraft
from ..models.exam_intelligence import ExamIntelligence
from ..models.research import ResearchReport
from ..utils.parsing import count_words


class ChapterDrafter(BaseAgent[ChapterDraft]):
    """
    Agent 4: Chapter Drafter

    Writes complete chapters that:
    - Follow the chapter plan exactly
    - Use textbook-style prose
    - Integrate research naturally
    - Include subtle exam references only
    - Exclude all CheatBook elements
    """

    name = "Agent 4: Chapter Drafter"
    description = "Writes complete publication-ready chapters"
    model = ModelConfig.OPUS  # Use Opus for quality writing
    tools = ["read", "write"]

    def get_system_prompt(self) -> str:
        return """You are the CHAPTER DRAFTER. Write a complete, publication-ready chapter for an Exam Focus eBook following the chapter plan exactly.

## CRITICAL UNDERSTANDING

An Exam Focus eBook is a **textbook-style resource informed by exam analysis but that does not display it**. The reader should experience a well-structured, comprehensive textbook—NOT an exam preparation guide.

### What You Are Writing
- ✅ A professional textbook chapter
- ✅ Clear, authoritative prose that builds understanding
- ✅ Content that covers examined areas thoroughly (without saying so)
- ✅ Hierarchical structure (## Chapter X: | ### 1. | #### 1.1.)
- ✅ Subtle exam references only: (covered in June 2024)

### What You Are NOT Writing
- ❌ Exam Intelligence boxes
- ❌ Mark schemes or time allocations
- ❌ "Answer framework" sections
- ❌ "Error prevention" or "Common mistakes" sections
- ❌ Pattern recognition guidance
- ❌ Worked exam examples with model answers
- ❌ CheatBook-style content

## HIERARCHICAL NUMBERING FORMAT

**Format:**
- Chapter heading: `## Chapter X: [Title]`
- Main sections: `### 1.`, `### 2.`, `### 3.` (always start at 1)
- Subsections: `#### 1.1.`, `#### 2.1.`, `#### 2.2.`

Each chapter's internal sections start fresh at 1, 2, 3... regardless of chapter number.

## WRITING STANDARDS

### Textbook Tone
- Clear, authoritative prose
- Technical accuracy without unnecessary jargon
- Explanations that build understanding progressively
- Examples that illustrate concepts practically

### Language Standards
| ❌ Don't Write | ✅ Do Write |
|----------------|-------------|
| "The arm's length principle, as articulated in Article 9..." | "The arm's length principle (Article 9, OECD Model) requires related companies to price transactions as if they were unrelated parties." |
| "It should be noted that..." | State it directly |
| "Candidates should be aware that..." | Do not address candidates—write as a textbook |

### Discussion Integration
- **Before presenting rules**: Provide context for why the rule exists
- **After stating provisions**: Explain the practical implications
- **Throughout**: Help readers understand rationale, not just memorise rules

### Subtle Exam References
The ONLY exam reference permitted is a parenthetical note:
```
The concept of beneficial ownership has been subject to significant judicial
interpretation. *(covered in June 2024)*
```

## WHAT TO EXCLUDE

- Exam Intelligence boxes
- Mark schemes and time allocations
- Answer frameworks and pattern sections
- Error prevention sections
- Conclusions and key takeaways
- Bibliography and learning objectives

## OUTPUT

Write the complete chapter in markdown format. Start with the chapter heading and proceed through all sections as planned.

The chapter should read as an authoritative professional textbook—comprehensive, clear, and educational."""

    def format_input(
        self,
        topic: str,
        chapter_plan: ChapterPlan,
        exam_intelligence: ExamIntelligence,
        research: ResearchReport,
    ) -> str:
        return f"""Write a complete chapter following this plan:

---

## CHAPTER PLAN

**Topic:** {topic}
**Chapter Number:** {chapter_plan.chapter_number}

### Outline:
{chapter_plan.get_outline()}

### Research to Integrate:
**OECD Position:**
{research.oecd_position}

**UN Differences:**
{chr(10).join(f"- {d.aspect}: OECD: {d.oecd_position} vs UN: {d.un_position}" for d in research.un_differences[:3])}

**BEPS/MLI:**
{', '.join(research.beps_mli.relevant_actions[:3])}

**Current Developments:**
{chr(10).join(f"- {d}" for d in research.current_developments[:3])}

### Subtle Exam References to Include:
{chr(10).join(f"- Section {r['section']}: {r['reference']}" for r in chapter_plan.subtle_exam_references[:5])}

---

## REQUIREMENTS

1. Follow the chapter plan structure exactly
2. Use hierarchical numbering: ## Chapter X: | ### 1. | #### 1.1.
3. Write textbook-style prose (NOT exam prep material)
4. Integrate research naturally into explanations
5. Include subtle exam references where planned
6. Explain the "why" behind rules, not just the "what"
7. NO CheatBook elements (no exam stats, mark schemes, answer frameworks)

Write the complete chapter now."""

    def parse_output(self, response: str) -> ChapterDraft:
        """Parse the agent's response into ChapterDraft."""
        # The response should be the complete markdown chapter
        content = response.strip()

        # Extract chapter number from content
        chapter_number = "1"
        import re
        match = re.search(r"##\s*Chapter\s+(\d+(?:\.\d+)?)", content)
        if match:
            chapter_number = match.group(1)

        # Count sections
        sections_count = len(re.findall(r"^###\s+\d+\.", content, re.MULTILINE))

        # Find exam references
        exam_refs = re.findall(r"\(covered in [^)]+\)", content)

        # Count words
        word_count = count_words(content)

        # Check for CheatBook elements (should be none)
        cheatbook_patterns = [
            r"exam intelligence",
            r"mark scheme",
            r"time allocation",
            r"error prevention",
            r"common mistakes",
            r"answer framework",
        ]
        has_cheatbook = any(
            re.search(p, content, re.IGNORECASE) for p in cheatbook_patterns
        )

        return ChapterDraft(
            topic=self._extract_topic(content),
            chapter_number=chapter_number,
            content=content,
            word_count=word_count,
            sections_count=sections_count,
            exam_references=exam_refs,
            cheatbook_elements_excluded=not has_cheatbook,
        )

    def _extract_topic(self, content: str) -> str:
        """Extract topic from chapter heading."""
        import re
        match = re.search(r"##\s*Chapter\s+\d+(?:\.\d+)?:\s*(.+?)(?:\n|$)", content)
        if match:
            return match.group(1).strip()
        return "Unknown"
