"""
Command-line interface for the ExamFocus multi-agent pipeline.
"""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from .config import config
from .pipeline import ContentPipeline
from .utils.logging import setup_logging

app = typer.Typer(
    name="examfocus",
    help="ExamFocus Multi-Agent Content Pipeline",
    add_completion=False,
)

console = Console()


@app.command()
def create(
    topic: str = typer.Argument(..., help="Topic name to create content for"),
    chapter: str = typer.Option("1", "--chapter", "-c", help="Chapter number"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output directory"),
    skip_qa: bool = typer.Option(False, "--skip-qa", help="Skip QA agents"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Create a new chapter using the full pipeline.

    Example:
        examfocus create "Article 10 Dividends" --chapter 5.3
    """
    setup_logging(level="DEBUG" if verbose else "INFO")

    try:
        config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration error: {e}[/red]")
        raise typer.Exit(1)

    console.print(Panel(
        f"[bold]Creating chapter for:[/bold] {topic}\n"
        f"[bold]Chapter:[/bold] {chapter}",
        title="ExamFocus Pipeline",
    ))

    pipeline = ContentPipeline()

    result = asyncio.run(
        pipeline.run(
            topic=topic,
            chapter_number=chapter,
            output_dir=output or config.paths.output_dir,
            skip_qa=skip_qa,
        )
    )

    if result.success:
        console.print(f"\n[green]✓ Chapter created successfully![/green]")
        console.print(f"Word count: {result.word_count}")
        console.print(f"Tokens used: {result.total_tokens}")
        console.print(f"Time: {result.total_time:.1f}s")
    else:
        console.print(f"\n[red]✗ Pipeline failed: {result.error}[/red]")
        raise typer.Exit(1)


@app.command()
def run_agent(
    agent: str = typer.Argument(..., help="Agent to run (1, 2, 3, 4, 5a, 5b, 5c, 5d)"),
    topic: str = typer.Argument(..., help="Topic name"),
    input_file: Optional[Path] = typer.Option(None, "--input", "-i", help="Input file"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Run a single agent independently.

    Example:
        examfocus run-agent 1 "Article 10 Dividends"
        examfocus run-agent 5a "Article 10 Dividends" --input draft.md
    """
    from .agents import (
        PastPaperAnalyzer,
        TopicResearcher,
        ChapterPlanner,
        ChapterDrafter,
        ContentAccuracyVerifier,
        ConsistencyFlowChecker,
        StructuralRefinement,
        DiscussionEnhancement,
    )

    setup_logging(level="DEBUG" if verbose else "INFO")

    try:
        config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration error: {e}[/red]")
        raise typer.Exit(1)

    agent_map = {
        "1": PastPaperAnalyzer,
        "2": TopicResearcher,
        "3": ChapterPlanner,
        "4": ChapterDrafter,
        "5a": ContentAccuracyVerifier,
        "5b": ConsistencyFlowChecker,
        "5c": StructuralRefinement,
        "5d": DiscussionEnhancement,
    }

    if agent not in agent_map:
        console.print(f"[red]Unknown agent: {agent}. Valid: {list(agent_map.keys())}[/red]")
        raise typer.Exit(1)

    agent_instance = agent_map[agent]()

    # Prepare input based on agent
    kwargs = {"topic": topic}

    if agent in ["5a", "5b", "5c", "5d"]:
        if not input_file:
            console.print(f"[red]Agent {agent} requires --input file[/red]")
            raise typer.Exit(1)
        kwargs["chapter_content"] = input_file.read_text()

    console.print(f"[bold]Running Agent {agent}[/bold] on topic: {topic}")

    result = asyncio.run(agent_instance.run(**kwargs))

    if result.success:
        console.print(f"[green]✓ Agent {agent} completed successfully![/green]")
        console.print(f"Tokens used: {result.tokens_used}")
        console.print(f"Time: {result.execution_time:.1f}s")

        if output_file and hasattr(result.data, "content"):
            output_file.write_text(result.data.content)
            console.print(f"Saved to: {output_file}")
    else:
        console.print(f"[red]✗ Agent {agent} failed: {result.error}[/red]")
        raise typer.Exit(1)


@app.command()
def validate():
    """
    Validate configuration and connectivity.
    """
    console.print("[bold]Validating configuration...[/bold]\n")

    # Check API key
    try:
        config.validate()
        console.print("[green]✓[/green] API key configured")
    except ValueError as e:
        console.print(f"[red]✗[/red] {e}")
        raise typer.Exit(1)

    # Check paths
    if config.paths.past_papers_dir.exists():
        console.print(f"[green]✓[/green] Past papers directory exists")
    else:
        console.print(f"[yellow]⚠[/yellow] Past papers directory not found: {config.paths.past_papers_dir}")

    if config.paths.syllabus_csv.exists():
        console.print(f"[green]✓[/green] Syllabus CSV exists")
    else:
        console.print(f"[yellow]⚠[/yellow] Syllabus CSV not found: {config.paths.syllabus_csv}")

    # Test API connectivity
    console.print("\n[bold]Testing API connectivity...[/bold]")

    from anthropic import Anthropic

    try:
        client = Anthropic(api_key=config.api_key)
        response = client.messages.create(
            model="claude-haiku-4-5-20250514",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hello"}],
        )
        console.print("[green]✓[/green] API connection successful")
    except Exception as e:
        console.print(f"[red]✗[/red] API connection failed: {e}")
        raise typer.Exit(1)

    console.print("\n[green]All checks passed![/green]")


@app.command()
def info():
    """
    Show pipeline information and agent details.
    """
    from rich.table import Table

    console.print(Panel(
        "[bold]ExamFocus Multi-Agent Content Pipeline[/bold]\n\n"
        "An 8-agent pipeline for creating publication-ready\n"
        "educational content based on exam analysis.",
        title="About",
    ))

    table = Table(title="Agent Overview")
    table.add_column("Agent", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Model")
    table.add_column("Purpose")

    agents = [
        ("1", "Past Paper Analyzer", "Sonnet", "Extract exam intelligence"),
        ("2", "Topic Researcher", "Sonnet", "Research authoritative sources"),
        ("3", "Chapter Planner", "Opus", "Create detailed chapter plan"),
        ("4", "Chapter Drafter", "Opus", "Write complete chapter"),
        ("5a", "Content Accuracy", "Sonnet", "Verify factual accuracy"),
        ("5b", "Consistency & Flow", "Sonnet", "Standardize terminology"),
        ("5c", "Structural Refinement", "Haiku", "Remove scaffolding"),
        ("5d", "Discussion Enhancement", "Opus", "Add integrated discussion"),
    ]

    for agent in agents:
        table.add_row(*agent)

    console.print(table)

    console.print("\n[bold]Pipeline Flow:[/bold]")
    console.print("  1 + 2 (parallel) → 3 → 4 → 5a → 5b → 5c → 5d → Final Chapter")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
