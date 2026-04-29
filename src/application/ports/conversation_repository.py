# src/application/ports/conversation_repository.py
from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from src.domain.entities.conversation import Conversation


class ConversationRepository(ABC):
    @abstractmethod
    async def save(self, conversation: Conversation) -> None:
        ...

    @abstractmethod
    async def find_by_id(self, conversation_id: UUID) -> Conversation | None:
        ...

    @abstractmethod
    async def delete(self, conversation_id: UUID) -> None:
        ...
