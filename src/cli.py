#!/usr/bin/env python3
# Copyright (c) 2026 Johnny Lu. Licensed under MIT License.
"""
CLI Tool for Kokoro Taiwan TTS - FR-07

Usage:
    tts-v610 "你好世界" -o output.mp3
    tts-v610 "你好世界" -v "zf_xiaoxiao(0.8)+af_heart(0.2)" -o output.mp3
    tts-v610 --ssml "<speak>...</speak>" -o output.mp3
    tts-v610 --file input.txt -o output/
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from src.config import (
    DEFAULT_VOICE,
    DEFAULT_SPEED,
    KOKORO_BACKEND_URL,
)
from src.engines.synthesis import SynthesisEngine
from src.audio_converter import convert_mp3_to_wav

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
        description="Kokoro Taiwan TTS CLI - 繁體中文語音合成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    tts-v610 "你好世界" -o output.mp3
    tts-v610 "你好世界" -v "zf_xiaoxiao(0.8)+af_heart(0.2)" -o output.mp3
    tts-v610 --ssml "<speak><prosody rate='0.9'>你好</prosody></speak>" -o output.mp3
    tts-v610 --file input.txt -o output/
    tts-v610 "快速語音" -s 1.5 -f wav -o output.wav
        """,
    )

    parser.add_argument(
        "-i", "--input",
        type=str,
        default=None,
        help="Input text or SSML markup (use --ssml flag for SSML mode)",
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="Output file path or directory (with -f for wav)",
    )

    parser.add_argument(
        "-v", "--voice",
        type=str,
        default=DEFAULT_VOICE,
        help=f"Voice or blend recipe (default: {DEFAULT_VOICE})",
    )

    parser.add_argument(
        "-s", "--speed",
        type=float,
        default=DEFAULT_SPEED,
        choices=[round(x * 0.1, 1) for x in range(5, 21)],
        help=f"Speech speed 0.5-2.0 (default: {DEFAULT_SPEED})",
    )

    parser.add_argument(
        "-f", "--format",
        type=str,
        default="mp3",
        choices=["mp3", "wav"],
        help="Output audio format (default: mp3)",
    )

    parser.add_argument(
        "--ssml",
        action="store_true",
        help="Treat input as SSML markup",
    )

    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Input file path (reads text from file)",
    )

    parser.add_argument(
        "--backend",
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )

    return parser.parse_args()


def read_input(args: argparse.Namespace) -> str:
    """
    Read input text from CLI argument, file, or stdin.

    Args:
        args: Parsed command line arguments

    Returns:
        Input text string

    Raises:
        ValueError: If no input provided
    """
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    if args.input is not None:
        return args.input.strip()

    if not sys.stdin.isatty():
        return sys.stdin.read().strip()

    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


async def synthesize(
    engine: SynthesisEngine,
    text: str,
    voice: str,
    speed: float,
    is_ssml: bool,
) -> bytes:
    """
    Synthesize audio from text.

    Args:
        engine: SynthesisEngine instance
        text: Input text or SSML
        voice: Voice to use
        speed: Speech speed
        is_ssml: Whether input is SSML

    Returns:
        Audio bytes
    """
    logger.info("Synthesizing (voice=%s, speed=%s, ssml=%s)", voice, speed, is_ssml)
    logger.debug("Input text: %s%s", text[:100], "..." if len(text) > 100 else "")

    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    return await engine.synthesize_text(text, voice, speed)


def _resolve_output_path(output_arg: str, fmt: str) -> Path:
    """Resolve output path from CLI argument."""
    output_path = Path(output_arg)
    if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
        output_path = output_path / f"output.{fmt}"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def _write_audio(output_path: Path, audio_data: bytes, fmt: str) -> bool:
    """Write audio data to file, handling format conversion."""
    if fmt == "mp3":
        with open(output_path, "wb") as f:
            f.write(audio_data)
        return True
    # WAV: convert via temp MP3
    temp_mp3 = output_path.with_suffix(".mp3")
    with open(temp_mp3, "wb") as f:
        f.write(audio_data)
    success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
    if temp_mp3.exists():
        temp_mp3.unlink()
    return success


async def main_async(args: argparse.Namespace) -> int:
    """Async main entry point."""
    try:
        text = read_input(args)
        if not text:
            logger.error("Empty input provided")
            return 1

        output_path = _resolve_output_path(args.output, args.format)
        engine = SynthesisEngine(backend_url=args.backend)

        try:
            audio_data = await synthesize(engine, text, args.voice, args.speed, args.ssml)
            if not audio_data:
                logger.error("No audio data generated")
                return 1

            if not _write_audio(output_path, audio_data, args.format):
                logger.error("Audio write/conversion failed")
                return 1

            logger.info("Saved %s: %s", args.format.upper(), output_path)
            return 0

        finally:
            await engine.close()

    except FileNotFoundError as e:
        logger.error("File error: %s", e)
        return 1
    except ValueError as e:
        logger.error("Input error: %s", e)
        return 1
    except (IOError, OSError) as e:
        logger.error("Synthesis error: %s", e, exc_info=True)
        return 1



def main() -> int:
    """Main entry point."""
    args = parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
