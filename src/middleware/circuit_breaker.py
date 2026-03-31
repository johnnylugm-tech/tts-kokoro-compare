"""Circuit Breaker - prevents cascading failures."""

import time
import logging
from enum import Enum
from typing import Callable, Any, Optional, TypeVar
from dataclasses import dataclass
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    threshold: int = 3  # Failures before opening
    timeout: float = 10.0  # Seconds before half-open
    expected_exceptions: tuple = (Exception,)


class CircuitBreakerOpen(Exception):
    """Exception raised when circuit breaker is open."""
    def __init__(self, message: str = "Circuit breaker is open"):
        self.message = message
        super().__init__(self.message)


class CircuitBreaker:
    """
    Circuit breaker pattern implementation.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Too many failures, requests are rejected
    - HALF_OPEN: Testing recovery, limited requests pass through
    
    Transitions:
    - CLOSED -> OPEN: After threshold failures
    - OPEN -> HALF_OPEN: After timeout
    - HALF_OPEN -> OPEN: If test request fails
    - HALF_OPEN -> CLOSED: If test request succeeds
    """
    
    def __init__(
        self,
        threshold: int = 3,
        timeout: float = 10.0,
        expected_exceptions: tuple = (Exception,),
    ):
        """
        Initialize circuit breaker.
        
        Args:
            threshold: Number of failures before opening circuit
            timeout: Seconds to wait before testing recovery
            expected_exceptions: Tuple of exception types to catch
        """
        self.threshold = threshold
        self.timeout = timeout
        self.expected_exceptions = expected_exceptions
        
        self.failures = 0
        self.successes = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute function through circuit breaker.
        
        Args:
            func: Function to call
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func
            
        Returns:
            Result of func
            
        Raises:
            CircuitBreakerOpen: If circuit is open
            Exception: If function raises an expected exception
        """
        # Check state and possibly transition
        self._check_and_transition()
        
        if self.state == CircuitState.OPEN:
            raise CircuitBreakerOpen(
                f"Circuit breaker is open. Last failure: {self.last_failure_time}"
            )
        
        # Execute function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    async def call_async(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute async function through circuit breaker.
        
        Args:
            func: Async function to call
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func
            
        Returns:
            Result of func
            
        Raises:
            CircuitBreakerOpen: If circuit is open
            Exception: If function raises an expected exception
        """
        self._check_and_transition()
        
        if self.state == CircuitState.OPEN:
            raise CircuitBreakerOpen(
                f"Circuit breaker is open. Last failure: {self.last_failure_time}"
            )
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    def _check_and_transition(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("Circuit breaker: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 0
                self.successes = 0
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) >= self.timeout
    
    def _on_success(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def _on_failure(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def reset(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def get_state(self) -> CircuitState:
        """Get current circuit breaker state."""
        return self.state
    
    def get_stats(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }


def circuit_breaker_decorator(
    threshold: int = 3,
    timeout: float = 10.0,
    expected_exceptions: tuple = (Exception,),
):
    """
    Decorator to add circuit breaker to a function.
    
    Args:
        threshold: Number of failures before opening
        timeout: Seconds before attempting reset
        expected_exceptions: Exceptions to catch
        
    Returns:
        Decorated function
    """
    breaker = CircuitBreaker(threshold, timeout, expected_exceptions)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            return breaker.call(func, *args, **kwargs)
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            return await breaker.call_async(func, *args, **kwargs)
        
        # Attach breaker to function for access
        wrapper.circuit_breaker = breaker
        async_wrapper.circuit_breaker = breaker
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper
    
    import asyncio
    return decorator
