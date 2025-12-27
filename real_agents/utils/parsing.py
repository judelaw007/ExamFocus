"""
Parsing utilities for agent outputs.
"""

import re
import json
from typing import Any, Optional


def extract_json(text: str) -> Optional[dict]:
    """
    Extract JSON from text that may contain markdown code blocks.
    """
    # Try to find JSON in code blocks first
    json_patterns = [
        r"```json\s*([\s\S]*?)\s*```",
        r"```\s*([\s\S]*?)\s*```",
        r"\{[\s\S]*\}",
    ]

    for pattern in json_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                json_str = match.group(1) if match.lastindex else match.group(0)
                return json.loads(json_str)
            except json.JSONDecodeError:
                continue

    return None


def extract_markdown_sections(text: str) -> dict[str, str]:
    """
    Extract sections from markdown text by headers.
    Returns a dict mapping header names to content.
    """
    sections = {}
    current_header = None
    current_content = []

    lines = text.split("\n")
    for line in lines:
        # Check for headers (## or ###)
        header_match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if header_match:
            # Save previous section
            if current_header:
                sections[current_header] = "\n".join(current_content).strip()

            current_header = header_match.group(2).strip()
            current_content = []
        else:
            current_content.append(line)

    # Save last section
    if current_header:
        sections[current_header] = "\n".join(current_content).strip()

    return sections


def count_words(text: str) -> int:
    """Count words in text, excluding markdown syntax."""
    # Remove markdown syntax
    text = re.sub(r"```[\s\S]*?```", "", text)  # Code blocks
    text = re.sub(r"`[^`]+`", "", text)  # Inline code
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # Links
    text = re.sub(r"[#*_~>`|]", "", text)  # Markdown characters
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace

    return len(text.split())


def extract_table_data(text: str) -> list[dict]:
    """
    Extract data from markdown tables.
    Returns list of dicts with column headers as keys.
    """
    tables = []
    lines = text.split("\n")

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check if this looks like a table header
        if "|" in line and not line.startswith("|--"):
            headers = [h.strip() for h in line.split("|") if h.strip()]

            # Check for separator line
            if i + 1 < len(lines) and re.match(r"^\|?[\s\-:|]+\|?$", lines[i + 1]):
                i += 2  # Skip separator

                # Read data rows
                table_data = []
                while i < len(lines) and "|" in lines[i]:
                    row_line = lines[i].strip()
                    if row_line.startswith("|--") or not row_line:
                        break
                    values = [v.strip() for v in row_line.split("|") if v.strip()]
                    if len(values) == len(headers):
                        table_data.append(dict(zip(headers, values)))
                    i += 1

                if table_data:
                    tables.extend(table_data)
                continue

        i += 1

    return tables
