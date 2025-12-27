"""
Configuration for the ExamFocus multi-agent pipeline.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ModelConfig:
    """Model configuration for different agent types."""

    # Model IDs
    OPUS: str = "claude-opus-4-5-20250514"
    SONNET: str = "claude-sonnet-4-5-20250514"
    HAIKU: str = "claude-haiku-4-5-20250514"

    # Default parameters
    max_tokens: int = 16000
    temperature: float = 0.7


@dataclass
class PathConfig:
    """Path configuration for the pipeline."""

    base_dir: Path = field(default_factory=lambda: Path("/home/user/ExamFocus"))

    @property
    def past_papers_dir(self) -> Path:
        return self.base_dir / "ADIT/Principles of International Taxation/Past Exam Questions and Answers"

    @property
    def syllabus_csv(self) -> Path:
        return self.base_dir / "ADIT/Principles of International Taxation/PIT_Syllabus_2026_Topics.csv"

    @property
    def methodology_doc(self) -> Path:
        return self.base_dir / "What_is_Exam_Focus_Document.md"

    @property
    def output_dir(self) -> Path:
        return self.base_dir / "output"

    @property
    def chapters_dir(self) -> Path:
        return self.base_dir / "ADIT/Principles of International Taxation"


@dataclass
class PipelineConfig:
    """Main pipeline configuration."""

    models: ModelConfig = field(default_factory=ModelConfig)
    paths: PathConfig = field(default_factory=PathConfig)

    # API Configuration
    api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))

    # Pipeline settings
    parallel_research: bool = True  # Run Agent 1 and 2 in parallel
    max_retries: int = 3
    retry_delay: float = 2.0

    # Quality gates
    max_change_percentage: float = 0.20  # 20% max change for QA agents
    min_accuracy_rate: float = 0.95  # 95% accuracy required

    # Web search settings
    min_searches_researcher: int = 5
    min_searches_accuracy: int = 5
    max_searches_accuracy: int = 20

    def validate(self) -> None:
        """Validate the configuration."""
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required. "
                "Set it in your environment or in a .env file."
            )


# Global config instance
config = PipelineConfig()
