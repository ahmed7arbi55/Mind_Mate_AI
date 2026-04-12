"""
Application Entry Point
========================
Run this file to start the FastAPI server for Face & Emotion Detection.

Usage:
    python run.py

The API will be available at:
    - API: http://127.0.0.1:8000
    - Docs: http://127.0.0.1:8000/docs
    - ReDoc: http://127.0.0.1:8000/redoc
"""

import uvicorn
import logging
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("🚀 Starting Face & Emotion Detection API...")
    logger.info("📖 API Documentation: http://%s:%s/docs", settings.host, settings.port)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level="info"
    )
