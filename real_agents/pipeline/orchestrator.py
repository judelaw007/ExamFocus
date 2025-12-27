"""
Pipeline Orchestrator for the ExamFocus multi-agent system.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import json

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from ..config import config
from ..agents import (
    PastPaperAnalyzer,
    TopicResearcher,
    ChapterPlanner,
    ChapterDrafter,
    ContentAccuracyVerifier,
    ConsistencyFlowChecker,
    StructuralRefinement,
    DiscussionEnhancement,
)
from ..models.exam_intelligence import ExamIntelligence
from ..models.research import ResearchReport
from ..models.chapter import ChapterPlan, ChapterDraft
from .quality_gates import QualityGate, QualityCheckResult, QualityStatus

console = Console()


@dataclass
class PipelineResult:
    """Result of a full pipeline run."""

    success: bool
    topic: str
    chapter_number: str
    final_chapter: Optional[str] = None
    word_count: int = 0
    total_tokens: int = 0
    total_time: float = 0.0
    quality_checks: list[QualityCheckResult] = field(default_factory=list)
    error: Optional[str] = None

    def summary(self) -> str:
        status = "✓ SUCCESS" if self.success else "✗ FAILED"
        return f"""
Pipeline Result: {status}
Topic: {self.topic}
Chapter: {self.chapter_number}
Word Count: {self.word_count}
Total Tokens: {self.total_tokens}
Total Time: {self.total_time:.1f}s
Quality: {len([q for q in self.quality_checks if q.status == QualityStatus.PASSED])}/{len(self.quality_checks)} passed
"""


class ContentPipeline:
    """
    Orchestrates the full content creation pipeline.

    Pipeline:
    1. Agent 1 (Past Paper) + Agent 2 (Researcher) - PARALLEL
    2. Agent 3 (Planner) - uses outputs from 1 & 2
    3. Agent 4 (Drafter) - uses plan from 3
    4. Agent 5a (Accuracy) - QA
    5. Agent 5b (Consistency) - QA
    6. Agent 5c (Structural) - QA
    7. Agent 5d (Discussion) - QA
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the pipeline with all agents."""
        self.api_key = api_key or config.api_key
        self.quality_gate = QualityGate()

        # Initialize agents
        self.past_paper_analyzer = PastPaperAnalyzer(self.api_key)
        self.topic_researcher = TopicResearcher(self.api_key)
        self.chapter_planner = ChapterPlanner(self.api_key)
        self.chapter_drafter = ChapterDrafter(self.api_key)
        self.accuracy_verifier = ContentAccuracyVerifier(self.api_key)
        self.consistency_checker = ConsistencyFlowChecker(self.api_key)
        self.structural_refiner = StructuralRefinement(self.api_key)
        self.discussion_enhancer = DiscussionEnhancement(self.api_key)

    async def run(
        self,
        topic: str,
        chapter_number: str = "1",
        output_dir: Optional[Path] = None,
        skip_qa: bool = False,
    ) -> PipelineResult:
        """
        Run the full content creation pipeline.

        Args:
            topic: The topic to create content for
            chapter_number: Chapter number
            output_dir: Directory to save outputs
            skip_qa: Skip QA agents (for testing)

        Returns:
            PipelineResult with the final chapter and metadata
        """
        start_time = asyncio.get_event_loop().time()
        total_tokens = 0
        quality_checks = []

        console.print(Panel(
            f"[bold green]Starting Content Pipeline[/bold green]\n"
            f"Topic: {topic}\n"
            f"Chapter: {chapter_number}",
            title="ExamFocus Pipeline",
        ))

        try:
            # Phase 1: Research (Parallel)
            console.print("\n[bold]Phase 1: Research[/bold] (Agents 1 & 2 in parallel)")

            exam_intel_task = self.past_paper_analyzer.run(topic=topic)
            research_task = self.topic_researcher.run(topic=topic)

            exam_intel_result, research_result = await asyncio.gather(
                exam_intel_task, research_task
            )

            if not exam_intel_result.success:
                raise Exception(f"Agent 1 failed: {exam_intel_result.error}")
            if not research_result.success:
                raise Exception(f"Agent 2 failed: {research_result.error}")

            exam_intel = exam_intel_result.data
            research = research_result.data
            total_tokens += exam_intel_result.tokens_used + research_result.tokens_used

            # Phase 2: Planning
            console.print("\n[bold]Phase 2: Planning[/bold] (Agent 3)")

            plan_result = await self.chapter_planner.run(
                topic=topic,
                chapter_number=chapter_number,
                exam_intelligence=exam_intel,
                research=research,
            )

            if not plan_result.success:
                raise Exception(f"Agent 3 failed: {plan_result.error}")

            chapter_plan = plan_result.data
            total_tokens += plan_result.tokens_used

            # Phase 3: Drafting
            console.print("\n[bold]Phase 3: Drafting[/bold] (Agent 4)")

            draft_result = await self.chapter_drafter.run(
                topic=topic,
                chapter_plan=chapter_plan,
                exam_intelligence=exam_intel,
                research=research,
            )

            if not draft_result.success:
                raise Exception(f"Agent 4 failed: {draft_result.error}")

            chapter_draft = draft_result.data
            total_tokens += draft_result.tokens_used

            current_content = chapter_draft.content
            original_word_count = chapter_draft.word_count

            # Phase 4: Quality Assurance
            if not skip_qa:
                console.print("\n[bold]Phase 4: Quality Assurance[/bold] (Agents 5a-5d)")

                # Agent 5a: Accuracy
                accuracy_result = await self.accuracy_verifier.run(
                    chapter_content=current_content,
                    topic=topic,
                )
                if accuracy_result.success:
                    qa_check = self.quality_gate.check_accuracy(
                        accuracy_result.data, original_word_count
                    )
                    quality_checks.append(qa_check)
                    self._print_quality_check(qa_check)
                    current_content = accuracy_result.data.corrected_chapter
                    total_tokens += accuracy_result.tokens_used

                # Agent 5b: Consistency
                consistency_result = await self.consistency_checker.run(
                    chapter_content=current_content,
                    topic=topic,
                )
                if consistency_result.success:
                    qa_check = self.quality_gate.check_consistency(consistency_result.data)
                    quality_checks.append(qa_check)
                    self._print_quality_check(qa_check)
                    current_content = consistency_result.data.corrected_chapter
                    total_tokens += consistency_result.tokens_used

                # Agent 5c: Structural
                structural_result = await self.structural_refiner.run(
                    chapter_content=current_content,
                    topic=topic,
                )
                if structural_result.success:
                    qa_check = self.quality_gate.check_structural(structural_result.data)
                    quality_checks.append(qa_check)
                    self._print_quality_check(qa_check)
                    current_content = structural_result.data.refined_chapter
                    total_tokens += structural_result.tokens_used

                # Agent 5d: Discussion
                discussion_result = await self.discussion_enhancer.run(
                    chapter_content=current_content,
                    topic=topic,
                )
                if discussion_result.success:
                    qa_check = self.quality_gate.check_discussion(discussion_result.data)
                    quality_checks.append(qa_check)
                    self._print_quality_check(qa_check)
                    current_content = discussion_result.data.enhanced_chapter
                    total_tokens += discussion_result.tokens_used

                # Overall quality check
                overall = self.quality_gate.overall_check(*[
                    q for q in quality_checks
                ])
                quality_checks.append(overall)

                if overall.status == QualityStatus.ESCALATE:
                    console.print(f"[red]⚠ Quality escalation: {overall.message}[/red]")

            # Calculate final word count
            from ..utils.parsing import count_words
            final_word_count = count_words(current_content)

            # Save output
            if output_dir:
                output_dir = Path(output_dir)
                output_dir.mkdir(parents=True, exist_ok=True)

                output_file = output_dir / f"chapter_{chapter_number}_{topic.replace(' ', '_')}.md"
                output_file.write_text(current_content)
                console.print(f"\n[green]✓ Saved to {output_file}[/green]")

            total_time = asyncio.get_event_loop().time() - start_time

            result = PipelineResult(
                success=True,
                topic=topic,
                chapter_number=chapter_number,
                final_chapter=current_content,
                word_count=final_word_count,
                total_tokens=total_tokens,
                total_time=total_time,
                quality_checks=quality_checks,
            )

            self._print_summary(result)
            return result

        except Exception as e:
            total_time = asyncio.get_event_loop().time() - start_time
            console.print(f"[red]Pipeline failed: {e}[/red]")

            return PipelineResult(
                success=False,
                topic=topic,
                chapter_number=chapter_number,
                total_tokens=total_tokens,
                total_time=total_time,
                quality_checks=quality_checks,
                error=str(e),
            )

    def _print_quality_check(self, check: QualityCheckResult) -> None:
        """Print a quality check result."""
        status_icons = {
            QualityStatus.PASSED: "[green]✓[/green]",
            QualityStatus.WARNING: "[yellow]⚠[/yellow]",
            QualityStatus.FAILED: "[red]✗[/red]",
            QualityStatus.ESCALATE: "[red]⚠[/red]",
        }
        icon = status_icons.get(check.status, "?")
        console.print(f"  {icon} Agent {check.agent}: {check.message}")

    def _print_summary(self, result: PipelineResult) -> None:
        """Print pipeline summary."""
        table = Table(title="Pipeline Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Topic", result.topic)
        table.add_row("Chapter", result.chapter_number)
        table.add_row("Word Count", str(result.word_count))
        table.add_row("Total Tokens", str(result.total_tokens))
        table.add_row("Total Time", f"{result.total_time:.1f}s")

        passed = len([q for q in result.quality_checks if q.status == QualityStatus.PASSED])
        table.add_row("Quality Checks", f"{passed}/{len(result.quality_checks)} passed")

        console.print(table)
