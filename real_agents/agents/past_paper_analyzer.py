"""
Agent 1: Past Paper Analyzer

Analyzes past exam papers to extract comprehensive exam intelligence.
"""

from typing import Optional
import json

from .base import BaseAgent
from ..config import config, ModelConfig
from ..models.exam_intelligence import (
    ExamIntelligence,
    FrequencyData,
    MarkAllocation,
    PartDistribution,
    QuestionPattern,
    WorkedExample,
    ExaminerExpectations,
    TrendDirection,
    QuestionFormat,
)
from ..utils.parsing import extract_json, extract_markdown_sections


class PastPaperAnalyzer(BaseAgent[ExamIntelligence]):
    """
    Agent 1: Past Paper Analyzer

    Searches all available past exam papers to extract:
    - Frequency analysis
    - Mark allocations
    - Question patterns
    - Worked example candidates
    - Examiner expectations
    """

    name = "Agent 1: Past Paper Analyzer"
    description = "Extracts exam intelligence from past papers"
    model = ModelConfig.SONNET
    tools = ["read", "search"]

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.past_papers_dir = config.paths.past_papers_dir

    def get_system_prompt(self) -> str:
        return """You are the PAST PAPER ANALYZER. Analyze all available past exam papers to extract comprehensive exam intelligence for the specified topic.

## MANDATORY PROTOCOL

### ENFORCEMENT RULES (NON-NEGOTIABLE)
1. You MUST search ALL available past papers—do not stop at first few
2. You MUST use EXACT question text—do not paraphrase
3. You MUST count precisely—verify statistics
4. You MUST include only factual observations from papers
5. You MUST state clearly if topic does not appear in past papers
6. If data is unavailable (e.g., pass rates), state "Not available" rather than omit

## WHAT TO EXTRACT

### 1. Frequency Analysis
- Count appearances out of total papers available
- Calculate percentage
- List specific exam sittings (e.g., June 2022, Dec 2023)
- Note trend: Increasing / Stable / Decreasing

### 2. Mark Allocation
- Range (min-max marks)
- Average marks
- Format: Full question / Sub-part / Both

### 3. Question Patterns
- Part A (Theory) vs Part B (Scenario) distribution
- Common trigger words examiners use
- Typical question structures
- How topic combines with other topics

### 4. Question Evolution
- How examiners have modified this question type over years
- New angles or variations introduced recently

### 5. Worked Example Candidates
Select based on frequency tier:
| Frequency | Examples to Select |
|-----------|-------------------|
| 80%+ | 5-8 showing pattern variations |
| 50-79% | 3-5 showing common patterns |
| 25-49% | 2-3 showing basic patterns |
| <25% | 1-2 showing core patterns |

### 6. Examiner Expectations
From suggested solutions, identify:
- What examiners reward
- Expected answer frameworks
- Common candidate errors noted

## OUTPUT FORMAT

You MUST output valid JSON in the following structure:

```json
{
  "topic": "string",
  "frequency": {
    "appearances": number,
    "total_papers": number,
    "percentage": number,
    "sittings": ["string"],
    "trend": "increasing|stable|decreasing"
  },
  "marks": {
    "range_min": number,
    "range_max": number,
    "average": number,
    "format": "full_question|sub_part|both"
  },
  "part_distribution": {
    "part_a": number,
    "part_b": number,
    "combined": number
  },
  "patterns": [
    {
      "name": "string",
      "trigger_words": ["string"],
      "structure": "string",
      "example_reference": "string"
    }
  ],
  "question_evolution": "string",
  "worked_examples": [
    {
      "exam_sitting": "string",
      "marks": number,
      "question_text": "string (verbatim)",
      "aspects_tested": ["string"],
      "selection_rationale": "string"
    }
  ],
  "examiner_expectations": {
    "rewards": ["string"],
    "frameworks": ["string"],
    "common_errors": ["string"]
  },
  "pass_rate": "string or null",
  "strategic_priority": number (1-5),
  "priority_rationale": "string"
}
```

Use the search_files tool to find and read all past papers, then analyze them thoroughly."""

    def format_input(self, topic: str) -> str:
        return f"""Analyze all past exam papers for the topic: **{topic}**

Search directory: {self.past_papers_dir}

Use the search_files tool with glob pattern "**/*.md" or "**/*.pdf" to find all past papers.
Then read each file and extract exam intelligence for this topic.

Remember:
- Search ALL available papers
- Use EXACT question text (verbatim)
- Count precisely and verify statistics
- If the topic doesn't appear, state that clearly

Output your analysis as JSON in the specified format."""

    def parse_output(self, response: str) -> ExamIntelligence:
        """Parse the agent's response into ExamIntelligence."""
        # Try to extract JSON
        data = extract_json(response)

        if not data:
            # Return a minimal result if parsing fails
            return ExamIntelligence(
                topic="Unknown",
                frequency=FrequencyData(
                    appearances=0,
                    total_papers=0,
                    percentage=0.0,
                    sittings=[],
                    trend=TrendDirection.STABLE,
                ),
                marks=MarkAllocation(
                    range_min=0,
                    range_max=0,
                    average=0.0,
                    format=QuestionFormat.BOTH,
                ),
                part_distribution=PartDistribution(),
                patterns=[],
                worked_examples=[],
                strategic_priority=3,
                priority_rationale="Could not parse exam intelligence",
            )

        # Parse frequency
        freq_data = data.get("frequency", {})
        frequency = FrequencyData(
            appearances=freq_data.get("appearances", 0),
            total_papers=freq_data.get("total_papers", 0),
            percentage=freq_data.get("percentage", 0.0),
            sittings=freq_data.get("sittings", []),
            trend=TrendDirection(freq_data.get("trend", "stable")),
        )

        # Parse marks
        marks_data = data.get("marks", {})
        marks = MarkAllocation(
            range_min=marks_data.get("range_min", 0),
            range_max=marks_data.get("range_max", 0),
            average=marks_data.get("average", 0.0),
            format=QuestionFormat(marks_data.get("format", "both")),
        )

        # Parse part distribution
        dist_data = data.get("part_distribution", {})
        part_distribution = PartDistribution(
            part_a=dist_data.get("part_a", 0),
            part_b=dist_data.get("part_b", 0),
            combined=dist_data.get("combined", 0),
        )

        # Parse patterns
        patterns = [
            QuestionPattern(**p) for p in data.get("patterns", [])
        ]

        # Parse worked examples
        worked_examples = [
            WorkedExample(**w) for w in data.get("worked_examples", [])
        ]

        # Parse examiner expectations
        exp_data = data.get("examiner_expectations", {})
        examiner_expectations = ExaminerExpectations(
            rewards=exp_data.get("rewards", []),
            frameworks=exp_data.get("frameworks", []),
            common_errors=exp_data.get("common_errors", []),
        )

        return ExamIntelligence(
            topic=data.get("topic", "Unknown"),
            frequency=frequency,
            marks=marks,
            part_distribution=part_distribution,
            patterns=patterns,
            question_evolution=data.get("question_evolution", ""),
            worked_examples=worked_examples,
            examiner_expectations=examiner_expectations,
            pass_rate=data.get("pass_rate"),
            strategic_priority=data.get("strategic_priority", 3),
            priority_rationale=data.get("priority_rationale", ""),
        )
