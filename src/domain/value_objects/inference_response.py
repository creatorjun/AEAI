# src/domain/value_objects/inference_response.py
from __future__ import annotations
from dataclasses import dataclass, field
from src.domain.entities.tool_call import ToolCall


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass
class InferenceResponse:
    content: str
    model: str
    usage: Usage
    tool_calls: list[ToolCall] = field(default_factory=list)
    thinking: str | None = None
    finish_reason: str = "stop"
    cached: bool = False
