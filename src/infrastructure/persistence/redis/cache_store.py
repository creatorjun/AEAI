# src/infrastructure/persistence/redis/cache_store.py
from __future__ import annotations
from typing import Any
import json
from redis.asyncio import Redis
from src.application.ports.cache_store import CacheStore


class RedisCacheStore(CacheStore):
    def __init__(self, client: Redis) -> None:
        self._client = client

    async def get(self, key: str) -> Any | None:
        raw = await self._client.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return raw

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        serialized = json.dumps(value, ensure_ascii=False)
        if ttl:
            await self._client.setex(key, ttl, serialized)
        else:
            await self._client.set(key, serialized)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        return bool(await self._client.exists(key))
