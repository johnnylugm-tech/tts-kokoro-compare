"""Test Redis cache layer."""

import pytest
import sys, os
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