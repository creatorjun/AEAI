# src/infrastructure/llm/common/message_converter.py
from __future__ import annotations
from src.domain.entities.message import Message
from src.domain.value_objects.role import Role


def to_openai_messages(messages: list[Message]) -> list[dict]:
    result: list[dict] = []
    for m in messages:
        entry: dict = {"role": m.role, "content": m.content}
        if m.tool_calls:
            entry["tool_calls"] = m.tool_calls
        if m.tool_call_id:
            entry["tool_call_id"] = m.tool_call_id
        result.append(entry)
    return result
