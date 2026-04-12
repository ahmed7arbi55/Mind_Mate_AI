"""Test script for live detection endpoint."""

from __future__ import annotations

import json

import requests

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "MySuperSecretKey"


def test_health() -> None:
    print("\n🏥 Testing /health ...")
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200


def test_start_live_detection() -> None:
    print("\n🎥 Testing /start_live_detection ...")
    payload = {
        "userId": 1,
        "departmentId": 2,
        "recordId": 1001,
        "callbackUrl": "http://127.0.0.1:9000/mock-callback",
    }
    response = requests.post(
        f"{BASE_URL}/start_live_detection",
        json=payload,
        headers={"X-API-KEY": API_KEY},
        timeout=10,
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code in (200, 202)


if __name__ == "__main__":
    print("🎭 Live Emotion Detection API Test")
    print("=" * 50)
    test_health()
    test_start_live_detection()
    print("\n✅ Tests finished")
