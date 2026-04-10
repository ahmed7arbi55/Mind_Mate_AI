"""Mood tracking for Mind Mate AI."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


MOOD_SCALE: dict[int, str] = {
    1: "Very Low",
    2: "Low",
    3: "Neutral",
    4: "Good",
    5: "Excellent",
}


@dataclass
class MoodEntry:
    """A single mood check-in."""

    score: int  # 1-5
    note: Optional[str]
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if self.score not in MOOD_SCALE:
            raise ValueError(f"Mood score must be between 1 and 5, got {self.score}")

    @property
    def label(self) -> str:
        """Human-readable mood label."""
        return MOOD_SCALE[self.score]

    def __str__(self) -> str:
        note_part = f" — {self.note}" if self.note else ""
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] Mood {self.score}/5 ({self.label}){note_part}"


class MoodTracker:
    """Tracks mood entries over time."""

    def __init__(self) -> None:
        self._entries: List[MoodEntry] = []

    def log(self, score: int, note: Optional[str] = None) -> MoodEntry:
        """Log a new mood entry and return it."""
        entry = MoodEntry(score=score, note=note)
        self._entries.append(entry)
        return entry

    @property
    def entries(self) -> List[MoodEntry]:
        return list(self._entries)

    @property
    def average(self) -> Optional[float]:
        """Return average mood score, or None if no entries."""
        if not self._entries:
            return None
        return sum(e.score for e in self._entries) / len(self._entries)

    def summary(self) -> str:
        """Return a short text summary of mood history."""
        if not self._entries:
            return "No mood entries recorded yet."
        avg = self.average
        last = self._entries[-1]
        return (
            f"Total check-ins: {len(self._entries)} | "
            f"Average mood: {avg:.1f}/5 | "
            f"Latest: {last.label} ({last.score}/5)"
        )
