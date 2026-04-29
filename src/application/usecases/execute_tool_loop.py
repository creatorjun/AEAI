# src/application/usecases/execute_tool_loop.py
from __future__ import annotations
from src.application.ports.llm_gateway import LlmGateway
from src.application.ports.tool_registry import ToolRegistry
from src.domain.entities.conversation import Conversation
from src.domain.entities.message import Message
from src.domain.entities.tool_call import ToolCall
from src.domain.value_objects.inference_request import InferenceRequest
from src.domain.value_objects.inference_response import InferenceResponse
from src.domain.value_objects.role import Role
import json


MAX_TOOL_ROUNDS = 5


class ExecuteToolLoop:
    def __init__(self, llm: LlmGateway, registry: ToolRegistry) -> None:
        self._llm = llm
        self._registry = registry

    async def execute(
        self,
        conversation: Conversation,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> InferenceResponse:
        tools = self._registry.list_definitions()
        for _ in range(MAX_TOOL_ROUNDS):
            request = InferenceRequest(
                messages=conversation.messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools,
            )
            response = await self._llm.complete(request)

            if not response.tool_calls:
                return response

            conversation.add_message(
                Message(
                    role=Role.ASSISTANT,
                    content=response.content,
                    tool_calls=[
                        {"id": tc.id, "name": tc.tool_name, "arguments": tc.arguments}
                        for tc in response.tool_calls
                    ],
                )
            )

            for tc in response.tool_calls:
                try:
                    result = await self._registry.execute(tc.tool_name, tc.arguments)
                    tc.result = result
                except Exception as e:
                    tc.error = str(e)
                    result = {"error": str(e)}

                conversation.add_message(
                    Message(
                        role=Role.TOOL,
                        content=json.dumps(result, ensure_ascii=False),
                        tool_call_id=tc.id,
                    )
                )

        return await self._llm.complete(
            InferenceRequest(
                messages=conversation.messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        )
