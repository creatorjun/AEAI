# src/infrastructure/config/settings.py
from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.domain.policies.model_policy import ModelPolicy


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+asyncpg://aeai:aeai@localhost:5432/aeai"
    redis_url: str = "redis://localhost:6379/0"

    mlx_server_url: str = "http://localhost:8080"
    vllm_server_url: str = "http://localhost:8000"

    mlx_model: str = "mlx-community/gemma-4-e4b-it-8bit"
    vllm_model: str = "google/gemma-4-e4b-it"

    cache_ttl: int = 3600
    max_history_messages: int = 50

    @property
    def default_model(self) -> str:
        return ModelPolicy.default_model(ModelPolicy.select_runtime())


@lru_cache
def get_settings() -> Settings:
    return Settings()
