"""
Web operation tools for agents.
"""

import aiohttp
from typing import Optional
import re
from html.parser import HTMLParser


class HTMLToTextParser(HTMLParser):
    """Simple HTML to text converter."""

    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_data = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head"):
            self.skip_data = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self.skip_data = False
        if tag in ("p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6", "li"):
            self.text.append("\n")

    def handle_data(self, data):
        if not self.skip_data:
            self.text.append(data.strip())

    def get_text(self) -> str:
        return " ".join(self.text)


class WebSearcher:
    """
    Tool for web searching.

    Note: This is a placeholder that simulates web search.
    In production, integrate with a real search API (Google, Bing, etc.)
    or use Claude's built-in web search capability.
    """

    name = "web_search"
    description = "Search the web for information"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def execute(self, query: str, num_results: int = 5) -> list[dict]:
        """
        Execute a web search.

        In a real implementation, this would call a search API.
        For now, this returns a placeholder indicating the search was requested.
        """
        # Placeholder - in production, integrate with search API
        return [
            {
                "query": query,
                "note": "Web search requested. In production, integrate with Google/Bing API.",
                "suggested_sources": [
                    "https://www.oecd.org/tax/treaties/",
                    "https://www.un.org/development/desa/financing/tax",
                    "https://www.ibfd.org/",
                ],
            }
        ]

    def to_claude_tool(self) -> dict:
        """Return Claude tool definition."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        }


class WebFetcher:
    """Tool for fetching web pages."""

    name = "web_fetch"
    description = "Fetch and extract content from a URL"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def execute(self, url: str, extract_text: bool = True) -> dict:
        """Fetch a URL and optionally extract text."""
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                headers = {
                    "User-Agent": "Mozilla/5.0 (compatible; ExamFocusBot/1.0)"
                }
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}",
                            "url": url,
                        }

                    content = await response.text()

                    result = {
                        "success": True,
                        "url": url,
                        "status": response.status,
                        "content_type": response.headers.get("Content-Type", ""),
                    }

                    if extract_text and "text/html" in result["content_type"]:
                        parser = HTMLToTextParser()
                        parser.feed(content)
                        result["text"] = parser.get_text()[:10000]  # Limit size
                    else:
                        result["raw_content"] = content[:10000]

                    return result

        except aiohttp.ClientError as e:
            return {"success": False, "error": str(e), "url": url}
        except Exception as e:
            return {"success": False, "error": str(e), "url": url}

    def to_claude_tool(self) -> dict:
        """Return Claude tool definition."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch",
                    },
                    "extract_text": {
                        "type": "boolean",
                        "description": "Whether to extract text from HTML",
                        "default": True,
                    },
                },
                "required": ["url"],
            },
        }
