# tests/unit/domain/test_conversation.py
from src.domain.entities.conversation import Conversation
from src.domain.entities.message import Message
from src.domain.value_objects.role import Role


def test_add_message_updates_conversation():
    conv = Conversation()
    msg = Message(role=Role.USER, content="hello")
    conv.add_message(msg)
    assert len(conv.messages) == 1
    assert conv.messages[0].content == "hello"


def test_last_messages_returns_slice():
    conv = Conversation()
    for i in range(10):
        conv.add_message(Message(role=Role.USER, content=str(i)))
    result = conv.last_messages(3)
    assert len(result) == 3
    assert result[-1].content == "9"
