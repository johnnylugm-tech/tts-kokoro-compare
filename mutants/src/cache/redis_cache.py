"""Redis Cache - optional audio caching layer."""

import hashlib
import json
import logging
from typing import Optional, Any
from dataclasses import dataclass

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


@dataclass
class CacheConfig:
    """Configuration for Redis cache."""
    enabled: bool = False
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    prefix: str = "kokoro_tts:"
    ttl: int = 3600  # Cache TTL in seconds


class RedisCache:
    """
    Redis-based cache for TTS audio.
    
    This is an optional layer that can reduce backend load
    for repeated requests.
    """
    
    def __init__(self, config: Optional[CacheConfig] = None):
        args = [config]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRedisCacheǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁRedisCacheǁ__init____mutmut_mutants'), args, kwargs, self)
    
    def xǁRedisCacheǁ__init____mutmut_orig(self, config: Optional[CacheConfig] = None):
        """
        Initialize Redis cache.
        
        Args:
            config: Cache configuration
        """
        self.config = config or CacheConfig()
        self._client = None
        self._connected = False
        
        if self.config.enabled:
            self._connect()
    
    def xǁRedisCacheǁ__init____mutmut_1(self, config: Optional[CacheConfig] = None):
        """
        Initialize Redis cache.
        
        Args:
            config: Cache configuration
        """
        self.config = None
        self._client = None
        self._connected = False
        
        if self.config.enabled:
            self._connect()
    
    def xǁRedisCacheǁ__init____mutmut_2(self, config: Optional[CacheConfig] = None):
        """
        Initialize Redis cache.
        
        Args:
            config: Cache configuration
        """
        self.config = config and CacheConfig()
        self._client = None
        self._connected = False
        
        if self.config.enabled:
            self._connect()
    
    def xǁRedisCacheǁ__init____mutmut_3(self, config: Optional[CacheConfig] = None):
        """
        Initialize Redis cache.
        
        Args:
            config: Cache configuration
        """
        self.config = config or CacheConfig()
        self._client = ""
        self._connected = False
        
        if self.config.enabled:
            self._connect()
    
    def xǁRedisCacheǁ__init____mutmut_4(self, config: Optional[CacheConfig] = None):
        """
        Initialize Redis cache.
        
        Args:
            config: Cache configuration
        """
        self.config = config or CacheConfig()
        self._client = None
        self._connected = None
        
        if self.config.enabled:
            self._connect()
    
    def xǁRedisCacheǁ__init____mutmut_5(self, config: Optional[CacheConfig] = None):
        """
        Initialize Redis cache.
        
        Args:
            config: Cache configuration
        """
        self.config = config or CacheConfig()
        self._client = None
        self._connected = True
        
        if self.config.enabled:
            self._connect()
    
    xǁRedisCacheǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRedisCacheǁ__init____mutmut_1': xǁRedisCacheǁ__init____mutmut_1, 
        'xǁRedisCacheǁ__init____mutmut_2': xǁRedisCacheǁ__init____mutmut_2, 
        'xǁRedisCacheǁ__init____mutmut_3': xǁRedisCacheǁ__init____mutmut_3, 
        'xǁRedisCacheǁ__init____mutmut_4': xǁRedisCacheǁ__init____mutmut_4, 
        'xǁRedisCacheǁ__init____mutmut_5': xǁRedisCacheǁ__init____mutmut_5
    }
    xǁRedisCacheǁ__init____mutmut_orig.__name__ = 'xǁRedisCacheǁ__init__'
    
    def _connect(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRedisCacheǁ_connect__mutmut_orig'), object.__getattribute__(self, 'xǁRedisCacheǁ_connect__mutmut_mutants'), args, kwargs, self)
    
    def xǁRedisCacheǁ_connect__mutmut_orig(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_1(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = None
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_2(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=None,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_3(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=None,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_4(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=None,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_5(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=None,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_6(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=None,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_7(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_8(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_9(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_10(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_11(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_12(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=True,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_13(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = None
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_14(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = False
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_15(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(None)
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_16(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning(None)
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_17(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("XXredis package not installed, cache disabledXX")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_18(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("REDIS PACKAGE NOT INSTALLED, CACHE DISABLED")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_19(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = None
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_20(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = True
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_21(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(None)
            self._connected = False
    
    def xǁRedisCacheǁ_connect__mutmut_22(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = None
    
    def xǁRedisCacheǁ_connect__mutmut_23(self) -> None:
        """Establish Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=False,  # We need bytes for audio
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"Redis cache connected: {self.config.host}:{self.config.port}")
        except ImportError:
            logger.warning("redis package not installed, cache disabled")
            self._connected = False
        except (ValueError, IOError, OSError) as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = True
    
    xǁRedisCacheǁ_connect__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRedisCacheǁ_connect__mutmut_1': xǁRedisCacheǁ_connect__mutmut_1, 
        'xǁRedisCacheǁ_connect__mutmut_2': xǁRedisCacheǁ_connect__mutmut_2, 
        'xǁRedisCacheǁ_connect__mutmut_3': xǁRedisCacheǁ_connect__mutmut_3, 
        'xǁRedisCacheǁ_connect__mutmut_4': xǁRedisCacheǁ_connect__mutmut_4, 
        'xǁRedisCacheǁ_connect__mutmut_5': xǁRedisCacheǁ_connect__mutmut_5, 
        'xǁRedisCacheǁ_connect__mutmut_6': xǁRedisCacheǁ_connect__mutmut_6, 
        'xǁRedisCacheǁ_connect__mutmut_7': xǁRedisCacheǁ_connect__mutmut_7, 
        'xǁRedisCacheǁ_connect__mutmut_8': xǁRedisCacheǁ_connect__mutmut_8, 
        'xǁRedisCacheǁ_connect__mutmut_9': xǁRedisCacheǁ_connect__mutmut_9, 
        'xǁRedisCacheǁ_connect__mutmut_10': xǁRedisCacheǁ_connect__mutmut_10, 
        'xǁRedisCacheǁ_connect__mutmut_11': xǁRedisCacheǁ_connect__mutmut_11, 
        'xǁRedisCacheǁ_connect__mutmut_12': xǁRedisCacheǁ_connect__mutmut_12, 
        'xǁRedisCacheǁ_connect__mutmut_13': xǁRedisCacheǁ_connect__mutmut_13, 
        'xǁRedisCacheǁ_connect__mutmut_14': xǁRedisCacheǁ_connect__mutmut_14, 
        'xǁRedisCacheǁ_connect__mutmut_15': xǁRedisCacheǁ_connect__mutmut_15, 
        'xǁRedisCacheǁ_connect__mutmut_16': xǁRedisCacheǁ_connect__mutmut_16, 
        'xǁRedisCacheǁ_connect__mutmut_17': xǁRedisCacheǁ_connect__mutmut_17, 
        'xǁRedisCacheǁ_connect__mutmut_18': xǁRedisCacheǁ_connect__mutmut_18, 
        'xǁRedisCacheǁ_connect__mutmut_19': xǁRedisCacheǁ_connect__mutmut_19, 
        'xǁRedisCacheǁ_connect__mutmut_20': xǁRedisCacheǁ_connect__mutmut_20, 
        'xǁRedisCacheǁ_connect__mutmut_21': xǁRedisCacheǁ_connect__mutmut_21, 
        'xǁRedisCacheǁ_connect__mutmut_22': xǁRedisCacheǁ_connect__mutmut_22, 
        'xǁRedisCacheǁ_connect__mutmut_23': xǁRedisCacheǁ_connect__mutmut_23
    }
    xǁRedisCacheǁ_connect__mutmut_orig.__name__ = 'xǁRedisCacheǁ_connect'
    
    def _generate_key(self, text: str, voice: str, speed: float, model: str) -> str:
        args = [text, voice, speed, model]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRedisCacheǁ_generate_key__mutmut_orig'), object.__getattribute__(self, 'xǁRedisCacheǁ_generate_key__mutmut_mutants'), args, kwargs, self)
    
    def xǁRedisCacheǁ_generate_key__mutmut_orig(self, text: str, voice: str, speed: float, model: str) -> str:
        """Generate cache key from request parameters."""
        # Create deterministic hash of request
        params = f"{model}:{voice}:{speed}:{text}"
        hash_value = hashlib.sha256(params.encode()).hexdigest()[:16]
        return f"{self.config.prefix}{hash_value}"
    
    def xǁRedisCacheǁ_generate_key__mutmut_1(self, text: str, voice: str, speed: float, model: str) -> str:
        """Generate cache key from request parameters."""
        # Create deterministic hash of request
        params = None
        hash_value = hashlib.sha256(params.encode()).hexdigest()[:16]
        return f"{self.config.prefix}{hash_value}"
    
    def xǁRedisCacheǁ_generate_key__mutmut_2(self, text: str, voice: str, speed: float, model: str) -> str:
        """Generate cache key from request parameters."""
        # Create deterministic hash of request
        params = f"{model}:{voice}:{speed}:{text}"
        hash_value = None
        return f"{self.config.prefix}{hash_value}"
    
    def xǁRedisCacheǁ_generate_key__mutmut_3(self, text: str, voice: str, speed: float, model: str) -> str:
        """Generate cache key from request parameters."""
        # Create deterministic hash of request
        params = f"{model}:{voice}:{speed}:{text}"
        hash_value = hashlib.sha256(None).hexdigest()[:16]
        return f"{self.config.prefix}{hash_value}"
    
    def xǁRedisCacheǁ_generate_key__mutmut_4(self, text: str, voice: str, speed: float, model: str) -> str:
        """Generate cache key from request parameters."""
        # Create deterministic hash of request
        params = f"{model}:{voice}:{speed}:{text}"
        hash_value = hashlib.sha256(params.encode()).hexdigest()[:17]
        return f"{self.config.prefix}{hash_value}"
    
    xǁRedisCacheǁ_generate_key__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRedisCacheǁ_generate_key__mutmut_1': xǁRedisCacheǁ_generate_key__mutmut_1, 
        'xǁRedisCacheǁ_generate_key__mutmut_2': xǁRedisCacheǁ_generate_key__mutmut_2, 
        'xǁRedisCacheǁ_generate_key__mutmut_3': xǁRedisCacheǁ_generate_key__mutmut_3, 
        'xǁRedisCacheǁ_generate_key__mutmut_4': xǁRedisCacheǁ_generate_key__mutmut_4
    }
    xǁRedisCacheǁ_generate_key__mutmut_orig.__name__ = 'xǁRedisCacheǁ_generate_key'
    
    async def get(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        args = [text, voice, speed, model]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁRedisCacheǁget__mutmut_orig'), object.__getattribute__(self, 'xǁRedisCacheǁget__mutmut_mutants'), args, kwargs, self)
    
    async def xǁRedisCacheǁget__mutmut_orig(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_1(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected and not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_2(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_3(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_4(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = None
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_5(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(None, voice, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_6(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, None, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_7(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, None, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_8(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, None)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_9(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(voice, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_10(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_11(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_12(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, )
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_13(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, model)
            result = None
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_14(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, model)
            result = self._client.get(None)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_15(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(None)
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_16(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(None)
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def xǁRedisCacheǁget__mutmut_17(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
        """
        Get cached audio for request.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            Cached audio bytes or None if not found
        """
        if not self._connected or not self._client:
            return None
        
        try:
            key = self._generate_key(text, voice, speed, model)
            result = self._client.get(key)
            
            if result:
                logger.debug(f"Cache hit: {key}")
                return result
            else:
                logger.debug(f"Cache miss: {key}")
                return None
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(None)
            return None
    
    xǁRedisCacheǁget__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRedisCacheǁget__mutmut_1': xǁRedisCacheǁget__mutmut_1, 
        'xǁRedisCacheǁget__mutmut_2': xǁRedisCacheǁget__mutmut_2, 
        'xǁRedisCacheǁget__mutmut_3': xǁRedisCacheǁget__mutmut_3, 
        'xǁRedisCacheǁget__mutmut_4': xǁRedisCacheǁget__mutmut_4, 
        'xǁRedisCacheǁget__mutmut_5': xǁRedisCacheǁget__mutmut_5, 
        'xǁRedisCacheǁget__mutmut_6': xǁRedisCacheǁget__mutmut_6, 
        'xǁRedisCacheǁget__mutmut_7': xǁRedisCacheǁget__mutmut_7, 
        'xǁRedisCacheǁget__mutmut_8': xǁRedisCacheǁget__mutmut_8, 
        'xǁRedisCacheǁget__mutmut_9': xǁRedisCacheǁget__mutmut_9, 
        'xǁRedisCacheǁget__mutmut_10': xǁRedisCacheǁget__mutmut_10, 
        'xǁRedisCacheǁget__mutmut_11': xǁRedisCacheǁget__mutmut_11, 
        'xǁRedisCacheǁget__mutmut_12': xǁRedisCacheǁget__mutmut_12, 
        'xǁRedisCacheǁget__mutmut_13': xǁRedisCacheǁget__mutmut_13, 
        'xǁRedisCacheǁget__mutmut_14': xǁRedisCacheǁget__mutmut_14, 
        'xǁRedisCacheǁget__mutmut_15': xǁRedisCacheǁget__mutmut_15, 
        'xǁRedisCacheǁget__mutmut_16': xǁRedisCacheǁget__mutmut_16, 
        'xǁRedisCacheǁget__mutmut_17': xǁRedisCacheǁget__mutmut_17
    }
    xǁRedisCacheǁget__mutmut_orig.__name__ = 'xǁRedisCacheǁget'
    
    async def set(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        args = [text, voice, speed, model, audio]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁRedisCacheǁset__mutmut_orig'), object.__getattribute__(self, 'xǁRedisCacheǁset__mutmut_mutants'), args, kwargs, self)
    
    async def xǁRedisCacheǁset__mutmut_orig(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_1(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected and not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_2(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_3(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_4(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return True
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_5(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = None
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_6(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(None, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_7(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, None, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_8(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, None, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_9(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, None)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_10(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_11(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_12(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_13(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, )
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_14(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                None,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_15(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                None,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_16(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                None,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_17(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_18(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_19(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_20(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(None)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_21(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return False
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def xǁRedisCacheǁset__mutmut_22(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(None)
            return False
    
    async def xǁRedisCacheǁset__mutmut_23(
        self,
        text: str,
        voice: str,
        speed: float,
        model: str,
        audio: bytes,
    ) -> bool:
        """
        Store audio in cache.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            audio: Audio bytes to cache
            
        Returns:
            True if cached successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.setex(
                key,
                self.config.ttl,
                audio,
            )
            logger.debug(f"Cached: {key} ({len(audio)} bytes)")
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache set error: {e}")
            return True
    
    xǁRedisCacheǁset__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRedisCacheǁset__mutmut_1': xǁRedisCacheǁset__mutmut_1, 
        'xǁRedisCacheǁset__mutmut_2': xǁRedisCacheǁset__mutmut_2, 
        'xǁRedisCacheǁset__mutmut_3': xǁRedisCacheǁset__mutmut_3, 
        'xǁRedisCacheǁset__mutmut_4': xǁRedisCacheǁset__mutmut_4, 
        'xǁRedisCacheǁset__mutmut_5': xǁRedisCacheǁset__mutmut_5, 
        'xǁRedisCacheǁset__mutmut_6': xǁRedisCacheǁset__mutmut_6, 
        'xǁRedisCacheǁset__mutmut_7': xǁRedisCacheǁset__mutmut_7, 
        'xǁRedisCacheǁset__mutmut_8': xǁRedisCacheǁset__mutmut_8, 
        'xǁRedisCacheǁset__mutmut_9': xǁRedisCacheǁset__mutmut_9, 
        'xǁRedisCacheǁset__mutmut_10': xǁRedisCacheǁset__mutmut_10, 
        'xǁRedisCacheǁset__mutmut_11': xǁRedisCacheǁset__mutmut_11, 
        'xǁRedisCacheǁset__mutmut_12': xǁRedisCacheǁset__mutmut_12, 
        'xǁRedisCacheǁset__mutmut_13': xǁRedisCacheǁset__mutmut_13, 
        'xǁRedisCacheǁset__mutmut_14': xǁRedisCacheǁset__mutmut_14, 
        'xǁRedisCacheǁset__mutmut_15': xǁRedisCacheǁset__mutmut_15, 
        'xǁRedisCacheǁset__mutmut_16': xǁRedisCacheǁset__mutmut_16, 
        'xǁRedisCacheǁset__mutmut_17': xǁRedisCacheǁset__mutmut_17, 
        'xǁRedisCacheǁset__mutmut_18': xǁRedisCacheǁset__mutmut_18, 
        'xǁRedisCacheǁset__mutmut_19': xǁRedisCacheǁset__mutmut_19, 
        'xǁRedisCacheǁset__mutmut_20': xǁRedisCacheǁset__mutmut_20, 
        'xǁRedisCacheǁset__mutmut_21': xǁRedisCacheǁset__mutmut_21, 
        'xǁRedisCacheǁset__mutmut_22': xǁRedisCacheǁset__mutmut_22, 
        'xǁRedisCacheǁset__mutmut_23': xǁRedisCacheǁset__mutmut_23
    }
    xǁRedisCacheǁset__mutmut_orig.__name__ = 'xǁRedisCacheǁset'
    
    async def delete(self, text: str, voice: str, speed: float, model: str) -> bool:
        args = [text, voice, speed, model]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁRedisCacheǁdelete__mutmut_orig'), object.__getattribute__(self, 'xǁRedisCacheǁdelete__mutmut_mutants'), args, kwargs, self)
    
    async def xǁRedisCacheǁdelete__mutmut_orig(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_1(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected and not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_2(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_3(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_4(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return True
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_5(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = None
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_6(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(None, voice, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_7(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, None, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_8(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, None, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_9(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, None)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_10(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(voice, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_11(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_12(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_13(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, )
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_14(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.delete(None)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_15(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.delete(key)
            return False
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_16(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(None)
            return False
    
    async def xǁRedisCacheǁdelete__mutmut_17(self, text: str, voice: str, speed: float, model: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            text: Input text
            voice: Voice identifier
            speed: Speed multiplier
            model: Model identifier
            
        Returns:
            True if deleted successfully
        """
        if not self._connected or not self._client:
            return False
        
        try:
            key = self._generate_key(text, voice, speed, model)
            self._client.delete(key)
            return True
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache delete error: {e}")
            return True
    
    xǁRedisCacheǁdelete__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRedisCacheǁdelete__mutmut_1': xǁRedisCacheǁdelete__mutmut_1, 
        'xǁRedisCacheǁdelete__mutmut_2': xǁRedisCacheǁdelete__mutmut_2, 
        'xǁRedisCacheǁdelete__mutmut_3': xǁRedisCacheǁdelete__mutmut_3, 
        'xǁRedisCacheǁdelete__mutmut_4': xǁRedisCacheǁdelete__mutmut_4, 
        'xǁRedisCacheǁdelete__mutmut_5': xǁRedisCacheǁdelete__mutmut_5, 
        'xǁRedisCacheǁdelete__mutmut_6': xǁRedisCacheǁdelete__mutmut_6, 
        'xǁRedisCacheǁdelete__mutmut_7': xǁRedisCacheǁdelete__mutmut_7, 
        'xǁRedisCacheǁdelete__mutmut_8': xǁRedisCacheǁdelete__mutmut_8, 
        'xǁRedisCacheǁdelete__mutmut_9': xǁRedisCacheǁdelete__mutmut_9, 
        'xǁRedisCacheǁdelete__mutmut_10': xǁRedisCacheǁdelete__mutmut_10, 
        'xǁRedisCacheǁdelete__mutmut_11': xǁRedisCacheǁdelete__mutmut_11, 
        'xǁRedisCacheǁdelete__mutmut_12': xǁRedisCacheǁdelete__mutmut_12, 
        'xǁRedisCacheǁdelete__mutmut_13': xǁRedisCacheǁdelete__mutmut_13, 
        'xǁRedisCacheǁdelete__mutmut_14': xǁRedisCacheǁdelete__mutmut_14, 
        'xǁRedisCacheǁdelete__mutmut_15': xǁRedisCacheǁdelete__mutmut_15, 
        'xǁRedisCacheǁdelete__mutmut_16': xǁRedisCacheǁdelete__mutmut_16, 
        'xǁRedisCacheǁdelete__mutmut_17': xǁRedisCacheǁdelete__mutmut_17
    }
    xǁRedisCacheǁdelete__mutmut_orig.__name__ = 'xǁRedisCacheǁdelete'
    
    async def clear(self) -> int:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁRedisCacheǁclear__mutmut_orig'), object.__getattribute__(self, 'xǁRedisCacheǁclear__mutmut_mutants'), args, kwargs, self)
    
    async def xǁRedisCacheǁclear__mutmut_orig(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or not self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(self._client.scan_iter(match=pattern))
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_1(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected and not self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(self._client.scan_iter(match=pattern))
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_2(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if self._connected or not self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(self._client.scan_iter(match=pattern))
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_3(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(self._client.scan_iter(match=pattern))
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_4(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or not self._client:
            return 1
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(self._client.scan_iter(match=pattern))
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_5(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or not self._client:
            return 0
        
        try:
            pattern = None
            keys = list(self._client.scan_iter(match=pattern))
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_6(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or not self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = None
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_7(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or not self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(None)
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_8(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or not self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(self._client.scan_iter(match=None))
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_9(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or not self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(self._client.scan_iter(match=pattern))
            if keys:
                return self._client.delete(*keys)
            return 1
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_10(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or not self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(self._client.scan_iter(match=pattern))
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(None)
            return 0
    
    async def xǁRedisCacheǁclear__mutmut_11(self) -> int:
        """
        Clear all cache entries with the configured prefix.
        
        Returns:
            Number of keys deleted
        """
        if not self._connected or not self._client:
            return 0
        
        try:
            pattern = f"{self.config.prefix}*"
            keys = list(self._client.scan_iter(match=pattern))
            if keys:
                return self._client.delete(*keys)
            return 0
        except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError) as e:
            logger.warning(f"Cache clear error: {e}")
            return 1
    
    xǁRedisCacheǁclear__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRedisCacheǁclear__mutmut_1': xǁRedisCacheǁclear__mutmut_1, 
        'xǁRedisCacheǁclear__mutmut_2': xǁRedisCacheǁclear__mutmut_2, 
        'xǁRedisCacheǁclear__mutmut_3': xǁRedisCacheǁclear__mutmut_3, 
        'xǁRedisCacheǁclear__mutmut_4': xǁRedisCacheǁclear__mutmut_4, 
        'xǁRedisCacheǁclear__mutmut_5': xǁRedisCacheǁclear__mutmut_5, 
        'xǁRedisCacheǁclear__mutmut_6': xǁRedisCacheǁclear__mutmut_6, 
        'xǁRedisCacheǁclear__mutmut_7': xǁRedisCacheǁclear__mutmut_7, 
        'xǁRedisCacheǁclear__mutmut_8': xǁRedisCacheǁclear__mutmut_8, 
        'xǁRedisCacheǁclear__mutmut_9': xǁRedisCacheǁclear__mutmut_9, 
        'xǁRedisCacheǁclear__mutmut_10': xǁRedisCacheǁclear__mutmut_10, 
        'xǁRedisCacheǁclear__mutmut_11': xǁRedisCacheǁclear__mutmut_11
    }
    xǁRedisCacheǁclear__mutmut_orig.__name__ = 'xǁRedisCacheǁclear'
    
    def close(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁRedisCacheǁclose__mutmut_orig'), object.__getattribute__(self, 'xǁRedisCacheǁclose__mutmut_mutants'), args, kwargs, self)
    
    def xǁRedisCacheǁclose__mutmut_orig(self) -> None:
        """Close Redis connection."""
        if self._client:
            self._client.close()
            self._connected = False
            logger.info("Redis cache closed")
    
    def xǁRedisCacheǁclose__mutmut_1(self) -> None:
        """Close Redis connection."""
        if self._client:
            self._client.close()
            self._connected = None
            logger.info("Redis cache closed")
    
    def xǁRedisCacheǁclose__mutmut_2(self) -> None:
        """Close Redis connection."""
        if self._client:
            self._client.close()
            self._connected = True
            logger.info("Redis cache closed")
    
    def xǁRedisCacheǁclose__mutmut_3(self) -> None:
        """Close Redis connection."""
        if self._client:
            self._client.close()
            self._connected = False
            logger.info(None)
    
    def xǁRedisCacheǁclose__mutmut_4(self) -> None:
        """Close Redis connection."""
        if self._client:
            self._client.close()
            self._connected = False
            logger.info("XXRedis cache closedXX")
    
    def xǁRedisCacheǁclose__mutmut_5(self) -> None:
        """Close Redis connection."""
        if self._client:
            self._client.close()
            self._connected = False
            logger.info("redis cache closed")
    
    def xǁRedisCacheǁclose__mutmut_6(self) -> None:
        """Close Redis connection."""
        if self._client:
            self._client.close()
            self._connected = False
            logger.info("REDIS CACHE CLOSED")
    
    xǁRedisCacheǁclose__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁRedisCacheǁclose__mutmut_1': xǁRedisCacheǁclose__mutmut_1, 
        'xǁRedisCacheǁclose__mutmut_2': xǁRedisCacheǁclose__mutmut_2, 
        'xǁRedisCacheǁclose__mutmut_3': xǁRedisCacheǁclose__mutmut_3, 
        'xǁRedisCacheǁclose__mutmut_4': xǁRedisCacheǁclose__mutmut_4, 
        'xǁRedisCacheǁclose__mutmut_5': xǁRedisCacheǁclose__mutmut_5, 
        'xǁRedisCacheǁclose__mutmut_6': xǁRedisCacheǁclose__mutmut_6
    }
    xǁRedisCacheǁclose__mutmut_orig.__name__ = 'xǁRedisCacheǁclose'


# Singleton instance
_cache_instance: Optional[RedisCache] = None


def get_cache(config: Optional[CacheConfig] = None) -> RedisCache:
    args = [config]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_cache__mutmut_orig, x_get_cache__mutmut_mutants, args, kwargs, None)


def x_get_cache__mutmut_orig(config: Optional[CacheConfig] = None) -> RedisCache:
    """
    Get or create cache singleton.
    
    Args:
        config: Optional cache configuration
        
    Returns:
        RedisCache instance
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache(config)
    return _cache_instance


def x_get_cache__mutmut_1(config: Optional[CacheConfig] = None) -> RedisCache:
    """
    Get or create cache singleton.
    
    Args:
        config: Optional cache configuration
        
    Returns:
        RedisCache instance
    """
    global _cache_instance
    if _cache_instance is not None:
        _cache_instance = RedisCache(config)
    return _cache_instance


def x_get_cache__mutmut_2(config: Optional[CacheConfig] = None) -> RedisCache:
    """
    Get or create cache singleton.
    
    Args:
        config: Optional cache configuration
        
    Returns:
        RedisCache instance
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = None
    return _cache_instance


def x_get_cache__mutmut_3(config: Optional[CacheConfig] = None) -> RedisCache:
    """
    Get or create cache singleton.
    
    Args:
        config: Optional cache configuration
        
    Returns:
        RedisCache instance
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache(None)
    return _cache_instance

x_get_cache__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_cache__mutmut_1': x_get_cache__mutmut_1, 
    'x_get_cache__mutmut_2': x_get_cache__mutmut_2, 
    'x_get_cache__mutmut_3': x_get_cache__mutmut_3
}
x_get_cache__mutmut_orig.__name__ = 'x_get_cache'
