#!/usr/bin/env python3
# Copyright (c) 2026 Johnny Lu. Licensed under MIT License.
"""
Audio Converter - FFmpeg-based audio format conversion (FR-08)

Provides MP3 to WAV conversion and other audio format transformations.
"""

import logging
import shutil
import subprocess  # nosec B404
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Check for ffmpeg availability
FFMPEG_PATH: Optional[str] = shutil.which("ffmpeg")


def is_ffmpeg_available() -> bool:
    """Check if ffmpeg is available on the system."""
    return FFMPEG_PATH is not None


def get_ffmpeg_path() -> str:
    """
    Get ffmpeg executable path.

    Returns:
        Path to ffmpeg executable

    Raises:
        RuntimeError: If ffmpeg is not found
    """
    if FFMPEG_PATH is None:
        raise RuntimeError(
            "ffmpeg not found in PATH. Please install ffmpeg: "
            "brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
        )
    return FFMPEG_PATH


def convert_mp3_to_wav(input_path: str, output_path: str) -> bool:
    """
    Convert MP3 audio file to WAV format using ffmpeg.

    Uses ffmpeg with PCM 16-bit little-endian codec for maximum compatibility.

    Args:
        input_path: Path to input MP3 file
        output_path: Path to output WAV file

    Returns:
        True if conversion succeeded, False otherwise
    """
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        logger.error("Input file not found: %s", input_path)
        return False

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        ffmpeg = get_ffmpeg_path()

        # Run ffmpeg conversion
        # -i: input file
        # -acodec pcm_s16le: PCM 16-bit little-endian
        # -ar 44100: sample rate 44100 Hz
        # -ac 2: stereo
        result = subprocess.run(  # nosec

            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            logger.error("ffmpeg conversion failed: %s", result.stderr)
            return False

        logger.debug("Converted %s -> %s", input_file, output_file)
        return True

    except RuntimeError as e:
        logger.error("ffmpeg not available: %s", e)
        return False
    except subprocess.SubprocessError as e:
        logger.error("Subprocess error during conversion: %s", e)
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error("Unexpected error during conversion: %s", e)
        return False


def convert_wav_to_mp3(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
    """
    Convert WAV audio file to MP3 format using ffmpeg.

    Args:
        input_path: Path to input WAV file
        output_path: Path to output MP3 file
        bitrate: MP3 bitrate (default: 192k)

    Returns:
        True if conversion succeeded, False otherwise
    """
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        logger.error("Input file not found: %s", input_path)
        return False

    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        ffmpeg = get_ffmpeg_path()

        result = subprocess.run(  # nosec B603
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            logger.error("ffmpeg conversion failed: %s", result.stderr)
            return False

        return True

    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error("Unexpected error during WAV->MP3 conversion: %s", e)
        return False


def get_audio_info(file_path: str) -> Optional[dict]:
    """
    Get audio file information using ffprobe.

    Args:
        file_path: Path to audio file

    Returns:
        Dictionary with audio info (duration, bitrate, format) or None
    """
    import json

    ffprobe_path = shutil.which("ffprobe")
    if ffprobe_path is None:
        return None

    try:
        result = subprocess.run(  # nosec B603
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(file_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)

        # Extract relevant info
        info = {
            "format": data.get("format", {}).get("format_name"),
            "duration": float(data.get("format", {}).get("duration", 0)),
            "bitrate": data.get("format", {}).get("bit_rate"),
            "size": int(data.get("format", {}).get("size", 0)),
        }

        # Audio stream info
        audio_stream = next(
            (s for s in data.get("streams", []) if s.get("codec_type") == "audio"),
            None,
        )

        if audio_stream:
            info.update({
                "codec": audio_stream.get("codec_name"),
                "sample_rate": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })

        return info

    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug("Could not get audio info: %s", e)
        return None
