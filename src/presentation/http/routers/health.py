# src/presentation/http/routers/health.py
from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
import platform

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    runtime: str
    platform: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    from src.domain.policies.model_policy import ModelPolicy
    runtime = ModelPolicy.select_runtime()
    return HealthResponse(
        status="ok",
        runtime=runtime,
        platform=platform.system(),
    )
