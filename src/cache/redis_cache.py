"""Redis Cache - optional audio caching layer."""

import hashlib
import json
import logging
from typing import Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


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
    
    def _connect(self) -> None:
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
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, cache disabled")
            self._connected = False
    
    def _generate_key(self, text: str, voice: str, speed: float, model: str) -> str:
        """Generate cache key from request parameters."""
        # Create deterministic hash of request
        params = f"{model}:{voice}:{speed}:{text}"
        hash_value = hashlib.sha256(params.encode()).hexdigest()[:16]
        return f"{self.config.prefix}{hash_value}"
    
    async def get(self, text: str, voice: str, speed: float, model: str) -> Optional[bytes]:
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
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def set(
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
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def delete(self, text: str, voice: str, speed: float, model: str) -> bool:
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
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def clear(self) -> int:
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
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            self._client.close()
            self._connected = False
            logger.info("Redis cache closed")


# Singleton instance
_cache_instance: Optional[RedisCache] = None


def get_cache(config: Optional[CacheConfig] = None) -> RedisCache:
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
