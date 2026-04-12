"""Request and response models for live detection flow."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class StartLiveDetectionRequest(BaseModel):
    """Incoming request to start the live camera detection pipeline."""

    user_id: int = Field(..., alias="userId")
    department_id: int = Field(..., alias="departmentId")
    record_id: int = Field(..., alias="recordId")
    callback_url: HttpUrl = Field(..., alias="callbackUrl")

    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class StartLiveDetectionResponse(BaseModel):
    """Immediate acknowledgment response."""

    status: str
    message: str
    user_id: int = Field(..., alias="userId")
    record_id: int = Field(..., alias="recordId")

    model_config = ConfigDict(populate_by_name=True)


class CallbackPayload(BaseModel):
    """Payload sent to external callback endpoint."""

    user_id: int = Field(..., alias="userId")
    audio_link: str = Field(..., alias="AudioLink")
    record_id: int = Field(..., alias="recordId")

    model_config = ConfigDict(populate_by_name=True)

