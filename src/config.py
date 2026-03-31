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
