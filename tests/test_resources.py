"""Tests for resource suggestions."""

import pytest

from mind_mate_ai.resources import CATEGORIES, format_resources, get_resources


def test_get_all_resources_returns_list():
    resources = get_resources()
    assert isinstance(resources, list)
    assert len(resources) > 0


def test_get_resources_by_category():
    crisis = get_resources("crisis")
    assert all(r["category"] == "crisis" for r in crisis)


def test_get_resources_unknown_category_returns_empty():
    result = get_resources("nonexistent_category")
    assert result == []


def test_all_resources_have_required_keys():
    for r in get_resources():
        assert "name" in r
        assert "description" in r
        assert "url" in r
        assert "category" in r
        assert r["category"] in CATEGORIES


def test_format_resources_empty():
    assert format_resources([]) == "No resources found."


def test_format_resources_nonempty():
    resources = get_resources("mindfulness")
    output = format_resources(resources)
    for r in resources:
        assert r["name"] in output
        assert r["url"] in output
