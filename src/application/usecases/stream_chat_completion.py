# src/application/usecases/stream_chat_completion.py
from __future__ import annotations
from collections.abc import AsyncIterator
from uuid import UUID
from src.application.ports.llm_gateway import LlmGateway
from src.application.ports.conversation_repository import ConversationRepository
from src.domain.entities.conversation import Conversation
from src.domain.entities.message import Message
from src.domain.value_objects.inference_request import InferenceRequest
from src.domain.value_objects.role import Role
from src.domain.errors.domain_errors import ConversationNotFoundError


class StreamChatCompletion:
    def __init__(
        self,
        llm: LlmGateway,
        repo: ConversationRepository,
    ) -> None:
        self._llm = llm
        self._repo = repo

    async def execute(
        self,
        conversation_id: UUID | None,
        user_message: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        if conversation_id:
            conv = await self._repo.find_by_id(conversation_id)
            if conv is None:
                raise ConversationNotFoundError(str(conversation_id))
        else:
            conv = Conversation()
            if system_prompt:
                conv.add_message(Message(role=Role.SYSTEM, content=system_prompt))

        conv.add_message(Message(role=Role.USER, content=user_message))

        request = InferenceRequest(
            messages=conv.messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        full_content: list[str] = []

        async def _stream() -> AsyncIterator[str]:
            async for chunk in self._llm.stream(request):
                full_content.append(chunk)
                yield chunk
            conv.add_message(Message(role=Role.ASSISTANT, content="".join(full_content)))
            await self._repo.save(conv)

        return _stream()
