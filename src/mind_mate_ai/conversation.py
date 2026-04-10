"""Conversation history management for Mind Mate AI."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Message:
    """A single message in a conversation."""

    role: str  # "user" or "assistant" or "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Return a dict suitable for the OpenAI messages API."""
        return {"role": self.role, "content": self.content}


class ConversationHistory:
    """Manages the history of a chat conversation."""

    SYSTEM_PROMPT = (
        "You are Mind Mate, a compassionate and supportive AI mental health companion. "
        "Your role is to provide empathetic listening, emotional support, and gentle guidance. "
        "You are NOT a replacement for professional mental health care. Always encourage users "
        "to seek professional help when discussing serious concerns such as self-harm, crisis "
        "situations, or severe mental health symptoms. Respond warmly, non-judgmentally, and "
        "in a conversational tone. Keep your responses concise and focused on the user's needs."
    )

    def __init__(self) -> None:
        self._messages: List[Message] = []
        self._system_message = Message(role="system", content=self.SYSTEM_PROMPT)

    @property
    def messages(self) -> List[Message]:
        """Return all non-system messages."""
        return list(self._messages)

    def add_user_message(self, content: str) -> None:
        """Append a user message to the history."""
        self._messages.append(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        """Append an assistant message to the history."""
        self._messages.append(Message(role="assistant", content=content))

    def to_api_messages(self) -> List[dict]:
        """Return the full message list (system + history) for the API call."""
        return [self._system_message.to_dict()] + [m.to_dict() for m in self._messages]

    def clear(self) -> None:
        """Reset conversation history (keeps system prompt)."""
        self._messages.clear()

    def __len__(self) -> int:
        return len(self._messages)
