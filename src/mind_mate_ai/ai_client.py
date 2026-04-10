"""AI chat client for Mind Mate AI."""

from __future__ import annotations

import os
from typing import Optional

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None  # type: ignore[assignment]

from mind_mate_ai.conversation import ConversationHistory


class AIClient:
    """Wraps the OpenAI chat completion API for Mind Mate conversations."""

    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
    ) -> None:
        self._model = model
        resolved_key = api_key or os.getenv("OPENAI_API_KEY")
        if openai is None:
            raise RuntimeError(
                "The 'openai' package is required. Install it with: pip install openai"
            )
        self._client = openai.OpenAI(api_key=resolved_key)

    def send(self, history: ConversationHistory, user_input: str) -> str:
        """
        Append *user_input* to *history*, call the API, store the reply,
        and return the assistant's reply text.
        """
        history.add_user_message(user_input)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=history.to_api_messages(),  # type: ignore[arg-type]
            temperature=0.7,
            max_tokens=512,
        )
        reply = response.choices[0].message.content or ""
        history.add_assistant_message(reply)
        return reply
