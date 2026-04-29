# src/domain/value_objects/inference_request.py
from __future__ import annotations
from dataclasses import dataclass, field
from src.domain.entities.message import Message
from src.domain.entities.tool_definition import ToolDefinition


@dataclass
class InferenceRequest:
    messages: list[Message]
    model: str
    temperature: float = 0.7
    max_tokens: int = 2048
    stream: bool = False
    tools: list[ToolDefinition] = field(default_factory=list)
    tool_choice: str = "auto"
    thinking: bool = False
