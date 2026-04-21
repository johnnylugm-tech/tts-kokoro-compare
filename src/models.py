"""Pydantic models for request/response schemas."""

from typing import Optional
from pydantic import BaseModel, Field


class SpeechRequest(BaseModel):
    """Request model for speech synthesis."""
    model: str = Field(default="tts-1", description="Model to use for synthesis")
    input: str = Field(..., description="Text or SSML input for synthesis")
    voice: Optional[str] = Field(default=None, description="Voice to use")
    speed: Optional[float] = Field(
        default=None, ge=0.5, le=2.0, description="Speech speed multiplier"
    )
    response_format: str = Field(default="mp3", description="Output audio format")


class SpeechResponse(BaseModel):
    """Response model for speech synthesis."""
    audio: bytes = Field(..., description="Raw audio data")
    content_type: str = Field(default="audio/mpeg", description="MIME type of audio")
