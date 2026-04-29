# src/domain/policies/model_policy.py
from __future__ import annotations
import platform
from src.domain.value_objects.runtime_type import RuntimeType


class ModelPolicy:
    @staticmethod
    def select_runtime() -> RuntimeType:
        if platform.system() == "Darwin":
            return RuntimeType.MLX
        return RuntimeType.VLLM

    @staticmethod
    def default_model(runtime: RuntimeType) -> str:
        return {
            RuntimeType.MLX: "mlx-community/gemma-4-e4b-it-8bit",
            RuntimeType.VLLM: "google/gemma-4-e4b-it",
        }[runtime]
