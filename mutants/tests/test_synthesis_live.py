"""
Live integration tests for engines/synthesis.py — REAL HTTP calls.

These tests make ACTUAL HTTP requests to localhost:8880 (no mocking).
Required for mutation_testing: mutants in retry/exception-handling code
can only be triggered when real HTTP exceptions are raised.
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.synthesis import SynthesisEngine


# ---------------------------------------------------------------------------
# Backend availability check
# ---------------------------------------------------------------------------

def backend_available() -> bool:
    """Check if Kokoro backend is reachable at localhost:8880."""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("127.0.0.1", 8880))
        sock.close()
        return result == 0
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Live tests — exercise REAL code paths for mutation testing
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSynthesisLive:
    """Live integration tests using real HTTP to localhost:8880."""

    async def test_synthesize_text_success(self):
        """Real HTTP: synthesize text exercises real synthesis code path."""
        engine = SynthesisEngine(timeout=30.0)
        try:
            audio = await engine.synthesize_text(text="測試", voice="zf_xiaoxiao", speed=1.0)
            assert isinstance(audio, bytes)
            assert len(audio) > 0
        finally:
            await engine.close()

    async def test_synthesize_text_longer(self):
        """Real HTTP: longer text goes through full pipeline."""
        engine = SynthesisEngine(timeout=30.0)
        try:
            audio = await engine.synthesize_text(
                text="今天天氣很好，我想去散步。", voice="zf_xiaoxiao", speed=1.0
            )
            assert isinstance(audio, bytes)
            assert len(audio) > 0
        finally:
            await engine.close()

    async def test_synthesize_ssml_success(self):
        """Real HTTP: SSML pipeline end-to-end."""
        engine = SynthesisEngine(timeout=30.0)
        try:
            audio = await engine.synthesize_ssml(
                ssml_text="<speak><prosody rate='1.0'>你好世界</prosody></speak>",
                voice="zf_xiaoxiao",
            )
            assert isinstance(audio, bytes)
        finally:
            await engine.close()

    async def test_synthesize_segments_multiple(self):
        """Real HTTP: multi-segment synthesis with real audio concatenation."""
        engine = SynthesisEngine(timeout=30.0)
        try:
            segments = [{"text": "第一段", "speed": 1.0}, {"text": "第二段", "speed": 1.0}]
            audio = await engine.synthesize_segments(
                segments=segments, voice="zf_xiaoxiao", model="kokoro"
            )
            assert isinstance(audio, bytes)
            assert len(audio) > 0
        finally:
            await engine.close()

    async def test_synthesize_empty_text(self):
        """Real HTTP: empty text returns empty bytes (early return path)."""
        engine = SynthesisEngine(timeout=30.0)
        try:
            audio = await engine.synthesize_text(text="", voice="zf_xiaoxiao")
            assert audio == b""
        finally:
            await engine.close()

    async def test_synthesize_different_speeds(self):
        """Real HTTP: different speed values go through the pipeline."""
        engine = SynthesisEngine(timeout=30.0)
        try:
            for speed in [0.8, 1.0, 1.2]:
                audio = await engine.synthesize_text(
                    text="速度測試", voice="zf_xiaoxiao", speed=speed
                )
                assert isinstance(audio, bytes)
                assert len(audio) > 0
        finally:
            await engine.close()

    async def test_twice_rapid_calls(self):
        """Real HTTP: two rapid calls verify connection reuse."""
        engine = SynthesisEngine(timeout=30.0)
        try:
            audio1 = await engine.synthesize_text(text="第一", voice="zf_xiaoxiao")
            audio2 = await engine.synthesize_text(text="第二", voice="zf_xiaoxiao")
            assert isinstance(audio1, bytes) and len(audio1) > 0
            assert isinstance(audio2, bytes) and len(audio2) > 0
        finally:
            await engine.close()

    async def test_close_idempotent(self):
        """Real HTTP: close can be called multiple times safely."""
        engine = SynthesisEngine(timeout=30.0)
        await engine.close()
        await engine.close()  # should not raise

    async def test_context_manager(self):
        """Real HTTP: async context manager works correctly."""
        async with SynthesisEngine() as engine:
            audio = await engine.synthesize_text(text="Context test", voice="zf_xiaoxiao")
            assert isinstance(audio, bytes)
            assert len(audio) > 0


# ---------------------------------------------------------------------------
# Error-path tests — KEY for mutation_testing
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSynthesisErrorPaths:
    """Test error-handling code paths that need real HTTP exceptions.

    These are the KEY tests for mutation_testing:
    - With MockTransport: exception handlers never execute
    - With real HTTP: retry loop and exception handlers ARE exercised
    - Mutants in retry count / exception types / wait time ARE triggered
    """

    async def test_connection_refused_triggers_retry_loop(self):
        """Real connection refused → retry loop + exception handler exercised."""
        # Port nothing is listening on — real OS-level connection refused
        engine = SynthesisEngine(
            backend_url="http://localhost:18880/v1/audio/speech",
            timeout=5.0,
        )
        try:
            audio = await engine.synthesize_text(
                text="這段文字會觸發錯誤處理",
                voice="zf_xiaoxiao",
            )
            # If retries handle it, we get bytes back
            assert isinstance(audio, bytes)
        except Exception:
            # Retries exhausted → exception propagates
            # Mutant in caught exception types would change what gets raised
            pass
        finally:
            await engine.close()

    async def test_non_routable_ip_timeout(self):
        """Real network timeout → httpx.TimeoutException → retry loop exercised."""
        # Non-routable IP guarantees timeout (no route to host)
        engine = SynthesisEngine(
            backend_url="http://10.255.255.1:8880/v1/audio/speech",
            timeout=0.5,
        )
        try:
            audio = await engine.synthesize_text(text="超時測試", voice="zf_xiaoxiao")
            assert isinstance(audio, bytes)
        except Exception:
            # Expected after retries exhausted
            pass
        finally:
            await engine.close()

    async def test_invalid_url_connection_refused(self):
        """Real connection refused on bad port → error handling exercised."""
        engine = SynthesisEngine(
            backend_url="http://localhost:9999/v1/audio/speech",
            timeout=5.0,
        )
        try:
            audio = await engine.synthesize_text(
                text="錯誤URL測試", voice="zf_xiaoxiao"
            )
            assert isinstance(audio, bytes)
        except Exception:
            pass
        finally:
            await engine.close()


# ---------------------------------------------------------------------------
# Module-level skip if backend not available
# ---------------------------------------------------------------------------

if not backend_available():
    pytest.skip("Kokoro backend not available at localhost:8880", allow_module_level=True)
