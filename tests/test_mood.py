"""Tests for MoodTracker."""

import pytest

from mind_mate_ai.mood import MoodEntry, MoodTracker


def test_mood_entry_valid_scores():
    for score in range(1, 6):
        entry = MoodEntry(score=score, note=None)
        assert entry.score == score


def test_mood_entry_invalid_score_raises():
    with pytest.raises(ValueError):
        MoodEntry(score=0, note=None)
    with pytest.raises(ValueError):
        MoodEntry(score=6, note=None)


def test_mood_entry_label():
    entry = MoodEntry(score=5, note=None)
    assert entry.label == "Excellent"


def test_mood_entry_str_with_note():
    entry = MoodEntry(score=3, note="Feeling okay")
    assert "Neutral" in str(entry)
    assert "Feeling okay" in str(entry)


def test_mood_entry_str_without_note():
    entry = MoodEntry(score=2, note=None)
    result = str(entry)
    assert "Low" in result
    assert "—" not in result


def test_tracker_log_and_retrieve():
    tracker = MoodTracker()
    entry = tracker.log(4, "Had a good day")
    assert len(tracker.entries) == 1
    assert tracker.entries[0] is entry


def test_tracker_average():
    tracker = MoodTracker()
    tracker.log(2)
    tracker.log(4)
    assert tracker.average == pytest.approx(3.0)


def test_tracker_average_empty():
    tracker = MoodTracker()
    assert tracker.average is None


def test_tracker_summary_empty():
    tracker = MoodTracker()
    assert "No mood entries" in tracker.summary()


def test_tracker_summary_with_entries():
    tracker = MoodTracker()
    tracker.log(3, "okay")
    tracker.log(5)
    summary = tracker.summary()
    assert "2" in summary
    assert "Excellent" in summary
