# Transformation Pipeline Prompt Template

Use this prompt to transform existing CheatBook-style chapters into Exam Focus eBook style.

---

## Prompt Template

```
TRANSFORM Chapter [X.X] - [Topic Name] from CheatBook style to Exam Focus eBook style.

Topic Code: [CODE] from PIT_Syllabus_2026_Topics.csv
Existing Chapter: [path to existing chapter]
Old Notes: [path to old notes .docx if available, or "None"]

Execute agents 4.1 → 4.2 in sequence—no skipping of agents, each agent must perform their full tasks (non-negotiable - we must be thorough). Each agent must complete fully before the next begins. Pass output to QA (5a-5d) when Agent 4.2 completes.

Reference: /What_is_Exam_Focus_Document.md
```

---

## Example Prompts

### Part I Examples

```
TRANSFORM Chapter 1 - Jurisdiction to Tax from CheatBook style to Exam Focus eBook style.

Topic Code: I.A from PIT_Syllabus_2026_Topics.csv
Existing Chapter: ADIT/Principles of International Taxation/Part I - Basic Principles of International Taxation/Chapter_1_Jurisdiction_to_Tax.md
Old Notes: ADIT/Principles of International Taxation/Part I - Basic Principles of International Taxation/old notes/JURISDICTION TO TAX_2.docx

Execute agents 4.1 → 4.2 in sequence—no skipping of agents, each agent must perform their full tasks (non-negotiable - we must be thorough). Each agent must complete fully before the next begins. Pass output to QA (5a-5d) when Agent 4.2 completes.

Reference: /What_is_Exam_Focus_Document.md
```

```
TRANSFORM Chapter 5.1 - Relief by Credit from CheatBook style to Exam Focus eBook style.

Topic Code: I.E.1 from PIT_Syllabus_2026_Topics.csv
Existing Chapter: ADIT/Principles of International Taxation/Part I - Basic Principles of International Taxation/Chapter_5.1_Relief_by_Credit.md
Old Notes: ADIT/Principles of International Taxation/Part I - Basic Principles of International Taxation/old notes/Methods of relief from international double taxation.docx

Execute agents 4.1 → 4.2 in sequence—no skipping of agents, each agent must perform their full tasks (non-negotiable - we must be thorough). Each agent must complete fully before the next begins. Pass output to QA (5a-5d) when Agent 4.2 completes.

Reference: /What_is_Exam_Focus_Document.md
```

### Part II Examples

```
TRANSFORM Chapter 7.2 - Permanent Establishment from CheatBook style to Exam Focus eBook style.

Topic Code: II.G.2 from PIT_Syllabus_2026_Topics.csv
Existing Chapter: ADIT/Principles of International Taxation/Part II - Double Taxation Conventions/Chapter_7.2_Article_5_Permanent_Establishment.md
Old Notes: None

Execute agents 4.1 → 4.2 in sequence—no skipping of agents, each agent must perform their full tasks (non-negotiable - we must be thorough). Each agent must complete fully before the next begins. Pass output to QA (5a-5d) when Agent 4.2 completes.

Reference: /What_is_Exam_Focus_Document.md
```

```
TRANSFORM Chapter 12.3 - Interest Article 11 from CheatBook style to Exam Focus eBook style.

Topic Code: II.K.3 from PIT_Syllabus_2026_Topics.csv
Existing Chapter: ADIT/Principles of International Taxation/Part II - Double Taxation Conventions/Chapter_12.3_Article_11_Interest.md
Old Notes: None

Execute agents 4.1 → 4.2 in sequence—no skipping of agents, each agent must perform their full tasks (non-negotiable - we must be thorough). Each agent must complete fully before the next begins. Pass output to QA (5a-5d) when Agent 4.2 completes.

Reference: /What_is_Exam_Focus_Document.md
```

---

## Quick Reference: Old Notes Mapping (Part I Only)

| Topic Codes | Old Notes File |
|-------------|---------------|
| I.A | JURISDICTION TO TAX_2.docx |
| I.B.1, I.B.2 | Taxes and tax systems.docx |
| I.C.1 - I.C.5 | State practice in exercising tax jurisdiction.docx |
| I.D.1 - I.D.3 | CAUSES OF INTERNATIONAL DOUBLE TAXATION 2.docx |
| I.E.1 - I.E.5 | Methods of relief from international double taxation.docx |
| I.F.1 - I.F.3 | Private international law and tax.docx |
| I.G.1 - I.G.3 | The history of international tax law.docx |
| I.H.1 - I.H.2 | Tax and international human rights instruments.docx |
| I.I | STATE RESPONSIBILITY IN INTERNATIONAL TAX.docx |

**Note:** Part II, III, IV, V, VI topics have no old notes available. Use "None" for Old Notes field.

---

## Pipeline Summary

```
┌────────────────────────────────────────────────────────────────┐
│                  TRANSFORMATION PIPELINE                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Agent 4.1: Transformation Planner                             │
│  ├── Read syllabus CSV (scope, word limits)                    │
│  ├── Read existing chapter                                     │
│  ├── Read old notes (if available)                             │
│  └── Output: Transformation Plan                               │
│                          │                                      │
│                          ▼                                      │
│  Agent 4.2: Chapter Transformer                                │
│  ├── Execute transformation plan                               │
│  ├── Remove CheatBook elements                                 │
│  ├── Apply hierarchical numbering                              │
│  ├── Rewrite in textbook style                                 │
│  └── Output: Transformed Chapter                               │
│                          │                                      │
│                          ▼                                      │
│  QA Agents (5a → 5b → 5c → 5d)                                 │
│  ├── 5a: Content Accuracy                                      │
│  ├── 5b: Consistency & Flow                                    │
│  ├── 5c: Structural Refinement                                 │
│  └── 5d: Discussion Enhancement                                │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Comparison: Creation vs Transformation

| Aspect | Creation Pipeline | Transformation Pipeline |
|--------|------------------|------------------------|
| **Use When** | No existing chapter | Existing CheatBook-style chapter |
| **Agents** | 1 → 2 → 3 → 4 | 4.1 → 4.2 |
| **Starting Input** | Topic only | Existing chapter + old notes |
| **Agent 1** | Past Paper Analyzer | (not used) |
| **Agent 2** | Topic Researcher | (not used) |
| **Agent 3** | Chapter Planner | (not used) |
| **Agent 4** | Chapter Drafter | (not used) |
| **Agent 4.1** | (not used) | Transformation Planner |
| **Agent 4.2** | (not used) | Chapter Transformer |
| **QA** | 5a → 5b → 5c → 5d | 5a → 5b → 5c → 5d |
