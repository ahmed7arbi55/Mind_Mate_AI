"""Application configuration."""

from __future__ import annotations

import os


class Settings:
    """Runtime settings loaded from environment variables."""

    host: str = os.getenv("API_HOST", "127.0.0.1")
    port: int = int(os.getenv("API_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    api_key: str = os.getenv("API_KEY", "MySuperSecretKey")

    device: str = os.getenv("DEVICE", "cpu")
    face_model_path: str = os.getenv("FACE_MODEL_PATH", "yolov8n-face.pt")
    emotion_model_path: str = os.getenv("EMOTION_MODEL_PATH", "repvgg.pth")
    face_conf_threshold: float = float(os.getenv("FACE_CONF_THRESHOLD", "0.5"))
    face_iou_threshold: float = float(os.getenv("FACE_IOU_THRESHOLD", "0.4"))
    emotion_temperature: float = float(os.getenv("EMOTION_TEMPERATURE", "1.0"))

    detection_duration_seconds: int = int(os.getenv("DETECTION_DURATION_SECONDS", "10"))
    webcam_index: int = int(os.getenv("WEBCAM_INDEX", "0"))

    webhook_timeout_seconds: int = int(os.getenv("WEBHOOK_TIMEOUT_SECONDS", "10"))
    webhook_retry_count: int = int(os.getenv("WEBHOOK_RETRY_COUNT", "3"))
    webhook_retry_delay_seconds: float = float(os.getenv("WEBHOOK_RETRY_DELAY_SECONDS", "1.5"))
    webhook_verify_ssl: bool = os.getenv("WEBHOOK_VERIFY_SSL", "true").lower() == "true"
    disable_ssl_verify_for_localhost: bool = (
        os.getenv("DISABLE_SSL_VERIFY_FOR_LOCALHOST", "true").lower() == "true"
    )


settings = Settings()

