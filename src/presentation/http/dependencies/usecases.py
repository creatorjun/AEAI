# src/presentation/http/dependencies/usecases.py
from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.presentation.http.dependencies.db import get_db_session
from src.application.usecases.create_chat_completion import CreateChatCompletion
from src.application.usecases.stream_chat_completion import StreamChatCompletion
from src.infrastructure.persistence.postgres.conversation_repository import PostgresConversationRepository
from src.infrastructure.persistence.redis.cache_store import RedisCacheStore
from src.infrastructure.config.settings import get_settings
from src.infrastructure.config.redis import get_redis_client
from src.domain.policies.model_policy import ModelPolicy
from src.domain.value_objects.runtime_type import RuntimeType


def _get_llm_gateway():
    settings = get_settings()
    runtime = ModelPolicy.select_runtime()
    if runtime == RuntimeType.MLX:
        from src.infrastructure.llm.mlx.mlx_adapter import MlxAdapter
        return MlxAdapter(base_url=settings.mlx_server_url)
    from src.infrastructure.llm.vllm.vllm_adapter import VllmAdapter
    return VllmAdapter(base_url=settings.vllm_server_url)


async def get_create_chat(
    session: AsyncSession = Depends(get_db_session),
) -> CreateChatCompletion:
    redis = await get_redis_client()
    return CreateChatCompletion(
        llm=_get_llm_gateway(),
        repo=PostgresConversationRepository(session),
        cache=RedisCacheStore(redis),
    )


async def get_stream_chat(
    session: AsyncSession = Depends(get_db_session),
) -> StreamChatCompletion:
    return StreamChatCompletion(
        llm=_get_llm_gateway(),
        repo=PostgresConversationRepository(session),
    )
