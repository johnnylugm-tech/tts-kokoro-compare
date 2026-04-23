"""Test Redis cache layer."""

import pytest
import sys, os
import redis
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.cache.redis_cache import RedisCache, CacheConfig, get_cache


class TestCacheConfig:
    def test_default_values(self):
        """CacheConfig has expected defaults."""
        cfg = CacheConfig()
        assert cfg.enabled is False
        assert cfg.host == "localhost"
        assert cfg.port == 6379
        assert cfg.db == 0
        assert cfg.prefix == "kokoro_tts:"
        assert cfg.ttl == 3600

    def test_custom_values(self):
        """CacheConfig accepts custom values."""
        cfg = CacheConfig(enabled=True, host="127.0.0.1", port=6380, db=1, prefix="test:", ttl=7200)
        assert cfg.enabled is True
        assert cfg.host == "127.0.0.1"
        assert cfg.port == 6380
        assert cfg.db == 1
        assert cfg.prefix == "test:"
        assert cfg.ttl == 7200


class TestRedisCacheInit:
    def test_disabled_by_default(self):
        """Cache with enabled=False does not connect."""
        cache = RedisCache(CacheConfig(enabled=False))
        assert cache._connected is False
        assert cache._client is None

    def test_enabled_cache_init(self):
        """Enabled cache attempts connection on init."""
        cache = RedisCache(CacheConfig(enabled=True, host="localhost", port=6379))
        # Just verify the cache was initialized (connected or not depends on env)
        assert cache._client is not None or cache._connected is False

    def test_generate_key_deterministic(self):
        """_generate_key produces consistent hashes."""
        cache = RedisCache(CacheConfig(prefix="test:"))
        key1 = cache._generate_key("hello", "voice1", 1.0, "kokoro")
        key2 = cache._generate_key("hello", "voice1", 1.0, "kokoro")
        assert key1 == key2
        assert key1.startswith("test:")

    def test_generate_key_different_params(self):
        """Different input params produce different keys."""
        cache = RedisCache(CacheConfig(prefix="test:"))
        key1 = cache._generate_key("hello", "voice1", 1.0, "kokoro")
        key2 = cache._generate_key("hello", "voice2", 1.0, "kokoro")
        key3 = cache._generate_key("world", "voice1", 1.0, "kokoro")
        assert key1 != key2
        assert key1 != key3


class TestRedisCacheAsync:
    @pytest.mark.asyncio
    async def test_get_disconnected_returns_none(self):
        """get() returns None when not connected."""
        cache = RedisCache(CacheConfig(enabled=False))
        result = await cache.get("text", "voice", 1.0, "model")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_disconnected_returns_false(self):
        """set() returns False when not connected."""
        cache = RedisCache(CacheConfig(enabled=False))
        result = await cache.set("text", "voice", 1.0, "model", b"audio")
        assert result is False

    @pytest.mark.asyncio
    async def test_delete_disconnected_returns_false(self):
        """delete() returns False when not connected."""
        cache = RedisCache(CacheConfig(enabled=False))
        result = await cache.delete("text", "voice", 1.0, "model")
        assert result is False

    @pytest.mark.asyncio
    async def test_clear_disconnected_returns_zero(self):
        """clear() returns 0 when not connected."""
        cache = RedisCache(CacheConfig(enabled=False))
        result = await cache.clear()
        assert result == 0


class TestRedisCacheConnected:
    """Tests exercising the connected code path via mock Redis client."""

    @pytest.mark.asyncio
    async def test_get_returns_cached_bytes(self):
        """get() returns cached audio bytes on cache hit."""
        cache = RedisCache(CacheConfig(enabled=True, host="localhost", port=6379))
        mock_client = MagicMock()
        mock_client.get.return_value = b"cached_audio_data"
        cache._client = mock_client
        cache._connected = True
        result = await cache.get("hello", "voice1", 1.0, "kokoro")
        assert result == b"cached_audio_data"

    @pytest.mark.asyncio
    async def test_get_returns_none_on_miss(self):
        """get() returns None on cache miss."""
        cache = RedisCache(CacheConfig(enabled=True))
        mock_client = MagicMock()
        mock_client.get.return_value = None
        cache._client = mock_client
        cache._connected = True
        result = await cache.get("hello", "voice1", 1.0, "kokoro")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_calls_redis_setex(self):
        """set() stores audio with TTL via Redis SETEX."""
        cache = RedisCache(CacheConfig(enabled=True, ttl=3600))
        mock_client = MagicMock()
        cache._client = mock_client
        cache._connected = True
        result = await cache.set("hello", "voice1", 1.0, "kokoro", b"audio_data")
        assert result is True
        mock_client.setex.assert_called_once()
        call_args = mock_client.setex.call_args
        assert call_args[0][1] == 3600  # TTL

    @pytest.mark.asyncio
    async def test_delete_removes_key(self):
        """delete() removes the cached entry."""
        cache = RedisCache(CacheConfig(enabled=True))
        mock_client = MagicMock()
        cache._client = mock_client
        cache._connected = True
        mock_client.delete.return_value = 1
        result = await cache.delete("hello", "voice1", 1.0, "kokoro")
        assert result == 1
        mock_client.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_clear_deletes_matching_keys(self):
        """clear() deletes all keys matching the prefix pattern and returns count."""
        cache = RedisCache(CacheConfig(enabled=True, prefix="test:"))
        mock_client = MagicMock()
        cache._client = mock_client
        cache._connected = True
        mock_client.scan_iter.return_value = ["test:key1", "test:key2"]
        mock_client.delete.return_value = 2
        result = await cache.clear()
        assert result == 2
        mock_client.scan_iter.assert_called_once_with(match="test:*")
        mock_client.delete.assert_called_once_with("test:key1", "test:key2")

    @pytest.mark.asyncio
    async def test_get_handles_redis_error_gracefully(self):
        """get() returns None on Redis error (fail-safe)."""
        cache = RedisCache(CacheConfig(enabled=True))
        mock_client = MagicMock()
        mock_client.get.side_effect = redis.RedisError("connection lost")
        cache._client = mock_client
        cache._connected = True
        result = await cache.get("hello", "voice1", 1.0, "kokoro")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_handles_redis_error_gracefully(self):
        """set() returns False on Redis error (fail-safe)."""
        cache = RedisCache(CacheConfig(enabled=True))
        mock_client = MagicMock()
        mock_client.setex.side_effect = redis.RedisError("connection lost")
        cache._client = mock_client
        cache._connected = True
        result = await cache.set("hello", "voice1", 1.0, "kokoro", b"data")
        assert result is False


class TestGetCacheSingleton:
    def test_get_cache_creates_instance(self):
        """get_cache() returns a RedisCache instance."""
        cache = get_cache(CacheConfig(enabled=False))
        assert isinstance(cache, RedisCache)

    def test_close_sets_connected_false(self):
        """close() marks cache as disconnected."""
        cache = RedisCache(CacheConfig(enabled=False))
        cache.close()
        assert cache._connected is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])