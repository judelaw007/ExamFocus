# ExamFocus Content Pipeline - Prompt Architecture

## Overview

This directory contains the specifications for the 8-prompt content creation and quality assurance pipeline for ExamFocus course materials.

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXAMFOCUS CONTENT PIPELINE                          │
│                              8-Prompt Architecture                          │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │   USER INPUT    │
                              │   Topic Name    │
                              └────────┬────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        CONTENT CREATION PHASE                                │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
          ┌────────────────────────────┼────────────────────────────┐
          │                            │                            │
          ▼                            ▼                            │
┌──────────────────┐        ┌──────────────────┐                    │
│ PROMPT 1         │        │ PROMPT 2         │                    │
│ Past Paper       │        │ Topic            │                    │
│ Analyzer         │        │ Researcher       │                    │
│                  │        │                  │                    │
│ Model: Sonnet    │        │ Model: Sonnet    │                    │
│ Tools: Read,     │        │ Tools: WebSearch │                    │
│   Glob, Grep     │        │   WebFetch       │                    │
│                  │        │                  │                    │
│ Searches: 0      │        │ Searches: 5-7    │                    │
└────────┬─────────┘        └────────┬─────────┘                    │
         │                           │                              │
         │    Exam Intelligence      │    Research Findings         │
         │                           │                              │
         └───────────┬───────────────┘                              │
                     │                                              │
                     ▼                                              │
          ┌──────────────────┐                                      │
          │ PROMPT 3         │                                      │
          │ Chapter          │◄─────────────────────────────────────┘
          │ Planner          │         Syllabus & Methodology
          │                  │
          │ Model: Opus      │
          │ Tools: Read      │
          │                  │
          │ Methodology:     │
          │ Exam Focus       │
          │ (embedded)       │
          └────────┬─────────┘
                   │
                   │    Detailed Chapter Plan
                   │
                   ▼
          ┌──────────────────┐
          │ PROMPT 4         │
          │ Chapter          │
          │ Drafter          │
          │                  │
          │ Model: Opus      │
          │ Tools: Read,     │
          │   Write          │
          │                  │
          │ Methodology:     │
          │ Exam Focus       │
          │ (embedded)       │
          └────────┬─────────┘
                   │
                   │    Draft Chapter
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        QUALITY ASSURANCE PHASE                               │
└──────────────────────────────────────────────────────────────────────────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ PROMPT 5a        │
          │ Content          │
          │ Accuracy         │
          │                  │
          │ Model: Sonnet    │
          │ Tools: WebSearch │
          │   WebFetch, Edit │
          │                  │
          │ Searches: 15-20  │
          └────────┬─────────┘
                   │
                   │    Accuracy-Verified Chapter
                   │
                   ▼
          ┌──────────────────┐
          │ PROMPT 5b        │
          │ Consistency      │
          │ & Flow           │
          │                  │
          │ Model: Sonnet    │
          │ Tools: Read,     │
          │   Edit           │
          └────────┬─────────┘
                   │
                   │    Consistency-Checked Chapter
                   │
                   ▼
          ┌──────────────────┐
          │ PROMPT 5c        │
          │ Structural       │
          │ Refinement       │
          │                  │
          │ Model: Haiku     │
          │ Tools: Read,     │
          │   Edit           │
          └────────┬─────────┘
                   │
                   │    Refined Chapter
                   │
                   ▼
          ┌──────────────────┐
          │ PROMPT 5d        │
          │ Discussion       │
          │ Enhancement      │
          │                  │
          │ Model: Opus      │
          │ Tools: Read,     │
          │   Edit           │
          └────────┬─────────┘
                   │
                   │
                   ▼
          ┌──────────────────┐
          │  FINAL OUTPUT    │
          │  Publication-    │
          │  Ready Chapter   │
          └──────────────────┘
```

---

## Prompt Summary

| Prompt | Name | Model | Tools | Web Searches | Purpose |
|--------|------|-------|-------|--------------|---------|
| 1 | Past Paper Analyzer | Sonnet | Read, Glob, Grep | 0 | Extract exam intelligence from past papers |
| 2 | Topic Researcher | Sonnet | WebSearch, WebFetch | 5-7 | Gather current authoritative information |
| 3 | Chapter Planner | Opus | Read | 0 | Create detailed chapter plan per Exam Focus methodology |
| 4 | Chapter Drafter | Opus | Read, Write | 0 | Write complete chapter following the plan |
| 5a | Content Accuracy | Sonnet | WebSearch, WebFetch, Edit | 15-20 | Verify all facts against current sources |
| 5b | Consistency & Flow | Sonnet | Read, Edit | 0 | Standardize terminology, remove redundancies |
| 5c | Structural Refinement | Haiku | Read, Edit | 0 | Remove educational scaffolding |
| 5d | Discussion Enhancement | Opus | Read, Edit | 0 | Ensure 15% integrated prose discussion |

---

## Cost & Performance Profile

| Model | Prompts Using | Characteristics |
|-------|---------------|-----------------|
| **Opus** | 3, 4, 5d | Highest quality - for strategic planning, quality writing |
| **Sonnet** | 1, 2, 5a, 5b | Balanced - for analysis, research, verification |
| **Haiku** | 5c | Fast & efficient - for simple pattern-based deletions |

---

## Data Flow Summary

```
User Input: "Article 10 Dividends"
     │
     ├──► Prompt 1: Analyzes 8 past papers → Frequency 63%, 12-20 marks, 4 patterns
     │
     ├──► Prompt 2: 5-7 web searches → OECD position, UN differences, BEPS impact
     │
     └──► Prompt 3: Creates detailed plan → 6 sections, 4 worked examples needed
              │
              └──► Prompt 4: Writes ~4000 word chapter with all components
                        │
                        └──► Prompt 5a: 15-20 searches verify facts → 3 corrections
                                  │
                                  └──► Prompt 5b: Standardizes terminology → 8 fixes
                                            │
                                            └──► Prompt 5c: Removes scaffolding → 5 deletions
                                                      │
                                                      └──► Prompt 5d: Adds discussion → 400 words
                                                                │
                                                                └──► FINAL: Publication-ready chapter
```

---

## File Index

| File | Description |
|------|-------------|
| `prompt-1-past-paper-analyzer.md` | Past Paper Analyzer specification |
| `prompt-2-topic-researcher.md` | Topic Researcher specification |
| `prompt-3-chapter-planner.md` | Chapter Planner specification (Exam Focus embedded) |
| `prompt-4-chapter-drafter.md` | Chapter Drafter specification (Exam Focus embedded) |
| `prompt-5a-content-accuracy.md` | Content Accuracy Verifier specification |
| `prompt-5b-consistency-flow.md` | Consistency & Flow Checker specification |
| `prompt-5c-structural-refinement.md` | Structural Refinement specification |
| `prompt-5d-discussion-enhancement.md` | Discussion Enhancement specification |
| `README.md` | This overview document |

---

## Usage

### Running the Full Pipeline

To create a new chapter, invoke prompts in sequence:

1. **Prompt 1** with topic name → Returns exam intelligence
2. **Prompt 2** with topic name + exam intelligence summary → Returns research
3. **Prompt 3** with exam intelligence + research → Returns chapter plan
4. **Prompt 4** with chapter plan + all context → Returns draft chapter
5. **Prompt 5a** with draft chapter → Returns accuracy-verified chapter
6. **Prompt 5b** with verified chapter → Returns consistency-checked chapter
7. **Prompt 5c** with checked chapter → Returns refined chapter
8. **Prompt 5d** with refined chapter → Returns publication-ready chapter

### Parallel Execution

Prompts 1 and 2 can run in parallel since they have no dependencies on each other.

All other prompts must run sequentially as each depends on the previous output.

---

## Embedded Methodologies

The following documents have been embedded into prompts:

| Document | Embedded In |
|----------|-------------|
| `What_is_Exam_Focus (1).md` | Prompt 3 (Planner), Prompt 4 (Drafter) |
| `Content Accuracy.md` | Prompt 5a |
| `Content Consistency & Flow Check.md` | Prompt 5b |
| `Structural Refinement Prompt.md` | Prompt 5c |
| `discussion_enhancement (1).md` | Prompt 5d |

Prompts are self-contained and do not need to reference external documents at runtime.

---

## Version

- **Pipeline Version**: 1.0
- **Created**: December 2024
- **Methodology**: Exam Focus
- **Target**: ADIT Module 1 - Principles of International Taxation
