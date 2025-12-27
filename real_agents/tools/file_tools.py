"""
File operation tools for agents.
"""

import asyncio
from pathlib import Path
from typing import Optional
import aiofiles
import glob as glob_module
import re


class FileReader:
    """Tool for reading files."""

    name = "read_file"
    description = "Read the contents of a file"

    async def execute(self, file_path: str) -> str:
        """Read a file and return its contents."""
        path = Path(file_path)
        if not path.exists():
            return f"Error: File not found: {file_path}"

        try:
            async with aiofiles.open(path, "r", encoding="utf-8") as f:
                content = await f.read()
            return content
        except Exception as e:
            return f"Error reading file: {e}"

    def to_claude_tool(self) -> dict:
        """Return Claude tool definition."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The absolute path to the file to read",
                    }
                },
                "required": ["file_path"],
            },
        }


class FileWriter:
    """Tool for writing files."""

    name = "write_file"
    description = "Write content to a file"

    async def execute(self, file_path: str, content: str) -> str:
        """Write content to a file."""
        path = Path(file_path)

        try:
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            async with aiofiles.open(path, "w", encoding="utf-8") as f:
                await f.write(content)
            return f"Successfully wrote {len(content)} characters to {file_path}"
        except Exception as e:
            return f"Error writing file: {e}"

    def to_claude_tool(self) -> dict:
        """Return Claude tool definition."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The absolute path to the file to write",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file",
                    },
                },
                "required": ["file_path", "content"],
            },
        }


class FileSearcher:
    """Tool for searching files using glob and grep patterns."""

    name = "search_files"
    description = "Search for files using glob patterns and optionally grep for content"

    async def glob(self, pattern: str, base_path: str = ".") -> list[str]:
        """Find files matching a glob pattern."""
        base = Path(base_path)
        matches = list(base.glob(pattern))
        return [str(m) for m in matches]

    async def grep(
        self, pattern: str, file_path: str, context_lines: int = 0
    ) -> list[dict]:
        """Search for a regex pattern in a file."""
        path = Path(file_path)
        if not path.exists():
            return []

        results = []
        try:
            async with aiofiles.open(path, "r", encoding="utf-8") as f:
                lines = await f.readlines()

            regex = re.compile(pattern, re.IGNORECASE)
            for i, line in enumerate(lines):
                if regex.search(line):
                    result = {
                        "line_number": i + 1,
                        "line": line.strip(),
                        "file": str(path),
                    }
                    if context_lines > 0:
                        start = max(0, i - context_lines)
                        end = min(len(lines), i + context_lines + 1)
                        result["context"] = [l.strip() for l in lines[start:end]]
                    results.append(result)
        except Exception:
            pass

        return results

    async def execute(
        self,
        glob_pattern: Optional[str] = None,
        grep_pattern: Optional[str] = None,
        base_path: str = ".",
    ) -> dict:
        """Execute file search."""
        result = {"files": [], "matches": []}

        if glob_pattern:
            result["files"] = await self.glob(glob_pattern, base_path)

        if grep_pattern and result["files"]:
            for file_path in result["files"]:
                matches = await self.grep(grep_pattern, file_path)
                result["matches"].extend(matches)

        return result

    def to_claude_tool(self) -> dict:
        """Return Claude tool definition."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "glob_pattern": {
                        "type": "string",
                        "description": "Glob pattern to find files (e.g., '**/*.md')",
                    },
                    "grep_pattern": {
                        "type": "string",
                        "description": "Regex pattern to search within files",
                    },
                    "base_path": {
                        "type": "string",
                        "description": "Base path for search",
                        "default": ".",
                    },
                },
            },
        }
