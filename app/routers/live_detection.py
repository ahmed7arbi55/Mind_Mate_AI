"""Router for live detection endpoint."""

from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, Depends

from app.core.security import verify_api_key
from app.models import StartLiveDetectionRequest, StartLiveDetectionResponse
from app.services.detection_service import run_live_detection_job

logger = logging.getLogger(__name__)

router = APIRouter(tags=["live-detection"])


@router.post("/start_live_detection", response_model=StartLiveDetectionResponse)
async def start_live_detection(
    payload: StartLiveDetectionRequest,
    _: str = Depends(verify_api_key),
) -> StartLiveDetectionResponse:
    """Start non-blocking live detection and return immediately."""
    logger.info(
        "Incoming /start_live_detection for userId=%s, departmentId=%s, recordId=%s",
        payload.user_id,
        payload.department_id,
        payload.record_id,
    )
    asyncio.create_task(run_live_detection_job(payload))
    return StartLiveDetectionResponse(
        status="accepted",
        message="Live detection started",
        userId=payload.user_id,
        recordId=payload.record_id,
    )

