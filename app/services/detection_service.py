"""Background live-detection service with webhook callback."""

from __future__ import annotations

import asyncio
import logging
import time
from collections import Counter
from typing import List
from urllib.parse import urlparse

import cv2
import httpx

from app.core.config import settings
from app.models import CallbackPayload, StartLiveDetectionRequest
from app.services import runtime_state

logger = logging.getLogger(__name__)

LOCAL_CALLBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _crop_faces(frame, detections) -> List:
    """Create safe face crops from model detections."""
    crops = []
    frame_h, frame_w = frame.shape[:2]
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        x1 = max(0, min(x1, frame_w - 1))
        y1 = max(0, min(y1, frame_h - 1))
        x2 = max(0, min(x2, frame_w))
        y2 = max(0, min(y2, frame_h))
        if x2 <= x1 or y2 <= y1:
            continue
        crop = frame[y1:y2, x1:x2]
        if crop.size > 0:
            crops.append(crop)
    return crops


def _detect_frame_emotions(frame) -> List[str]:
    if not runtime_state.models_ready():
        raise RuntimeError("Models are not initialized")

    detections = runtime_state.face_detector.detect_faces(frame)
    if not detections:
        return []

    face_crops = _crop_faces(frame, detections)
    if not face_crops:
        return []

    results = runtime_state.emotion_classifier.classify_emotions(face_crops)
    return [item["label"] for item in results if "label" in item]


def _capture_and_detect(duration_seconds: int) -> List[str]:
    """Open camera, process frames for fixed duration, and collect emotions."""
    cap = cv2.VideoCapture(settings.webcam_index)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open camera index {settings.webcam_index}")

    logger.info("Camera opened on index %s", settings.webcam_index)
    start = time.monotonic()
    all_emotions: List[str] = []
    processed_frames = 0

    try:
        while time.monotonic() - start < duration_seconds:
            ok, frame = cap.read()
            if not ok or frame is None:
                logger.warning("Failed to read camera frame")
                continue

            processed_frames += 1
            frame_emotions = _detect_frame_emotions(frame)
            all_emotions.extend(frame_emotions)
    finally:
        cap.release()
        logger.info("Camera released after processing %s frames", processed_frames)

    return all_emotions


def _dominant_emotion(emotions: List[str]) -> str:
    if not emotions:
        return "unknown"
    return Counter(emotions).most_common(1)[0][0]


async def _send_callback_with_retry(callback_url: str, payload: CallbackPayload) -> None:
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": settings.api_key,
    }

    json_payload = payload.model_dump(by_alias=True)
    json_payload["audioLink"] = json_payload["AudioLink"]

    parsed = urlparse(callback_url)
    is_local_callback = parsed.hostname in LOCAL_CALLBACK_HOSTS
    verify_ssl = settings.webhook_verify_ssl
    if is_local_callback and settings.disable_ssl_verify_for_localhost:
        verify_ssl = False
        logger.warning(
            "SSL verification disabled for local callback URL: %s",
            callback_url,
        )

    async with httpx.AsyncClient(
        timeout=settings.webhook_timeout_seconds,
        verify=verify_ssl,
    ) as client:
        last_error: Exception | None = None
        for attempt in range(1, settings.webhook_retry_count + 1):
            try:
                response = await client.post(
                    callback_url,
                    json=json_payload,
                    headers=headers,
                )
                response.raise_for_status()
                logger.info("Callback sent successfully on attempt %s", attempt)
                return
            except Exception as exc:
                last_error = exc
                logger.error("Callback attempt %s failed: %s", attempt, exc)
                if attempt < settings.webhook_retry_count:
                    await asyncio.sleep(settings.webhook_retry_delay_seconds)

        raise RuntimeError(
            f"All callback retries failed ({settings.webhook_retry_count} attempts)"
        ) from last_error


async def run_live_detection_job(request_data: StartLiveDetectionRequest) -> None:
    """Background job that runs live detection then posts callback."""
    logger.info(
        "Background detection started for userId=%s, recordId=%s",
        request_data.user_id,
        request_data.record_id,
    )
    try:
        emotions = await asyncio.to_thread(
            _capture_and_detect, settings.detection_duration_seconds
        )
        dominant = _dominant_emotion(emotions)
        logger.info(
            "Detection complete for userId=%s, dominantEmotion=%s, totalDetections=%s",
            request_data.user_id,
            dominant,
            len(emotions),
        )

        callback_payload = CallbackPayload(
            userId=request_data.user_id,
            AudioLink=dominant,
            recordId=request_data.record_id,
        )
        await _send_callback_with_retry(str(request_data.callback_url), callback_payload)
    except Exception:
        logger.exception(
            "Live detection job failed for userId=%s, recordId=%s",
            request_data.user_id,
            request_data.record_id,
        )
