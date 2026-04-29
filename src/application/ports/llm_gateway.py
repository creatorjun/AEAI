# src/application/ports/llm_gateway.py
from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from src.domain.value_objects.inference_request import InferenceRequest
from src.domain.value_objects.inference_response import InferenceResponse


class LlmGateway(ABC):
    @abstractmethod
    async def complete(self, request: InferenceRequest) -> InferenceResponse:
        ...

    @abstractmethod
    async def stream(self, request: InferenceRequest) -> AsyncIterator[str]:
        ...
