"""Shared runtime state for model instances."""

from __future__ import annotations

import logging

from app.core.config import settings
from app.services.emotion_classifier import EmotionClassifier
from app.services.face_detector import FaceDetector

logger = logging.getLogger(__name__)

face_detector: FaceDetector | None = None
emotion_classifier: EmotionClassifier | None = None


def initialize_models() -> None:
    """Load existing local models once at startup."""
    global face_detector, emotion_classifier
    logger.info("Loading face detector model from %s", settings.face_model_path)
    face_detector = FaceDetector(
        model_path=settings.face_model_path,
        device=settings.device,
        conf_threshold=settings.face_conf_threshold,
        iou_threshold=settings.face_iou_threshold,
    )
    logger.info("Loading emotion model from %s", settings.emotion_model_path)
    emotion_classifier = EmotionClassifier(
        device=settings.device,
        model_path=settings.emotion_model_path,
        temperature=settings.emotion_temperature,
    )
    logger.info("Model initialization completed")


def models_ready() -> bool:
    return face_detector is not None and emotion_classifier is not None

