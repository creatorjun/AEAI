# src/infrastructure/tools/in_memory_tool_registry.py
from __future__ import annotations
from collections.abc import Callable, Awaitable
from typing import Any
from src.application.ports.tool_registry import ToolRegistry
from src.domain.entities.tool_definition import ToolDefinition
from src.domain.errors.domain_errors import ToolNotFoundError


class InMemoryToolRegistry(ToolRegistry):
    def __init__(self) -> None:
        self._definitions: dict[str, ToolDefinition] = {}
        self._handlers: dict[str, Callable[..., Awaitable[Any]]] = {}

    def register(
        self,
        definition: ToolDefinition,
        handler: Callable[..., Awaitable[Any]],
    ) -> None:
        self._definitions[definition.name] = definition
        self._handlers[definition.name] = handler

    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        if tool_name not in self._handlers:
            raise ToolNotFoundError(tool_name)
        return await self._handlers[tool_name](**arguments)

    def list_definitions(self) -> list[ToolDefinition]:
        return list(self._definitions.values())
