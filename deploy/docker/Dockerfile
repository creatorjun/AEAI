# deploy/docker/Dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv pip install --system --no-cache .

COPY . .

EXPOSE 8001

CMD ["uvicorn", "src.bootstrap.app:app", "--host", "0.0.0.0", "--port", "8001"]
