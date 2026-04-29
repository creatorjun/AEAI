#!/usr/bin/env bash
# deploy/scripts/start_mlx_server.sh
set -euo pipefail

MODEL=${MLX_MODEL:-mlx-community/gemma-4-e4b-it-8bit}
PORT=${MLX_PORT:-8080}

python -m mlx_lm.server \
  --model "$MODEL" \
  --port "$PORT" \
  --trust-remote-code
