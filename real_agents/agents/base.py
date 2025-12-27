"""
Base agent class for the ExamFocus pipeline.
"""

import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, Optional, TypeVar
from datetime import datetime

from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from rich.console import Console
from rich.panel import Panel

from ..config import config, ModelConfig

console = Console()

# Generic type for agent output
T = TypeVar("T")


@dataclass
class AgentOutput(Generic[T]):
    """Standard output wrapper for all agents."""

    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    execution_time: float = 0.0
    tokens_used: int = 0

    def __post_init__(self):
        self.metadata["timestamp"] = datetime.now().isoformat()


class BaseAgent(ABC, Generic[T]):
    """
    Base class for all agents in the ExamFocus pipeline.

    Each agent:
    - Has a specific role and model assignment
    - Has access to specific tools
    - Produces structured output
    - Can be run autonomously
    """

    # Override in subclasses
    name: str = "base_agent"
    description: str = "Base agent"
    model: str = ModelConfig.SONNET
    tools: list = []

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the agent."""
        self.api_key = api_key or config.api_key
        self.client = AsyncAnthropic(api_key=self.api_key)
        self._tool_instances = {}
        self._init_tools()

    def _init_tools(self):
        """Initialize tool instances."""
        from ..tools import FileReader, FileWriter, FileSearcher, WebSearcher, WebFetcher

        tool_map = {
            "read": FileReader(),
            "write": FileWriter(),
            "search": FileSearcher(),
            "web_search": WebSearcher(),
            "web_fetch": WebFetcher(),
        }
        for tool_name in self.tools:
            if tool_name in tool_map:
                self._tool_instances[tool_name] = tool_map[tool_name]

    def get_claude_tools(self) -> list[dict]:
        """Get tool definitions for Claude API."""
        return [tool.to_claude_tool() for tool in self._tool_instances.values()]

    async def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool and return the result."""
        # Map Claude tool names to our tools
        tool_name_map = {
            "read_file": "read",
            "write_file": "write",
            "search_files": "search",
            "web_search": "web_search",
            "web_fetch": "web_fetch",
        }

        internal_name = tool_name_map.get(tool_name, tool_name)
        tool = self._tool_instances.get(internal_name)

        if not tool:
            return f"Error: Unknown tool {tool_name}"

        try:
            result = await tool.execute(**tool_input)
            if isinstance(result, dict):
                return json.dumps(result, indent=2)
            return str(result)
        except Exception as e:
            return f"Error executing tool: {e}"

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    @abstractmethod
    def format_input(self, **kwargs) -> str:
        """Format the input for this agent."""
        pass

    @abstractmethod
    def parse_output(self, response: str) -> T:
        """Parse the agent's response into structured output."""
        pass

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def _call_claude(self, messages: list[dict]) -> tuple[str, int]:
        """Call Claude API with retry logic."""
        tools = self.get_claude_tools() if self._tool_instances else None

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=config.models.max_tokens,
            system=self.get_system_prompt(),
            messages=messages,
            tools=tools,
        )

        # Handle tool use
        while response.stop_reason == "tool_use":
            tool_results = []
            for content in response.content:
                if content.type == "tool_use":
                    console.print(f"  [dim]Using tool: {content.name}[/dim]")
                    result = await self.execute_tool(content.name, content.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result,
                        }
                    )

            # Continue conversation with tool results
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            response = await self.client.messages.create(
                model=self.model,
                max_tokens=config.models.max_tokens,
                system=self.get_system_prompt(),
                messages=messages,
                tools=tools,
            )

        # Extract text response
        text_response = ""
        for content in response.content:
            if hasattr(content, "text"):
                text_response += content.text

        tokens = response.usage.input_tokens + response.usage.output_tokens
        return text_response, tokens

    async def run(self, **kwargs) -> AgentOutput[T]:
        """
        Run the agent with the given inputs.

        Returns an AgentOutput containing the structured result.
        """
        start_time = asyncio.get_event_loop().time()

        console.print(Panel(f"[bold blue]{self.name}[/bold blue] starting...", expand=False))

        try:
            # Format input
            user_message = self.format_input(**kwargs)

            # Call Claude
            messages = [{"role": "user", "content": user_message}]
            response, tokens = await self._call_claude(messages)

            # Parse output
            parsed = self.parse_output(response)

            execution_time = asyncio.get_event_loop().time() - start_time

            console.print(
                f"[green]✓[/green] {self.name} completed in {execution_time:.1f}s "
                f"({tokens} tokens)"
            )

            return AgentOutput(
                success=True,
                data=parsed,
                execution_time=execution_time,
                tokens_used=tokens,
            )

        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            console.print(f"[red]✗[/red] {self.name} failed: {e}")

            return AgentOutput(
                success=False,
                error=str(e),
                execution_time=execution_time,
            )
