"""Command-line interface for Mind Mate AI."""

from __future__ import annotations

import sys

from mind_mate_ai.ai_client import AIClient
from mind_mate_ai.conversation import ConversationHistory
from mind_mate_ai.mood import MoodTracker
from mind_mate_ai.resources import CATEGORIES, format_resources, get_resources

BANNER = r"""
  __  __ _           _   __  __       _         _    ___ 
 |  \/  (_)_ __   __| | |  \/  | __ _| |_ ___  / \  |_ _|
 | |\/| | | '_ \ / _` | | |\/| |/ _` | __/ _ \/ _ \  | | 
 | |  | | | | | | (_| | | |  | | (_| | ||  __/ ___ \ | | 
 |_|  |_|_|_| |_|\__,_| |_|  |_|\__,_|\__\___/_/   \_\___|

  Your compassionate AI mental health companion
"""

HELP_TEXT = """
Commands:
  /mood           – Log your current mood (1-5 scale)
  /history        – Show mood history summary
  /resources      – List mental health resources
  /resources <category>  – Filter resources by category
                    Categories: crisis, general, mindfulness, professional, support
  /clear          – Clear conversation history
  /help           – Show this help message
  /quit           – Exit the application
"""


def run_cli() -> None:
    """Entry-point for the Mind Mate AI CLI."""
    print(BANNER)
    print("Type /help for available commands or just start chatting!\n")
    print(
        "DISCLAIMER: Mind Mate AI is not a substitute for professional mental health care.\n"
        "If you are in crisis, please contact a crisis helpline immediately.\n"
    )

    history = ConversationHistory()
    mood_tracker = MoodTracker()

    try:
        client = AIClient()
    except RuntimeError as exc:
        print(f"Error initializing AI client: {exc}")
        sys.exit(1)

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Take care of yourself. 💙")
            break

        if not user_input:
            continue

        # ── built-in commands ──────────────────────────────────────────────
        if user_input.lower() == "/quit":
            print("Goodbye! Take care of yourself. 💙")
            break

        if user_input.lower() == "/help":
            print(HELP_TEXT)
            continue

        if user_input.lower() == "/clear":
            history.clear()
            print("Conversation history cleared.\n")
            continue

        if user_input.lower() == "/history":
            print(mood_tracker.summary())
            continue

        if user_input.lower().startswith("/resources"):
            parts = user_input.split(maxsplit=1)
            category = parts[1].strip().lower() if len(parts) > 1 else None
            if category and category not in CATEGORIES:
                print(f"Unknown category '{category}'. Valid: {', '.join(CATEGORIES)}")
            else:
                print(format_resources(get_resources(category)))
            continue

        if user_input.lower() == "/mood":
            _handle_mood_log(mood_tracker)
            continue

        # ── AI conversation ────────────────────────────────────────────────
        print("Mind Mate: ", end="", flush=True)
        try:
            reply = client.send(history, user_input)
            print(reply, "\n")
        except Exception as exc:  # noqa: BLE001
            print(f"\n[Error communicating with AI: {exc}]\n")


def _handle_mood_log(tracker: MoodTracker) -> None:
    """Prompt the user to log their mood."""
    print("How are you feeling right now? (1 = Very Low, 5 = Excellent)")
    try:
        raw = input("Mood score [1-5]: ").strip()
        score = int(raw)
        note_input = input("Optional note (press Enter to skip): ").strip()
        note = note_input if note_input else None
        entry = tracker.log(score, note)
        print(f"Logged: {entry}\n")
    except (ValueError, EOFError, KeyboardInterrupt):
        print("Mood log cancelled.\n")


def main() -> None:
    """Main entry point."""
    run_cli()


if __name__ == "__main__":
    main()
