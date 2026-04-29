# src/application/ports/tool_registry.py
from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Callable, Awaitable
from typing import Any
from src.domain.entities.tool_definition import ToolDefinition


class ToolRegistry(ABC):
    @abstractmethod
    def register(
        self,
        definition: ToolDefinition,
        handler: Callable[..., Awaitable[Any]],
    ) -> None:
        ...

    @abstractmethod
    async def execute(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        ...

    @abstractmethod
    def list_definitions(self) -> list[ToolDefinition]:
        ...
