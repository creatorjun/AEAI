# src/infrastructure/config/database.py
from __future__ import annotations
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.infrastructure.config.settings import get_settings
from src.infrastructure.persistence.postgres.models import Base

_engine = None
async_session_factory: async_sessionmaker[AsyncSession] | None = None


async def init_db() -> None:
    global _engine, async_session_factory
    settings = get_settings()
    _engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)
    async_session_factory = async_sessionmaker(_engine, expire_on_commit=False)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
