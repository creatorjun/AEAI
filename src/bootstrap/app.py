# src/bootstrap/app.py
from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.presentation.http.routers.chat import router as chat_router
from src.presentation.http.routers.health import router as health_router
from src.infrastructure.config.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="AEAI",
        description="AI Serving Platform — Gemma 4 E4B via MLX (macOS) / vLLM (Linux)",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(health_router)
    app.include_router(chat_router, prefix="/api/v1")
    return app


app = create_app()
