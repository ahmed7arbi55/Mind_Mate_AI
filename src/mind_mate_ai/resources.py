"""Mental health resource suggestions for Mind Mate AI."""

from __future__ import annotations

from typing import List


RESOURCES: List[dict] = [
    {
        "name": "Crisis Text Line",
        "description": "Free 24/7 support for people in crisis. Text HOME to 741741.",
        "url": "https://www.crisistextline.org",
        "category": "crisis",
    },
    {
        "name": "National Suicide Prevention Lifeline",
        "description": "24/7 free, confidential support. Call or text 988.",
        "url": "https://988lifeline.org",
        "category": "crisis",
    },
    {
        "name": "SAMHSA National Helpline",
        "description": (
            "Free, confidential, 24/7 treatment referral and information service. "
            "Call 1-800-662-4357."
        ),
        "url": "https://www.samhsa.gov/find-help/national-helpline",
        "category": "general",
    },
    {
        "name": "Headspace",
        "description": "Guided meditation and mindfulness exercises.",
        "url": "https://www.headspace.com",
        "category": "mindfulness",
    },
    {
        "name": "Calm",
        "description": "Sleep, meditation, and relaxation app.",
        "url": "https://www.calm.com",
        "category": "mindfulness",
    },
    {
        "name": "Psychology Today Therapist Finder",
        "description": "Find a licensed therapist near you.",
        "url": "https://www.psychologytoday.com/us/therapists",
        "category": "professional",
    },
    {
        "name": "BetterHelp",
        "description": "Online professional counseling and therapy.",
        "url": "https://www.betterhelp.com",
        "category": "professional",
    },
    {
        "name": "7 Cups",
        "description": "Free emotional support through trained listeners.",
        "url": "https://www.7cups.com",
        "category": "support",
    },
]

CATEGORIES = ["crisis", "general", "mindfulness", "professional", "support"]


def get_resources(category: str | None = None) -> List[dict]:
    """Return resources, optionally filtered by category."""
    if category is None:
        return list(RESOURCES)
    return [r for r in RESOURCES if r["category"] == category]


def format_resources(resources: List[dict]) -> str:
    """Format a list of resources as a readable string."""
    if not resources:
        return "No resources found."
    lines = []
    for r in resources:
        lines.append(f"• {r['name']}: {r['description']}")
        lines.append(f"  {r['url']}")
    return "\n".join(lines)
