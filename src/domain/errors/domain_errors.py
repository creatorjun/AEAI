# src/domain/errors/domain_errors.py


class DomainError(Exception):
    pass


class ConversationNotFoundError(DomainError):
    def __init__(self, conversation_id: str) -> None:
        super().__init__(f"Conversation not found: {conversation_id}")


class ToolNotFoundError(DomainError):
    def __init__(self, tool_name: str) -> None:
        super().__init__(f"Tool not registered: {tool_name}")


class RuntimeNotAvailableError(DomainError):
    def __init__(self, runtime: str) -> None:
        super().__init__(f"Runtime not available: {runtime}")


class InferenceError(DomainError):
    pass
