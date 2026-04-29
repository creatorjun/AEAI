# src/domain/entities/message.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from src.domain.value_objects.role import Role


@dataclass
class Message:
    role: Role
    content: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tool_call_id: str | None = None
    tool_calls: list[dict] | None = None
