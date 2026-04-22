#!/usr/bin/env python3
"""
Behavioral tests - circuit_breaker.py

Tests actual state transitions:
- CLOSED -> OPEN: after threshold failures
- OPEN -> HALF_OPEN: after timeout
- HALF_OPEN -> OPEN: test request fails
- HALF_OPEN -> CLOSED: test request succeeds

Also tests: get_stats(), get_state(), reset(), decorator
"""

import pytest
import time
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.middleware.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpen,
    CircuitState,
    circuit_breaker_decorator,
)


class TestCircuitBreakerStateTransitions:
    """Behavioral tests for state transitions."""

    def test_closed_to_open_on_threshold_failures(self):
        """CLOSED -> OPEN after threshold failures."""
        cb = CircuitBreaker(threshold=3, timeout=10.0)

        assert cb.state == CircuitState.CLOSED

        # Fail 2 times - should still be CLOSED
        for _ in range(2):
            cb._on_failure()
        assert cb.state == CircuitState.CLOSED

        # 3rd failure -> OPEN
        cb._on_failure()
        assert cb.state == CircuitState.OPEN

    def test_open_rejects_calls_immediately(self):
        """OPEN state raises CircuitBreakerOpen."""
        cb = CircuitBreaker(threshold=2, timeout=10.0)
        cb.state = CircuitState.OPEN
        cb.last_failure_time = time.time()

        with pytest.raises(CircuitBreakerOpen) as exc_info:
            cb.call(lambda: "result")
        assert "Circuit breaker is open" in str(exc_info.value)

    def test_open_to_half_open_after_timeout(self):
        """OPEN -> HALF_OPEN after timeout elapses."""
        cb = CircuitBreaker(threshold=2, timeout=0.1)
        cb.state = CircuitState.OPEN
        cb.last_failure_time = time.time() - 1  # already past timeout

        # _should_attempt_reset should return True
        assert cb._should_attempt_reset() is True

        # _check_and_transition should move to HALF_OPEN
        cb._check_and_transition()
        assert cb.state == CircuitState.HALF_OPEN

    def test_open_to_half_open_requires_timeout_elapsed(self):
        """OPEN stays OPEN if timeout not elapsed."""
        cb = CircuitBreaker(threshold=2, timeout=10.0)
        cb.state = CircuitState.OPEN
        cb.last_failure_time = time.time()  # just now

        # _should_attempt_reset should return False
        assert cb._should_attempt_reset() is False

        # State should remain OPEN
        cb._check_and_transition()
        assert cb.state == CircuitState.OPEN

    def test_half_open_to_closed_on_success(self):
        """HALF_OPEN -> CLOSED after successful call."""
        cb = CircuitBreaker(threshold=2, timeout=10.0)
        cb.state = CircuitState.HALF_OPEN
        cb._half_open_attempts = 0
        cb.successes = 0

        # Simulate success while in HALF_OPEN
        cb._on_success()
        # One success with _max_half_open_attempts=1 -> CLOSED
        assert cb.state == CircuitState.CLOSED

    def test_half_open_to_open_on_failure(self):
        """HALF_OPEN -> OPEN if test request fails."""
        cb = CircuitBreaker(threshold=2, timeout=10.0)
        cb.state = CircuitState.HALF_OPEN
        cb._half_open_attempts = 0

        cb._on_failure()
        assert cb.state == CircuitState.OPEN
        assert cb._half_open_attempts == 1

    def test_success_in_closed_resets_failure_count(self):
        """Success in CLOSED resets failure count."""
        cb = CircuitBreaker(threshold=3, timeout=10.0)
        cb.failures = 2
        cb.state = CircuitState.CLOSED

        cb._on_success()
        assert cb.failures == 0
        assert cb.state == CircuitState.CLOSED

    def test_half_open_ignores_success_without_enough(self):
        """HALF_OPEN with insufficient successes stays HALF_OPEN."""
        cb = CircuitBreaker(threshold=2, timeout=10.0)
        cb.state = CircuitState.HALF_OPEN
        cb.successes = 0
        cb._max_half_open_attempts = 2  # need 2 successes

        cb._on_success()  # only 1 success
        assert cb.state == CircuitState.HALF_OPEN
        assert cb.successes == 1

    def test_failure_in_half_open_increments_attempts(self):
        """Failure in HALF_OPEN increments _half_open_attempts."""
        cb = CircuitBreaker(threshold=2, timeout=10.0)
        cb.state = CircuitState.HALF_OPEN
        cb._half_open_attempts = 0

        cb._on_failure()
        assert cb._half_open_attempts == 1


class TestCircuitBreakerCall:
    """Tests for CircuitBreaker.call() and call_async()."""

    def test_call_passes_result_through(self):
        """call() returns function result on success."""
        cb = CircuitBreaker(threshold=3, timeout=10.0)
        result = cb.call(lambda: 42)
        assert result == 42
        assert cb.state == CircuitState.CLOSED

    def test_call_passes_args_kwargs(self):
        """call() forwards args and kwargs."""
        cb = CircuitBreaker(threshold=3, timeout=10.0)
        result = cb.call(lambda a, b, key=1: a + b + key, 10, 20, key=5)
        assert result == 35

    def test_call_failure_increments_failures(self):
        """call() increments failure count on expected exception."""
        cb = CircuitBreaker(threshold=3, timeout=10.0, expected_exceptions=(ValueError,))
        assert cb.failures == 0
        with pytest.raises(ValueError):
            cb.call(lambda: (_ for _ in ()).throw(ValueError("fail")))
        assert cb.failures == 1

    def test_call_unexpected_exception_not_caught(self):
        """call() re-raises unexpected exceptions."""
        cb = CircuitBreaker(threshold=3, timeout=10.0, expected_exceptions=(ValueError,))

        with pytest.raises(TypeError):
            cb.call(lambda: (_ for _ in ()).throw(TypeError("unexpected")))

    def test_call_open_state_raises(self):
        """call() raises CircuitBreakerOpen when OPEN."""
        cb = CircuitBreaker(threshold=1, timeout=10.0)
        cb.state = CircuitState.OPEN
        cb.last_failure_time = time.time()

        with pytest.raises(CircuitBreakerOpen):
            cb.call(lambda: "result")

    @pytest.mark.asyncio
    async def test_call_async_success(self):
        """call_async() returns async function result."""
        cb = CircuitBreaker(threshold=3, timeout=10.0)

        async def async_func():
            return "async_result"

        result = await cb.call_async(async_func)
        assert result == "async_result"

    @pytest.mark.asyncio
    async def test_call_async_failure(self):
        """call_async() handles async failures."""
        cb = CircuitBreaker(threshold=3, timeout=10.0, expected_exceptions=(ValueError,))

        async def async_fail():
            raise ValueError("async failure")

        with pytest.raises(ValueError):
            await cb.call_async(async_fail)
        assert cb.failures == 1

    @pytest.mark.asyncio
    async def test_call_async_open_raises(self):
        """call_async() raises CircuitBreakerOpen when OPEN."""
        cb = CircuitBreaker(threshold=1, timeout=10.0)
        cb.state = CircuitState.OPEN
        cb.last_failure_time = time.time()

        async def async_func():
            return "result"

        with pytest.raises(CircuitBreakerOpen):
            await cb.call_async(async_func)


class TestCircuitBreakerReset:
    """Tests for reset()."""

    def test_reset_closes_circuit(self):
        """reset() sets state to CLOSED."""
        cb = CircuitBreaker(threshold=2, timeout=10.0)
        cb.state = CircuitState.OPEN
        cb.failures = 5
        cb._half_open_attempts = 3

        cb.reset()
        assert cb.state == CircuitState.CLOSED

    def test_reset_clears_counters(self):
        """reset() clears failures and successes."""
        cb = CircuitBreaker(threshold=2, timeout=10.0)
        cb.failures = 10
        cb.successes = 5
        cb.last_failure_time = time.time()

        cb.reset()
        assert cb.failures == 0
        assert cb.successes == 0
        assert cb.last_failure_time is None


class TestCircuitBreakerStats:
    """Tests for get_state() and get_stats()."""

    def test_get_state_returns_current_state(self):
        """get_state() returns CircuitState enum."""
        cb = CircuitBreaker(threshold=3, timeout=10.0)
        assert cb.get_state() == CircuitState.CLOSED

        cb.state = CircuitState.OPEN
        assert cb.get_state() == CircuitState.OPEN

        cb.state = CircuitState.HALF_OPEN
        assert cb.get_state() == CircuitState.HALF_OPEN

    def test_get_stats_returns_dict(self):
        """get_stats() returns dict with all stats."""
        cb = CircuitBreaker(threshold=3, timeout=10.0)
        stats = cb.get_stats()

        assert isinstance(stats, dict)
        assert stats["state"] == "closed"
        assert stats["failures"] == 0
        assert stats["successes"] == 0
        assert stats["threshold"] == 3
        assert stats["timeout"] == 10.0
        assert "last_failure_time" in stats


class TestCircuitBreakerDecorator:
    """Tests for circuit_breaker_decorator."""

    def test_decorator_sync_function(self):
        """Decorator works on sync functions."""
        @circuit_breaker_decorator(threshold=2, timeout=10.0)
        def failing_func():
            raise ValueError("fail")

        # Get the breaker attached to the function
        breaker = failing_func.circuit_breaker
        assert breaker is not None
        assert breaker.threshold == 2

    def test_decorator_sync_works(self):
        """Decorator allows successful sync calls."""
        @circuit_breaker_decorator(threshold=3, timeout=10.0)
        def success_func():
            return "ok"

        result = success_func()
        assert result == "ok"

    @pytest.mark.asyncio
    async def test_decorator_async_function(self):
        """Decorator works on async functions."""
        @circuit_breaker_decorator(threshold=2, timeout=10.0)
        async def async_func():
            return "async ok"

        result = await async_func()
        assert result == "async ok"

    def test_decorator_sync_failure_opens_circuit(self):
        """Sync function failures open circuit."""
        @circuit_breaker_decorator(threshold=2, timeout=10.0, expected_exceptions=(ValueError,))
        def fail_func():
            raise ValueError("fail")

        breaker = fail_func.circuit_breaker

        # Fail twice to open
        with pytest.raises(ValueError):
            fail_func()
        with pytest.raises(ValueError):
            fail_func()

        assert breaker.state == CircuitState.OPEN

        # 3rd call should be rejected
        with pytest.raises(CircuitBreakerOpen):
            fail_func()


class TestShouldAttemptReset:
    """Tests for _should_attempt_reset()."""

    def test_no_last_failure_time_returns_true(self):
        """If never failed, should attempt reset."""
        cb = CircuitBreaker(threshold=3, timeout=10.0)
        cb.last_failure_time = None
        assert cb._should_attempt_reset() is True

    def test_timeout_not_elapsed_returns_false(self):
        """If timeout not elapsed, should not reset."""
        cb = CircuitBreaker(threshold=3, timeout=10.0)
        cb.last_failure_time = time.time()  # just now
        assert cb._should_attempt_reset() is False

    def test_timeout_elapsed_returns_true(self):
        """If timeout elapsed, should reset."""
        cb = CircuitBreaker(threshold=3, timeout=0.05)
        cb.last_failure_time = time.time() - 1
        assert cb._should_attempt_reset() is True


class TestCircuitBreakerConfig:
    """Tests for CircuitBreakerConfig dataclass."""

    def test_config_defaults(self):
        """Config has correct defaults."""
        from src.middleware.circuit_breaker import CircuitBreakerConfig
        config = CircuitBreakerConfig()
        assert config.threshold == 3
        assert config.timeout == 10.0
        assert config.expected_exceptions == (Exception,)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
