"""
Logging utilities for the ExamFocus pipeline.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from rich.logging import RichHandler


def setup_logging(
    level: str = "INFO",
    log_file: bool = True,
    log_dir: Path = Path("logs"),
) -> None:
    """Set up logging for the pipeline."""
    # Create log directory
    if log_file:
        log_dir.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    root_logger.handlers = []

    # Console handler with Rich
    console_handler = RichHandler(
        rich_tracebacks=True,
        show_time=True,
        show_path=False,
    )
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    # File handler
    if log_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_handler = logging.FileHandler(
            log_dir / f"pipeline_{timestamp}.log",
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )
        )
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module."""
    return logging.getLogger(name)
