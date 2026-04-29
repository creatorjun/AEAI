# src/infrastructure/persistence/postgres/conversation_repository.py
from __future__ import annotations
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.application.ports.conversation_repository import ConversationRepository
from src.domain.entities.conversation import Conversation
from src.domain.entities.message import Message
from src.domain.value_objects.role import Role
from src.infrastructure.persistence.postgres.models import ConversationOrm, MessageOrm


class PostgresConversationRepository(ConversationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, conversation: Conversation) -> None:
        existing = await self._session.get(ConversationOrm, conversation.id)
        if existing is None:
            orm = ConversationOrm(
                id=conversation.id,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
                metadata_=conversation.metadata,
            )
            self._session.add(orm)
        else:
            existing.updated_at = conversation.updated_at
            existing.metadata_ = conversation.metadata
            for msg in conversation.messages:
                msg_exists = await self._session.get(MessageOrm, msg.id)
                if msg_exists is None:
                    self._session.add(
                        MessageOrm(
                            id=msg.id,
                            conversation_id=conversation.id,
                            role=msg.role,
                            content=msg.content,
                            tool_call_id=msg.tool_call_id,
                            tool_calls=msg.tool_calls,
                            created_at=msg.created_at,
                        )
                    )
            await self._session.flush()
            return

        for msg in conversation.messages:
            self._session.add(
                MessageOrm(
                    id=msg.id,
                    conversation_id=conversation.id,
                    role=msg.role,
                    content=msg.content,
                    tool_call_id=msg.tool_call_id,
                    tool_calls=msg.tool_calls,
                    created_at=msg.created_at,
                )
            )
        await self._session.flush()

    async def find_by_id(self, conversation_id: UUID) -> Conversation | None:
        stmt = select(ConversationOrm).where(ConversationOrm.id == conversation_id)
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()
        if orm is None:
            return None
        conv = Conversation(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            metadata=orm.metadata_,
        )
        for m in orm.messages:
            conv.messages.append(
                Message(
                    id=m.id,
                    role=Role(m.role),
                    content=m.content,
                    tool_call_id=m.tool_call_id,
                    tool_calls=m.tool_calls,
                    created_at=m.created_at,
                )
            )
        return conv

    async def delete(self, conversation_id: UUID) -> None:
        orm = await self._session.get(ConversationOrm, conversation_id)
        if orm:
            await self._session.delete(orm)
            await self._session.flush()
