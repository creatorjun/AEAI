# src/presentation/http/schemas/chat.py
from __future__ import annotations
from pydantic import BaseModel, Field
from uuid import UUID


class ChatRequest(BaseModel):
    conversation_id: UUID | None = None
    message: str = Field(..., min_length=1)
    model: str | None = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1, le=32768)
    system_prompt: str | None = None
    stream: bool = False


class ToolCallSchema(BaseModel):
    id: str
    tool_name: str
    arguments: dict


class UsageSchema(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    conversation_id: UUID
    content: str
    model: str
    usage: UsageSchema
    tool_calls: list[ToolCallSchema] = []
    finish_reason: str
    cached: bool
