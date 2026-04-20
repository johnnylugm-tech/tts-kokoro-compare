"""Test speech router endpoints - expanded coverage."""

import pytest
import sys, os
from unittest.mock import MagicMock, patch, AsyncMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.routers.speech import (
    get_effective_voice,
    get_effective_speed,
    router,
    generate_speech,
    list_voices,
    circuit_breaker_health,
    reset_circuit_breaker,
    get_synthesis_engine,
    get_circuit_breaker,
    get_cache,
)
from src.models import SpeechRequest
from src.cache.redis_cache import RedisCache, CacheConfig


# Unit tests for helper functions (no I/O)
class TestGetEffectiveVoice:
    def test_explicit_voice(self):
        """request.voice overrides everything."""
        req = SpeechRequest(model="kokoro", input="hello", voice="af_heart")
        assert get_effective_voice(req) == "af_heart"

    def test_model_mapping(self):
        """MODEL_MAP lookup for known model."""
        req = SpeechRequest(model="tts-1", input="hello")
        voice = get_effective_voice(req)
        assert isinstance(voice, str)
        assert len(voice) > 0

    def test_default_voice(self):
        """Unknown model + no voice → DEFAULT_VOICE."""
        req = SpeechRequest(model="unknown-model", input="hello")
        voice = get_effective_voice(req)
        assert voice is not None

    def test_empty_voice_stays_none(self):
        """Voice param present but empty → fallback."""
        req = SpeechRequest(model="kokoro", input="hello", voice="")
        assert isinstance(get_effective_voice(req), str)


class TestGetEffectiveSpeed:
    def test_explicit_speed(self):
        """request.speed is used when provided."""
        req = SpeechRequest(model="kokoro", input="hello", speed=1.5)
        assert get_effective_speed(req) == 1.5

    def test_none_speed(self):
        """speed=None → DEFAULT_SPEED."""
        req = SpeechRequest(model="kokoro", input="hello", speed=None)
        speed = get_effective_speed(req)
        assert speed == 1.0  # DEFAULT_SPEED from config

    def test_speed_bounds(self):
        """Speed value is returned as-is."""
        req = SpeechRequest(model="kokoro", input="hello", speed=0.8)
        assert get_effective_speed(req) == 0.8


class TestRouterSetup:
    def test_router_prefix(self):
        """Router has /v1/proxy prefix."""
        assert router.prefix == "/v1/proxy"

    def test_speech_endpoint_registered(self):
        """POST /v1/proxy/speech is in routes."""
        paths = [r.path for r in router.routes]
        assert "/v1/proxy/speech" in paths


class TestGetSynthesisEngine:
    def test_returns_synthesis_engine(self):
        """get_synthesis_engine() returns an engine instance."""
        engine = get_synthesis_engine()
        assert engine is not None


class TestGetCircuitBreaker:
    def test_returns_circuit_breaker(self):
        """get_circuit_breaker() returns a breaker instance."""
        breaker = get_circuit_breaker()
        assert breaker is not None


class TestGetCache:
    def test_returns_redis_cache(self):
        """get_cache() returns a RedisCache instance."""
        cache = get_cache()
        assert isinstance(cache, RedisCache)


class TestListVoices:
    @pytest.mark.asyncio
    async def test_returns_fallback_on_error(self):
        """list_voices() falls back gracefully on error."""
        with patch("src.routers.speech.KOKORO_VOICES_URL", "http://test/api/voices"):
            with patch("httpx.AsyncClient") as mock_client:
                mock_instance = AsyncMock()
                mock_instance.__aenter__.side_effect = OSError("network error")
                mock_client.return_value = mock_instance

                result = await list_voices()
                assert "voices" in result
                assert result.get("fallback") is True


class TestCircuitBreakerEndpoints:
    @pytest.mark.asyncio
    async def test_circuit_breaker_health(self):
        """circuit_breaker_health() returns breaker stats."""
        result = await circuit_breaker_health()
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_reset_circuit_breaker(self):
        """reset_circuit_breaker() resets and returns stats."""
        result = await reset_circuit_breaker()
        assert "status" in result
        assert result["status"] == "reset"


class TestGenerateSpeechValidation:
    @pytest.mark.asyncio
    async def test_empty_input_raises(self):
        """Empty input text raises HTTP 400."""
        from fastapi import HTTPException

        req = SpeechRequest(model="kokoro", input="", voice="zf_xiaoxiao")
        try:
            await generate_speech(req)
            pytest.fail("Should have raised HTTPException")
        except HTTPException as e:
            assert e.status_code == 400

    @pytest.mark.asyncio
    async def test_whitespace_only_input_raises(self):
        """Whitespace-only input raises HTTP 400."""
        from fastapi import HTTPException

        req = SpeechRequest(model="kokoro", input="   ", voice="zf_xiaoxiao")
        try:
            await generate_speech(req)
            pytest.fail("Should have raised HTTPException")
        except HTTPException as e:
            assert e.status_code == 400

    @pytest.mark.asyncio
    async def test_input_too_long_raises(self):
        """Input over 5000 chars raises HTTP 400."""
        from fastapi import HTTPException

        req = SpeechRequest(model="kokoro", input="a" * 5001, voice="zf_xiaoxiao")
        try:
            await generate_speech(req)
            pytest.fail("Should have raised HTTPException")
        except HTTPException as e:
            assert e.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])