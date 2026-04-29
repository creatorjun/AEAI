# src/domain/entities/tool_call.py
from __future__ import annotations
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Any


@dataclass
class ToolCall:
    tool_name: str
    arguments: dict[str, Any]
    id: str = field(default_factory=lambda: str(uuid4()))
    result: Any | None = None
    error: str | None = None

    @property
    def is_completed(self) -> bool:
        return self.result is not None or self.error is not None
