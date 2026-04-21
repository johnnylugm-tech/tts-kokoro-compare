"""Synthesis Engine - handles TTS synthesis with parallel processing."""

import asyncio
import logging
from typing import List, Dict, Optional, Any
from concurrent.futures import ThreadPoolExecutor

import httpx

from ..config import (
    KOKORO_BACKEND_URL,
    DEFAULT_VOICE,
    DEFAULT_SPEED,
    REQUEST_TIMEOUT,
)
from .text_splitter import TextSplitter
from .ssml_parser import SSMLParser
from .taiwan_linguistic import TaiwanLinguisticEngine

logger = logging.getLogger(__name__)


class SynthesisEngine:
    """
    TTS Synthesis Engine with parallel processing support.

    Handles:
    - Single segment synthesis
    - Multi-segment parallel synthesis
    - SSML parsing and synthesis
    - Audio concatenation
    """

    def __init__(
        self,
        backend_url: str = KOKORO_BACKEND_URL,
        timeout: float = REQUEST_TIMEOUT,
    ):
        """
        Initialize synthesis engine.

        Args:
            backend_url: URL of the Kokoro TTS backend
            timeout: Request timeout in seconds
        """
        self.backend_url = backend_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        self.text_splitter = TextSplitter()
        self.ssml_parser = SSMLParser()
        self.linguistic_engine = TaiwanLinguisticEngine()
        self._executor = ThreadPoolExecutor(max_workers=4)

    async def synthesize(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
        model: str = "kokoro",
    ) -> bytes:
        """
        Synthesize a single text segment.

        Args:
            text: Text to synthesize
            voice: Voice to use
            speed: Speech speed multiplier
            model: Model identifier

        Returns:
            Raw audio bytes
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to synthesize")
            return b""

        logger.info(f"Synthesizing text (len={len(text)}, voice={voice}, speed={speed})")

        try:
            # Apply Taiwan linguistic processing
            processed_text = self.linguistic_engine.preprocess_for_tts(text)

            # Prepare request payload (OpenAI-compatible format)
            payload = {
                "model": model,
                "input": processed_text,
                "voice": voice,
                "speed": speed,
            }

            # Make request to backend
            response = await self.client.post(
                self.backend_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            response.raise_for_status()

            audio_data = response.content
            logger.debug(f"Received audio data: {len(audio_data)} bytes")

            return audio_data

        except httpx.TimeoutException:
            logger.error(f"Request timeout for text: {text[:50]}...")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during synthesis: {e}")
            raise
        except (ValueError, IOError, OSError) as e:
            logger.error(f"Unexpected error during synthesis: {e}")
            raise

    async def synthesize_segments(
        self,
        segments: List[Dict[str, Any]],
        voice: str = DEFAULT_VOICE,
        model: str = "kokoro",
    ) -> bytes:
        """
        Synthesize multiple segments in parallel and concatenate.

        Args:
            segments: List of dicts with "text" and optional "speed"
            voice: Voice to use for all segments
            model: Model identifier

        Returns:
            Concatenated audio bytes
        """
        if not segments:
            return b""

        # Prepare tasks for parallel execution
        tasks = []
        for i, seg in enumerate(segments):
            text = seg.get("text", "")
            speed = seg.get("speed", DEFAULT_SPEED)

            if text and text.strip():
                logger.debug(f"Queuing segment {i}: {text[:30]}... (speed={speed})")
                tasks.append(
                    self._synthesize_segment_with_retry(text, voice, speed, model)
                )

        if not tasks:
            return b""

        # Execute all syntheses in parallel
        logger.info(f"Starting parallel synthesis of {len(tasks)} segments")
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        audio_chunks: List[bytes] = []
        errors: List[str] = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Segment {i} failed: {result}")
                errors.append(f"Segment {i}: {str(result)}")
            elif isinstance(result, bytes) and result:
                audio_chunks.append(result)
            elif isinstance(result, Exception):
                errors.append(f"Segment {i}: {type(result).__name__}")

        if not audio_chunks:
            error_msg = f"All segments failed: {'; '.join(errors)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Concatenate audio chunks
        final_audio = self._concatenate_audio(audio_chunks)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")

        return final_audio

    async def _synthesize_segment_with_retry(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        max_retries: int = 2,
    ) -> bytes:
        """
        Synthesize a segment with retry logic.

        Args:
            text: Text to synthesize
            voice: Voice to use
            speed: Speech speed
            model: Model identifier
            max_retries: Maximum retry attempts

        Returns:
            Audio bytes
        """
        last_error: Optional[Exception] = None

        for attempt in range(max_retries + 1):
            try:
                return await self.synthesize(text, voice, speed, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)

        raise last_error or RuntimeError("Synthesis failed")

    def _concatenate_audio(self, chunks: List[bytes]) -> bytes:
        """
        Concatenate multiple audio chunks.

        Args:
            chunks: List of audio byte chunks

        Returns:
            Concatenated audio bytes
        """
        if len(chunks) == 1:
            return chunks[0]

        # Simple concatenation for MP3
        # Note: For production, could use pydub for crossfade
        return b"".join(chunks)

    async def synthesize_ssml(
        self,
        ssml_text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
    ) -> bytes:
        """
        Complete SSML processing pipeline.

        Pipeline:
        1. Parse SSML
        2. Apply Taiwan linguistic processing
        3. Split into segments
        4. Parallel synthesis
        5. Concatenate audio

        Args:
            ssml_text: SSML markup string
            voice: Voice to use
            speed: Default speech speed

        Returns:
            Final audio bytes
        """
        logger.info(f"Processing SSML (len={len(ssml_text)}, voice={voice})")

        # Step 1: Parse SSML
        parsed = self.ssml_parser.parse(ssml_text)

        if parsed.is_ssml and parsed.segments:
            # Use parsed segments with speed adjustments
            segments = []
            for seg in parsed.segments:
                if seg.text.strip():
                    segments.append({
                        "text": seg.text,
                        "speed": seg.speed if seg.speed else speed,
                        "pause_chars": seg.pause_chars,
                    })
        else:
            # Fallback: treat as plain text
            text = parsed.input_text if parsed.input_text else ssml_text

            # Step 2: Apply Taiwan linguistic processing
            processed = self.linguistic_engine.preprocess_for_tts(text)

            # Step 3: Split into segments
            split_segments = self.text_splitter.split(processed)

            segments = [{"text": seg, "speed": speed} for seg in split_segments]

        if not segments:
            logger.warning("No segments to synthesize")
            return b""

        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def synthesize_text(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
        model: str = "kokoro",
    ) -> bytes:
        """
        Synthesize plain text with full processing pipeline.

        Args:
            text: Plain text to synthesize
            voice: Voice to use
            speed: Speech speed
            model: Model identifier

        Returns:
            Audio bytes
        """
        logger.info(f"Synthesizing text (len={len(text)}, voice={voice}, speed={speed})")

        # Check if SSML
        if self.ssml_parser.is_ssml(text):
            return await self.synthesize_ssml(text, voice, speed)

        # Apply Taiwan linguistic processing
        processed = self.linguistic_engine.preprocess_for_tts(text)

        # Split into segments
        segments = self.text_splitter.split(processed)

        if not segments:
            return b""

        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def close(self):
        """Close the HTTP client and cleanup resources."""
        await self.client.aclose()
        self._executor.shutdown(wait=False)
        logger.info("SynthesisEngine closed")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
