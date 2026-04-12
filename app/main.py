"""FastAPI application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import live_detection_router
from app.services.runtime_state import initialize_models, models_ready

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Initializing existing emotion detection models")
    initialize_models()
    yield
    logger.info("Application shutdown complete")


app = FastAPI(
    title="Emotion Detection API",
    description="API that starts live emotion detection and posts the dominant result to callbackUrl.",
    version="3.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_request(request: Request, call_next):
    logger.info("Incoming request: %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("Completed request: %s %s", request.method, response.status_code)
    return response


@app.get("/")
async def root():
    return {"service": "Emotion Detection API", "status": "running"}


@app.get("/health")
async def health():
    return {
        "status": "healthy" if models_ready() else "degraded",
        "modelsReady": models_ready(),
    }


app.include_router(live_detection_router)
