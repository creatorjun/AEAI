# src/infrastructure/llm/common/stream_normalizer.py
from __future__ import annotations
import json


def parse_sse_chunk(raw: str) -> str | None:
    for line in raw.splitlines():
        if line.startswith("data: "):
            data = line[6:].strip()
            if data == "[DONE]":
                return None
            try:
                payload = json.loads(data)
                delta = payload["choices"][0]["delta"]
                return delta.get("content", "")
            except Exception:
                return None
    return None
