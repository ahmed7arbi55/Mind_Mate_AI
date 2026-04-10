"""Tests for ConversationHistory."""

import pytest

from mind_mate_ai.conversation import ConversationHistory, Message


def test_message_to_dict():
    msg = Message(role="user", content="Hello")
    assert msg.to_dict() == {"role": "user", "content": "Hello"}


def test_initial_history_is_empty():
    history = ConversationHistory()
    assert len(history) == 0
    assert history.messages == []


def test_add_user_message():
    history = ConversationHistory()
    history.add_user_message("Hi there")
    assert len(history) == 1
    assert history.messages[0].role == "user"
    assert history.messages[0].content == "Hi there"


def test_add_assistant_message():
    history = ConversationHistory()
    history.add_assistant_message("Hello, how can I help?")
    assert len(history) == 1
    assert history.messages[0].role == "assistant"


def test_to_api_messages_includes_system_prompt():
    history = ConversationHistory()
    history.add_user_message("hello")
    api_msgs = history.to_api_messages()
    assert api_msgs[0]["role"] == "system"
    assert "Mind Mate" in api_msgs[0]["content"]


def test_to_api_messages_order():
    history = ConversationHistory()
    history.add_user_message("first")
    history.add_assistant_message("second")
    api_msgs = history.to_api_messages()
    # system, user, assistant
    assert len(api_msgs) == 3
    assert api_msgs[1]["role"] == "user"
    assert api_msgs[2]["role"] == "assistant"


def test_clear_resets_history():
    history = ConversationHistory()
    history.add_user_message("one")
    history.add_assistant_message("two")
    history.clear()
    assert len(history) == 0


def test_clear_preserves_system_prompt():
    history = ConversationHistory()
    history.add_user_message("hello")
    history.clear()
    api_msgs = history.to_api_messages()
    assert api_msgs[0]["role"] == "system"
    assert len(api_msgs) == 1
