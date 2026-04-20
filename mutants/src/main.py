"""Kokoro Taiwan Proxy - FastAPI Application."""

import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import (
    KOKORO_BACKEND_URL,
    KOKORO_VOICES_URL,
    WARMUP_ENABLED,
    WARMUP_TEXT,
    LOG_FORMAT,
    LOG_LEVEL,
)
from .routers import speech
from .engines.synthesis import SynthesisEngine

# Configure logging
logging.basicConfig(
    format=LOG_FORMAT,
    level=getattr(logging, LOG_LEVEL),
)
logger = logging.getLogger(__name__)

# Global synthesis engine for warmup
_synthesis_engine: SynthesisEngine | None = None
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


async def warmup_backend() -> bool:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return await _mutmut_trampoline(x_warmup_backend__mutmut_orig, x_warmup_backend__mutmut_mutants, args, kwargs, None)


async def x_warmup_backend__mutmut_orig() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_1() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_2() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info(None)
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_3() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("XXWarmup disabledXX")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_4() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_5() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("WARMUP DISABLED")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_6() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return False
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_7() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info(None)
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_8() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("XXStarting backend warmup...XX")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_9() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_10() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("STARTING BACKEND WARMUP...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_11() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=None) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_12() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=31.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_13() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = None
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_14() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "XXmodelXX": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_15() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "MODEL": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_16() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "XXkokoroXX",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_17() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "KOKORO",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_18() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "XXinputXX": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_19() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "INPUT": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_20() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "XXvoiceXX": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_21() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "VOICE": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_22() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "XXzf_xiaoxiaoXX",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_23() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "ZF_XIAOXIAO",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_24() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "XXspeedXX": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_25() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "SPEED": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_26() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 2.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_27() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = None
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_28() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                None,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_29() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=None,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_30() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_31() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_32() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                None
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_33() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return False
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return False


async def x_warmup_backend__mutmut_34() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(None)
        return False


async def x_warmup_backend__mutmut_35() -> bool:
    """
    Perform warmup request to load model weights.
    
    Returns:
        True if warmup succeeded
    """
    if not WARMUP_ENABLED:
        logger.info("Warmup disabled")
        return True
    
    logger.info("Starting backend warmup...")
    
    try:
        import httpx
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup with a simple request
            payload = {
                "model": "kokoro",
                "input": WARMUP_TEXT,
                "voice": "zf_xiaoxiao",
                "speed": 1.0,
            }
            
            response = await client.post(
                KOKORO_BACKEND_URL,
                json=payload,
            )
            
            response.raise_for_status()
            
            logger.info(
                f"Warmup successful: received {len(response.content)} bytes"
            )
            return True
            
    except (httpx.HTTPError, httpx.TimeoutException, OSError) as e:
        logger.warning(f"Warmup failed: {e}")
        return True

x_warmup_backend__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_warmup_backend__mutmut_1': x_warmup_backend__mutmut_1, 
    'x_warmup_backend__mutmut_2': x_warmup_backend__mutmut_2, 
    'x_warmup_backend__mutmut_3': x_warmup_backend__mutmut_3, 
    'x_warmup_backend__mutmut_4': x_warmup_backend__mutmut_4, 
    'x_warmup_backend__mutmut_5': x_warmup_backend__mutmut_5, 
    'x_warmup_backend__mutmut_6': x_warmup_backend__mutmut_6, 
    'x_warmup_backend__mutmut_7': x_warmup_backend__mutmut_7, 
    'x_warmup_backend__mutmut_8': x_warmup_backend__mutmut_8, 
    'x_warmup_backend__mutmut_9': x_warmup_backend__mutmut_9, 
    'x_warmup_backend__mutmut_10': x_warmup_backend__mutmut_10, 
    'x_warmup_backend__mutmut_11': x_warmup_backend__mutmut_11, 
    'x_warmup_backend__mutmut_12': x_warmup_backend__mutmut_12, 
    'x_warmup_backend__mutmut_13': x_warmup_backend__mutmut_13, 
    'x_warmup_backend__mutmut_14': x_warmup_backend__mutmut_14, 
    'x_warmup_backend__mutmut_15': x_warmup_backend__mutmut_15, 
    'x_warmup_backend__mutmut_16': x_warmup_backend__mutmut_16, 
    'x_warmup_backend__mutmut_17': x_warmup_backend__mutmut_17, 
    'x_warmup_backend__mutmut_18': x_warmup_backend__mutmut_18, 
    'x_warmup_backend__mutmut_19': x_warmup_backend__mutmut_19, 
    'x_warmup_backend__mutmut_20': x_warmup_backend__mutmut_20, 
    'x_warmup_backend__mutmut_21': x_warmup_backend__mutmut_21, 
    'x_warmup_backend__mutmut_22': x_warmup_backend__mutmut_22, 
    'x_warmup_backend__mutmut_23': x_warmup_backend__mutmut_23, 
    'x_warmup_backend__mutmut_24': x_warmup_backend__mutmut_24, 
    'x_warmup_backend__mutmut_25': x_warmup_backend__mutmut_25, 
    'x_warmup_backend__mutmut_26': x_warmup_backend__mutmut_26, 
    'x_warmup_backend__mutmut_27': x_warmup_backend__mutmut_27, 
    'x_warmup_backend__mutmut_28': x_warmup_backend__mutmut_28, 
    'x_warmup_backend__mutmut_29': x_warmup_backend__mutmut_29, 
    'x_warmup_backend__mutmut_30': x_warmup_backend__mutmut_30, 
    'x_warmup_backend__mutmut_31': x_warmup_backend__mutmut_31, 
    'x_warmup_backend__mutmut_32': x_warmup_backend__mutmut_32, 
    'x_warmup_backend__mutmut_33': x_warmup_backend__mutmut_33, 
    'x_warmup_backend__mutmut_34': x_warmup_backend__mutmut_34, 
    'x_warmup_backend__mutmut_35': x_warmup_backend__mutmut_35
}
x_warmup_backend__mutmut_orig.__name__ = 'x_warmup_backend'


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    global _synthesis_engine
    
    # Startup
    logger.info("=" * 50)
    logger.info("Kokoro Taiwan Proxy starting...")
    logger.info(f"Backend URL: {KOKORO_BACKEND_URL}")
    logger.info("=" * 50)
    
    # Initialize synthesis engine
    _synthesis_engine = SynthesisEngine()
    
    # Warmup backend
    if WARMUP_ENABLED:
        warmup_success = await warmup_backend()
        if not warmup_success:
            logger.warning("Warmup failed, service will start anyway")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    if _synthesis_engine:
        await _synthesis_engine.close()
    logger.info("Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Kokoro Taiwan Proxy",
    description=(
        "TTS Proxy with Taiwan-optimized linguistic processing. "
        "Provides OpenAI-compatible API with SSML support."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info(f"Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    logger.info(f"Response: {response.status_code}")
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Include routers
app.include_router(speech.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Kokoro Taiwan Proxy",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status and backend URL
    """
    # Check if backend is reachable
    backend_reachable = False
    
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                KOKORO_VOICES_URL,
            )
            backend_reachable = response.status_code == 200
    except httpx.HTTPError as e:
        logger.warning(f"Health check failed: {e}")
        backend_reachable = False
    
    return {
        "status": "ok" if backend_reachable else "degraded",
        "backend": KOKORO_BACKEND_URL,
        "backend_reachable": backend_reachable,
    }


@app.get("/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes/load balancer.
    
    Returns:
        Ready status
    """
    return {"ready": True}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8881,  # Proxy on 8881, backend on 8880
        reload=False,
        log_level="info",
    )
