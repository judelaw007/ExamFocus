# Prompt 5c: Structural Refinement

## Configuration

| Setting | Value |
|---------|-------|
| **Model** | `claude-sonnet-4-5-20241022` |
| **Tools** | `Read`, `Edit` |
| **Position** | 5c of 8 (Third Quality Prompt) |
| **Input** | Prompt 5b (Consistency-Checked Chapter) |
| **Output** | Prompt 5d (Discussion Enhancement) |

---

## Prompt

```
You are the STRUCTURAL REFINEMENT prompt. Remove educational scaffolding and apply hierarchical numbering. Do NOT rewrite any substantive content.

## INPUT
- **Chapter:** {chapter_content}
- **Topic:** {topic_name}

---

## MANDATORY PROTOCOL

### ⚠️ ENFORCEMENT RULES (NON-NEGOTIABLE)
1. You MUST scan the entire chapter for ALL scaffolding elements before making any changes
2. You MUST delete every instance of scaffolding listed below—NO EXCEPTIONS, NO MERCY
3. You MUST apply hierarchical numbering to all sections
4. You MUST NOT rewrite, improve, or enhance any remaining content
5. You MUST preserve all substantive content exactly as written
6. If uncertain whether something is scaffolding, err on the side of DELETION for items matching the patterns below

### ⚠️ CRITICAL: COMMON FAILURES TO AVOID

**Educational Scaffolding Failures:**
- **DO NOT** preserve "Key Takeaways" sections just because they contain useful content—they are SCAFFOLDING and must be DELETED
- **DO NOT** skip scaffolding removal because the section has a numbered heading
- **DO NOT** confuse scaffolding sections with substantive content—if it matches a pattern below, DELETE IT

**Exam Skills Scaffolding Failures:**
- **DO NOT** preserve "Question Analysis" sections—these are exam technique, not knowledge
- **DO NOT** preserve "Answer Planning" templates—these are exam technique, not knowledge
- **DO NOT** preserve "Mark Scheme Mapping" tables—these are exam technique, not knowledge
- **DO NOT** preserve "Common Errors" sections—these are exam technique, not knowledge
- **DO NOT** preserve "Time Management" guidance—these are exam technique, not knowledge
- **DO NOT** preserve "Pre-Answer Checklist" sections—these are exam technique, not knowledge
- **DO NOT** preserve "Error Prevention" or "Top X Mistakes" sections—these are exam technique, not knowledge

**The Distinction That Matters:**
- **KNOWLEDGE** = What the law IS, how it works, substantive analysis → PRESERVE
- **EXAM SKILLS** = How to ANSWER questions, time allocation, error avoidance → DELETE

---

## TASK 1: APPLY HIERARCHICAL NUMBERING

Convert all sections to decimal hierarchy:

| Level | Format | Example |
|-------|--------|---------|
| `##` Top-level | 1., 2., 3. | `## 1. Concept Foundation` |
| `###` Second-level | 1.1., 1.2., 2.1. | `### 1.1. What is Tax?` |
| `####` Third-level | 1.1.1., 1.2.1. | `#### 1.1.1. Sub-topic` |

- Reset sub-numbering for each new parent section
- Keep special headers unnumbered (e.g., EXAM INTELLIGENCE box at chapter start)

---

## TASK 2: REMOVE SCAFFOLDING (MANDATORY - NO EXCEPTIONS)

### ⚠️ DELETE ALL of these—even if they contain useful-looking content:

#### Category A: Educational Scaffolding

| Category | Patterns to Delete | Examples |
|----------|-------------------|----------|
| **Key Takeaways** | Any section titled "KEY TAKEAWAYS", "Key Takeaways", "Key Points", "Takeaways", "Main Points", summary boxes with bullet points restating chapter content | `## K. KEY TAKEAWAYS`, `## 11. Key Takeaways`, boxed summaries |
| **Key Vocabulary** | "KEY VOCABULARY", "Key Terms", "Glossary", term definition lists at section ends | Standalone glossary sections |
| **References** | "References", "Sources", "Further Reading", "Bibliography", reference sections at chapter end (KEEP in-text citations like case names) | `## References`, `**Primary Sources**:` lists |
| **Summaries** | "Summary", "Section Summary", "Chapter Summary", "In summary..." paragraphs that merely restate what was covered | Restating paragraphs at section ends |
| **Learning Objectives** | "By the end of this section...", "Learning objectives", "You will learn...", outcome bullet lists | Pre-section objective lists |
| **Time Indicators** | "Estimated reading time", "X minutes", page counts, word counts | `Reading time: 15 min` |
| **Next Steps** | "Before proceeding to...", "Continue to Section X", "In the next section...", "Next, we will..." | Navigation text between sections |
| **Section Markers** | "End of Section X", "Conclusion of Chapter X", chapter footers, `---` followed by chapter attribution | `*Chapter 1 | Exam Focus*` footers |
| **Generic Conclusions** | "In this section we discussed...", "We have now covered...", "This concludes..." | Wrap-up paragraphs that add no new insight |

#### Category B: Exam Skills Scaffolding (NOT Knowledge Content)

These are exam TECHNIQUE elements, not substantive knowledge. DELETE ALL:

| Category | Patterns to Delete | Examples |
|----------|-------------------|----------|
| **Question Analysis** | "Question Analysis:", analysis of what question is testing, breakdown of question requirements | `**Question Analysis**: - Tests knowledge of...` |
| **Answer Planning** | "Answer Planning", planning templates, answer structure outlines before model answers | `**Answer Planning** (3 minutes): Introduction: ... Part 1: ...` |
| **Mark Scheme Mapping** | "Mark Scheme Mapping", tables showing marks per component, mark allocation breakdowns | `| Component | Marks | Achieved By |` tables after answers |
| **Common Errors** | "Common Errors", "Candidate Mistakes", lists of what NOT to do | `**Common Errors**: - ❌ Failing to...` |
| **Time Management** | Time allocation guidance within worked examples, "X minutes" breakdowns | `**Time Management**: 48 minutes total - Reading: 5 min` |
| **Pre-Answer Checklists** | "Pre-Answer Checklist", checkbox lists of things to verify before writing | `- [ ] Have I identified...` |
| **Self-Review Questions** | "Quick Self-Review", "Test Yourself", self-assessment questions | `### Quick Self-Review Questions` |
| **Error Prevention** | "Error Prevention", "Top X Mistakes", standalone sections about avoiding errors | `## Error Prevention`, `### Top 10 Candidate Mistakes` |

### ⚠️ CRITICAL DISTINCTION: Knowledge vs. Exam Skills

**DELETE (Exam Skills)**: HOW to answer questions, time management, planning templates, error avoidance
**PRESERVE (Knowledge)**: WHAT the law is, substantive analysis, model answer CONTENT (not the scaffolding around it)

### Deletion Decision Tree:
1. Does the section/paragraph MATCH a pattern above? → **DELETE IT**
2. Does it primarily RESTATE content covered elsewhere? → **DELETE IT**
3. Does it serve as NAVIGATION between sections? → **DELETE IT**
4. Is it a SUMMARY without new analytical insight? → **DELETE IT**

---

## WHAT TO PRESERVE

Keep exactly as written:
- All substantive explanatory content (knowledge about the law)
- **Model Answer CONTENT ONLY** from worked examples (the actual answer text)
- Analytical conclusions that add NEW insight (not restatements)
- In-text citations and case references
- Tables containing substantive information (not summary tables)
- EXAM INTELLIGENCE boxes (these are different from Key Takeaways)

### ⚠️ WORKED EXAMPLES: What to Keep vs. Delete

For each worked example, the structure should become:

**KEEP:**
- Question text (the actual exam question)
- Model Answer sections (the substantive answer content)
- Section headers within answers (e.g., "Introduction", "Conclusion")

**DELETE:**
- Question Analysis (before the answer)
- Answer Planning (before the answer)
- Mark Scheme Mapping (after the answer)
- Common Errors (after the answer)
- Time Management (anywhere)

**Result:** Question → Model Answer (clean, no scaffolding)

---

## OUTPUT FORMAT

### 1. SCAFFOLDING SCAN RESULTS
Before making changes, list ALL scaffolding found:

| # | Category | Section/Location | Content Preview | Action |
|---|----------|------------------|-----------------|--------|
| 1 | Key Takeaways | Section 11 / Lines 759-790 | "JURISDICTION TO TAX - EXAM ESSENTIALS..." | DELETE |
| 2 | References | End of chapter | "Primary Sources:..." | DELETE |
[List ALL items found]

### 2. NUMBERING APPLIED
| Original Header | New Header |
|-----------------|------------|
| `## A. CONCEPT FOUNDATION` | `## 1. Concept Foundation` |
| `### 1. What is Tax?` | `### 1.1. What is Tax?` |
[All header changes]

### 3. DELETION LOG
| # | Category | Text Deleted (first 100 chars) | Lines Removed |
|---|----------|-------------------------------|---------------|
| 1 | Key Takeaways | "## 11. Key Takeaways ... JURISDICTION TO TAX - EXAM ESSENTIALS..." | ~35 lines |
| 2 | References | "## References ... Primary Sources:..." | ~20 lines |
[All deletions with line counts]

### 4. DELETION SUMMARY

**Category A: Educational Scaffolding**
| Category | Items Found | Items Deleted | Status |
|----------|-------------|---------------|--------|
| Key Takeaways | X | X | ✓ Complete |
| Key Vocabulary | X | X | ✓ Complete |
| References | X | X | ✓ Complete |
| Summaries | X | X | ✓ Complete |
| Learning Objectives | X | X | ✓ Complete |
| Time Indicators | X | X | ✓ Complete |
| Next Steps | X | X | ✓ Complete |
| Section Markers | X | X | ✓ Complete |
| Generic Conclusions | X | X | ✓ Complete |

**Category B: Exam Skills Scaffolding**
| Category | Items Found | Items Deleted | Status |
|----------|-------------|---------------|--------|
| Question Analysis | X | X | ✓ Complete |
| Answer Planning | X | X | ✓ Complete |
| Mark Scheme Mapping | X | X | ✓ Complete |
| Common Errors | X | X | ✓ Complete |
| Time Management | X | X | ✓ Complete |
| Pre-Answer Checklists | X | X | ✓ Complete |
| Self-Review Questions | X | X | ✓ Complete |
| Error Prevention | X | X | ✓ Complete |

| **TOTAL** | **X** | **X** | **✓ All Removed** |

### 5. PRESERVED VERIFICATION
| Element | Status | Evidence |
|---------|--------|----------|
| Substantive content | ✓ Preserved | All explanatory sections intact |
| Model answer content | ✓ Preserved | Answer text retained (scaffolding removed) |
| In-text citations | ✓ Preserved | Case names kept in body text |
| EXAM INTELLIGENCE boxes | ✓ Preserved | Chapter header boxes intact |

### 6. REFINED CHAPTER
[Full chapter with numbering applied and ALL scaffolding removed]

---

## PRE-SUBMISSION CHECKLIST

Before outputting, VERIFY each item:

**Scan & Numbering:**
- [ ] Scanned ENTIRE chapter for scaffolding BEFORE making changes
- [ ] Hierarchical numbering applied to ALL sections

**Category A - Educational Scaffolding DELETED:**
- [ ] ALL Key Takeaways sections DELETED
- [ ] ALL Reference/Bibliography sections DELETED
- [ ] ALL Summary sections DELETED
- [ ] ALL Learning Objectives DELETED
- [ ] ALL section markers and footers DELETED
- [ ] ALL Time Indicators DELETED
- [ ] ALL Next Steps/Navigation DELETED
- [ ] ALL Generic Conclusions DELETED

**Category B - Exam Skills Scaffolding DELETED:**
- [ ] ALL Question Analysis sections DELETED
- [ ] ALL Answer Planning sections DELETED
- [ ] ALL Mark Scheme Mapping tables DELETED
- [ ] ALL Common Errors sections DELETED
- [ ] ALL Time Management guidance DELETED
- [ ] ALL Pre-Answer Checklists DELETED
- [ ] ALL Self-Review Questions DELETED
- [ ] ALL Error Prevention sections DELETED

**Preservation Verified:**
- [ ] Model answer CONTENT preserved (scaffolding around it removed)
- [ ] In-text citations PRESERVED (not deleted with References)
- [ ] EXAM INTELLIGENCE boxes PRESERVED

### Final Verification Questions:
1. **Is there ANY remaining section that matches a scaffolding pattern?** If yes, DELETE IT.
2. **For each worked example:** Does it contain ONLY Question + Model Answer? If not, DELETE the scaffolding.
3. **Is there an Error Prevention or Common Mistakes section anywhere?** If yes, DELETE IT.

**BEGIN STRUCTURAL REFINEMENT NOW.**
```

---

## Input Schema

```json
{
  "topic_name": "string",
  "chapter_content": "string - Consistency-checked chapter from Prompt 5b"
}
```

## Output Schema

```json
{
  "scaffolding_scan": [
    {"category": "string", "location": "string", "preview": "string", "action": "DELETE"}
  ],
  "numbering_applied": [
    {"original": "string", "new": "string"}
  ],
  "deletions": [
    {"category": "string", "text_preview": "string", "lines_removed": "number"}
  ],
  "summary": {
    "total_found": "number",
    "total_deleted": "number",
    "by_category": {...}
  },
  "preserved_verification": {
    "substantive_content": "boolean",
    "worked_examples": "boolean",
    "answer_frameworks": "boolean",
    "citations": "boolean"
  },
  "refined_chapter": "string"
}
```

---

## Model Selection Rationale

**Why Sonnet?**
- Requires careful context understanding to distinguish scaffolding from substantive content
- Must follow complex multi-step instructions accurately
- Needs to make multiple precise edits without errors
- Pattern matching alone is insufficient—requires judgment about edge cases
- Haiku was found to skip scaffolding deletions, particularly Key Takeaways sections
