#!/usr/bin/env python3
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
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

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


def parse_args() -> argparse.Namespace:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_parse_args__mutmut_orig, x_parse_args__mutmut_mutants, args, kwargs, None)


def x_parse_args__mutmut_orig() -> argparse.Namespace:
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


def x_parse_args__mutmut_1() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = None
    
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


def x_parse_args__mutmut_2() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog=None,
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


def x_parse_args__mutmut_3() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
        description=None,
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


def x_parse_args__mutmut_4() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
        description="Kokoro Taiwan TTS CLI - 繁體中文語音合成工具",
        formatter_class=None,
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


def x_parse_args__mutmut_5() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
        description="Kokoro Taiwan TTS CLI - 繁體中文語音合成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=None,
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


def x_parse_args__mutmut_6() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
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


def x_parse_args__mutmut_7() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
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


def x_parse_args__mutmut_8() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
        description="Kokoro Taiwan TTS CLI - 繁體中文語音合成工具",
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


def x_parse_args__mutmut_9() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
        description="Kokoro Taiwan TTS CLI - 繁體中文語音合成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
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


def x_parse_args__mutmut_10() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="XXtts-v610XX",
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


def x_parse_args__mutmut_11() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="TTS-V610",
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


def x_parse_args__mutmut_12() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
        description="XXKokoro Taiwan TTS CLI - 繁體中文語音合成工具XX",
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


def x_parse_args__mutmut_13() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
        description="kokoro taiwan tts cli - 繁體中文語音合成工具",
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


def x_parse_args__mutmut_14() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tts-v610",
        description="KOKORO TAIWAN TTS CLI - 繁體中文語音合成工具",
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


def x_parse_args__mutmut_15() -> argparse.Namespace:
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
        None, "--input",
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


def x_parse_args__mutmut_16() -> argparse.Namespace:
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
        "-i", None,
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


def x_parse_args__mutmut_17() -> argparse.Namespace:
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
        type=None,
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


def x_parse_args__mutmut_18() -> argparse.Namespace:
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
        help=None,
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


def x_parse_args__mutmut_19() -> argparse.Namespace:
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
        "--input",
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


def x_parse_args__mutmut_20() -> argparse.Namespace:
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
        "-i", type=str,
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


def x_parse_args__mutmut_21() -> argparse.Namespace:
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


def x_parse_args__mutmut_22() -> argparse.Namespace:
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


def x_parse_args__mutmut_23() -> argparse.Namespace:
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


def x_parse_args__mutmut_24() -> argparse.Namespace:
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
        "XX-iXX", "--input",
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


def x_parse_args__mutmut_25() -> argparse.Namespace:
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
        "-I", "--input",
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


def x_parse_args__mutmut_26() -> argparse.Namespace:
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
        "-i", "XX--inputXX",
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


def x_parse_args__mutmut_27() -> argparse.Namespace:
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
        "-i", "--INPUT",
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


def x_parse_args__mutmut_28() -> argparse.Namespace:
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
        help="XXInput text or SSML markup (use --ssml flag for SSML mode)XX",
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


def x_parse_args__mutmut_29() -> argparse.Namespace:
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
        help="input text or ssml markup (use --ssml flag for ssml mode)",
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


def x_parse_args__mutmut_30() -> argparse.Namespace:
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
        help="INPUT TEXT OR SSML MARKUP (USE --SSML FLAG FOR SSML MODE)",
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


def x_parse_args__mutmut_31() -> argparse.Namespace:
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
        None, "--output",
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


def x_parse_args__mutmut_32() -> argparse.Namespace:
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
        "-o", None,
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


def x_parse_args__mutmut_33() -> argparse.Namespace:
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
        type=None,
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


def x_parse_args__mutmut_34() -> argparse.Namespace:
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
        required=None,
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


def x_parse_args__mutmut_35() -> argparse.Namespace:
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
        help=None,
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


def x_parse_args__mutmut_36() -> argparse.Namespace:
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
        "--output",
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


def x_parse_args__mutmut_37() -> argparse.Namespace:
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
        "-o", type=str,
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


def x_parse_args__mutmut_38() -> argparse.Namespace:
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


def x_parse_args__mutmut_39() -> argparse.Namespace:
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


def x_parse_args__mutmut_40() -> argparse.Namespace:
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


def x_parse_args__mutmut_41() -> argparse.Namespace:
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
        "XX-oXX", "--output",
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


def x_parse_args__mutmut_42() -> argparse.Namespace:
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
        "-O", "--output",
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


def x_parse_args__mutmut_43() -> argparse.Namespace:
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
        "-o", "XX--outputXX",
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


def x_parse_args__mutmut_44() -> argparse.Namespace:
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
        "-o", "--OUTPUT",
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


def x_parse_args__mutmut_45() -> argparse.Namespace:
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
        required=False,
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


def x_parse_args__mutmut_46() -> argparse.Namespace:
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
        help="XXOutput file path or directory (with -f for wav)XX",
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


def x_parse_args__mutmut_47() -> argparse.Namespace:
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
        help="output file path or directory (with -f for wav)",
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


def x_parse_args__mutmut_48() -> argparse.Namespace:
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
        help="OUTPUT FILE PATH OR DIRECTORY (WITH -F FOR WAV)",
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


def x_parse_args__mutmut_49() -> argparse.Namespace:
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
        None, "--voice",
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


def x_parse_args__mutmut_50() -> argparse.Namespace:
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
        "-v", None,
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


def x_parse_args__mutmut_51() -> argparse.Namespace:
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
        type=None,
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


def x_parse_args__mutmut_52() -> argparse.Namespace:
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
        default=None,
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


def x_parse_args__mutmut_53() -> argparse.Namespace:
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
        help=None,
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


def x_parse_args__mutmut_54() -> argparse.Namespace:
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
        "--voice",
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


def x_parse_args__mutmut_55() -> argparse.Namespace:
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
        "-v", type=str,
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


def x_parse_args__mutmut_56() -> argparse.Namespace:
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


def x_parse_args__mutmut_57() -> argparse.Namespace:
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


def x_parse_args__mutmut_58() -> argparse.Namespace:
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


def x_parse_args__mutmut_59() -> argparse.Namespace:
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
        "XX-vXX", "--voice",
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


def x_parse_args__mutmut_60() -> argparse.Namespace:
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
        "-V", "--voice",
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


def x_parse_args__mutmut_61() -> argparse.Namespace:
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
        "-v", "XX--voiceXX",
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


def x_parse_args__mutmut_62() -> argparse.Namespace:
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
        "-v", "--VOICE",
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


def x_parse_args__mutmut_63() -> argparse.Namespace:
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
        None, "--speed",
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


def x_parse_args__mutmut_64() -> argparse.Namespace:
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
        "-s", None,
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


def x_parse_args__mutmut_65() -> argparse.Namespace:
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
        type=None,
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


def x_parse_args__mutmut_66() -> argparse.Namespace:
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
        default=None,
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


def x_parse_args__mutmut_67() -> argparse.Namespace:
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
        choices=None,
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


def x_parse_args__mutmut_68() -> argparse.Namespace:
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
        help=None,
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


def x_parse_args__mutmut_69() -> argparse.Namespace:
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
        "--speed",
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


def x_parse_args__mutmut_70() -> argparse.Namespace:
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
        "-s", type=float,
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


def x_parse_args__mutmut_71() -> argparse.Namespace:
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


def x_parse_args__mutmut_72() -> argparse.Namespace:
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


def x_parse_args__mutmut_73() -> argparse.Namespace:
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


def x_parse_args__mutmut_74() -> argparse.Namespace:
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


def x_parse_args__mutmut_75() -> argparse.Namespace:
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
        "XX-sXX", "--speed",
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


def x_parse_args__mutmut_76() -> argparse.Namespace:
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
        "-S", "--speed",
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


def x_parse_args__mutmut_77() -> argparse.Namespace:
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
        "-s", "XX--speedXX",
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


def x_parse_args__mutmut_78() -> argparse.Namespace:
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
        "-s", "--SPEED",
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


def x_parse_args__mutmut_79() -> argparse.Namespace:
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
        choices=[round(None, 1) for x in range(5, 21)],
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


def x_parse_args__mutmut_80() -> argparse.Namespace:
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
        choices=[round(x * 0.1, None) for x in range(5, 21)],
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


def x_parse_args__mutmut_81() -> argparse.Namespace:
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
        choices=[round(1) for x in range(5, 21)],
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


def x_parse_args__mutmut_82() -> argparse.Namespace:
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
        choices=[round(x * 0.1, ) for x in range(5, 21)],
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


def x_parse_args__mutmut_83() -> argparse.Namespace:
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
        choices=[round(x / 0.1, 1) for x in range(5, 21)],
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


def x_parse_args__mutmut_84() -> argparse.Namespace:
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
        choices=[round(x * 1.1, 1) for x in range(5, 21)],
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


def x_parse_args__mutmut_85() -> argparse.Namespace:
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
        choices=[round(x * 0.1, 2) for x in range(5, 21)],
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


def x_parse_args__mutmut_86() -> argparse.Namespace:
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
        choices=[round(x * 0.1, 1) for x in range(None, 21)],
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


def x_parse_args__mutmut_87() -> argparse.Namespace:
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
        choices=[round(x * 0.1, 1) for x in range(5, None)],
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


def x_parse_args__mutmut_88() -> argparse.Namespace:
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
        choices=[round(x * 0.1, 1) for x in range(21)],
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


def x_parse_args__mutmut_89() -> argparse.Namespace:
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
        choices=[round(x * 0.1, 1) for x in range(5, )],
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


def x_parse_args__mutmut_90() -> argparse.Namespace:
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
        choices=[round(x * 0.1, 1) for x in range(6, 21)],
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


def x_parse_args__mutmut_91() -> argparse.Namespace:
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
        choices=[round(x * 0.1, 1) for x in range(5, 22)],
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


def x_parse_args__mutmut_92() -> argparse.Namespace:
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
        None, "--format",
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


def x_parse_args__mutmut_93() -> argparse.Namespace:
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
        "-f", None,
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


def x_parse_args__mutmut_94() -> argparse.Namespace:
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
        type=None,
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


def x_parse_args__mutmut_95() -> argparse.Namespace:
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
        default=None,
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


def x_parse_args__mutmut_96() -> argparse.Namespace:
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
        choices=None,
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


def x_parse_args__mutmut_97() -> argparse.Namespace:
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
        help=None,
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


def x_parse_args__mutmut_98() -> argparse.Namespace:
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
        "--format",
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


def x_parse_args__mutmut_99() -> argparse.Namespace:
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
        "-f", type=str,
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


def x_parse_args__mutmut_100() -> argparse.Namespace:
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


def x_parse_args__mutmut_101() -> argparse.Namespace:
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


def x_parse_args__mutmut_102() -> argparse.Namespace:
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


def x_parse_args__mutmut_103() -> argparse.Namespace:
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


def x_parse_args__mutmut_104() -> argparse.Namespace:
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
        "XX-fXX", "--format",
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


def x_parse_args__mutmut_105() -> argparse.Namespace:
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
        "-F", "--format",
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


def x_parse_args__mutmut_106() -> argparse.Namespace:
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
        "-f", "XX--formatXX",
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


def x_parse_args__mutmut_107() -> argparse.Namespace:
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
        "-f", "--FORMAT",
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


def x_parse_args__mutmut_108() -> argparse.Namespace:
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
        default="XXmp3XX",
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


def x_parse_args__mutmut_109() -> argparse.Namespace:
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
        default="MP3",
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


def x_parse_args__mutmut_110() -> argparse.Namespace:
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
        choices=["XXmp3XX", "wav"],
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


def x_parse_args__mutmut_111() -> argparse.Namespace:
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
        choices=["MP3", "wav"],
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


def x_parse_args__mutmut_112() -> argparse.Namespace:
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
        choices=["mp3", "XXwavXX"],
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


def x_parse_args__mutmut_113() -> argparse.Namespace:
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
        choices=["mp3", "WAV"],
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


def x_parse_args__mutmut_114() -> argparse.Namespace:
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
        help="XXOutput audio format (default: mp3)XX",
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


def x_parse_args__mutmut_115() -> argparse.Namespace:
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
        help="output audio format (default: mp3)",
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


def x_parse_args__mutmut_116() -> argparse.Namespace:
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
        help="OUTPUT AUDIO FORMAT (DEFAULT: MP3)",
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


def x_parse_args__mutmut_117() -> argparse.Namespace:
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
        None,
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


def x_parse_args__mutmut_118() -> argparse.Namespace:
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
        action=None,
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


def x_parse_args__mutmut_119() -> argparse.Namespace:
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
        help=None,
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


def x_parse_args__mutmut_120() -> argparse.Namespace:
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


def x_parse_args__mutmut_121() -> argparse.Namespace:
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


def x_parse_args__mutmut_122() -> argparse.Namespace:
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


def x_parse_args__mutmut_123() -> argparse.Namespace:
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
        "XX--ssmlXX",
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


def x_parse_args__mutmut_124() -> argparse.Namespace:
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
        "--SSML",
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


def x_parse_args__mutmut_125() -> argparse.Namespace:
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
        action="XXstore_trueXX",
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


def x_parse_args__mutmut_126() -> argparse.Namespace:
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
        action="STORE_TRUE",
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


def x_parse_args__mutmut_127() -> argparse.Namespace:
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
        help="XXTreat input as SSML markupXX",
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


def x_parse_args__mutmut_128() -> argparse.Namespace:
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
        help="treat input as ssml markup",
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


def x_parse_args__mutmut_129() -> argparse.Namespace:
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
        help="TREAT INPUT AS SSML MARKUP",
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


def x_parse_args__mutmut_130() -> argparse.Namespace:
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
        None,
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


def x_parse_args__mutmut_131() -> argparse.Namespace:
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
        type=None,
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


def x_parse_args__mutmut_132() -> argparse.Namespace:
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
        help=None,
    )
    
    parser.add_argument(
        "--backend",
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_133() -> argparse.Namespace:
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


def x_parse_args__mutmut_134() -> argparse.Namespace:
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


def x_parse_args__mutmut_135() -> argparse.Namespace:
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
        help="Input file path (reads text from file)",
    )
    
    parser.add_argument(
        "--backend",
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_136() -> argparse.Namespace:
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
        )
    
    parser.add_argument(
        "--backend",
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_137() -> argparse.Namespace:
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
        "XX--fileXX",
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


def x_parse_args__mutmut_138() -> argparse.Namespace:
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
        "--FILE",
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


def x_parse_args__mutmut_139() -> argparse.Namespace:
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
        help="XXInput file path (reads text from file)XX",
    )
    
    parser.add_argument(
        "--backend",
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_140() -> argparse.Namespace:
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
        help="input file path (reads text from file)",
    )
    
    parser.add_argument(
        "--backend",
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_141() -> argparse.Namespace:
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
        help="INPUT FILE PATH (READS TEXT FROM FILE)",
    )
    
    parser.add_argument(
        "--backend",
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_142() -> argparse.Namespace:
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
        None,
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_143() -> argparse.Namespace:
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
        type=None,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_144() -> argparse.Namespace:
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
        default=None,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_145() -> argparse.Namespace:
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
        help=None,
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_146() -> argparse.Namespace:
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
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_147() -> argparse.Namespace:
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
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_148() -> argparse.Namespace:
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
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_149() -> argparse.Namespace:
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
        )
    
    return parser.parse_args()


def x_parse_args__mutmut_150() -> argparse.Namespace:
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
        "XX--backendXX",
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()


def x_parse_args__mutmut_151() -> argparse.Namespace:
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
        "--BACKEND",
        type=str,
        default=KOKORO_BACKEND_URL,
        help=f"Backend URL (default: {KOKORO_BACKEND_URL})",
    )
    
    return parser.parse_args()

x_parse_args__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_parse_args__mutmut_1': x_parse_args__mutmut_1, 
    'x_parse_args__mutmut_2': x_parse_args__mutmut_2, 
    'x_parse_args__mutmut_3': x_parse_args__mutmut_3, 
    'x_parse_args__mutmut_4': x_parse_args__mutmut_4, 
    'x_parse_args__mutmut_5': x_parse_args__mutmut_5, 
    'x_parse_args__mutmut_6': x_parse_args__mutmut_6, 
    'x_parse_args__mutmut_7': x_parse_args__mutmut_7, 
    'x_parse_args__mutmut_8': x_parse_args__mutmut_8, 
    'x_parse_args__mutmut_9': x_parse_args__mutmut_9, 
    'x_parse_args__mutmut_10': x_parse_args__mutmut_10, 
    'x_parse_args__mutmut_11': x_parse_args__mutmut_11, 
    'x_parse_args__mutmut_12': x_parse_args__mutmut_12, 
    'x_parse_args__mutmut_13': x_parse_args__mutmut_13, 
    'x_parse_args__mutmut_14': x_parse_args__mutmut_14, 
    'x_parse_args__mutmut_15': x_parse_args__mutmut_15, 
    'x_parse_args__mutmut_16': x_parse_args__mutmut_16, 
    'x_parse_args__mutmut_17': x_parse_args__mutmut_17, 
    'x_parse_args__mutmut_18': x_parse_args__mutmut_18, 
    'x_parse_args__mutmut_19': x_parse_args__mutmut_19, 
    'x_parse_args__mutmut_20': x_parse_args__mutmut_20, 
    'x_parse_args__mutmut_21': x_parse_args__mutmut_21, 
    'x_parse_args__mutmut_22': x_parse_args__mutmut_22, 
    'x_parse_args__mutmut_23': x_parse_args__mutmut_23, 
    'x_parse_args__mutmut_24': x_parse_args__mutmut_24, 
    'x_parse_args__mutmut_25': x_parse_args__mutmut_25, 
    'x_parse_args__mutmut_26': x_parse_args__mutmut_26, 
    'x_parse_args__mutmut_27': x_parse_args__mutmut_27, 
    'x_parse_args__mutmut_28': x_parse_args__mutmut_28, 
    'x_parse_args__mutmut_29': x_parse_args__mutmut_29, 
    'x_parse_args__mutmut_30': x_parse_args__mutmut_30, 
    'x_parse_args__mutmut_31': x_parse_args__mutmut_31, 
    'x_parse_args__mutmut_32': x_parse_args__mutmut_32, 
    'x_parse_args__mutmut_33': x_parse_args__mutmut_33, 
    'x_parse_args__mutmut_34': x_parse_args__mutmut_34, 
    'x_parse_args__mutmut_35': x_parse_args__mutmut_35, 
    'x_parse_args__mutmut_36': x_parse_args__mutmut_36, 
    'x_parse_args__mutmut_37': x_parse_args__mutmut_37, 
    'x_parse_args__mutmut_38': x_parse_args__mutmut_38, 
    'x_parse_args__mutmut_39': x_parse_args__mutmut_39, 
    'x_parse_args__mutmut_40': x_parse_args__mutmut_40, 
    'x_parse_args__mutmut_41': x_parse_args__mutmut_41, 
    'x_parse_args__mutmut_42': x_parse_args__mutmut_42, 
    'x_parse_args__mutmut_43': x_parse_args__mutmut_43, 
    'x_parse_args__mutmut_44': x_parse_args__mutmut_44, 
    'x_parse_args__mutmut_45': x_parse_args__mutmut_45, 
    'x_parse_args__mutmut_46': x_parse_args__mutmut_46, 
    'x_parse_args__mutmut_47': x_parse_args__mutmut_47, 
    'x_parse_args__mutmut_48': x_parse_args__mutmut_48, 
    'x_parse_args__mutmut_49': x_parse_args__mutmut_49, 
    'x_parse_args__mutmut_50': x_parse_args__mutmut_50, 
    'x_parse_args__mutmut_51': x_parse_args__mutmut_51, 
    'x_parse_args__mutmut_52': x_parse_args__mutmut_52, 
    'x_parse_args__mutmut_53': x_parse_args__mutmut_53, 
    'x_parse_args__mutmut_54': x_parse_args__mutmut_54, 
    'x_parse_args__mutmut_55': x_parse_args__mutmut_55, 
    'x_parse_args__mutmut_56': x_parse_args__mutmut_56, 
    'x_parse_args__mutmut_57': x_parse_args__mutmut_57, 
    'x_parse_args__mutmut_58': x_parse_args__mutmut_58, 
    'x_parse_args__mutmut_59': x_parse_args__mutmut_59, 
    'x_parse_args__mutmut_60': x_parse_args__mutmut_60, 
    'x_parse_args__mutmut_61': x_parse_args__mutmut_61, 
    'x_parse_args__mutmut_62': x_parse_args__mutmut_62, 
    'x_parse_args__mutmut_63': x_parse_args__mutmut_63, 
    'x_parse_args__mutmut_64': x_parse_args__mutmut_64, 
    'x_parse_args__mutmut_65': x_parse_args__mutmut_65, 
    'x_parse_args__mutmut_66': x_parse_args__mutmut_66, 
    'x_parse_args__mutmut_67': x_parse_args__mutmut_67, 
    'x_parse_args__mutmut_68': x_parse_args__mutmut_68, 
    'x_parse_args__mutmut_69': x_parse_args__mutmut_69, 
    'x_parse_args__mutmut_70': x_parse_args__mutmut_70, 
    'x_parse_args__mutmut_71': x_parse_args__mutmut_71, 
    'x_parse_args__mutmut_72': x_parse_args__mutmut_72, 
    'x_parse_args__mutmut_73': x_parse_args__mutmut_73, 
    'x_parse_args__mutmut_74': x_parse_args__mutmut_74, 
    'x_parse_args__mutmut_75': x_parse_args__mutmut_75, 
    'x_parse_args__mutmut_76': x_parse_args__mutmut_76, 
    'x_parse_args__mutmut_77': x_parse_args__mutmut_77, 
    'x_parse_args__mutmut_78': x_parse_args__mutmut_78, 
    'x_parse_args__mutmut_79': x_parse_args__mutmut_79, 
    'x_parse_args__mutmut_80': x_parse_args__mutmut_80, 
    'x_parse_args__mutmut_81': x_parse_args__mutmut_81, 
    'x_parse_args__mutmut_82': x_parse_args__mutmut_82, 
    'x_parse_args__mutmut_83': x_parse_args__mutmut_83, 
    'x_parse_args__mutmut_84': x_parse_args__mutmut_84, 
    'x_parse_args__mutmut_85': x_parse_args__mutmut_85, 
    'x_parse_args__mutmut_86': x_parse_args__mutmut_86, 
    'x_parse_args__mutmut_87': x_parse_args__mutmut_87, 
    'x_parse_args__mutmut_88': x_parse_args__mutmut_88, 
    'x_parse_args__mutmut_89': x_parse_args__mutmut_89, 
    'x_parse_args__mutmut_90': x_parse_args__mutmut_90, 
    'x_parse_args__mutmut_91': x_parse_args__mutmut_91, 
    'x_parse_args__mutmut_92': x_parse_args__mutmut_92, 
    'x_parse_args__mutmut_93': x_parse_args__mutmut_93, 
    'x_parse_args__mutmut_94': x_parse_args__mutmut_94, 
    'x_parse_args__mutmut_95': x_parse_args__mutmut_95, 
    'x_parse_args__mutmut_96': x_parse_args__mutmut_96, 
    'x_parse_args__mutmut_97': x_parse_args__mutmut_97, 
    'x_parse_args__mutmut_98': x_parse_args__mutmut_98, 
    'x_parse_args__mutmut_99': x_parse_args__mutmut_99, 
    'x_parse_args__mutmut_100': x_parse_args__mutmut_100, 
    'x_parse_args__mutmut_101': x_parse_args__mutmut_101, 
    'x_parse_args__mutmut_102': x_parse_args__mutmut_102, 
    'x_parse_args__mutmut_103': x_parse_args__mutmut_103, 
    'x_parse_args__mutmut_104': x_parse_args__mutmut_104, 
    'x_parse_args__mutmut_105': x_parse_args__mutmut_105, 
    'x_parse_args__mutmut_106': x_parse_args__mutmut_106, 
    'x_parse_args__mutmut_107': x_parse_args__mutmut_107, 
    'x_parse_args__mutmut_108': x_parse_args__mutmut_108, 
    'x_parse_args__mutmut_109': x_parse_args__mutmut_109, 
    'x_parse_args__mutmut_110': x_parse_args__mutmut_110, 
    'x_parse_args__mutmut_111': x_parse_args__mutmut_111, 
    'x_parse_args__mutmut_112': x_parse_args__mutmut_112, 
    'x_parse_args__mutmut_113': x_parse_args__mutmut_113, 
    'x_parse_args__mutmut_114': x_parse_args__mutmut_114, 
    'x_parse_args__mutmut_115': x_parse_args__mutmut_115, 
    'x_parse_args__mutmut_116': x_parse_args__mutmut_116, 
    'x_parse_args__mutmut_117': x_parse_args__mutmut_117, 
    'x_parse_args__mutmut_118': x_parse_args__mutmut_118, 
    'x_parse_args__mutmut_119': x_parse_args__mutmut_119, 
    'x_parse_args__mutmut_120': x_parse_args__mutmut_120, 
    'x_parse_args__mutmut_121': x_parse_args__mutmut_121, 
    'x_parse_args__mutmut_122': x_parse_args__mutmut_122, 
    'x_parse_args__mutmut_123': x_parse_args__mutmut_123, 
    'x_parse_args__mutmut_124': x_parse_args__mutmut_124, 
    'x_parse_args__mutmut_125': x_parse_args__mutmut_125, 
    'x_parse_args__mutmut_126': x_parse_args__mutmut_126, 
    'x_parse_args__mutmut_127': x_parse_args__mutmut_127, 
    'x_parse_args__mutmut_128': x_parse_args__mutmut_128, 
    'x_parse_args__mutmut_129': x_parse_args__mutmut_129, 
    'x_parse_args__mutmut_130': x_parse_args__mutmut_130, 
    'x_parse_args__mutmut_131': x_parse_args__mutmut_131, 
    'x_parse_args__mutmut_132': x_parse_args__mutmut_132, 
    'x_parse_args__mutmut_133': x_parse_args__mutmut_133, 
    'x_parse_args__mutmut_134': x_parse_args__mutmut_134, 
    'x_parse_args__mutmut_135': x_parse_args__mutmut_135, 
    'x_parse_args__mutmut_136': x_parse_args__mutmut_136, 
    'x_parse_args__mutmut_137': x_parse_args__mutmut_137, 
    'x_parse_args__mutmut_138': x_parse_args__mutmut_138, 
    'x_parse_args__mutmut_139': x_parse_args__mutmut_139, 
    'x_parse_args__mutmut_140': x_parse_args__mutmut_140, 
    'x_parse_args__mutmut_141': x_parse_args__mutmut_141, 
    'x_parse_args__mutmut_142': x_parse_args__mutmut_142, 
    'x_parse_args__mutmut_143': x_parse_args__mutmut_143, 
    'x_parse_args__mutmut_144': x_parse_args__mutmut_144, 
    'x_parse_args__mutmut_145': x_parse_args__mutmut_145, 
    'x_parse_args__mutmut_146': x_parse_args__mutmut_146, 
    'x_parse_args__mutmut_147': x_parse_args__mutmut_147, 
    'x_parse_args__mutmut_148': x_parse_args__mutmut_148, 
    'x_parse_args__mutmut_149': x_parse_args__mutmut_149, 
    'x_parse_args__mutmut_150': x_parse_args__mutmut_150, 
    'x_parse_args__mutmut_151': x_parse_args__mutmut_151
}
x_parse_args__mutmut_orig.__name__ = 'x_parse_args'


def read_input(args: argparse.Namespace) -> str:
    args = [args]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_read_input__mutmut_orig, x_read_input__mutmut_mutants, args, kwargs, None)


def x_read_input__mutmut_orig(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_1(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = None
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_2(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(None)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_3(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_4(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(None)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_5(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(None, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_6(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, None, encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_7(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding=None) as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_8(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open("r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_9(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_10(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", ) as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_11(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "XXrXX", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_12(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "R", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_13(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="XXutf-8XX") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_14(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="UTF-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_15(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_16(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("No input provided. Use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_17(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError(None)


def x_read_input__mutmut_18(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("XXNo input provided. Use -i/--input, --file, or pipe input via stdin.XX")


def x_read_input__mutmut_19(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("no input provided. use -i/--input, --file, or pipe input via stdin.")


def x_read_input__mutmut_20(args: argparse.Namespace) -> str:
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
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {args.file}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    if args.input is not None:
        # Use CLI argument (including empty string - let caller validate)
        return args.input.strip()
    
    # Try reading from stdin (if piped)
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    
    raise ValueError("NO INPUT PROVIDED. USE -I/--INPUT, --FILE, OR PIPE INPUT VIA STDIN.")

x_read_input__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_read_input__mutmut_1': x_read_input__mutmut_1, 
    'x_read_input__mutmut_2': x_read_input__mutmut_2, 
    'x_read_input__mutmut_3': x_read_input__mutmut_3, 
    'x_read_input__mutmut_4': x_read_input__mutmut_4, 
    'x_read_input__mutmut_5': x_read_input__mutmut_5, 
    'x_read_input__mutmut_6': x_read_input__mutmut_6, 
    'x_read_input__mutmut_7': x_read_input__mutmut_7, 
    'x_read_input__mutmut_8': x_read_input__mutmut_8, 
    'x_read_input__mutmut_9': x_read_input__mutmut_9, 
    'x_read_input__mutmut_10': x_read_input__mutmut_10, 
    'x_read_input__mutmut_11': x_read_input__mutmut_11, 
    'x_read_input__mutmut_12': x_read_input__mutmut_12, 
    'x_read_input__mutmut_13': x_read_input__mutmut_13, 
    'x_read_input__mutmut_14': x_read_input__mutmut_14, 
    'x_read_input__mutmut_15': x_read_input__mutmut_15, 
    'x_read_input__mutmut_16': x_read_input__mutmut_16, 
    'x_read_input__mutmut_17': x_read_input__mutmut_17, 
    'x_read_input__mutmut_18': x_read_input__mutmut_18, 
    'x_read_input__mutmut_19': x_read_input__mutmut_19, 
    'x_read_input__mutmut_20': x_read_input__mutmut_20
}
x_read_input__mutmut_orig.__name__ = 'x_read_input'


async def synthesize(
    engine: SynthesisEngine,
    text: str,
    voice: str,
    speed: float,
    is_ssml: bool,
) -> bytes:
    args = [engine, text, voice, speed, is_ssml]# type: ignore
    kwargs = {}# type: ignore
    return await _mutmut_trampoline(x_synthesize__mutmut_orig, x_synthesize__mutmut_mutants, args, kwargs, None)


async def x_synthesize__mutmut_orig(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_1(
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
    logger.info(None)
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_2(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(None)
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_3(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:101]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_4(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'XX...XX' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_5(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) >= 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_6(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 101 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_7(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else 'XXXX'}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_8(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(None, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_9(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, None, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_10(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, None)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_11(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(voice, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_12(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, speed)
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_13(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, )
    else:
        return await engine.synthesize_text(text, voice, speed)


async def x_synthesize__mutmut_14(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(None, voice, speed)


async def x_synthesize__mutmut_15(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, None, speed)


async def x_synthesize__mutmut_16(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, None)


async def x_synthesize__mutmut_17(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(voice, speed)


async def x_synthesize__mutmut_18(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, speed)


async def x_synthesize__mutmut_19(
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
    logger.info(f"Synthesizing (voice={voice}, speed={speed}, ssml={is_ssml})")
    logger.debug(f"Input text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    if is_ssml:
        return await engine.synthesize_ssml(text, voice, speed)
    else:
        return await engine.synthesize_text(text, voice, )

x_synthesize__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_synthesize__mutmut_1': x_synthesize__mutmut_1, 
    'x_synthesize__mutmut_2': x_synthesize__mutmut_2, 
    'x_synthesize__mutmut_3': x_synthesize__mutmut_3, 
    'x_synthesize__mutmut_4': x_synthesize__mutmut_4, 
    'x_synthesize__mutmut_5': x_synthesize__mutmut_5, 
    'x_synthesize__mutmut_6': x_synthesize__mutmut_6, 
    'x_synthesize__mutmut_7': x_synthesize__mutmut_7, 
    'x_synthesize__mutmut_8': x_synthesize__mutmut_8, 
    'x_synthesize__mutmut_9': x_synthesize__mutmut_9, 
    'x_synthesize__mutmut_10': x_synthesize__mutmut_10, 
    'x_synthesize__mutmut_11': x_synthesize__mutmut_11, 
    'x_synthesize__mutmut_12': x_synthesize__mutmut_12, 
    'x_synthesize__mutmut_13': x_synthesize__mutmut_13, 
    'x_synthesize__mutmut_14': x_synthesize__mutmut_14, 
    'x_synthesize__mutmut_15': x_synthesize__mutmut_15, 
    'x_synthesize__mutmut_16': x_synthesize__mutmut_16, 
    'x_synthesize__mutmut_17': x_synthesize__mutmut_17, 
    'x_synthesize__mutmut_18': x_synthesize__mutmut_18, 
    'x_synthesize__mutmut_19': x_synthesize__mutmut_19
}
x_synthesize__mutmut_orig.__name__ = 'x_synthesize'


async def main_async(args: argparse.Namespace) -> int:
    args = [args]# type: ignore
    kwargs = {}# type: ignore
    return await _mutmut_trampoline(x_main_async__mutmut_orig, x_main_async__mutmut_mutants, args, kwargs, None)


async def x_main_async__mutmut_orig(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_1(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = None
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_2(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(None)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_3(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_4(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error(None)
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_5(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("XXEmpty input providedXX")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_6(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_7(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("EMPTY INPUT PROVIDED")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_8(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 2
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_9(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = None
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_10(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(None)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_11(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() and (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_12(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix or "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_13(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_14(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "XX.XX" not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_15(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_16(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = None
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_17(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path * f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_18(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=None, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_19(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=None)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_20(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_21(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, )
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_22(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=False, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_23(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=False)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_24(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = None
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_25(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=None)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_26(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = None
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_27(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                None,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_28(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                None,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_29(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                None,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_30(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                None,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_31(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                None,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_32(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_33(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_34(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_35(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_36(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_37(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_38(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error(None)
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_39(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("XXNo audio data generatedXX")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_40(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("no audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_41(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("NO AUDIO DATA GENERATED")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_42(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 2
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_43(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format != "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_44(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "XXmp3XX":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_45(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "MP3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_46(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(None, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_47(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, None) as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_48(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open("wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_49(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, ) as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_50(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "XXwbXX") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_51(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "WB") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_52(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(None)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_53(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(None)
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_54(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = None
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_55(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(None)
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_56(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix("XX.mp3XX")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_57(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".MP3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_58(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(None, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_59(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, None) as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_60(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open("wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_61(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, ) as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_62(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "XXwbXX") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_63(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "WB") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_64(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(None)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_65(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = None
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_66(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(None, str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_67(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), None)
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_68(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_69(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), )
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_70(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(None), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_71(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(None))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_72(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_73(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error(None)
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_74(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("XXFFmpeg conversion failedXX")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_75(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("ffmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_76(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFMPEG CONVERSION FAILED")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_77(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 2
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_78(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(None)
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_79(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 1
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_80(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(None)
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_81(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 2
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_82(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(None)
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_83(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 2
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 1


async def x_main_async__mutmut_84(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(None, exc_info=True)
        return 1


async def x_main_async__mutmut_85(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=None)
        return 1


async def x_main_async__mutmut_86(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(exc_info=True)
        return 1


async def x_main_async__mutmut_87(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", )
        return 1


async def x_main_async__mutmut_88(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=False)
        return 1


async def x_main_async__mutmut_89(args: argparse.Namespace) -> int:
    """
    Async main entry point.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 = success)
    """
    try:
        # Read input
        text = read_input(args)
        
        if not text:
            logger.error("Empty input provided")
            return 1
        
        # Determine output path
        output_path = Path(args.output)
        
        # If output is a directory, generate filename
        if output_path.is_dir() or (not output_path.suffix and "." not in output_path.name):
            output_path = output_path / f"output.{args.format}"
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize synthesis engine
        engine = SynthesisEngine(backend_url=args.backend)
        
        try:
            # Synthesize
            audio_data = await synthesize(
                engine,
                text,
                args.voice,
                args.speed,
                args.ssml,
            )
            
            if not audio_data:
                logger.error("No audio data generated")
                return 1
            
            # Write MP3 directly
            if args.format == "mp3":
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Saved MP3: {output_path} ({len(audio_data)} bytes)")
            else:
                # Convert MP3 to WAV using ffmpeg
                temp_mp3 = output_path.with_suffix(".mp3")
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                success = convert_mp3_to_wav(str(temp_mp3), str(output_path))
                
                # Clean up temp file
                if temp_mp3.exists():
                    temp_mp3.unlink()
                
                if not success:
                    logger.error("FFmpeg conversion failed")
                    return 1
                
                logger.info(f"Saved WAV: {output_path}")
        
        finally:
            await engine.close()
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except (ValueError, IOError, OSError) as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        return 2

x_main_async__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_main_async__mutmut_1': x_main_async__mutmut_1, 
    'x_main_async__mutmut_2': x_main_async__mutmut_2, 
    'x_main_async__mutmut_3': x_main_async__mutmut_3, 
    'x_main_async__mutmut_4': x_main_async__mutmut_4, 
    'x_main_async__mutmut_5': x_main_async__mutmut_5, 
    'x_main_async__mutmut_6': x_main_async__mutmut_6, 
    'x_main_async__mutmut_7': x_main_async__mutmut_7, 
    'x_main_async__mutmut_8': x_main_async__mutmut_8, 
    'x_main_async__mutmut_9': x_main_async__mutmut_9, 
    'x_main_async__mutmut_10': x_main_async__mutmut_10, 
    'x_main_async__mutmut_11': x_main_async__mutmut_11, 
    'x_main_async__mutmut_12': x_main_async__mutmut_12, 
    'x_main_async__mutmut_13': x_main_async__mutmut_13, 
    'x_main_async__mutmut_14': x_main_async__mutmut_14, 
    'x_main_async__mutmut_15': x_main_async__mutmut_15, 
    'x_main_async__mutmut_16': x_main_async__mutmut_16, 
    'x_main_async__mutmut_17': x_main_async__mutmut_17, 
    'x_main_async__mutmut_18': x_main_async__mutmut_18, 
    'x_main_async__mutmut_19': x_main_async__mutmut_19, 
    'x_main_async__mutmut_20': x_main_async__mutmut_20, 
    'x_main_async__mutmut_21': x_main_async__mutmut_21, 
    'x_main_async__mutmut_22': x_main_async__mutmut_22, 
    'x_main_async__mutmut_23': x_main_async__mutmut_23, 
    'x_main_async__mutmut_24': x_main_async__mutmut_24, 
    'x_main_async__mutmut_25': x_main_async__mutmut_25, 
    'x_main_async__mutmut_26': x_main_async__mutmut_26, 
    'x_main_async__mutmut_27': x_main_async__mutmut_27, 
    'x_main_async__mutmut_28': x_main_async__mutmut_28, 
    'x_main_async__mutmut_29': x_main_async__mutmut_29, 
    'x_main_async__mutmut_30': x_main_async__mutmut_30, 
    'x_main_async__mutmut_31': x_main_async__mutmut_31, 
    'x_main_async__mutmut_32': x_main_async__mutmut_32, 
    'x_main_async__mutmut_33': x_main_async__mutmut_33, 
    'x_main_async__mutmut_34': x_main_async__mutmut_34, 
    'x_main_async__mutmut_35': x_main_async__mutmut_35, 
    'x_main_async__mutmut_36': x_main_async__mutmut_36, 
    'x_main_async__mutmut_37': x_main_async__mutmut_37, 
    'x_main_async__mutmut_38': x_main_async__mutmut_38, 
    'x_main_async__mutmut_39': x_main_async__mutmut_39, 
    'x_main_async__mutmut_40': x_main_async__mutmut_40, 
    'x_main_async__mutmut_41': x_main_async__mutmut_41, 
    'x_main_async__mutmut_42': x_main_async__mutmut_42, 
    'x_main_async__mutmut_43': x_main_async__mutmut_43, 
    'x_main_async__mutmut_44': x_main_async__mutmut_44, 
    'x_main_async__mutmut_45': x_main_async__mutmut_45, 
    'x_main_async__mutmut_46': x_main_async__mutmut_46, 
    'x_main_async__mutmut_47': x_main_async__mutmut_47, 
    'x_main_async__mutmut_48': x_main_async__mutmut_48, 
    'x_main_async__mutmut_49': x_main_async__mutmut_49, 
    'x_main_async__mutmut_50': x_main_async__mutmut_50, 
    'x_main_async__mutmut_51': x_main_async__mutmut_51, 
    'x_main_async__mutmut_52': x_main_async__mutmut_52, 
    'x_main_async__mutmut_53': x_main_async__mutmut_53, 
    'x_main_async__mutmut_54': x_main_async__mutmut_54, 
    'x_main_async__mutmut_55': x_main_async__mutmut_55, 
    'x_main_async__mutmut_56': x_main_async__mutmut_56, 
    'x_main_async__mutmut_57': x_main_async__mutmut_57, 
    'x_main_async__mutmut_58': x_main_async__mutmut_58, 
    'x_main_async__mutmut_59': x_main_async__mutmut_59, 
    'x_main_async__mutmut_60': x_main_async__mutmut_60, 
    'x_main_async__mutmut_61': x_main_async__mutmut_61, 
    'x_main_async__mutmut_62': x_main_async__mutmut_62, 
    'x_main_async__mutmut_63': x_main_async__mutmut_63, 
    'x_main_async__mutmut_64': x_main_async__mutmut_64, 
    'x_main_async__mutmut_65': x_main_async__mutmut_65, 
    'x_main_async__mutmut_66': x_main_async__mutmut_66, 
    'x_main_async__mutmut_67': x_main_async__mutmut_67, 
    'x_main_async__mutmut_68': x_main_async__mutmut_68, 
    'x_main_async__mutmut_69': x_main_async__mutmut_69, 
    'x_main_async__mutmut_70': x_main_async__mutmut_70, 
    'x_main_async__mutmut_71': x_main_async__mutmut_71, 
    'x_main_async__mutmut_72': x_main_async__mutmut_72, 
    'x_main_async__mutmut_73': x_main_async__mutmut_73, 
    'x_main_async__mutmut_74': x_main_async__mutmut_74, 
    'x_main_async__mutmut_75': x_main_async__mutmut_75, 
    'x_main_async__mutmut_76': x_main_async__mutmut_76, 
    'x_main_async__mutmut_77': x_main_async__mutmut_77, 
    'x_main_async__mutmut_78': x_main_async__mutmut_78, 
    'x_main_async__mutmut_79': x_main_async__mutmut_79, 
    'x_main_async__mutmut_80': x_main_async__mutmut_80, 
    'x_main_async__mutmut_81': x_main_async__mutmut_81, 
    'x_main_async__mutmut_82': x_main_async__mutmut_82, 
    'x_main_async__mutmut_83': x_main_async__mutmut_83, 
    'x_main_async__mutmut_84': x_main_async__mutmut_84, 
    'x_main_async__mutmut_85': x_main_async__mutmut_85, 
    'x_main_async__mutmut_86': x_main_async__mutmut_86, 
    'x_main_async__mutmut_87': x_main_async__mutmut_87, 
    'x_main_async__mutmut_88': x_main_async__mutmut_88, 
    'x_main_async__mutmut_89': x_main_async__mutmut_89
}
x_main_async__mutmut_orig.__name__ = 'x_main_async'


def main() -> int:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_main__mutmut_orig, x_main__mutmut_mutants, args, kwargs, None)


def x_main__mutmut_orig() -> int:
    """Main entry point."""
    args = parse_args()
    return asyncio.run(main_async(args))


def x_main__mutmut_1() -> int:
    """Main entry point."""
    args = None
    return asyncio.run(main_async(args))


def x_main__mutmut_2() -> int:
    """Main entry point."""
    args = parse_args()
    return asyncio.run(None)


def x_main__mutmut_3() -> int:
    """Main entry point."""
    args = parse_args()
    return asyncio.run(main_async(None))

x_main__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_main__mutmut_1': x_main__mutmut_1, 
    'x_main__mutmut_2': x_main__mutmut_2, 
    'x_main__mutmut_3': x_main__mutmut_3
}
x_main__mutmut_orig.__name__ = 'x_main'


if __name__ == "__main__":
    sys.exit(main())
