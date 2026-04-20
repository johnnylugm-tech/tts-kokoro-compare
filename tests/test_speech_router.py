"""Test speech router endpoints."""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.routers.speech import (
    get_effective_voice,
    get_effective_speed,
    router,
)
from src.models import SpeechRequest

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
        # Empty string is falsy → falls back to model map or default
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])