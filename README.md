# AEAI — AI Serving Platform

FastAPI + PostgreSQL + Redis + Gemma 4 E4B

- macOS: MLX runtime
- Linux: vLLM runtime

## Architecture

Clean Architecture (Presentation → Application → Domain ← Infrastructure)

## Quick Start

```bash
cp .env.example .env
docker compose up -d
uv run uvicorn src.bootstrap.app:app --reload
```
