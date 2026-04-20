"""Speech router - /v1/proxy/speech endpoint."""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Response

from ..models import SpeechRequest
from ..config import (
    DEFAULT_VOICE,
    DEFAULT_SPEED,
    MODEL_MAP,
    KOKORO_VOICES_URL,
)
from ..engines.synthesis import SynthesisEngine
from ..engines.ssml_parser import SSMLParser
from ..engines.taiwan_linguistic import TaiwanLinguisticEngine
from ..engines.text_splitter import TextSplitter
from ..middleware.circuit_breaker import CircuitBreaker, CircuitBreakerOpen
from ..cache.redis_cache import RedisCache, CacheConfig

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/proxy", tags=["speech"])

# Global instances
_synthesis_engine: Optional[SynthesisEngine] = None
_circuit_breaker: Optional[CircuitBreaker] = None
_cache: Optional[RedisCache] = None
_ssml_parser = SSMLParser()
_text_splitter = TextSplitter()
_linguistic_engine = TaiwanLinguisticEngine()


def get_synthesis_engine() -> SynthesisEngine:
    """Get or create synthesis engine singleton."""
    global _synthesis_engine
    if _synthesis_engine is None:
        _synthesis_engine = SynthesisEngine()
    return _synthesis_engine


def get_circuit_breaker() -> CircuitBreaker:
    """Get or create circuit breaker singleton."""
    global _circuit_breaker
    if _circuit_breaker is None:
        _circuit_breaker = CircuitBreaker(
            threshold=3,
            timeout=10.0,
        )
    return _circuit_breaker


def get_cache() -> RedisCache:
    """Get or create cache singleton."""
    global _cache
    if _cache is None:
        _cache = RedisCache(CacheConfig(enabled=False))  # Disabled by default
    return _cache


def get_effective_voice(request: SpeechRequest) -> str:
    """
    Determine effective voice based on request and model mapping.
    
    Args:
        request: Speech request
        
    Returns:
        Voice identifier to use
    """
    if request.voice:
        return request.voice
    
    model_voice = MODEL_MAP.get(request.model)
    if model_voice:
        return model_voice
    
    return DEFAULT_VOICE


def get_effective_speed(request: SpeechRequest) -> float:
    """
    Determine effective speed based on request.
    
    Args:
        request: Speech request
        
    Returns:
        Speed multiplier
    """
    return request.speed if request.speed is not None else DEFAULT_SPEED


@router.post("/speech")
async def generate_speech(request: SpeechRequest) -> Response:
    """
    Generate speech audio from text or SSML input.
    
    This endpoint provides a OpenAI-compatible interface with additional
    Taiwan-specific language processing.
    
    Request Body:
        model: Model identifier (tts-1, tts-1-hd, kokoro, custom-gentle)
        input: Text or SSML markup
        voice: Optional voice override
        speed: Optional speed multiplier (0.5-2.0)
        response_format: Output format (mp3, etc.)
    
    Returns:
        Audio data in specified format
    """
    # Get components
    engine = get_synthesis_engine()
    circuit_breaker = get_circuit_breaker()
    cache = get_cache()
    
    # Log request
    logger.info(
        f"Speech request: model={request.model}, "
        f"input_len={len(request.input)}, "
        f"voice={request.voice}, "
        f"speed={request.speed}"
    )
    
    # Validate input
    if not request.input or not request.input.strip():
        raise HTTPException(status_code=400, detail="Empty input text")
    
    if len(request.input) > 5000:
        raise HTTPException(status_code=400, detail="Input text too long (max 5000 chars)")
    
    # Check circuit breaker
    if circuit_breaker.get_state().value == "open":
        logger.warning("Circuit breaker is open, rejecting request")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable (circuit breaker open)"
        )
    
    try:
        # Check cache
        cached_audio = await cache.get(
            text=request.input,
            voice=get_effective_voice(request),
            speed=get_effective_speed(request),
            model=request.model,
        )
        
        if cached_audio:
            logger.info("Returning cached audio")
            return Response(
                content=cached_audio,
                media_type="audio/mpeg",
                headers={"X-Cache": "HIT"},
            )
        
        # Determine effective parameters
        voice = get_effective_voice(request)
        speed = get_effective_speed(request)
        
        # Check if SSML
        is_ssml = _ssml_parser.is_ssml(request.input)
        
        # Synthesize using circuit breaker
        try:
            audio_data: bytes
            if is_ssml:
                audio_data = await circuit_breaker.call_async(
                    engine.synthesize_ssml,  # type: ignore[arg-type]
                    request.input,
                    voice,
                    speed,
                )
            else:
                audio_data = await circuit_breaker.call_async(
                    engine.synthesize_text,  # type: ignore[arg-type]
                    request.input,
                    voice,
                    speed,
                    request.model,
                )
        except CircuitBreakerOpen:
            raise HTTPException(
                status_code=503,
                detail="Backend service unavailable (circuit breaker open)"
            )
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="No audio generated")
        
        # Cache the result
        await cache.set(
            text=request.input,
            voice=voice,
            speed=speed,
            model=request.model,
            audio=audio_data,
        )
        
        logger.info(f"Generated audio: {len(audio_data)} bytes")
        
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={"X-Cache": "MISS"},
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Speech synthesis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")


@router.get("/voices")
async def list_voices() -> dict:
    """
    List available voices from the Kokoro backend.
    
    Returns:
        Dictionary with list of available voices
    """
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(KOKORO_VOICES_URL)
            response.raise_for_status()
            voices = response.json()
            return {"voices": voices}
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.error(f"Failed to fetch voices: {e}")
        # Return default voices as fallback
        return {
            "voices": [
                {"id": "zf_xiaoxiao", "name": "Xiaoxiao (Taiwan Female)"},
                {"id": "af_heart", "name": "Heart (American Female)"},
                {"id": "custom-gentle", "name": "Gentle Mix"},
            ],
            "fallback": True,
        }


@router.get("/health/circuit")
async def circuit_breaker_health() -> dict:
    """Get circuit breaker status."""
    breaker = get_circuit_breaker()
    return breaker.get_stats()


@router.post("/health/circuit/reset")
async def reset_circuit_breaker() -> dict:
    """Manually reset circuit breaker."""
    breaker = get_circuit_breaker()
    breaker.reset()
    return {"status": "reset", "circuit_breaker": breaker.get_stats()}
