# ExamFocus Multi-Agent Content Pipeline

A production-ready multi-agent system for creating publication-ready educational content.

## Overview

This pipeline uses 8 specialized AI agents to create comprehensive textbook chapters:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTENT PIPELINE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐                             │
│  │  Agent 1    │    │  Agent 2    │  ← PARALLEL                 │
│  │ Past Paper  │    │  Topic      │                             │
│  │ Analyzer    │    │ Researcher  │                             │
│  └──────┬──────┘    └──────┬──────┘                             │
│         │                  │                                     │
│         └────────┬─────────┘                                     │
│                  ▼                                               │
│         ┌─────────────┐                                          │
│         │  Agent 3    │                                          │
│         │  Chapter    │                                          │
│         │  Planner    │                                          │
│         └──────┬──────┘                                          │
│                ▼                                                 │
│         ┌─────────────┐                                          │
│         │  Agent 4    │                                          │
│         │  Chapter    │                                          │
│         │  Drafter    │                                          │
│         └──────┬──────┘                                          │
│                ▼                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   QA PIPELINE                             │   │
│  │  5a: Accuracy → 5b: Consistency → 5c: Structural → 5d    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

```bash
# Install dependencies
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Configuration

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

Or create a `.env` file:

```
ANTHROPIC_API_KEY=your-api-key
```

## Usage

### Full Pipeline

Create a complete chapter:

```bash
examfocus create "Article 10 Dividends" --chapter 5.3
```

Options:
- `--chapter, -c`: Chapter number (default: "1")
- `--output, -o`: Output directory
- `--skip-qa`: Skip QA agents (for testing)
- `--verbose, -v`: Verbose output

### Single Agent

Run a specific agent:

```bash
# Research agents (no input file needed)
examfocus run-agent 1 "Article 10 Dividends"
examfocus run-agent 2 "Article 10 Dividends"

# QA agents (require input file)
examfocus run-agent 5a "Article 10 Dividends" --input draft.md
```

### Validation

Check configuration:

```bash
examfocus validate
```

### Information

Show pipeline info:

```bash
examfocus info
```

## Agents

| Agent | Name | Model | Purpose |
|-------|------|-------|---------|
| 1 | Past Paper Analyzer | Sonnet | Extract exam intelligence from past papers |
| 2 | Topic Researcher | Sonnet | Research authoritative sources |
| 3 | Chapter Planner | Opus | Create detailed chapter plan |
| 4 | Chapter Drafter | Opus | Write complete chapter |
| 5a | Content Accuracy | Sonnet | Verify factual accuracy |
| 5b | Consistency & Flow | Sonnet | Standardize terminology |
| 5c | Structural Refinement | Haiku | Remove scaffolding |
| 5d | Discussion Enhancement | Opus | Add integrated discussion |

## Programmatic Usage

```python
import asyncio
from real_agents import ContentPipeline

async def main():
    pipeline = ContentPipeline()

    result = await pipeline.run(
        topic="Article 10 Dividends",
        chapter_number="5.3",
    )

    if result.success:
        print(f"Created chapter with {result.word_count} words")
        print(result.final_chapter)
    else:
        print(f"Failed: {result.error}")

asyncio.run(main())
```

### Running Individual Agents

```python
import asyncio
from real_agents.agents import PastPaperAnalyzer, TopicResearcher

async def main():
    # Run agents in parallel
    analyzer = PastPaperAnalyzer()
    researcher = TopicResearcher()

    exam_intel, research = await asyncio.gather(
        analyzer.run(topic="Article 10 Dividends"),
        researcher.run(topic="Article 10 Dividends"),
    )

    print(exam_intel.data.summary())
    print(research.data.summary())

asyncio.run(main())
```

## Architecture

### Project Structure

```
real_agents/
├── __init__.py
├── config.py              # Configuration
├── cli.py                 # CLI interface
├── agents/
│   ├── __init__.py
│   ├── base.py            # Base agent class
│   ├── past_paper_analyzer.py
│   ├── topic_researcher.py
│   ├── chapter_planner.py
│   ├── chapter_drafter.py
│   ├── qa_accuracy.py
│   ├── qa_consistency.py
│   ├── qa_structural.py
│   └── qa_discussion.py
├── models/
│   ├── __init__.py
│   ├── exam_intelligence.py
│   ├── research.py
│   ├── chapter.py
│   └── qa.py
├── pipeline/
│   ├── __init__.py
│   ├── orchestrator.py    # Pipeline orchestration
│   └── quality_gates.py   # Quality checks
├── tools/
│   ├── __init__.py
│   ├── file_tools.py
│   └── web_tools.py
└── utils/
    ├── __init__.py
    ├── parsing.py
    └── logging.py
```

### Key Components

1. **BaseAgent**: Abstract base class for all agents
   - Handles Claude API calls with retry logic
   - Manages tool execution
   - Provides structured output parsing

2. **ContentPipeline**: Orchestrates the full pipeline
   - Runs agents in parallel where possible
   - Manages data flow between agents
   - Applies quality gates

3. **QualityGate**: Validates agent outputs
   - Checks for escalation conditions
   - Tracks quality metrics

## Quality Gates

The pipeline includes automatic quality checks:

- **Accuracy**: Verifies correction counts and accuracy rates
- **Consistency**: Monitors content removal
- **Structural**: Ensures substantive content preservation
- **Discussion**: Validates discussion percentage

Issues trigger:
- **PASSED**: Continue pipeline
- **WARNING**: Log warning, continue
- **ESCALATE**: Require human review

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
ruff check .
```

## License

MIT License
