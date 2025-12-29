# Supervisor Checklist - Quality Pipeline

## Overview

This checklist is used by the supervising prompt (Claude) to verify quality prompt outputs before pushing each chapter.

---

## Pre-Push Verification

### Prompt 5a: Content Accuracy
| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Corrections are factual | Changes fix actual errors, not style preferences | |
| Sources cited | Each correction has authoritative source | |
| Minimal intervention | Only incorrect content changed, not rewritten | |
| Original voice preserved | Author's style maintained | |

### Prompt 5b: Consistency & Flow
| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Terminology standardized | Consistent terms throughout | |
| No content incorrectly removed | Only true redundancies deleted | |
| Cross-references valid | All internal links correct | |
| Contradictions resolved | Conflicts fixed with authority | |

### Prompt 5c: Structural Refinement
| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Only scaffolding removed | Learning objectives, time indicators, etc. | |
| Substantive content preserved | Core material untouched | |
| Worked examples intact | All exam examples remain | |
| Answer frameworks intact | Exam Focus methodology preserved | |

### Prompt 5d: Discussion Enhancement
| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| ~15% discussion achieved | Prose woven throughout | |
| Adds value | Explains WHY, not just WHAT | |
| Voice consistent | Sounds like expert teacher | |
| No existing content changed | Only additions made | |

---

## Overall Quality Gate

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Exam Focus methodology intact | 30-Second Rule still applies | |
| Exam Intelligence box preserved | Statistics and priorities unchanged | |
| Worked examples complete | All solution cycles present | |
| No regressions | Chapter not worse than before | |

---

## Stop Conditions (Escalate to User)

- [ ] Prompt made unexpectedly large changes (>20% of content)
- [ ] Accuracy corrections seem questionable
- [ ] Substantive content was removed
- [ ] Discussion additions don't fit the chapter
- [ ] Multiple quality checks fail

---

## Reporting Template

```
Chapter [X] Complete ([sub-files if any])
├── 5a: [N] corrections made ([types])
├── 5b: [N] terminology fixes, [N] redundancies removed
├── 5c: [N] scaffolding items removed
├── 5d: [N] words of discussion added
├── Quality: ✓ Passed / ✗ Failed [reason]
└── Status: Pushed / Escalated
```

---

## Section Completion Report

```
Part [X] Complete
├── Chapters processed: [N]
├── Total corrections: [N]
├── Total discussion added: [N] words
├── Issues encountered: [list or "None"]
└── Ready for: Part [X+1] / User review
```
