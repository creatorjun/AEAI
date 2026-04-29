#!/usr/bin/env bash
# deploy/scripts/start_vllm_server.sh
set -euo pipefail

MODEL=${VLLM_MODEL:-google/gemma-4-e4b-it}
PORT=${VLLM_PORT:-8000}
GPU_MEM=${VLLM_GPU_MEM_UTIL:-0.90}

vllm serve "$MODEL" \
  --port "$PORT" \
  --dtype bfloat16 \
  --gpu-memory-utilization "$GPU_MEM" \
  --enable-auto-tool-choice \
  --tool-call-parser gemma4 \
  --chat-template examples/tool_chat_template_gemma4.jinja
