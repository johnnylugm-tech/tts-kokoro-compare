#!/usr/bin/env python3
"""
Audio Converter - FFmpeg-based audio format conversion (FR-08)

Provides MP3 to WAV conversion and other audio format transformations.
"""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Check for ffmpeg availability
FFMPEG_PATH: Optional[str] = shutil.which("ffmpeg")
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def is_ffmpeg_available() -> bool:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_is_ffmpeg_available__mutmut_orig, x_is_ffmpeg_available__mutmut_mutants, args, kwargs, None)


def x_is_ffmpeg_available__mutmut_orig() -> bool:
    """Check if ffmpeg is available on the system."""
    return FFMPEG_PATH is not None


def x_is_ffmpeg_available__mutmut_1() -> bool:
    """Check if ffmpeg is available on the system."""
    return FFMPEG_PATH is None

x_is_ffmpeg_available__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_is_ffmpeg_available__mutmut_1': x_is_ffmpeg_available__mutmut_1
}
x_is_ffmpeg_available__mutmut_orig.__name__ = 'x_is_ffmpeg_available'


def get_ffmpeg_path() -> str:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_ffmpeg_path__mutmut_orig, x_get_ffmpeg_path__mutmut_mutants, args, kwargs, None)


def x_get_ffmpeg_path__mutmut_orig() -> str:
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


def x_get_ffmpeg_path__mutmut_1() -> str:
    """
    Get ffmpeg executable path.
    
    Returns:
        Path to ffmpeg executable
        
    Raises:
        RuntimeError: If ffmpeg is not found
    """
    if FFMPEG_PATH is not None:
        raise RuntimeError(
            "ffmpeg not found in PATH. Please install ffmpeg: "
            "brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
        )
    return FFMPEG_PATH


def x_get_ffmpeg_path__mutmut_2() -> str:
    """
    Get ffmpeg executable path.
    
    Returns:
        Path to ffmpeg executable
        
    Raises:
        RuntimeError: If ffmpeg is not found
    """
    if FFMPEG_PATH is None:
        raise RuntimeError(
            None
        )
    return FFMPEG_PATH


def x_get_ffmpeg_path__mutmut_3() -> str:
    """
    Get ffmpeg executable path.
    
    Returns:
        Path to ffmpeg executable
        
    Raises:
        RuntimeError: If ffmpeg is not found
    """
    if FFMPEG_PATH is None:
        raise RuntimeError(
            "XXffmpeg not found in PATH. Please install ffmpeg: XX"
            "brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
        )
    return FFMPEG_PATH


def x_get_ffmpeg_path__mutmut_4() -> str:
    """
    Get ffmpeg executable path.
    
    Returns:
        Path to ffmpeg executable
        
    Raises:
        RuntimeError: If ffmpeg is not found
    """
    if FFMPEG_PATH is None:
        raise RuntimeError(
            "ffmpeg not found in path. please install ffmpeg: "
            "brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
        )
    return FFMPEG_PATH


def x_get_ffmpeg_path__mutmut_5() -> str:
    """
    Get ffmpeg executable path.
    
    Returns:
        Path to ffmpeg executable
        
    Raises:
        RuntimeError: If ffmpeg is not found
    """
    if FFMPEG_PATH is None:
        raise RuntimeError(
            "FFMPEG NOT FOUND IN PATH. PLEASE INSTALL FFMPEG: "
            "brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
        )
    return FFMPEG_PATH


def x_get_ffmpeg_path__mutmut_6() -> str:
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
            "XXbrew install ffmpeg (macOS) or apt install ffmpeg (Linux)XX"
        )
    return FFMPEG_PATH


def x_get_ffmpeg_path__mutmut_7() -> str:
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
            "brew install ffmpeg (macos) or apt install ffmpeg (linux)"
        )
    return FFMPEG_PATH


def x_get_ffmpeg_path__mutmut_8() -> str:
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
            "BREW INSTALL FFMPEG (MACOS) OR APT INSTALL FFMPEG (LINUX)"
        )
    return FFMPEG_PATH

x_get_ffmpeg_path__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_ffmpeg_path__mutmut_1': x_get_ffmpeg_path__mutmut_1, 
    'x_get_ffmpeg_path__mutmut_2': x_get_ffmpeg_path__mutmut_2, 
    'x_get_ffmpeg_path__mutmut_3': x_get_ffmpeg_path__mutmut_3, 
    'x_get_ffmpeg_path__mutmut_4': x_get_ffmpeg_path__mutmut_4, 
    'x_get_ffmpeg_path__mutmut_5': x_get_ffmpeg_path__mutmut_5, 
    'x_get_ffmpeg_path__mutmut_6': x_get_ffmpeg_path__mutmut_6, 
    'x_get_ffmpeg_path__mutmut_7': x_get_ffmpeg_path__mutmut_7, 
    'x_get_ffmpeg_path__mutmut_8': x_get_ffmpeg_path__mutmut_8
}
x_get_ffmpeg_path__mutmut_orig.__name__ = 'x_get_ffmpeg_path'


def convert_mp3_to_wav(input_path: str, output_path: str) -> bool:
    args = [input_path, output_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_convert_mp3_to_wav__mutmut_orig, x_convert_mp3_to_wav__mutmut_mutants, args, kwargs, None)


def x_convert_mp3_to_wav__mutmut_orig(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_1(input_path: str, output_path: str) -> bool:
    """
    Convert MP3 audio file to WAV format using ffmpeg.
    
    Uses ffmpeg with PCM 16-bit little-endian codec for maximum compatibility.
    
    Args:
        input_path: Path to input MP3 file
        output_path: Path to output WAV file
        
    Returns:
        True if conversion succeeded, False otherwise
    """
    input_file = None
    output_file = Path(output_path)
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_2(input_path: str, output_path: str) -> bool:
    """
    Convert MP3 audio file to WAV format using ffmpeg.
    
    Uses ffmpeg with PCM 16-bit little-endian codec for maximum compatibility.
    
    Args:
        input_path: Path to input MP3 file
        output_path: Path to output WAV file
        
    Returns:
        True if conversion succeeded, False otherwise
    """
    input_file = Path(None)
    output_file = Path(output_path)
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_3(input_path: str, output_path: str) -> bool:
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
    output_file = None
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_4(input_path: str, output_path: str) -> bool:
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
    output_file = Path(None)
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_5(input_path: str, output_path: str) -> bool:
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
    
    if input_file.exists():
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_6(input_path: str, output_path: str) -> bool:
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
        logger.error(None)
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_7(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return True
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        # Run ffmpeg conversion
        # -i: input file
        # -acodec pcm_s16le: PCM 16-bit little-endian
        # -ar 44100: sample rate 44100 Hz
        # -ac 2: stereo
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_8(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=None, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        # Run ffmpeg conversion
        # -i: input file
        # -acodec pcm_s16le: PCM 16-bit little-endian
        # -ar 44100: sample rate 44100 Hz
        # -ac 2: stereo
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_9(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=None)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        # Run ffmpeg conversion
        # -i: input file
        # -acodec pcm_s16le: PCM 16-bit little-endian
        # -ar 44100: sample rate 44100 Hz
        # -ac 2: stereo
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_10(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    # Ensure output directory exists
    output_file.parent.mkdir(exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        # Run ffmpeg conversion
        # -i: input file
        # -acodec pcm_s16le: PCM 16-bit little-endian
        # -ar 44100: sample rate 44100 Hz
        # -ac 2: stereo
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_11(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, )
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        # Run ffmpeg conversion
        # -i: input file
        # -acodec pcm_s16le: PCM 16-bit little-endian
        # -ar 44100: sample rate 44100 Hz
        # -ac 2: stereo
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_12(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=False, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        # Run ffmpeg conversion
        # -i: input file
        # -acodec pcm_s16le: PCM 16-bit little-endian
        # -ar 44100: sample rate 44100 Hz
        # -ac 2: stereo
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_13(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=False)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        # Run ffmpeg conversion
        # -i: input file
        # -acodec pcm_s16le: PCM 16-bit little-endian
        # -ar 44100: sample rate 44100 Hz
        # -ac 2: stereo
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_14(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = None
        
        # Run ffmpeg conversion
        # -i: input file
        # -acodec pcm_s16le: PCM 16-bit little-endian
        # -ar 44100: sample rate 44100 Hz
        # -ac 2: stereo
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_15(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = None
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_16(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            None,
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_17(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=None,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_18(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            text=None,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_19(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            check=None,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_20(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_21(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_22(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_23(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_24(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "XX-iXX", str(input_file),
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_25(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-I", str(input_file),
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_26(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(None),
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_27(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "XX-acodecXX", "pcm_s16le",
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_28(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-ACODEC", "pcm_s16le",
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_29(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "XXpcm_s16leXX",
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_30(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "PCM_S16LE",
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_31(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "XX-arXX", "44100",
                "-ac", "2",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_32(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-AR", "44100",
                "-ac", "2",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_33(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "XX44100XX",
                "-ac", "2",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_34(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "XX-acXX", "2",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_35(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-AC", "2",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_36(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "XX2XX",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_37(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                "XX-yXX",  # Overwrite output file
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_38(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                "-Y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_39(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                "-y",  # Overwrite output file
                str(None),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_40(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                "-y",  # Overwrite output file
                str(output_file),
            ],
            capture_output=False,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_41(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            text=False,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_42(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            check=True,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_43(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
        
        if result.returncode == 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_44(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
        
        if result.returncode != 1:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_45(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(None)
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_46(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return True
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_47(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(None)
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_48(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return False
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_49(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(None)
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_50(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return True
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_51(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(None)
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_52(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return True
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False


def x_convert_mp3_to_wav__mutmut_53(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(None)
        return False


def x_convert_mp3_to_wav__mutmut_54(input_path: str, output_path: str) -> bool:
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
        logger.error(f"Input file not found: {input_path}")
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
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        logger.debug(f"Converted {input_file} -> {output_file}")
        return True
        
    except RuntimeError as e:
        logger.error(f"ffmpeg not available: {e}")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error during conversion: {e}")
        return False
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return True

x_convert_mp3_to_wav__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_convert_mp3_to_wav__mutmut_1': x_convert_mp3_to_wav__mutmut_1, 
    'x_convert_mp3_to_wav__mutmut_2': x_convert_mp3_to_wav__mutmut_2, 
    'x_convert_mp3_to_wav__mutmut_3': x_convert_mp3_to_wav__mutmut_3, 
    'x_convert_mp3_to_wav__mutmut_4': x_convert_mp3_to_wav__mutmut_4, 
    'x_convert_mp3_to_wav__mutmut_5': x_convert_mp3_to_wav__mutmut_5, 
    'x_convert_mp3_to_wav__mutmut_6': x_convert_mp3_to_wav__mutmut_6, 
    'x_convert_mp3_to_wav__mutmut_7': x_convert_mp3_to_wav__mutmut_7, 
    'x_convert_mp3_to_wav__mutmut_8': x_convert_mp3_to_wav__mutmut_8, 
    'x_convert_mp3_to_wav__mutmut_9': x_convert_mp3_to_wav__mutmut_9, 
    'x_convert_mp3_to_wav__mutmut_10': x_convert_mp3_to_wav__mutmut_10, 
    'x_convert_mp3_to_wav__mutmut_11': x_convert_mp3_to_wav__mutmut_11, 
    'x_convert_mp3_to_wav__mutmut_12': x_convert_mp3_to_wav__mutmut_12, 
    'x_convert_mp3_to_wav__mutmut_13': x_convert_mp3_to_wav__mutmut_13, 
    'x_convert_mp3_to_wav__mutmut_14': x_convert_mp3_to_wav__mutmut_14, 
    'x_convert_mp3_to_wav__mutmut_15': x_convert_mp3_to_wav__mutmut_15, 
    'x_convert_mp3_to_wav__mutmut_16': x_convert_mp3_to_wav__mutmut_16, 
    'x_convert_mp3_to_wav__mutmut_17': x_convert_mp3_to_wav__mutmut_17, 
    'x_convert_mp3_to_wav__mutmut_18': x_convert_mp3_to_wav__mutmut_18, 
    'x_convert_mp3_to_wav__mutmut_19': x_convert_mp3_to_wav__mutmut_19, 
    'x_convert_mp3_to_wav__mutmut_20': x_convert_mp3_to_wav__mutmut_20, 
    'x_convert_mp3_to_wav__mutmut_21': x_convert_mp3_to_wav__mutmut_21, 
    'x_convert_mp3_to_wav__mutmut_22': x_convert_mp3_to_wav__mutmut_22, 
    'x_convert_mp3_to_wav__mutmut_23': x_convert_mp3_to_wav__mutmut_23, 
    'x_convert_mp3_to_wav__mutmut_24': x_convert_mp3_to_wav__mutmut_24, 
    'x_convert_mp3_to_wav__mutmut_25': x_convert_mp3_to_wav__mutmut_25, 
    'x_convert_mp3_to_wav__mutmut_26': x_convert_mp3_to_wav__mutmut_26, 
    'x_convert_mp3_to_wav__mutmut_27': x_convert_mp3_to_wav__mutmut_27, 
    'x_convert_mp3_to_wav__mutmut_28': x_convert_mp3_to_wav__mutmut_28, 
    'x_convert_mp3_to_wav__mutmut_29': x_convert_mp3_to_wav__mutmut_29, 
    'x_convert_mp3_to_wav__mutmut_30': x_convert_mp3_to_wav__mutmut_30, 
    'x_convert_mp3_to_wav__mutmut_31': x_convert_mp3_to_wav__mutmut_31, 
    'x_convert_mp3_to_wav__mutmut_32': x_convert_mp3_to_wav__mutmut_32, 
    'x_convert_mp3_to_wav__mutmut_33': x_convert_mp3_to_wav__mutmut_33, 
    'x_convert_mp3_to_wav__mutmut_34': x_convert_mp3_to_wav__mutmut_34, 
    'x_convert_mp3_to_wav__mutmut_35': x_convert_mp3_to_wav__mutmut_35, 
    'x_convert_mp3_to_wav__mutmut_36': x_convert_mp3_to_wav__mutmut_36, 
    'x_convert_mp3_to_wav__mutmut_37': x_convert_mp3_to_wav__mutmut_37, 
    'x_convert_mp3_to_wav__mutmut_38': x_convert_mp3_to_wav__mutmut_38, 
    'x_convert_mp3_to_wav__mutmut_39': x_convert_mp3_to_wav__mutmut_39, 
    'x_convert_mp3_to_wav__mutmut_40': x_convert_mp3_to_wav__mutmut_40, 
    'x_convert_mp3_to_wav__mutmut_41': x_convert_mp3_to_wav__mutmut_41, 
    'x_convert_mp3_to_wav__mutmut_42': x_convert_mp3_to_wav__mutmut_42, 
    'x_convert_mp3_to_wav__mutmut_43': x_convert_mp3_to_wav__mutmut_43, 
    'x_convert_mp3_to_wav__mutmut_44': x_convert_mp3_to_wav__mutmut_44, 
    'x_convert_mp3_to_wav__mutmut_45': x_convert_mp3_to_wav__mutmut_45, 
    'x_convert_mp3_to_wav__mutmut_46': x_convert_mp3_to_wav__mutmut_46, 
    'x_convert_mp3_to_wav__mutmut_47': x_convert_mp3_to_wav__mutmut_47, 
    'x_convert_mp3_to_wav__mutmut_48': x_convert_mp3_to_wav__mutmut_48, 
    'x_convert_mp3_to_wav__mutmut_49': x_convert_mp3_to_wav__mutmut_49, 
    'x_convert_mp3_to_wav__mutmut_50': x_convert_mp3_to_wav__mutmut_50, 
    'x_convert_mp3_to_wav__mutmut_51': x_convert_mp3_to_wav__mutmut_51, 
    'x_convert_mp3_to_wav__mutmut_52': x_convert_mp3_to_wav__mutmut_52, 
    'x_convert_mp3_to_wav__mutmut_53': x_convert_mp3_to_wav__mutmut_53, 
    'x_convert_mp3_to_wav__mutmut_54': x_convert_mp3_to_wav__mutmut_54
}
x_convert_mp3_to_wav__mutmut_orig.__name__ = 'x_convert_mp3_to_wav'


def convert_wav_to_mp3(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
    args = [input_path, output_path, bitrate]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_convert_wav_to_mp3__mutmut_orig, x_convert_wav_to_mp3__mutmut_mutants, args, kwargs, None)


def x_convert_wav_to_mp3__mutmut_orig(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_1(input_path: str, output_path: str, bitrate: str = "XX192kXX") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_2(input_path: str, output_path: str, bitrate: str = "192K") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_3(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
    """
    Convert WAV audio file to MP3 format using ffmpeg.
    
    Args:
        input_path: Path to input WAV file
        output_path: Path to output MP3 file
        bitrate: MP3 bitrate (default: 192k)
        
    Returns:
        True if conversion succeeded, False otherwise
    """
    input_file = None
    output_file = Path(output_path)
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_4(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
    """
    Convert WAV audio file to MP3 format using ffmpeg.
    
    Args:
        input_path: Path to input WAV file
        output_path: Path to output MP3 file
        bitrate: MP3 bitrate (default: 192k)
        
    Returns:
        True if conversion succeeded, False otherwise
    """
    input_file = Path(None)
    output_file = Path(output_path)
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_5(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
    output_file = None
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_6(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
    output_file = Path(None)
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_7(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
    
    if input_file.exists():
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_8(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(None)
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_9(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return True
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_10(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=None, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_11(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=None)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_12(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_13(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, )
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_14(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=False, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_15(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=False)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_16(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = None
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_17(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = None
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_18(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            None,
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_19(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=None,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_20(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            text=None,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_21(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            check=None,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_22(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_23(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_24(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_25(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_26(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "XX-iXX", str(input_file),
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_27(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-I", str(input_file),
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_28(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(None),
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_29(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "XX-acodecXX", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_30(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-ACODEC", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_31(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "XXlibmp3lameXX",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_32(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "LIBMP3LAME",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_33(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "XX-b:aXX", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_34(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-B:A", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_35(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "XX-yXX",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_36(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "-Y",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_37(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(None),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_38(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=False,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_39(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
            [
                ffmpeg,
                "-i", str(input_file),
                "-acodec", "libmp3lame",
                "-b:a", bitrate,
                "-y",
                str(output_file),
            ],
            capture_output=True,
            text=False,
            check=False,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_40(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            check=True,
        )
        
        if result.returncode != 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_41(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
        
        if result.returncode == 0:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_42(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
        
        if result.returncode != 1:
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_43(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(None)
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_44(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return True
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_45(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return False
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return False


def x_convert_wav_to_mp3__mutmut_46(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(None)
        return False


def x_convert_wav_to_mp3__mutmut_47(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
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
        logger.error(f"Input file not found: {input_path}")
        return False
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        ffmpeg = get_ffmpeg_path()
        
        result = subprocess.run(
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
            logger.error(f"ffmpeg conversion failed: {result.stderr}")
            return False
        
        return True
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.error(f"Unexpected error during WAV->MP3 conversion: {e}")
        return True

x_convert_wav_to_mp3__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_convert_wav_to_mp3__mutmut_1': x_convert_wav_to_mp3__mutmut_1, 
    'x_convert_wav_to_mp3__mutmut_2': x_convert_wav_to_mp3__mutmut_2, 
    'x_convert_wav_to_mp3__mutmut_3': x_convert_wav_to_mp3__mutmut_3, 
    'x_convert_wav_to_mp3__mutmut_4': x_convert_wav_to_mp3__mutmut_4, 
    'x_convert_wav_to_mp3__mutmut_5': x_convert_wav_to_mp3__mutmut_5, 
    'x_convert_wav_to_mp3__mutmut_6': x_convert_wav_to_mp3__mutmut_6, 
    'x_convert_wav_to_mp3__mutmut_7': x_convert_wav_to_mp3__mutmut_7, 
    'x_convert_wav_to_mp3__mutmut_8': x_convert_wav_to_mp3__mutmut_8, 
    'x_convert_wav_to_mp3__mutmut_9': x_convert_wav_to_mp3__mutmut_9, 
    'x_convert_wav_to_mp3__mutmut_10': x_convert_wav_to_mp3__mutmut_10, 
    'x_convert_wav_to_mp3__mutmut_11': x_convert_wav_to_mp3__mutmut_11, 
    'x_convert_wav_to_mp3__mutmut_12': x_convert_wav_to_mp3__mutmut_12, 
    'x_convert_wav_to_mp3__mutmut_13': x_convert_wav_to_mp3__mutmut_13, 
    'x_convert_wav_to_mp3__mutmut_14': x_convert_wav_to_mp3__mutmut_14, 
    'x_convert_wav_to_mp3__mutmut_15': x_convert_wav_to_mp3__mutmut_15, 
    'x_convert_wav_to_mp3__mutmut_16': x_convert_wav_to_mp3__mutmut_16, 
    'x_convert_wav_to_mp3__mutmut_17': x_convert_wav_to_mp3__mutmut_17, 
    'x_convert_wav_to_mp3__mutmut_18': x_convert_wav_to_mp3__mutmut_18, 
    'x_convert_wav_to_mp3__mutmut_19': x_convert_wav_to_mp3__mutmut_19, 
    'x_convert_wav_to_mp3__mutmut_20': x_convert_wav_to_mp3__mutmut_20, 
    'x_convert_wav_to_mp3__mutmut_21': x_convert_wav_to_mp3__mutmut_21, 
    'x_convert_wav_to_mp3__mutmut_22': x_convert_wav_to_mp3__mutmut_22, 
    'x_convert_wav_to_mp3__mutmut_23': x_convert_wav_to_mp3__mutmut_23, 
    'x_convert_wav_to_mp3__mutmut_24': x_convert_wav_to_mp3__mutmut_24, 
    'x_convert_wav_to_mp3__mutmut_25': x_convert_wav_to_mp3__mutmut_25, 
    'x_convert_wav_to_mp3__mutmut_26': x_convert_wav_to_mp3__mutmut_26, 
    'x_convert_wav_to_mp3__mutmut_27': x_convert_wav_to_mp3__mutmut_27, 
    'x_convert_wav_to_mp3__mutmut_28': x_convert_wav_to_mp3__mutmut_28, 
    'x_convert_wav_to_mp3__mutmut_29': x_convert_wav_to_mp3__mutmut_29, 
    'x_convert_wav_to_mp3__mutmut_30': x_convert_wav_to_mp3__mutmut_30, 
    'x_convert_wav_to_mp3__mutmut_31': x_convert_wav_to_mp3__mutmut_31, 
    'x_convert_wav_to_mp3__mutmut_32': x_convert_wav_to_mp3__mutmut_32, 
    'x_convert_wav_to_mp3__mutmut_33': x_convert_wav_to_mp3__mutmut_33, 
    'x_convert_wav_to_mp3__mutmut_34': x_convert_wav_to_mp3__mutmut_34, 
    'x_convert_wav_to_mp3__mutmut_35': x_convert_wav_to_mp3__mutmut_35, 
    'x_convert_wav_to_mp3__mutmut_36': x_convert_wav_to_mp3__mutmut_36, 
    'x_convert_wav_to_mp3__mutmut_37': x_convert_wav_to_mp3__mutmut_37, 
    'x_convert_wav_to_mp3__mutmut_38': x_convert_wav_to_mp3__mutmut_38, 
    'x_convert_wav_to_mp3__mutmut_39': x_convert_wav_to_mp3__mutmut_39, 
    'x_convert_wav_to_mp3__mutmut_40': x_convert_wav_to_mp3__mutmut_40, 
    'x_convert_wav_to_mp3__mutmut_41': x_convert_wav_to_mp3__mutmut_41, 
    'x_convert_wav_to_mp3__mutmut_42': x_convert_wav_to_mp3__mutmut_42, 
    'x_convert_wav_to_mp3__mutmut_43': x_convert_wav_to_mp3__mutmut_43, 
    'x_convert_wav_to_mp3__mutmut_44': x_convert_wav_to_mp3__mutmut_44, 
    'x_convert_wav_to_mp3__mutmut_45': x_convert_wav_to_mp3__mutmut_45, 
    'x_convert_wav_to_mp3__mutmut_46': x_convert_wav_to_mp3__mutmut_46, 
    'x_convert_wav_to_mp3__mutmut_47': x_convert_wav_to_mp3__mutmut_47
}
x_convert_wav_to_mp3__mutmut_orig.__name__ = 'x_convert_wav_to_mp3'


def get_audio_info(file_path: str) -> Optional[dict]:
    args = [file_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_audio_info__mutmut_orig, x_get_audio_info__mutmut_mutants, args, kwargs, None)


def x_get_audio_info__mutmut_orig(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_1(file_path: str) -> Optional[dict]:
    """
    Get audio file information using ffprobe.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Dictionary with audio info (duration, bitrate, format) or None
    """
    import json
    
    ffprobe_path = None
    if ffprobe_path is None:
        return None
    
    try:
        result = subprocess.run(
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_2(file_path: str) -> Optional[dict]:
    """
    Get audio file information using ffprobe.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Dictionary with audio info (duration, bitrate, format) or None
    """
    import json
    
    ffprobe_path = shutil.which(None)
    if ffprobe_path is None:
        return None
    
    try:
        result = subprocess.run(
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_3(file_path: str) -> Optional[dict]:
    """
    Get audio file information using ffprobe.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Dictionary with audio info (duration, bitrate, format) or None
    """
    import json
    
    ffprobe_path = shutil.which("XXffprobeXX")
    if ffprobe_path is None:
        return None
    
    try:
        result = subprocess.run(
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_4(file_path: str) -> Optional[dict]:
    """
    Get audio file information using ffprobe.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Dictionary with audio info (duration, bitrate, format) or None
    """
    import json
    
    ffprobe_path = shutil.which("FFPROBE")
    if ffprobe_path is None:
        return None
    
    try:
        result = subprocess.run(
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_5(file_path: str) -> Optional[dict]:
    """
    Get audio file information using ffprobe.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Dictionary with audio info (duration, bitrate, format) or None
    """
    import json
    
    ffprobe_path = shutil.which("ffprobe")
    if ffprobe_path is not None:
        return None
    
    try:
        result = subprocess.run(
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_6(file_path: str) -> Optional[dict]:
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
        result = None
        
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_7(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            None,
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_8(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(file_path),
            ],
            capture_output=None,
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_9(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(file_path),
            ],
            capture_output=True,
            text=None,
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_10(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            check=None,
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_11(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_12(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(file_path),
            ],
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_13(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(file_path),
            ],
            capture_output=True,
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_14(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_15(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "XX-vXX", "quiet",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_16(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-V", "quiet",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_17(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "XXquietXX",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_18(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "QUIET",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_19(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "XX-print_formatXX", "json",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_20(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-PRINT_FORMAT", "json",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_21(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "XXjsonXX",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_22(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "JSON",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_23(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "XX-show_formatXX",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_24(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-SHOW_FORMAT",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_25(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "XX-show_streamsXX",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_26(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-SHOW_STREAMS",
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_27(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(None),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_28(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(file_path),
            ],
            capture_output=False,
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_29(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
            [
                ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(file_path),
            ],
            capture_output=True,
            text=False,
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_30(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            check=False,
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_31(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
        
        data = None
        
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_32(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
        
        data = json.loads(None)
        
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_33(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
        info = None
        
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_34(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "XXformatXX": data.get("format", {}).get("format_name"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_35(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "FORMAT": data.get("format", {}).get("format_name"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_36(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "format": data.get("format", {}).get(None),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_37(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "format": data.get(None, {}).get("format_name"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_38(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "format": data.get("format", None).get("format_name"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_39(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "format": data.get({}).get("format_name"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_40(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "format": data.get("format", ).get("format_name"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_41(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "format": data.get("XXformatXX", {}).get("format_name"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_42(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "format": data.get("FORMAT", {}).get("format_name"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_43(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "format": data.get("format", {}).get("XXformat_nameXX"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_44(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "format": data.get("format", {}).get("FORMAT_NAME"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_45(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "XXdurationXX": float(data.get("format", {}).get("duration", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_46(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "DURATION": float(data.get("format", {}).get("duration", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_47(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(None),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_48(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("format", {}).get(None, 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_49(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("format", {}).get("duration", None)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_50(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("format", {}).get(0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_51(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("format", {}).get("duration", )),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_52(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get(None, {}).get("duration", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_53(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("format", None).get("duration", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_54(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get({}).get("duration", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_55(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("format", ).get("duration", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_56(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("XXformatXX", {}).get("duration", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_57(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("FORMAT", {}).get("duration", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_58(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("format", {}).get("XXdurationXX", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_59(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("format", {}).get("DURATION", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_60(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "duration": float(data.get("format", {}).get("duration", 1)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_61(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "XXbitrateXX": data.get("format", {}).get("bit_rate"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_62(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "BITRATE": data.get("format", {}).get("bit_rate"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_63(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "bitrate": data.get("format", {}).get(None),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_64(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "bitrate": data.get(None, {}).get("bit_rate"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_65(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "bitrate": data.get("format", None).get("bit_rate"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_66(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "bitrate": data.get({}).get("bit_rate"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_67(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "bitrate": data.get("format", ).get("bit_rate"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_68(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "bitrate": data.get("XXformatXX", {}).get("bit_rate"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_69(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "bitrate": data.get("FORMAT", {}).get("bit_rate"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_70(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "bitrate": data.get("format", {}).get("XXbit_rateXX"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_71(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "bitrate": data.get("format", {}).get("BIT_RATE"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_72(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "XXsizeXX": int(data.get("format", {}).get("size", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_73(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "SIZE": int(data.get("format", {}).get("size", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_74(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(None),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_75(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("format", {}).get(None, 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_76(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("format", {}).get("size", None)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_77(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("format", {}).get(0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_78(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("format", {}).get("size", )),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_79(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get(None, {}).get("size", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_80(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("format", None).get("size", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_81(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get({}).get("size", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_82(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("format", ).get("size", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_83(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("XXformatXX", {}).get("size", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_84(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("FORMAT", {}).get("size", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_85(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("format", {}).get("XXsizeXX", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_86(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("format", {}).get("SIZE", 0)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_87(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            "size": int(data.get("format", {}).get("size", 1)),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_88(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
        audio_stream = None
        
        if audio_stream:
            info.update({
                "codec": audio_stream.get("codec_name"),
                "sample_rate": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_89(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            None,
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_90(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_91(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            )
        
        if audio_stream:
            info.update({
                "codec": audio_stream.get("codec_name"),
                "sample_rate": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_92(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get(None, []) if s.get("codec_type") == "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_93(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("streams", None) if s.get("codec_type") == "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_94(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get([]) if s.get("codec_type") == "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_95(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("streams", ) if s.get("codec_type") == "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_96(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("XXstreamsXX", []) if s.get("codec_type") == "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_97(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("STREAMS", []) if s.get("codec_type") == "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_98(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("streams", []) if s.get(None) == "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_99(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("streams", []) if s.get("XXcodec_typeXX") == "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_100(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("streams", []) if s.get("CODEC_TYPE") == "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_101(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("streams", []) if s.get("codec_type") != "audio"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_102(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("streams", []) if s.get("codec_type") == "XXaudioXX"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_103(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            (s for s in data.get("streams", []) if s.get("codec_type") == "AUDIO"),
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
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_104(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
            info.update(None)
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_105(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "XXcodecXX": audio_stream.get("codec_name"),
                "sample_rate": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_106(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "CODEC": audio_stream.get("codec_name"),
                "sample_rate": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_107(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "codec": audio_stream.get(None),
                "sample_rate": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_108(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "codec": audio_stream.get("XXcodec_nameXX"),
                "sample_rate": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_109(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "codec": audio_stream.get("CODEC_NAME"),
                "sample_rate": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_110(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "XXsample_rateXX": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_111(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "SAMPLE_RATE": audio_stream.get("sample_rate"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_112(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "sample_rate": audio_stream.get(None),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_113(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "sample_rate": audio_stream.get("XXsample_rateXX"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_114(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "sample_rate": audio_stream.get("SAMPLE_RATE"),
                "channels": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_115(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "XXchannelsXX": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_116(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "CHANNELS": audio_stream.get("channels"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_117(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "channels": audio_stream.get(None),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_118(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "channels": audio_stream.get("XXchannelsXX"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_119(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
                "channels": audio_stream.get("CHANNELS"),
            })
        
        return info
        
    except (RuntimeError, subprocess.SubprocessError, OSError) as e:
        logger.debug(f"Could not get audio info: {e}")
        return None


def x_get_audio_info__mutmut_120(file_path: str) -> Optional[dict]:
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
        result = subprocess.run(
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
        logger.debug(None)
        return None

x_get_audio_info__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_audio_info__mutmut_1': x_get_audio_info__mutmut_1, 
    'x_get_audio_info__mutmut_2': x_get_audio_info__mutmut_2, 
    'x_get_audio_info__mutmut_3': x_get_audio_info__mutmut_3, 
    'x_get_audio_info__mutmut_4': x_get_audio_info__mutmut_4, 
    'x_get_audio_info__mutmut_5': x_get_audio_info__mutmut_5, 
    'x_get_audio_info__mutmut_6': x_get_audio_info__mutmut_6, 
    'x_get_audio_info__mutmut_7': x_get_audio_info__mutmut_7, 
    'x_get_audio_info__mutmut_8': x_get_audio_info__mutmut_8, 
    'x_get_audio_info__mutmut_9': x_get_audio_info__mutmut_9, 
    'x_get_audio_info__mutmut_10': x_get_audio_info__mutmut_10, 
    'x_get_audio_info__mutmut_11': x_get_audio_info__mutmut_11, 
    'x_get_audio_info__mutmut_12': x_get_audio_info__mutmut_12, 
    'x_get_audio_info__mutmut_13': x_get_audio_info__mutmut_13, 
    'x_get_audio_info__mutmut_14': x_get_audio_info__mutmut_14, 
    'x_get_audio_info__mutmut_15': x_get_audio_info__mutmut_15, 
    'x_get_audio_info__mutmut_16': x_get_audio_info__mutmut_16, 
    'x_get_audio_info__mutmut_17': x_get_audio_info__mutmut_17, 
    'x_get_audio_info__mutmut_18': x_get_audio_info__mutmut_18, 
    'x_get_audio_info__mutmut_19': x_get_audio_info__mutmut_19, 
    'x_get_audio_info__mutmut_20': x_get_audio_info__mutmut_20, 
    'x_get_audio_info__mutmut_21': x_get_audio_info__mutmut_21, 
    'x_get_audio_info__mutmut_22': x_get_audio_info__mutmut_22, 
    'x_get_audio_info__mutmut_23': x_get_audio_info__mutmut_23, 
    'x_get_audio_info__mutmut_24': x_get_audio_info__mutmut_24, 
    'x_get_audio_info__mutmut_25': x_get_audio_info__mutmut_25, 
    'x_get_audio_info__mutmut_26': x_get_audio_info__mutmut_26, 
    'x_get_audio_info__mutmut_27': x_get_audio_info__mutmut_27, 
    'x_get_audio_info__mutmut_28': x_get_audio_info__mutmut_28, 
    'x_get_audio_info__mutmut_29': x_get_audio_info__mutmut_29, 
    'x_get_audio_info__mutmut_30': x_get_audio_info__mutmut_30, 
    'x_get_audio_info__mutmut_31': x_get_audio_info__mutmut_31, 
    'x_get_audio_info__mutmut_32': x_get_audio_info__mutmut_32, 
    'x_get_audio_info__mutmut_33': x_get_audio_info__mutmut_33, 
    'x_get_audio_info__mutmut_34': x_get_audio_info__mutmut_34, 
    'x_get_audio_info__mutmut_35': x_get_audio_info__mutmut_35, 
    'x_get_audio_info__mutmut_36': x_get_audio_info__mutmut_36, 
    'x_get_audio_info__mutmut_37': x_get_audio_info__mutmut_37, 
    'x_get_audio_info__mutmut_38': x_get_audio_info__mutmut_38, 
    'x_get_audio_info__mutmut_39': x_get_audio_info__mutmut_39, 
    'x_get_audio_info__mutmut_40': x_get_audio_info__mutmut_40, 
    'x_get_audio_info__mutmut_41': x_get_audio_info__mutmut_41, 
    'x_get_audio_info__mutmut_42': x_get_audio_info__mutmut_42, 
    'x_get_audio_info__mutmut_43': x_get_audio_info__mutmut_43, 
    'x_get_audio_info__mutmut_44': x_get_audio_info__mutmut_44, 
    'x_get_audio_info__mutmut_45': x_get_audio_info__mutmut_45, 
    'x_get_audio_info__mutmut_46': x_get_audio_info__mutmut_46, 
    'x_get_audio_info__mutmut_47': x_get_audio_info__mutmut_47, 
    'x_get_audio_info__mutmut_48': x_get_audio_info__mutmut_48, 
    'x_get_audio_info__mutmut_49': x_get_audio_info__mutmut_49, 
    'x_get_audio_info__mutmut_50': x_get_audio_info__mutmut_50, 
    'x_get_audio_info__mutmut_51': x_get_audio_info__mutmut_51, 
    'x_get_audio_info__mutmut_52': x_get_audio_info__mutmut_52, 
    'x_get_audio_info__mutmut_53': x_get_audio_info__mutmut_53, 
    'x_get_audio_info__mutmut_54': x_get_audio_info__mutmut_54, 
    'x_get_audio_info__mutmut_55': x_get_audio_info__mutmut_55, 
    'x_get_audio_info__mutmut_56': x_get_audio_info__mutmut_56, 
    'x_get_audio_info__mutmut_57': x_get_audio_info__mutmut_57, 
    'x_get_audio_info__mutmut_58': x_get_audio_info__mutmut_58, 
    'x_get_audio_info__mutmut_59': x_get_audio_info__mutmut_59, 
    'x_get_audio_info__mutmut_60': x_get_audio_info__mutmut_60, 
    'x_get_audio_info__mutmut_61': x_get_audio_info__mutmut_61, 
    'x_get_audio_info__mutmut_62': x_get_audio_info__mutmut_62, 
    'x_get_audio_info__mutmut_63': x_get_audio_info__mutmut_63, 
    'x_get_audio_info__mutmut_64': x_get_audio_info__mutmut_64, 
    'x_get_audio_info__mutmut_65': x_get_audio_info__mutmut_65, 
    'x_get_audio_info__mutmut_66': x_get_audio_info__mutmut_66, 
    'x_get_audio_info__mutmut_67': x_get_audio_info__mutmut_67, 
    'x_get_audio_info__mutmut_68': x_get_audio_info__mutmut_68, 
    'x_get_audio_info__mutmut_69': x_get_audio_info__mutmut_69, 
    'x_get_audio_info__mutmut_70': x_get_audio_info__mutmut_70, 
    'x_get_audio_info__mutmut_71': x_get_audio_info__mutmut_71, 
    'x_get_audio_info__mutmut_72': x_get_audio_info__mutmut_72, 
    'x_get_audio_info__mutmut_73': x_get_audio_info__mutmut_73, 
    'x_get_audio_info__mutmut_74': x_get_audio_info__mutmut_74, 
    'x_get_audio_info__mutmut_75': x_get_audio_info__mutmut_75, 
    'x_get_audio_info__mutmut_76': x_get_audio_info__mutmut_76, 
    'x_get_audio_info__mutmut_77': x_get_audio_info__mutmut_77, 
    'x_get_audio_info__mutmut_78': x_get_audio_info__mutmut_78, 
    'x_get_audio_info__mutmut_79': x_get_audio_info__mutmut_79, 
    'x_get_audio_info__mutmut_80': x_get_audio_info__mutmut_80, 
    'x_get_audio_info__mutmut_81': x_get_audio_info__mutmut_81, 
    'x_get_audio_info__mutmut_82': x_get_audio_info__mutmut_82, 
    'x_get_audio_info__mutmut_83': x_get_audio_info__mutmut_83, 
    'x_get_audio_info__mutmut_84': x_get_audio_info__mutmut_84, 
    'x_get_audio_info__mutmut_85': x_get_audio_info__mutmut_85, 
    'x_get_audio_info__mutmut_86': x_get_audio_info__mutmut_86, 
    'x_get_audio_info__mutmut_87': x_get_audio_info__mutmut_87, 
    'x_get_audio_info__mutmut_88': x_get_audio_info__mutmut_88, 
    'x_get_audio_info__mutmut_89': x_get_audio_info__mutmut_89, 
    'x_get_audio_info__mutmut_90': x_get_audio_info__mutmut_90, 
    'x_get_audio_info__mutmut_91': x_get_audio_info__mutmut_91, 
    'x_get_audio_info__mutmut_92': x_get_audio_info__mutmut_92, 
    'x_get_audio_info__mutmut_93': x_get_audio_info__mutmut_93, 
    'x_get_audio_info__mutmut_94': x_get_audio_info__mutmut_94, 
    'x_get_audio_info__mutmut_95': x_get_audio_info__mutmut_95, 
    'x_get_audio_info__mutmut_96': x_get_audio_info__mutmut_96, 
    'x_get_audio_info__mutmut_97': x_get_audio_info__mutmut_97, 
    'x_get_audio_info__mutmut_98': x_get_audio_info__mutmut_98, 
    'x_get_audio_info__mutmut_99': x_get_audio_info__mutmut_99, 
    'x_get_audio_info__mutmut_100': x_get_audio_info__mutmut_100, 
    'x_get_audio_info__mutmut_101': x_get_audio_info__mutmut_101, 
    'x_get_audio_info__mutmut_102': x_get_audio_info__mutmut_102, 
    'x_get_audio_info__mutmut_103': x_get_audio_info__mutmut_103, 
    'x_get_audio_info__mutmut_104': x_get_audio_info__mutmut_104, 
    'x_get_audio_info__mutmut_105': x_get_audio_info__mutmut_105, 
    'x_get_audio_info__mutmut_106': x_get_audio_info__mutmut_106, 
    'x_get_audio_info__mutmut_107': x_get_audio_info__mutmut_107, 
    'x_get_audio_info__mutmut_108': x_get_audio_info__mutmut_108, 
    'x_get_audio_info__mutmut_109': x_get_audio_info__mutmut_109, 
    'x_get_audio_info__mutmut_110': x_get_audio_info__mutmut_110, 
    'x_get_audio_info__mutmut_111': x_get_audio_info__mutmut_111, 
    'x_get_audio_info__mutmut_112': x_get_audio_info__mutmut_112, 
    'x_get_audio_info__mutmut_113': x_get_audio_info__mutmut_113, 
    'x_get_audio_info__mutmut_114': x_get_audio_info__mutmut_114, 
    'x_get_audio_info__mutmut_115': x_get_audio_info__mutmut_115, 
    'x_get_audio_info__mutmut_116': x_get_audio_info__mutmut_116, 
    'x_get_audio_info__mutmut_117': x_get_audio_info__mutmut_117, 
    'x_get_audio_info__mutmut_118': x_get_audio_info__mutmut_118, 
    'x_get_audio_info__mutmut_119': x_get_audio_info__mutmut_119, 
    'x_get_audio_info__mutmut_120': x_get_audio_info__mutmut_120
}
x_get_audio_info__mutmut_orig.__name__ = 'x_get_audio_info'
