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
        args = [backend_url, timeout]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSynthesisEngineǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁSynthesisEngineǁ__init____mutmut_mutants'), args, kwargs, self)
    
    def xǁSynthesisEngineǁ__init____mutmut_orig(
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
    
    def xǁSynthesisEngineǁ__init____mutmut_1(
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
        self.backend_url = None
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        self.text_splitter = TextSplitter()
        self.ssml_parser = SSMLParser()
        self.linguistic_engine = TaiwanLinguisticEngine()
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def xǁSynthesisEngineǁ__init____mutmut_2(
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
        self.timeout = None
        self.client = httpx.AsyncClient(timeout=timeout)
        self.text_splitter = TextSplitter()
        self.ssml_parser = SSMLParser()
        self.linguistic_engine = TaiwanLinguisticEngine()
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def xǁSynthesisEngineǁ__init____mutmut_3(
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
        self.client = None
        self.text_splitter = TextSplitter()
        self.ssml_parser = SSMLParser()
        self.linguistic_engine = TaiwanLinguisticEngine()
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def xǁSynthesisEngineǁ__init____mutmut_4(
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
        self.client = httpx.AsyncClient(timeout=None)
        self.text_splitter = TextSplitter()
        self.ssml_parser = SSMLParser()
        self.linguistic_engine = TaiwanLinguisticEngine()
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def xǁSynthesisEngineǁ__init____mutmut_5(
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
        self.text_splitter = None
        self.ssml_parser = SSMLParser()
        self.linguistic_engine = TaiwanLinguisticEngine()
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def xǁSynthesisEngineǁ__init____mutmut_6(
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
        self.ssml_parser = None
        self.linguistic_engine = TaiwanLinguisticEngine()
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def xǁSynthesisEngineǁ__init____mutmut_7(
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
        self.linguistic_engine = None
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def xǁSynthesisEngineǁ__init____mutmut_8(
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
        self._executor = None
    
    def xǁSynthesisEngineǁ__init____mutmut_9(
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
        self._executor = ThreadPoolExecutor(max_workers=None)
    
    def xǁSynthesisEngineǁ__init____mutmut_10(
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
        self._executor = ThreadPoolExecutor(max_workers=5)
    
    xǁSynthesisEngineǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSynthesisEngineǁ__init____mutmut_1': xǁSynthesisEngineǁ__init____mutmut_1, 
        'xǁSynthesisEngineǁ__init____mutmut_2': xǁSynthesisEngineǁ__init____mutmut_2, 
        'xǁSynthesisEngineǁ__init____mutmut_3': xǁSynthesisEngineǁ__init____mutmut_3, 
        'xǁSynthesisEngineǁ__init____mutmut_4': xǁSynthesisEngineǁ__init____mutmut_4, 
        'xǁSynthesisEngineǁ__init____mutmut_5': xǁSynthesisEngineǁ__init____mutmut_5, 
        'xǁSynthesisEngineǁ__init____mutmut_6': xǁSynthesisEngineǁ__init____mutmut_6, 
        'xǁSynthesisEngineǁ__init____mutmut_7': xǁSynthesisEngineǁ__init____mutmut_7, 
        'xǁSynthesisEngineǁ__init____mutmut_8': xǁSynthesisEngineǁ__init____mutmut_8, 
        'xǁSynthesisEngineǁ__init____mutmut_9': xǁSynthesisEngineǁ__init____mutmut_9, 
        'xǁSynthesisEngineǁ__init____mutmut_10': xǁSynthesisEngineǁ__init____mutmut_10
    }
    xǁSynthesisEngineǁ__init____mutmut_orig.__name__ = 'xǁSynthesisEngineǁ__init__'
    
    async def synthesize(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
        model: str = "kokoro",
    ) -> bytes:
        args = [text, voice, speed, model]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁSynthesisEngineǁsynthesize__mutmut_orig'), object.__getattribute__(self, 'xǁSynthesisEngineǁsynthesize__mutmut_mutants'), args, kwargs, self)
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_orig(
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_1(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
        model: str = "XXkokoroXX",
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_2(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
        model: str = "KOKORO",
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_3(
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
        if not text and not text.strip():
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_4(
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
        if text or not text.strip():
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_5(
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
        if not text or text.strip():
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_6(
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
            logger.warning(None)
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_7(
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
            logger.warning("XXEmpty text provided to synthesizeXX")
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_8(
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
            logger.warning("empty text provided to synthesize")
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_9(
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
            logger.warning("EMPTY TEXT PROVIDED TO SYNTHESIZE")
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_10(
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
            return b"XXXX"
        
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_11(
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
        
        logger.info(None)
        
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_12(
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
            processed_text = None
            
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_13(
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
            processed_text = self.linguistic_engine.preprocess_for_tts(None)
            
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_14(
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
            payload = None
            
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_15(
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
                "XXmodelXX": model,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_16(
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
                "MODEL": model,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_17(
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
                "XXinputXX": processed_text,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_18(
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
                "INPUT": processed_text,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_19(
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
                "XXvoiceXX": voice,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_20(
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
                "VOICE": voice,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_21(
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
                "XXspeedXX": speed,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_22(
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
                "SPEED": speed,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_23(
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
            response = None
            
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_24(
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
                None,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_25(
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
                json=None,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_26(
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
                headers=None,
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_27(
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_28(
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_29(
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_30(
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
                headers={"XXContent-TypeXX": "application/json"},
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_31(
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
                headers={"content-type": "application/json"},
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_32(
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
                headers={"CONTENT-TYPE": "application/json"},
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_33(
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
                headers={"Content-Type": "XXapplication/jsonXX"},
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_34(
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
                headers={"Content-Type": "APPLICATION/JSON"},
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_35(
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
            
            audio_data = None
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_36(
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
            logger.debug(None)
            
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_37(
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
            logger.error(None)
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_38(
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
            logger.error(f"Request timeout for text: {text[:51]}...")
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
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_39(
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
            logger.error(None)
            raise
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during synthesis: {e}")
            raise
        except (ValueError, IOError, OSError) as e:
            logger.error(f"Unexpected error during synthesis: {e}")
            raise
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_40(
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
            logger.error(None)
            raise
        except (ValueError, IOError, OSError) as e:
            logger.error(f"Unexpected error during synthesis: {e}")
            raise
    
    async def xǁSynthesisEngineǁsynthesize__mutmut_41(
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
            logger.error(None)
            raise
    
    xǁSynthesisEngineǁsynthesize__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSynthesisEngineǁsynthesize__mutmut_1': xǁSynthesisEngineǁsynthesize__mutmut_1, 
        'xǁSynthesisEngineǁsynthesize__mutmut_2': xǁSynthesisEngineǁsynthesize__mutmut_2, 
        'xǁSynthesisEngineǁsynthesize__mutmut_3': xǁSynthesisEngineǁsynthesize__mutmut_3, 
        'xǁSynthesisEngineǁsynthesize__mutmut_4': xǁSynthesisEngineǁsynthesize__mutmut_4, 
        'xǁSynthesisEngineǁsynthesize__mutmut_5': xǁSynthesisEngineǁsynthesize__mutmut_5, 
        'xǁSynthesisEngineǁsynthesize__mutmut_6': xǁSynthesisEngineǁsynthesize__mutmut_6, 
        'xǁSynthesisEngineǁsynthesize__mutmut_7': xǁSynthesisEngineǁsynthesize__mutmut_7, 
        'xǁSynthesisEngineǁsynthesize__mutmut_8': xǁSynthesisEngineǁsynthesize__mutmut_8, 
        'xǁSynthesisEngineǁsynthesize__mutmut_9': xǁSynthesisEngineǁsynthesize__mutmut_9, 
        'xǁSynthesisEngineǁsynthesize__mutmut_10': xǁSynthesisEngineǁsynthesize__mutmut_10, 
        'xǁSynthesisEngineǁsynthesize__mutmut_11': xǁSynthesisEngineǁsynthesize__mutmut_11, 
        'xǁSynthesisEngineǁsynthesize__mutmut_12': xǁSynthesisEngineǁsynthesize__mutmut_12, 
        'xǁSynthesisEngineǁsynthesize__mutmut_13': xǁSynthesisEngineǁsynthesize__mutmut_13, 
        'xǁSynthesisEngineǁsynthesize__mutmut_14': xǁSynthesisEngineǁsynthesize__mutmut_14, 
        'xǁSynthesisEngineǁsynthesize__mutmut_15': xǁSynthesisEngineǁsynthesize__mutmut_15, 
        'xǁSynthesisEngineǁsynthesize__mutmut_16': xǁSynthesisEngineǁsynthesize__mutmut_16, 
        'xǁSynthesisEngineǁsynthesize__mutmut_17': xǁSynthesisEngineǁsynthesize__mutmut_17, 
        'xǁSynthesisEngineǁsynthesize__mutmut_18': xǁSynthesisEngineǁsynthesize__mutmut_18, 
        'xǁSynthesisEngineǁsynthesize__mutmut_19': xǁSynthesisEngineǁsynthesize__mutmut_19, 
        'xǁSynthesisEngineǁsynthesize__mutmut_20': xǁSynthesisEngineǁsynthesize__mutmut_20, 
        'xǁSynthesisEngineǁsynthesize__mutmut_21': xǁSynthesisEngineǁsynthesize__mutmut_21, 
        'xǁSynthesisEngineǁsynthesize__mutmut_22': xǁSynthesisEngineǁsynthesize__mutmut_22, 
        'xǁSynthesisEngineǁsynthesize__mutmut_23': xǁSynthesisEngineǁsynthesize__mutmut_23, 
        'xǁSynthesisEngineǁsynthesize__mutmut_24': xǁSynthesisEngineǁsynthesize__mutmut_24, 
        'xǁSynthesisEngineǁsynthesize__mutmut_25': xǁSynthesisEngineǁsynthesize__mutmut_25, 
        'xǁSynthesisEngineǁsynthesize__mutmut_26': xǁSynthesisEngineǁsynthesize__mutmut_26, 
        'xǁSynthesisEngineǁsynthesize__mutmut_27': xǁSynthesisEngineǁsynthesize__mutmut_27, 
        'xǁSynthesisEngineǁsynthesize__mutmut_28': xǁSynthesisEngineǁsynthesize__mutmut_28, 
        'xǁSynthesisEngineǁsynthesize__mutmut_29': xǁSynthesisEngineǁsynthesize__mutmut_29, 
        'xǁSynthesisEngineǁsynthesize__mutmut_30': xǁSynthesisEngineǁsynthesize__mutmut_30, 
        'xǁSynthesisEngineǁsynthesize__mutmut_31': xǁSynthesisEngineǁsynthesize__mutmut_31, 
        'xǁSynthesisEngineǁsynthesize__mutmut_32': xǁSynthesisEngineǁsynthesize__mutmut_32, 
        'xǁSynthesisEngineǁsynthesize__mutmut_33': xǁSynthesisEngineǁsynthesize__mutmut_33, 
        'xǁSynthesisEngineǁsynthesize__mutmut_34': xǁSynthesisEngineǁsynthesize__mutmut_34, 
        'xǁSynthesisEngineǁsynthesize__mutmut_35': xǁSynthesisEngineǁsynthesize__mutmut_35, 
        'xǁSynthesisEngineǁsynthesize__mutmut_36': xǁSynthesisEngineǁsynthesize__mutmut_36, 
        'xǁSynthesisEngineǁsynthesize__mutmut_37': xǁSynthesisEngineǁsynthesize__mutmut_37, 
        'xǁSynthesisEngineǁsynthesize__mutmut_38': xǁSynthesisEngineǁsynthesize__mutmut_38, 
        'xǁSynthesisEngineǁsynthesize__mutmut_39': xǁSynthesisEngineǁsynthesize__mutmut_39, 
        'xǁSynthesisEngineǁsynthesize__mutmut_40': xǁSynthesisEngineǁsynthesize__mutmut_40, 
        'xǁSynthesisEngineǁsynthesize__mutmut_41': xǁSynthesisEngineǁsynthesize__mutmut_41
    }
    xǁSynthesisEngineǁsynthesize__mutmut_orig.__name__ = 'xǁSynthesisEngineǁsynthesize'

    async def synthesize_segments(
        self,
        segments: List[Dict[str, Any]],
        voice: str = DEFAULT_VOICE,
        model: str = "kokoro",
    ) -> bytes:
        args = [segments, voice, model]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁSynthesisEngineǁsynthesize_segments__mutmut_orig'), object.__getattribute__(self, 'xǁSynthesisEngineǁsynthesize_segments__mutmut_mutants'), args, kwargs, self)

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_orig(
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_1(
        self,
        segments: List[Dict[str, Any]],
        voice: str = DEFAULT_VOICE,
        model: str = "XXkokoroXX",
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_2(
        self,
        segments: List[Dict[str, Any]],
        voice: str = DEFAULT_VOICE,
        model: str = "KOKORO",
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_3(
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
        if segments:
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_4(
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
            return b"XXXX"
        
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_5(
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
        tasks = None
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_6(
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
        for i, seg in enumerate(None):
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_7(
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
            text = None
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_8(
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
            text = seg.get(None, "")
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_9(
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
            text = seg.get("text", None)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_10(
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
            text = seg.get("")
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_11(
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
            text = seg.get("text", )
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_12(
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
            text = seg.get("XXtextXX", "")
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_13(
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
            text = seg.get("TEXT", "")
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_14(
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
            text = seg.get("text", "XXXX")
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_15(
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
            speed = None
            
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_16(
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
            speed = seg.get(None, DEFAULT_SPEED)
            
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_17(
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
            speed = seg.get("speed", None)
            
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_18(
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
            speed = seg.get(DEFAULT_SPEED)
            
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_19(
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
            speed = seg.get("speed", )
            
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_20(
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
            speed = seg.get("XXspeedXX", DEFAULT_SPEED)
            
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_21(
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
            speed = seg.get("SPEED", DEFAULT_SPEED)
            
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_22(
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
            
            if text or text.strip():
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_23(
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
                logger.debug(None)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_24(
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
                logger.debug(f"Queuing segment {i}: {text[:31]}... (speed={speed})")
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_25(
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
                    None
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_26(
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
                    self._synthesize_segment_with_retry(None, voice, speed, model)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_27(
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
                    self._synthesize_segment_with_retry(text, None, speed, model)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_28(
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
                    self._synthesize_segment_with_retry(text, voice, None, model)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_29(
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
                    self._synthesize_segment_with_retry(text, voice, speed, None)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_30(
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
                    self._synthesize_segment_with_retry(voice, speed, model)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_31(
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
                    self._synthesize_segment_with_retry(text, speed, model)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_32(
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
                    self._synthesize_segment_with_retry(text, voice, model)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_33(
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
                    self._synthesize_segment_with_retry(text, voice, speed, )
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_34(
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
        
        if tasks:
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_35(
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
            return b"XXXX"
        
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_36(
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
        logger.info(None)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_37(
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
        results = None
        
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_38(
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
        results = await asyncio.gather(*tasks, return_exceptions=None)
        
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_39(
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
        results = await asyncio.gather(return_exceptions=True)
        
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_40(
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
        results = await asyncio.gather(*tasks, )
        
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_41(
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
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_42(
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
        audio_chunks: List[bytes] = None
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_43(
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
        errors: List[str] = None
        
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_44(
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
        
        for i, result in enumerate(None):
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_45(
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
                logger.error(None)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_46(
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
                errors.append(None)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_47(
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
                errors.append(f"Segment {i}: {str(None)}")
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_48(
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
            elif isinstance(result, bytes) or result:
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_49(
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
                audio_chunks.append(None)
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

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_50(
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
                errors.append(None)
        
        if not audio_chunks:
            error_msg = f"All segments failed: {'; '.join(errors)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Concatenate audio chunks
        final_audio = self._concatenate_audio(audio_chunks)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_51(
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
                errors.append(f"Segment {i}: {type(None).__name__}")
        
        if not audio_chunks:
            error_msg = f"All segments failed: {'; '.join(errors)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Concatenate audio chunks
        final_audio = self._concatenate_audio(audio_chunks)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_52(
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
        
        if audio_chunks:
            error_msg = f"All segments failed: {'; '.join(errors)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Concatenate audio chunks
        final_audio = self._concatenate_audio(audio_chunks)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_53(
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
            error_msg = None
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Concatenate audio chunks
        final_audio = self._concatenate_audio(audio_chunks)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_54(
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
            error_msg = f"All segments failed: {'; '.join(None)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Concatenate audio chunks
        final_audio = self._concatenate_audio(audio_chunks)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_55(
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
            error_msg = f"All segments failed: {'XX; XX'.join(errors)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        # Concatenate audio chunks
        final_audio = self._concatenate_audio(audio_chunks)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_56(
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
            logger.error(None)
            raise RuntimeError(error_msg)
        
        # Concatenate audio chunks
        final_audio = self._concatenate_audio(audio_chunks)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_57(
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
            raise RuntimeError(None)
        
        # Concatenate audio chunks
        final_audio = self._concatenate_audio(audio_chunks)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_58(
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
        final_audio = None
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_59(
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
        final_audio = self._concatenate_audio(None)
        logger.info(f"Concatenated {len(audio_chunks)} audio chunks -> {len(final_audio)} bytes")
        
        return final_audio

    async def xǁSynthesisEngineǁsynthesize_segments__mutmut_60(
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
        logger.info(None)
        
        return final_audio
    
    xǁSynthesisEngineǁsynthesize_segments__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSynthesisEngineǁsynthesize_segments__mutmut_1': xǁSynthesisEngineǁsynthesize_segments__mutmut_1, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_2': xǁSynthesisEngineǁsynthesize_segments__mutmut_2, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_3': xǁSynthesisEngineǁsynthesize_segments__mutmut_3, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_4': xǁSynthesisEngineǁsynthesize_segments__mutmut_4, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_5': xǁSynthesisEngineǁsynthesize_segments__mutmut_5, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_6': xǁSynthesisEngineǁsynthesize_segments__mutmut_6, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_7': xǁSynthesisEngineǁsynthesize_segments__mutmut_7, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_8': xǁSynthesisEngineǁsynthesize_segments__mutmut_8, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_9': xǁSynthesisEngineǁsynthesize_segments__mutmut_9, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_10': xǁSynthesisEngineǁsynthesize_segments__mutmut_10, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_11': xǁSynthesisEngineǁsynthesize_segments__mutmut_11, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_12': xǁSynthesisEngineǁsynthesize_segments__mutmut_12, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_13': xǁSynthesisEngineǁsynthesize_segments__mutmut_13, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_14': xǁSynthesisEngineǁsynthesize_segments__mutmut_14, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_15': xǁSynthesisEngineǁsynthesize_segments__mutmut_15, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_16': xǁSynthesisEngineǁsynthesize_segments__mutmut_16, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_17': xǁSynthesisEngineǁsynthesize_segments__mutmut_17, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_18': xǁSynthesisEngineǁsynthesize_segments__mutmut_18, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_19': xǁSynthesisEngineǁsynthesize_segments__mutmut_19, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_20': xǁSynthesisEngineǁsynthesize_segments__mutmut_20, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_21': xǁSynthesisEngineǁsynthesize_segments__mutmut_21, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_22': xǁSynthesisEngineǁsynthesize_segments__mutmut_22, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_23': xǁSynthesisEngineǁsynthesize_segments__mutmut_23, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_24': xǁSynthesisEngineǁsynthesize_segments__mutmut_24, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_25': xǁSynthesisEngineǁsynthesize_segments__mutmut_25, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_26': xǁSynthesisEngineǁsynthesize_segments__mutmut_26, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_27': xǁSynthesisEngineǁsynthesize_segments__mutmut_27, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_28': xǁSynthesisEngineǁsynthesize_segments__mutmut_28, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_29': xǁSynthesisEngineǁsynthesize_segments__mutmut_29, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_30': xǁSynthesisEngineǁsynthesize_segments__mutmut_30, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_31': xǁSynthesisEngineǁsynthesize_segments__mutmut_31, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_32': xǁSynthesisEngineǁsynthesize_segments__mutmut_32, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_33': xǁSynthesisEngineǁsynthesize_segments__mutmut_33, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_34': xǁSynthesisEngineǁsynthesize_segments__mutmut_34, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_35': xǁSynthesisEngineǁsynthesize_segments__mutmut_35, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_36': xǁSynthesisEngineǁsynthesize_segments__mutmut_36, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_37': xǁSynthesisEngineǁsynthesize_segments__mutmut_37, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_38': xǁSynthesisEngineǁsynthesize_segments__mutmut_38, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_39': xǁSynthesisEngineǁsynthesize_segments__mutmut_39, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_40': xǁSynthesisEngineǁsynthesize_segments__mutmut_40, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_41': xǁSynthesisEngineǁsynthesize_segments__mutmut_41, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_42': xǁSynthesisEngineǁsynthesize_segments__mutmut_42, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_43': xǁSynthesisEngineǁsynthesize_segments__mutmut_43, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_44': xǁSynthesisEngineǁsynthesize_segments__mutmut_44, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_45': xǁSynthesisEngineǁsynthesize_segments__mutmut_45, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_46': xǁSynthesisEngineǁsynthesize_segments__mutmut_46, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_47': xǁSynthesisEngineǁsynthesize_segments__mutmut_47, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_48': xǁSynthesisEngineǁsynthesize_segments__mutmut_48, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_49': xǁSynthesisEngineǁsynthesize_segments__mutmut_49, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_50': xǁSynthesisEngineǁsynthesize_segments__mutmut_50, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_51': xǁSynthesisEngineǁsynthesize_segments__mutmut_51, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_52': xǁSynthesisEngineǁsynthesize_segments__mutmut_52, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_53': xǁSynthesisEngineǁsynthesize_segments__mutmut_53, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_54': xǁSynthesisEngineǁsynthesize_segments__mutmut_54, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_55': xǁSynthesisEngineǁsynthesize_segments__mutmut_55, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_56': xǁSynthesisEngineǁsynthesize_segments__mutmut_56, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_57': xǁSynthesisEngineǁsynthesize_segments__mutmut_57, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_58': xǁSynthesisEngineǁsynthesize_segments__mutmut_58, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_59': xǁSynthesisEngineǁsynthesize_segments__mutmut_59, 
        'xǁSynthesisEngineǁsynthesize_segments__mutmut_60': xǁSynthesisEngineǁsynthesize_segments__mutmut_60
    }
    xǁSynthesisEngineǁsynthesize_segments__mutmut_orig.__name__ = 'xǁSynthesisEngineǁsynthesize_segments'

    async def _synthesize_segment_with_retry(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        max_retries: int = 2,
    ) -> bytes:
        args = [text, voice, speed, model, max_retries]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_orig'), object.__getattribute__(self, 'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_mutants'), args, kwargs, self)

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_orig(
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

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_1(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        max_retries: int = 3,
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

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_2(
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
        last_error: Optional[Exception] = ""
        
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

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_3(
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
        
        for attempt in range(None):
            try:
                return await self.synthesize(text, voice, speed, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_4(
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
        
        for attempt in range(max_retries - 1):
            try:
                return await self.synthesize(text, voice, speed, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_5(
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
        
        for attempt in range(max_retries + 2):
            try:
                return await self.synthesize(text, voice, speed, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_6(
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
                return await self.synthesize(None, voice, speed, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_7(
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
                return await self.synthesize(text, None, speed, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_8(
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
                return await self.synthesize(text, voice, None, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_9(
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
                return await self.synthesize(text, voice, speed, None)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_10(
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
                return await self.synthesize(voice, speed, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_11(
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
                return await self.synthesize(text, speed, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_12(
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
                return await self.synthesize(text, voice, model)
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_13(
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
                return await self.synthesize(text, voice, speed, )
            except (ValueError, IOError, OSError, httpx.HTTPError) as synth_err:
                last_error = synth_err
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_14(
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
                last_error = None
                if attempt < max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_15(
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
                if attempt <= max_retries:
                    wait_time = 2 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_16(
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
                    wait_time = None
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_17(
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
                    wait_time = 2 ** attempt / 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_18(
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
                    wait_time = 2 * attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_19(
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
                    wait_time = 3 ** attempt * 0.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_20(
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
                    wait_time = 2 ** attempt * 1.5
                    logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_21(
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
                    logger.warning(None)
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_22(
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
                    logger.warning(f"Retry {attempt - 1}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_23(
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
                    logger.warning(f"Retry {attempt + 2}/{max_retries} after {wait_time}s: {synth_err}")
                    await asyncio.sleep(wait_time)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_24(
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
                    await asyncio.sleep(None)
        
        raise last_error or RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_25(
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
        
        raise last_error and RuntimeError("Synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_26(
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
        
        raise last_error or RuntimeError(None)

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_27(
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
        
        raise last_error or RuntimeError("XXSynthesis failedXX")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_28(
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
        
        raise last_error or RuntimeError("synthesis failed")

    async def xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_29(
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
        
        raise last_error or RuntimeError("SYNTHESIS FAILED")
    
    xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_1': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_1, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_2': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_2, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_3': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_3, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_4': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_4, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_5': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_5, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_6': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_6, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_7': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_7, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_8': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_8, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_9': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_9, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_10': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_10, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_11': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_11, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_12': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_12, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_13': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_13, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_14': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_14, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_15': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_15, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_16': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_16, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_17': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_17, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_18': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_18, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_19': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_19, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_20': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_20, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_21': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_21, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_22': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_22, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_23': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_23, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_24': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_24, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_25': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_25, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_26': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_26, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_27': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_27, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_28': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_28, 
        'xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_29': xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_29
    }
    xǁSynthesisEngineǁ_synthesize_segment_with_retry__mutmut_orig.__name__ = 'xǁSynthesisEngineǁ_synthesize_segment_with_retry'

    def _concatenate_audio(self, chunks: List[bytes]) -> bytes:
        args = [chunks]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSynthesisEngineǁ_concatenate_audio__mutmut_orig'), object.__getattribute__(self, 'xǁSynthesisEngineǁ_concatenate_audio__mutmut_mutants'), args, kwargs, self)

    def xǁSynthesisEngineǁ_concatenate_audio__mutmut_orig(self, chunks: List[bytes]) -> bytes:
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

    def xǁSynthesisEngineǁ_concatenate_audio__mutmut_1(self, chunks: List[bytes]) -> bytes:
        """
        Concatenate multiple audio chunks.
        
        Args:
            chunks: List of audio byte chunks
            
        Returns:
            Concatenated audio bytes
        """
        if len(chunks) != 1:
            return chunks[0]
        
        # Simple concatenation for MP3
        # Note: For production, could use pydub for crossfade
        return b"".join(chunks)

    def xǁSynthesisEngineǁ_concatenate_audio__mutmut_2(self, chunks: List[bytes]) -> bytes:
        """
        Concatenate multiple audio chunks.
        
        Args:
            chunks: List of audio byte chunks
            
        Returns:
            Concatenated audio bytes
        """
        if len(chunks) == 2:
            return chunks[0]
        
        # Simple concatenation for MP3
        # Note: For production, could use pydub for crossfade
        return b"".join(chunks)

    def xǁSynthesisEngineǁ_concatenate_audio__mutmut_3(self, chunks: List[bytes]) -> bytes:
        """
        Concatenate multiple audio chunks.
        
        Args:
            chunks: List of audio byte chunks
            
        Returns:
            Concatenated audio bytes
        """
        if len(chunks) == 1:
            return chunks[1]
        
        # Simple concatenation for MP3
        # Note: For production, could use pydub for crossfade
        return b"".join(chunks)

    def xǁSynthesisEngineǁ_concatenate_audio__mutmut_4(self, chunks: List[bytes]) -> bytes:
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
        return b"".join(None)

    def xǁSynthesisEngineǁ_concatenate_audio__mutmut_5(self, chunks: List[bytes]) -> bytes:
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
        return b"XXXX".join(chunks)
    
    xǁSynthesisEngineǁ_concatenate_audio__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSynthesisEngineǁ_concatenate_audio__mutmut_1': xǁSynthesisEngineǁ_concatenate_audio__mutmut_1, 
        'xǁSynthesisEngineǁ_concatenate_audio__mutmut_2': xǁSynthesisEngineǁ_concatenate_audio__mutmut_2, 
        'xǁSynthesisEngineǁ_concatenate_audio__mutmut_3': xǁSynthesisEngineǁ_concatenate_audio__mutmut_3, 
        'xǁSynthesisEngineǁ_concatenate_audio__mutmut_4': xǁSynthesisEngineǁ_concatenate_audio__mutmut_4, 
        'xǁSynthesisEngineǁ_concatenate_audio__mutmut_5': xǁSynthesisEngineǁ_concatenate_audio__mutmut_5
    }
    xǁSynthesisEngineǁ_concatenate_audio__mutmut_orig.__name__ = 'xǁSynthesisEngineǁ_concatenate_audio'

    async def synthesize_ssml(
        self,
        ssml_text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
    ) -> bytes:
        args = [ssml_text, voice, speed]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁSynthesisEngineǁsynthesize_ssml__mutmut_orig'), object.__getattribute__(self, 'xǁSynthesisEngineǁsynthesize_ssml__mutmut_mutants'), args, kwargs, self)

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_orig(
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_1(
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
        logger.info(None)
        
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_2(
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
        parsed = None
        
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_3(
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
        parsed = self.ssml_parser.parse(None)
        
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_4(
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
        
        if parsed.is_ssml or parsed.segments:
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_5(
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
            segments = None
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_6(
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
                    segments.append(None)
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_7(
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
                        "XXtextXX": seg.text,
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_8(
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
                        "TEXT": seg.text,
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_9(
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
                        "XXspeedXX": seg.speed if seg.speed else speed,
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_10(
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
                        "SPEED": seg.speed if seg.speed else speed,
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_11(
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
                        "XXpause_charsXX": seg.pause_chars,
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_12(
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
                        "PAUSE_CHARS": seg.pause_chars,
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_13(
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
            text = None
            
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

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_14(
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
            processed = None
            
            # Step 3: Split into segments
            split_segments = self.text_splitter.split(processed)
            
            segments = [{"text": seg, "speed": speed} for seg in split_segments]
        
        if not segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_15(
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
            processed = self.linguistic_engine.preprocess_for_tts(None)
            
            # Step 3: Split into segments
            split_segments = self.text_splitter.split(processed)
            
            segments = [{"text": seg, "speed": speed} for seg in split_segments]
        
        if not segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_16(
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
            split_segments = None
            
            segments = [{"text": seg, "speed": speed} for seg in split_segments]
        
        if not segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_17(
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
            split_segments = self.text_splitter.split(None)
            
            segments = [{"text": seg, "speed": speed} for seg in split_segments]
        
        if not segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_18(
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
            
            segments = None
        
        if not segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_19(
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
            
            segments = [{"XXtextXX": seg, "speed": speed} for seg in split_segments]
        
        if not segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_20(
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
            
            segments = [{"TEXT": seg, "speed": speed} for seg in split_segments]
        
        if not segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_21(
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
            
            segments = [{"text": seg, "XXspeedXX": speed} for seg in split_segments]
        
        if not segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_22(
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
            
            segments = [{"text": seg, "SPEED": speed} for seg in split_segments]
        
        if not segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_23(
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
        
        if segments:
            logger.warning("No segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_24(
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
            logger.warning(None)
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_25(
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
            logger.warning("XXNo segments to synthesizeXX")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_26(
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
            logger.warning("no segments to synthesize")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_27(
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
            logger.warning("NO SEGMENTS TO SYNTHESIZE")
            return b""
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_28(
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
            return b"XXXX"
        
        # Step 4 & 5: Synthesize and concatenate
        return await self.synthesize_segments(segments, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_29(
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
        return await self.synthesize_segments(None, voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_30(
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
        return await self.synthesize_segments(segments, None, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_31(
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
        return await self.synthesize_segments(segments, voice, None)

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_32(
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
        return await self.synthesize_segments(voice, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_33(
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
        return await self.synthesize_segments(segments, "kokoro")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_34(
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
        return await self.synthesize_segments(segments, voice, )

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_35(
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
        return await self.synthesize_segments(segments, voice, "XXkokoroXX")

    async def xǁSynthesisEngineǁsynthesize_ssml__mutmut_36(
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
        return await self.synthesize_segments(segments, voice, "KOKORO")
    
    xǁSynthesisEngineǁsynthesize_ssml__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSynthesisEngineǁsynthesize_ssml__mutmut_1': xǁSynthesisEngineǁsynthesize_ssml__mutmut_1, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_2': xǁSynthesisEngineǁsynthesize_ssml__mutmut_2, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_3': xǁSynthesisEngineǁsynthesize_ssml__mutmut_3, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_4': xǁSynthesisEngineǁsynthesize_ssml__mutmut_4, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_5': xǁSynthesisEngineǁsynthesize_ssml__mutmut_5, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_6': xǁSynthesisEngineǁsynthesize_ssml__mutmut_6, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_7': xǁSynthesisEngineǁsynthesize_ssml__mutmut_7, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_8': xǁSynthesisEngineǁsynthesize_ssml__mutmut_8, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_9': xǁSynthesisEngineǁsynthesize_ssml__mutmut_9, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_10': xǁSynthesisEngineǁsynthesize_ssml__mutmut_10, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_11': xǁSynthesisEngineǁsynthesize_ssml__mutmut_11, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_12': xǁSynthesisEngineǁsynthesize_ssml__mutmut_12, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_13': xǁSynthesisEngineǁsynthesize_ssml__mutmut_13, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_14': xǁSynthesisEngineǁsynthesize_ssml__mutmut_14, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_15': xǁSynthesisEngineǁsynthesize_ssml__mutmut_15, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_16': xǁSynthesisEngineǁsynthesize_ssml__mutmut_16, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_17': xǁSynthesisEngineǁsynthesize_ssml__mutmut_17, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_18': xǁSynthesisEngineǁsynthesize_ssml__mutmut_18, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_19': xǁSynthesisEngineǁsynthesize_ssml__mutmut_19, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_20': xǁSynthesisEngineǁsynthesize_ssml__mutmut_20, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_21': xǁSynthesisEngineǁsynthesize_ssml__mutmut_21, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_22': xǁSynthesisEngineǁsynthesize_ssml__mutmut_22, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_23': xǁSynthesisEngineǁsynthesize_ssml__mutmut_23, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_24': xǁSynthesisEngineǁsynthesize_ssml__mutmut_24, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_25': xǁSynthesisEngineǁsynthesize_ssml__mutmut_25, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_26': xǁSynthesisEngineǁsynthesize_ssml__mutmut_26, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_27': xǁSynthesisEngineǁsynthesize_ssml__mutmut_27, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_28': xǁSynthesisEngineǁsynthesize_ssml__mutmut_28, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_29': xǁSynthesisEngineǁsynthesize_ssml__mutmut_29, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_30': xǁSynthesisEngineǁsynthesize_ssml__mutmut_30, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_31': xǁSynthesisEngineǁsynthesize_ssml__mutmut_31, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_32': xǁSynthesisEngineǁsynthesize_ssml__mutmut_32, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_33': xǁSynthesisEngineǁsynthesize_ssml__mutmut_33, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_34': xǁSynthesisEngineǁsynthesize_ssml__mutmut_34, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_35': xǁSynthesisEngineǁsynthesize_ssml__mutmut_35, 
        'xǁSynthesisEngineǁsynthesize_ssml__mutmut_36': xǁSynthesisEngineǁsynthesize_ssml__mutmut_36
    }
    xǁSynthesisEngineǁsynthesize_ssml__mutmut_orig.__name__ = 'xǁSynthesisEngineǁsynthesize_ssml'

    async def synthesize_text(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
        model: str = "kokoro",
    ) -> bytes:
        args = [text, voice, speed, model]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁSynthesisEngineǁsynthesize_text__mutmut_orig'), object.__getattribute__(self, 'xǁSynthesisEngineǁsynthesize_text__mutmut_mutants'), args, kwargs, self)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_orig(
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

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_1(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
        model: str = "XXkokoroXX",
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

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_2(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        speed: float = DEFAULT_SPEED,
        model: str = "KOKORO",
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

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_3(
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
        logger.info(None)
        
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

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_4(
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
        if self.ssml_parser.is_ssml(None):
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

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_5(
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
            return await self.synthesize_ssml(None, voice, speed)
        
        # Apply Taiwan linguistic processing
        processed = self.linguistic_engine.preprocess_for_tts(text)
        
        # Split into segments
        segments = self.text_splitter.split(processed)
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_6(
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
            return await self.synthesize_ssml(text, None, speed)
        
        # Apply Taiwan linguistic processing
        processed = self.linguistic_engine.preprocess_for_tts(text)
        
        # Split into segments
        segments = self.text_splitter.split(processed)
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_7(
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
            return await self.synthesize_ssml(text, voice, None)
        
        # Apply Taiwan linguistic processing
        processed = self.linguistic_engine.preprocess_for_tts(text)
        
        # Split into segments
        segments = self.text_splitter.split(processed)
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_8(
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
            return await self.synthesize_ssml(voice, speed)
        
        # Apply Taiwan linguistic processing
        processed = self.linguistic_engine.preprocess_for_tts(text)
        
        # Split into segments
        segments = self.text_splitter.split(processed)
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_9(
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
            return await self.synthesize_ssml(text, speed)
        
        # Apply Taiwan linguistic processing
        processed = self.linguistic_engine.preprocess_for_tts(text)
        
        # Split into segments
        segments = self.text_splitter.split(processed)
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_10(
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
            return await self.synthesize_ssml(text, voice, )
        
        # Apply Taiwan linguistic processing
        processed = self.linguistic_engine.preprocess_for_tts(text)
        
        # Split into segments
        segments = self.text_splitter.split(processed)
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_11(
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
        processed = None
        
        # Split into segments
        segments = self.text_splitter.split(processed)
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_12(
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
        processed = self.linguistic_engine.preprocess_for_tts(None)
        
        # Split into segments
        segments = self.text_splitter.split(processed)
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_13(
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
        segments = None
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_14(
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
        segments = self.text_splitter.split(None)
        
        if not segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_15(
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
        
        if segments:
            return b""
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_16(
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
            return b"XXXX"
        
        # Synthesize segments
        segment_dicts = [{"text": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_17(
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
        segment_dicts = None
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_18(
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
        segment_dicts = [{"XXtextXX": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_19(
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
        segment_dicts = [{"TEXT": seg, "speed": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_20(
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
        segment_dicts = [{"text": seg, "XXspeedXX": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_21(
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
        segment_dicts = [{"text": seg, "SPEED": speed} for seg in segments]
        return await self.synthesize_segments(segment_dicts, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_22(
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
        return await self.synthesize_segments(None, voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_23(
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
        return await self.synthesize_segments(segment_dicts, None, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_24(
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
        return await self.synthesize_segments(segment_dicts, voice, None)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_25(
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
        return await self.synthesize_segments(voice, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_26(
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
        return await self.synthesize_segments(segment_dicts, model)

    async def xǁSynthesisEngineǁsynthesize_text__mutmut_27(
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
        return await self.synthesize_segments(segment_dicts, voice, )
    
    xǁSynthesisEngineǁsynthesize_text__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSynthesisEngineǁsynthesize_text__mutmut_1': xǁSynthesisEngineǁsynthesize_text__mutmut_1, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_2': xǁSynthesisEngineǁsynthesize_text__mutmut_2, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_3': xǁSynthesisEngineǁsynthesize_text__mutmut_3, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_4': xǁSynthesisEngineǁsynthesize_text__mutmut_4, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_5': xǁSynthesisEngineǁsynthesize_text__mutmut_5, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_6': xǁSynthesisEngineǁsynthesize_text__mutmut_6, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_7': xǁSynthesisEngineǁsynthesize_text__mutmut_7, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_8': xǁSynthesisEngineǁsynthesize_text__mutmut_8, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_9': xǁSynthesisEngineǁsynthesize_text__mutmut_9, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_10': xǁSynthesisEngineǁsynthesize_text__mutmut_10, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_11': xǁSynthesisEngineǁsynthesize_text__mutmut_11, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_12': xǁSynthesisEngineǁsynthesize_text__mutmut_12, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_13': xǁSynthesisEngineǁsynthesize_text__mutmut_13, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_14': xǁSynthesisEngineǁsynthesize_text__mutmut_14, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_15': xǁSynthesisEngineǁsynthesize_text__mutmut_15, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_16': xǁSynthesisEngineǁsynthesize_text__mutmut_16, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_17': xǁSynthesisEngineǁsynthesize_text__mutmut_17, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_18': xǁSynthesisEngineǁsynthesize_text__mutmut_18, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_19': xǁSynthesisEngineǁsynthesize_text__mutmut_19, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_20': xǁSynthesisEngineǁsynthesize_text__mutmut_20, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_21': xǁSynthesisEngineǁsynthesize_text__mutmut_21, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_22': xǁSynthesisEngineǁsynthesize_text__mutmut_22, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_23': xǁSynthesisEngineǁsynthesize_text__mutmut_23, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_24': xǁSynthesisEngineǁsynthesize_text__mutmut_24, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_25': xǁSynthesisEngineǁsynthesize_text__mutmut_25, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_26': xǁSynthesisEngineǁsynthesize_text__mutmut_26, 
        'xǁSynthesisEngineǁsynthesize_text__mutmut_27': xǁSynthesisEngineǁsynthesize_text__mutmut_27
    }
    xǁSynthesisEngineǁsynthesize_text__mutmut_orig.__name__ = 'xǁSynthesisEngineǁsynthesize_text'

    async def close(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁSynthesisEngineǁclose__mutmut_orig'), object.__getattribute__(self, 'xǁSynthesisEngineǁclose__mutmut_mutants'), args, kwargs, self)

    async def xǁSynthesisEngineǁclose__mutmut_orig(self):
        """Close the HTTP client and cleanup resources."""
        await self.client.aclose()
        self._executor.shutdown(wait=False)
        logger.info("SynthesisEngine closed")

    async def xǁSynthesisEngineǁclose__mutmut_1(self):
        """Close the HTTP client and cleanup resources."""
        await self.client.aclose()
        self._executor.shutdown(wait=None)
        logger.info("SynthesisEngine closed")

    async def xǁSynthesisEngineǁclose__mutmut_2(self):
        """Close the HTTP client and cleanup resources."""
        await self.client.aclose()
        self._executor.shutdown(wait=True)
        logger.info("SynthesisEngine closed")

    async def xǁSynthesisEngineǁclose__mutmut_3(self):
        """Close the HTTP client and cleanup resources."""
        await self.client.aclose()
        self._executor.shutdown(wait=False)
        logger.info(None)

    async def xǁSynthesisEngineǁclose__mutmut_4(self):
        """Close the HTTP client and cleanup resources."""
        await self.client.aclose()
        self._executor.shutdown(wait=False)
        logger.info("XXSynthesisEngine closedXX")

    async def xǁSynthesisEngineǁclose__mutmut_5(self):
        """Close the HTTP client and cleanup resources."""
        await self.client.aclose()
        self._executor.shutdown(wait=False)
        logger.info("synthesisengine closed")

    async def xǁSynthesisEngineǁclose__mutmut_6(self):
        """Close the HTTP client and cleanup resources."""
        await self.client.aclose()
        self._executor.shutdown(wait=False)
        logger.info("SYNTHESISENGINE CLOSED")
    
    xǁSynthesisEngineǁclose__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSynthesisEngineǁclose__mutmut_1': xǁSynthesisEngineǁclose__mutmut_1, 
        'xǁSynthesisEngineǁclose__mutmut_2': xǁSynthesisEngineǁclose__mutmut_2, 
        'xǁSynthesisEngineǁclose__mutmut_3': xǁSynthesisEngineǁclose__mutmut_3, 
        'xǁSynthesisEngineǁclose__mutmut_4': xǁSynthesisEngineǁclose__mutmut_4, 
        'xǁSynthesisEngineǁclose__mutmut_5': xǁSynthesisEngineǁclose__mutmut_5, 
        'xǁSynthesisEngineǁclose__mutmut_6': xǁSynthesisEngineǁclose__mutmut_6
    }
    xǁSynthesisEngineǁclose__mutmut_orig.__name__ = 'xǁSynthesisEngineǁclose'

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
