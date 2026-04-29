# src/domain/value_objects/runtime_type.py
from enum import StrEnum


class RuntimeType(StrEnum):
    MLX = "mlx"
    VLLM = "vllm"
