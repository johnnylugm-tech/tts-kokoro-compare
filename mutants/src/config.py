"""Configuration settings for Kokoro Taiwan Proxy."""

from typing import Dict

# Kokoro Backend URLs
KOKORO_BACKEND_URL = "http://localhost:8880/v1/audio/speech"
KOKORO_VOICES_URL = "http://localhost:8880/v1/audio/voices"

# Default settings
DEFAULT_VOICE = "zf_xiaoxiao"
DEFAULT_SPEED = 1.0
MAX_CHARS_PER_REQUEST = 250  # Maximum characters per segment
LEXICON_MIN_SIZE = 50  # Minimum Taiwan lexicon entries required
NFR_TTFB_TARGET_MS = 300  # Target time-to-first-byte in milliseconds
REQUEST_TIMEOUT = 30.0  # seconds

# Circuit breaker settings
CIRCUIT_BREAKER_THRESHOLD = 3  # failures before opening
CIRCUIT_BREAKER_TIMEOUT = 10.0  # seconds before half-open

# Warmup settings
WARMUP_ENABLED = True
WARMUP_TEXT = "你好，測試中"

# Model to voice/persona mapping
MODEL_MAP: Dict[str, str] = {
    "tts-1": "kokoro",
    "tts-1-hd": "kokoro",
    "kokoro": "kokoro",
    "custom-gentle": "zf_xiaoxiao(0.8)+af_heart(0.2)",
}

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
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
