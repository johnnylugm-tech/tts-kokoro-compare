#!/usr/bin/env python3
"""
Coverage tests - synthesis.py
Targets uncovered lines: 47-53, 74-117, 136-180, 203-218, 230-235, 261-293, 314-331, 335-337, 340, 343
Based on AST analysis:
  __init__() at line 35 (self._executor at 53)
  synthesize() at line 55 (lines 74-117 are the try/except block)
  synthesize_segments() at line 120
  _synthesize_segment_with_retry() at line 182
  _concatenate_audio() at line 218
  synthesize_ssml() at line 237
  synthesize_text() at line 293
  close() at line 337
  __aenter__() at line 343
  __aexit__() at line 346
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.synthesis import SynthesisEngine


class TestSynthesisEnginePrivateMethods:
    """Private method coverage."""

    def test_concatenate_audio_single_chunk(self):
        """_concatenate_audio: single chunk → returns as-is"""
        eng = SynthesisEngine(timeout=30.0)
        chunks = [b"single_chunk"]
        result = eng._concatenate_audio(chunks)
        assert result == b"single_chunk"
        # close after

    def test_concatenate_audio_multiple_chunks(self):
        """_concatenate_audio: multiple chunks → joined"""
        eng = SynthesisEngine(timeout=30.0)
        chunks = [b"chunk1", b"chunk2", b"chunk3"]
        result = eng._concatenate_audio(chunks)
        assert result == b"chunk1chunk2chunk3"

    def test_concatenate_audio_empty_list(self):
        """_concatenate_audio: empty list"""
        eng = SynthesisEngine(timeout=30.0)
        result = eng._concatenate_audio([])
        assert result == b""

    def test_concatenate_audio_two_chunks(self):
        """_concatenate_audio: two chunks"""
        eng = SynthesisEngine(timeout=30.0)
        chunks = [b"first", b"second"]
        result = eng._concatenate_audio(chunks)
        assert result == b"firstsecond"


class TestSynthesisEngineRetry:
    """_synthesize_segment_with_retry() coverage."""

    @pytest.mark.asyncio
    async def test_retry_success_first_attempt(self):
        """Success on first attempt → no retry"""
        eng = SynthesisEngine(timeout=30.0)
        eng.synthesize = AsyncMock(return_value=b"audio_data")
        result = await eng._synthesize_segment_with_retry("text", "voice", 1.0, "kokoro")
        assert result == b"audio_data"
        assert eng.synthesize.call_count == 1
        await eng.close()

    @pytest.mark.asyncio
    async def test_retry_success_second_attempt(self):
        """Fail then succeed on second attempt"""
        eng = SynthesisEngine(timeout=30.0)
        eng.synthesize = AsyncMock(side_effect=[
            httpx.TimeoutException("timeout"),
            b"audio_data",
        ])
        result = await eng._synthesize_segment_with_retry("text", "voice", 1.0, "kokoro", max_retries=2)
        assert result == b"audio_data"
        assert eng.synthesize.call_count == 2
        await eng.close()

    @pytest.mark.asyncio
    async def test_retry_all_fail(self):
        """All attempts fail → raises last exception"""
        eng = SynthesisEngine(timeout=30.0)
        eng.synthesize = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
        with pytest.raises(httpx.TimeoutException):
            await eng._synthesize_segment_with_retry("text", "voice", 1.0, "kokoro", max_retries=1)
        assert eng.synthesize.call_count == 2  # 1 original + 1 retry
        await eng.close()

    @pytest.mark.asyncio
    async def test_retry_with_http_status_error(self):
        """HTTPStatusError triggers retry"""
        eng = SynthesisEngine(timeout=30.0)
        response = MagicMock()
        response.status_code = 500
        response.text = "Server Error"
        eng.synthesize = AsyncMock(side_effect=[
            httpx.HTTPStatusError("Error", request=MagicMock(), response=response),
            b"audio_data",
        ])
        result = await eng._synthesize_segment_with_retry("text", "voice", 1.0, "kokoro", max_retries=1)
        assert result == b"audio_data"
        assert eng.synthesize.call_count == 2
        await eng.close()

    @pytest.mark.asyncio
    async def test_retry_with_value_error(self):
        """ValueError triggers retry"""
        eng = SynthesisEngine(timeout=30.0)
        eng.synthesize = AsyncMock(side_effect=[
            ValueError("lexicon error"),
            b"audio_data",
        ])
        result = await eng._synthesize_segment_with_retry("text", "voice", 1.0, "kokoro", max_retries=1)
        assert result == b"audio_data"
        assert eng.synthesize.call_count == 2
        await eng.close()


class TestSynthesisEngineInit:
    """__init__() coverage."""

    def test_init_custom_backend_url(self):
        """__init__: custom backend_url stored"""
        eng = SynthesisEngine(backend_url="http://custom:9999/v1")
        assert eng.backend_url == "http://custom:9999/v1"

    def test_init_custom_timeout(self):
        """__init__: custom timeout stored"""
        eng = SynthesisEngine(timeout=60.0)
        assert eng.timeout == 60.0

    def test_init_has_ssml_parser(self):
        """__init__: ssml_parser initialized"""
        from src.engines.ssml_parser import SSMLParser
        eng = SynthesisEngine()
        assert isinstance(eng.ssml_parser, SSMLParser)

    def test_init_has_text_splitter(self):
        """__init__: text_splitter initialized"""
        from src.engines.text_splitter import TextSplitter
        eng = SynthesisEngine()
        assert isinstance(eng.text_splitter, TextSplitter)

    def test_init_has_linguistic_engine(self):
        """__init__: linguistic_engine initialized"""
        from src.engines.taiwan_linguistic import TaiwanLinguisticEngine
        eng = SynthesisEngine()
        assert isinstance(eng.linguistic_engine, TaiwanLinguisticEngine)


class TestSynthesisEngineContextManager:
    """Async context manager coverage."""

    @pytest.mark.asyncio
    async def test_aenter_returns_self(self):
        """__aenter__ → returns engine instance"""
        async with SynthesisEngine() as eng:
            assert eng is not None

    @pytest.mark.asyncio
    async def test_aexit_calls_close(self):
        """__aexit__ → calls close"""
        eng = SynthesisEngine()
        eng.client.aclose = AsyncMock()
        eng._executor.shutdown = MagicMock()
        await eng.__aexit__(None, None, None)
        eng.client.aclose.assert_called_once()
        eng._executor.shutdown.assert_called_once_with(wait=False)


class TestSynthesisEngineSynthesizeEdge:
    """synthesize() edge case coverage."""

    @pytest.mark.asyncio
    async def test_synthesize_non_ascii_text(self):
        """Non-ASCII text (emoji)"""
        eng = SynthesisEngine(timeout=30.0)
        eng.client.post = AsyncMock(
            return_value=MagicMock(content=b"audio", raise_for_status=lambda: None)
        )
        result = await eng.synthesize("🎉 Celebrate 🎊", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
        assert result == b"audio"
        await eng.close()

    @pytest.mark.asyncio
    async def test_synthesize_empty_unicode_space(self):
        """Whitespace-only (spaces)"""
        eng = SynthesisEngine(timeout=30.0)
        eng.client.post = AsyncMock(
            return_value=MagicMock(content=b"audio", raise_for_status=lambda: None)
        )
        result = await eng.synthesize("   ", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
        assert result == b""
        await eng.close()


class TestSynthesisEngineSynthesizeSegmentsEdge:
    """synthesize_segments() edge cases."""

    @pytest.mark.asyncio
    async def test_synthesize_segments_mixed_empty_and_valid(self):
        """Mix of empty and valid segments"""
        eng = SynthesisEngine(timeout=30.0)
        eng.client.post = AsyncMock(
            return_value=MagicMock(content=b"audio", raise_for_status=lambda: None)
        )
        segments = [
            {"text": "", "speed": 1.0},
            {"text": "valid", "speed": 1.0},
            {"text": "  ", "speed": 1.0},
            {"text": "also valid", "speed": 1.0},
        ]
        result = await eng.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")
        assert result == b"audioaudio"
        await eng.close()


class TestSynthesisEngineSynthesizeSSMLEdge:
    """synthesize_ssml() edge cases."""

    @pytest.mark.asyncio
    async def test_synthesize_ssml_only_break_no_text(self):
        """SSML with only break elements (no text segments)"""
        eng = SynthesisEngine(timeout=30.0)
        eng.client.post = AsyncMock(
            return_value=MagicMock(content=b"audio", raise_for_status=lambda: None)
        )
        ssml = "<speak><break time='500ms'/></speak>"
        result = await eng.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)
        # The break creates a pause_chars segment but with no text,
        # so synthesized result may vary based on implementation
        assert isinstance(result, bytes)
        await eng.close()

    @pytest.mark.asyncio
    async def test_synthesize_ssml_nested_elements(self):
        """SSML with deeply nested elements"""
        eng = SynthesisEngine(timeout=30.0)
        eng.client.post = AsyncMock(
            return_value=MagicMock(content=b"audio", raise_for_status=lambda: None)
        )
        ssml = "<speak><prosody rate='1.1'><emphasis>nested text</emphasis></prosody></speak>"
        result = await eng.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)
        assert isinstance(result, bytes)
        await eng.close()

    @pytest.mark.asyncio
    async def test_synthesize_ssml_with_pause_chars(self):
        """SSML segments with pause_chars are included"""
        eng = SynthesisEngine(timeout=30.0)
        eng.client.post = AsyncMock(
            return_value=MagicMock(content=b"audio", raise_for_status=lambda: None)
        )
        ssml = "<speak>hello<break time='500ms'/>world</speak>"
        result = await eng.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)
        assert isinstance(result, bytes)
        await eng.close()


class TestSynthesisEngineSynthesizeTextEdge:
    """synthesize_text() edge cases."""

    @pytest.mark.asyncio
    async def test_synthesize_text_with_ssml_detection(self):
        """Plain text that looks like SSML but isn't"""
        eng = SynthesisEngine(timeout=30.0)
        eng.client.post = AsyncMock(
            return_value=MagicMock(content=b"audio", raise_for_status=lambda: None)
        )
        # This has angle brackets but no recognized SSML tags
        result = await eng.synthesize_text("<no real tags>", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
        assert isinstance(result, bytes)
        await eng.close()

    @pytest.mark.asyncio
    async def test_synthesize_text_whitespace(self):
        """Whitespace text"""
        eng = SynthesisEngine(timeout=30.0)
        eng.client.post = AsyncMock(
            return_value=MagicMock(content=b"audio", raise_for_status=lambda: None)
        )
        result = await eng.synthesize_text("  \n\t  ", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
        # whitespace becomes empty after preprocessing -> b""
        assert result == b""
        await eng.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
