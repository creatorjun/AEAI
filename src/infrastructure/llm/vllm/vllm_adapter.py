# src/infrastructure/llm/vllm/vllm_adapter.py
from __future__ import annotations
import httpx
from collections.abc import AsyncIterator
from src.application.ports.llm_gateway import LlmGateway
from src.domain.value_objects.inference_request import InferenceRequest
from src.domain.value_objects.inference_response import InferenceResponse, Usage
from src.domain.entities.tool_call import ToolCall
from src.domain.errors.domain_errors import InferenceError
from src.infrastructure.llm.common.message_converter import to_openai_messages
from src.infrastructure.llm.common.stream_normalizer import parse_sse_chunk


class VllmAdapter(LlmGateway):
    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 120.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def complete(self, request: InferenceRequest) -> InferenceResponse:
        payload = self._build_payload(request, stream=False)
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                resp = await client.post(f"{self._base_url}/v1/chat/completions", json=payload)
                resp.raise_for_status()
            except httpx.HTTPError as e:
                raise InferenceError(str(e)) from e
        data = resp.json()
        choice = data["choices"][0]
        message = choice["message"]
        tool_calls = self._parse_tool_calls(message.get("tool_calls"))
        usage_data = data.get("usage", {})
        return InferenceResponse(
            content=message.get("content") or "",
            model=data.get("model", request.model),
            usage=Usage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
            ),
            tool_calls=tool_calls,
            finish_reason=choice.get("finish_reason", "stop"),
        )

    async def stream(self, request: InferenceRequest) -> AsyncIterator[str]:
        payload = self._build_payload(request, stream=True)
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            async with client.stream(
                "POST", f"{self._base_url}/v1/chat/completions", json=payload
            ) as resp:
                async for line in resp.aiter_lines():
                    chunk = parse_sse_chunk(line)
                    if chunk is not None:
                        yield chunk

    def _build_payload(self, request: InferenceRequest, stream: bool) -> dict:
        payload: dict = {
            "model": request.model,
            "messages": to_openai_messages(request.messages),
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": stream,
        }
        if request.tools:
            payload["tools"] = [t.to_openai_schema() for t in request.tools]
            payload["tool_choice"] = request.tool_choice
        return payload

    @staticmethod
    def _parse_tool_calls(raw: list[dict] | None) -> list[ToolCall]:
        if not raw:
            return []
        result: list[ToolCall] = []
        for item in raw:
            fn = item.get("function", {})
            import json
            try:
                args = json.loads(fn.get("arguments", "{}"))
            except Exception:
                args = {}
            result.append(ToolCall(tool_name=fn.get("name", ""), arguments=args, id=item.get("id", "")))
        return result
