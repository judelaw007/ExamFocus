# ExamFocus Content Pipeline - Agent Architecture

## Overview

This directory contains the specifications for the 8-agent content creation and quality assurance pipeline for ExamFocus course materials.

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXAMFOCUS CONTENT PIPELINE                          │
│                              8-Agent Architecture                           │
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
│ AGENT 1          │        │ AGENT 2          │                    │
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
          │ AGENT 3          │                                      │
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
          │ AGENT 4          │
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
          │ AGENT 5a         │
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
          │ AGENT 5b         │
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
          │ AGENT 5c         │
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
          │ AGENT 5d         │
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

## Agent Summary

| Agent | Name | Model | Tools | Web Searches | Purpose |
|-------|------|-------|-------|--------------|---------|
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

| Model | Agents Using | Characteristics |
|-------|--------------|-----------------|
| **Opus** | 3, 4, 5d | Highest quality - for strategic planning, quality writing |
| **Sonnet** | 1, 2, 5a, 5b | Balanced - for analysis, research, verification |
| **Haiku** | 5c | Fast & efficient - for simple pattern-based deletions |

---

## Data Flow Summary

```
User Input: "Article 10 Dividends"
     │
     ├──► Agent 1: Analyzes 8 past papers → Frequency 63%, 12-20 marks, 4 patterns
     │
     ├──► Agent 2: 5-7 web searches → OECD position, UN differences, BEPS impact
     │
     └──► Agent 3: Creates detailed plan → 6 sections, 4 worked examples needed
              │
              └──► Agent 4: Writes ~4000 word chapter with all components
                        │
                        └──► Agent 5a: 15-20 searches verify facts → 3 corrections
                                  │
                                  └──► Agent 5b: Standardizes terminology → 8 fixes
                                            │
                                            └──► Agent 5c: Removes scaffolding → 5 deletions
                                                      │
                                                      └──► Agent 5d: Adds discussion → 400 words
                                                                │
                                                                └──► FINAL: Publication-ready chapter
```

---

## File Index

| File | Description |
|------|-------------|
| `agent-1-past-paper-analyzer.md` | Past Paper Analyzer specification |
| `agent-2-topic-researcher.md` | Topic Researcher specification |
| `agent-3-chapter-planner.md` | Chapter Planner specification (Exam Focus embedded) |
| `agent-4-chapter-drafter.md` | Chapter Drafter specification (Exam Focus embedded) |
| `agent-5a-content-accuracy.md` | Content Accuracy Verifier specification |
| `agent-5b-consistency-flow.md` | Consistency & Flow Checker specification |
| `agent-5c-structural-refinement.md` | Structural Refinement specification |
| `agent-5d-discussion-enhancement.md` | Discussion Enhancement specification |
| `README.md` | This overview document |

---

## Usage

### Running the Full Pipeline

To create a new chapter, invoke agents in sequence:

1. **Agent 1** with topic name → Returns exam intelligence
2. **Agent 2** with topic name + exam intelligence summary → Returns research
3. **Agent 3** with exam intelligence + research → Returns chapter plan
4. **Agent 4** with chapter plan + all context → Returns draft chapter
5. **Agent 5a** with draft chapter → Returns accuracy-verified chapter
6. **Agent 5b** with verified chapter → Returns consistency-checked chapter
7. **Agent 5c** with checked chapter → Returns refined chapter
8. **Agent 5d** with refined chapter → Returns publication-ready chapter

### Parallel Execution

Agents 1 and 2 can run in parallel since they have no dependencies on each other.

All other agents must run sequentially as each depends on the previous output.

---

## Embedded Methodologies

The following documents have been embedded into agent prompts:

| Document | Embedded In |
|----------|-------------|
| `What_is_Exam_Focus (1).md` | Agent 3 (Planner), Agent 4 (Drafter) |
| `Content Accuracy.md` | Agent 5a |
| `Content Consistency & Flow Check.md` | Agent 5b |
| `Structural Refinement Prompt.md` | Agent 5c |
| `discussion_enhancement (1).md` | Agent 5d |

Agents are self-contained and do not need to reference external documents at runtime.

---

## Version

- **Pipeline Version**: 1.0
- **Created**: December 2024
- **Methodology**: Exam Focus
- **Target**: ADIT Module 1 - Principles of International Taxation
