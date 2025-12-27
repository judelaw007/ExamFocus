"""
Agent 4.2: Chapter Transformer

Executes transformation plans to convert CheatBook chapters to Exam Focus style.
"""

from typing import Optional
import re

from .base import BaseAgent
from ..config import ModelConfig
from ..models.transformation import TransformationPlan, TransformedChapter
from ..utils.parsing import extract_json, count_words


class ChapterTransformer(BaseAgent[TransformedChapter]):
    """
    Agent 4.2: Chapter Transformer

    Executes the transformation plan from Agent 4.1 to convert
    CheatBook-style chapters into Exam Focus eBook style.

    This agent performs the actual rewriting:
    - Removes all CheatBook elements
    - Applies hierarchical numbering
    - Rewrites in textbook prose style
    - Integrates old notes if available
    - Stays within word count targets
    """

    name = "Agent 4.2: Chapter Transformer"
    description = "Transforms CheatBook chapters to Exam Focus eBook style"
    model = ModelConfig.OPUS  # Quality writing needs Opus
    tools = ["read", "write"]

    def get_system_prompt(self) -> str:
        return """You are the CHAPTER TRANSFORMER. Execute the transformation plan to convert a CheatBook-style chapter into Exam Focus eBook style.

## CRITICAL UNDERSTANDING

You are TRANSFORMING an existing chapter, not writing from scratch. You must:
1. Preserve accurate, valuable content
2. Remove ALL CheatBook elements
3. Restructure into hierarchical numbering
4. Rewrite in textbook prose style
5. Stay within word count targets

### What You Are Producing
- ✅ A professional textbook chapter
- ✅ Clear, authoritative prose
- ✅ Hierarchical structure (## Chapter X: | ### 1. | #### 1.1.)
- ✅ Subtle exam references only: (ADIT June 2024) or (ADIT December 2023)

### What You Are Removing
- ❌ Exam Intelligence boxes
- ❌ Mark schemes and time allocations
- ❌ Worked exam examples with model answers
- ❌ Pattern recognition sections
- ❌ Error prevention sections
- ❌ Answer frameworks
- ❌ Conclusions, key takeaways
- ❌ Bibliography and References sections (these do not add knowledge)
- ❌ Web Resources sections

## HIERARCHICAL NUMBERING FORMAT

**⚠️ CRITICAL: Each Chapter Has Independent Internal Numbering**

Section numbers are NOT tied to chapter number. Each chapter starts fresh at 1, 2, 3...

Format:
- Chapter heading: `## Chapter X: [Title]`
- Main sections: `### 1.`, `### 2.`, `### 3.`
- Subsections: `#### 1.1.`, `#### 2.1.`

Example for Chapter 5:
```markdown
## Chapter 5: Relief from Double Taxation

### 1. The Credit Method

The credit method allows taxpayers to offset foreign taxes...

#### 1.1. Direct Credit

Direct credit applies to taxes paid directly...

### 2. The Exemption Method

Under the exemption method...
```

## TRANSFORMATION PROCESS

### Step 1: Extract Valuable Content
Keep: Accurate explanations, technical details, case references
Remove: Exam statistics, mark allocations, "how to answer" frameworks

### Step 2: Apply New Structure
Follow the structural mapping from the transformation plan.

### Step 3: Rewrite in Textbook Style
Transform from exam-focused to textbook style.

BEFORE (CheatBook):
```
### Answer Framework (15 marks):
1. Identify applicable treaty article (3 marks)
2. State relevant provisions (4 marks)
```

AFTER (Exam Focus):
```
### 3.2. Applying Treaty Provisions

When determining tax treatment, the starting point is identifying
which treaty article governs the type of income...
```

### Step 4: Integrate Old Notes (if available)
Merge content seamlessly with consistent tone and style.

### Step 5: Add Subtle Exam References
Format: *(ADIT [Month] [Year])* - e.g., (ADIT June 2023) or (ADIT December 2024)
Maximum 3-5 per chapter.
Do NOT use "(covered in...)" or "(illustrated in...)" - just use (ADIT Month Year).

### Step 6: Verify Word Count
Stay within the target range specified in the plan.

## OUTPUT

You MUST output the complete transformed chapter in markdown format.

Do NOT output JSON. Output the actual chapter content.

After the chapter, add a brief metadata section:
```
---
TRANSFORMATION METADATA:
- Word Count: [count]
- CheatBook Elements Removed: Yes/No
- Exam References Added: [count]
- Old Notes Integrated: Yes/No
---
```"""

    def format_input(
        self,
        transformation_plan: TransformationPlan,
        existing_chapter: str,
        old_notes: Optional[str] = None,
    ) -> str:
        # Format the plan summary
        plan_summary = f"""
## TRANSFORMATION PLAN SUMMARY

**Topic:** {transformation_plan.topic_code} - {transformation_plan.topic_description}

**Word Count Target:** {transformation_plan.word_count_strategy.target_min} - {transformation_plan.word_count_strategy.target_max}
**Current Word Count:** {transformation_plan.word_count_strategy.current_count}
**Strategy:** {transformation_plan.word_count_strategy.strategy}

### Proposed New Structure:
{transformation_plan.proposed_outline}

### Content to Remove:
{chr(10).join(f"- {c.element_type} at {c.location}: {c.replacement_strategy}" for c in transformation_plan.content_to_remove[:10])}

### Content to Keep:
{chr(10).join(f"- {c.section}: {c.description}" for c in transformation_plan.content_to_keep[:10])}

### Subtle Exam References to Add:
{chr(10).join(f"- Section {r['section']}: {r['reference']}" for r in transformation_plan.subtle_exam_references[:5])}

### Content Gaps to Fill:
{chr(10).join(f"- {g.gap} (Priority: {g.priority})" for g in transformation_plan.content_gaps[:5])}

### Areas to Develop (for word count):
{chr(10).join(f"- {a}" for a in transformation_plan.word_count_strategy.areas_to_develop[:5])}

### Areas to Trim (if over word count):
{chr(10).join(f"- {a}" for a in transformation_plan.word_count_strategy.areas_to_trim[:5])}

### Special Instructions:
{transformation_plan.special_instructions}
"""

        old_notes_section = ""
        if old_notes:
            old_notes_section = f"""
## OLD NOTES TO INTEGRATE

{old_notes[:2000]}...
"""

        return f"""Transform this chapter following the plan:

{plan_summary}

---

## EXISTING CHAPTER (to transform)

{existing_chapter}

{old_notes_section}

---

## YOUR TASK

1. Remove ALL CheatBook elements listed in the plan
2. Apply the new hierarchical structure
3. Rewrite in textbook prose style
4. Integrate old notes where specified
5. Add subtle exam references (max 3-5)
6. Stay within word count target: {transformation_plan.word_count_strategy.target_min}-{transformation_plan.word_count_strategy.target_max}

Output the COMPLETE transformed chapter in markdown format.
End with the transformation metadata section."""

    def parse_output(self, response: str) -> TransformedChapter:
        """Parse the agent's response into TransformedChapter."""
        content = response.strip()

        # Extract metadata if present
        metadata_match = re.search(
            r"---\s*TRANSFORMATION METADATA:(.*?)---",
            content,
            re.DOTALL | re.IGNORECASE
        )

        if metadata_match:
            # Remove metadata from content
            content = content[:metadata_match.start()].strip()

        # Extract chapter number
        chapter_number = "1"
        chapter_match = re.search(r"##\s*Chapter\s+(\d+(?:\.\d+)?)", content)
        if chapter_match:
            chapter_number = chapter_match.group(1)

        # Extract topic from chapter heading
        topic_match = re.search(r"##\s*Chapter\s+\d+(?:\.\d+)?:\s*(.+?)(?:\n|$)", content)
        topic_description = topic_match.group(1).strip() if topic_match else "Unknown"

        # Count words
        word_count = count_words(content)

        # Count exam references
        exam_refs = len(re.findall(r"\(covered in [^)]+\)", content))

        # Check for CheatBook elements (should be none)
        cheatbook_patterns = [
            r"EXAM INTELLIGENCE",
            r"\d+\s*marks?\)",
            r"\d+\s*minutes?\)",
            r"Worked Example",
            r"Model Answer",
            r"Mark Scheme",
            r"Common Errors",
            r"Pattern Variations",
            r"Recognition Triggers",
            r"Answer Framework",
            r"Error Prevention",
            r"Strategic Priority",
            r"★",
        ]
        has_cheatbook = any(
            re.search(p, content, re.IGNORECASE) for p in cheatbook_patterns
        )

        # Check hierarchical numbering
        has_correct_numbering = bool(re.search(r"^##\s*Chapter\s+\d+", content, re.MULTILINE))
        has_correct_numbering = has_correct_numbering and bool(
            re.search(r"^###\s+\d+\.", content, re.MULTILINE)
        )

        return TransformedChapter(
            topic_code="",  # Would need to be passed through
            topic_description=topic_description,
            chapter_number=chapter_number,
            content=content,
            word_count=word_count,
            within_target=True,  # Would need target range to verify
            cheatbook_elements_removed=not has_cheatbook,
            hierarchical_numbering_correct=has_correct_numbering,
            exam_references_count=exam_refs,
            old_notes_integrated=False,  # Would need to track
            content_gaps_filled=False,  # Would need to track
        )
