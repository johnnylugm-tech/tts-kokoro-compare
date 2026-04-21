"""Kokoro Taiwan Proxy - FastAPI Application."""
# Copyright (c) 2026 Johnny Lu. Licensed under MIT License.

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import (
    KOKORO_BACKEND_URL,
    KOKORO_VOICES_URL,
    WARMUP_ENABLED,
    WARMUP_TEXT,
    LOG_FORMAT,
    LOG_LEVEL,
)
from .routers import speech
from .engines.synthesis import SynthesisEngine

# Configure logging
logging.basicConfig(
    format=LOG_FORMAT,
    level=getattr(logging, LOG_LEVEL),
)
logger = logging.getLogger(__name__)

# Global synthesis engine for warmup
_synthesis_engine: SynthesisEngine | None = None


async def warmup_backend() -> bool:
    """
    Perform warmup request to load model weights.

    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True

    logger.info("Starting backend warmup...")

    try:
        import httpx

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }

            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )

            response.raise_for_status()

            logger.info(
                "Warmup successful: received %s bytes", len(response.content)
            )
            return True

    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning("Warmup failed: %s", e)
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    global _synthesis_engine

    # Startup
    logger.info("=" * 50)
    logger.info("Kokoro Taiwan Proxy starting...")
    logger.info("Backend URL: %s", KOKORO_BACKEND_URL)
    logger.info("=" * 50)

    # Initialize synthesis engine
    _synthesis_engine = SynthesisEngine()

    # Warmup backend
    if WARMUP_ENABLED:
        warmup_success = await warmup_backend()
        if not warmup_success:
            logger.warning("Warmup failed, service will start anyway")

    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down...")
    if _synthesis_engine:
        await _synthesis_engine.close()
    logger.info("Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Kokoro Taiwan Proxy",
    description=(
        "TTS Proxy with Taiwan-optimized linguistic processing. "
        "Provides OpenAI-compatible API with SSML support."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info("Request: %s %s", request.method, request.url.path)

    response = await call_next(request)

    logger.info("Response: %s", response.status_code)
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Include routers
app.include_router(speech.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Kokoro Taiwan Proxy",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status and backend URL
    """
    # Check if backend is reachable
    backend_reachable = False

    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                KOKORO_VOICES_URL,
            )
            backend_reachable = response.status_code == 200
    except httpx.HTTPError as e:
        logger.warning("Health check failed: %s", e)
        backend_reachable = False

    return {
        "status": "ok" if backend_reachable else "degraded",
        "backend": KOKORO_BACKEND_URL,
        "backend_reachable": backend_reachable,
    }


@app.get("/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes/load balancer.

    Returns:
        Ready status
    """
    return {"ready": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",  # nosec - CLI server needs external access
        port=8881,  # Proxy on 8881, backend on 8880
        reload=False,
        log_level="info",
    )
