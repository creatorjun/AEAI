# src/infrastructure/config/redis.py
from __future__ import annotations
from redis.asyncio import Redis, from_url
from src.infrastructure.config.settings import get_settings

_client: Redis | None = None


async def get_redis_client() -> Redis:
    global _client
    if _client is None:
        settings = get_settings()
        _client = from_url(settings.redis_url, decode_responses=True)
    return _client
