"""Circuit Breaker - prevents cascading failures."""

import time
import logging
from enum import Enum
from typing import Callable, Any, Optional, TypeVar
from dataclasses import dataclass
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar("T")
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
        args = [message]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerOpenǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerOpenǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁCircuitBreakerOpenǁ__init____mutmut_orig(self, message: str = "Circuit breaker is open"):
        self.message = message
        super().__init__(self.message)
    def xǁCircuitBreakerOpenǁ__init____mutmut_1(self, message: str = "XXCircuit breaker is openXX"):
        self.message = message
        super().__init__(self.message)
    def xǁCircuitBreakerOpenǁ__init____mutmut_2(self, message: str = "circuit breaker is open"):
        self.message = message
        super().__init__(self.message)
    def xǁCircuitBreakerOpenǁ__init____mutmut_3(self, message: str = "CIRCUIT BREAKER IS OPEN"):
        self.message = message
        super().__init__(self.message)
    def xǁCircuitBreakerOpenǁ__init____mutmut_4(self, message: str = "Circuit breaker is open"):
        self.message = None
        super().__init__(self.message)
    def xǁCircuitBreakerOpenǁ__init____mutmut_5(self, message: str = "Circuit breaker is open"):
        self.message = message
        super().__init__(None)
    
    xǁCircuitBreakerOpenǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerOpenǁ__init____mutmut_1': xǁCircuitBreakerOpenǁ__init____mutmut_1, 
        'xǁCircuitBreakerOpenǁ__init____mutmut_2': xǁCircuitBreakerOpenǁ__init____mutmut_2, 
        'xǁCircuitBreakerOpenǁ__init____mutmut_3': xǁCircuitBreakerOpenǁ__init____mutmut_3, 
        'xǁCircuitBreakerOpenǁ__init____mutmut_4': xǁCircuitBreakerOpenǁ__init____mutmut_4, 
        'xǁCircuitBreakerOpenǁ__init____mutmut_5': xǁCircuitBreakerOpenǁ__init____mutmut_5
    }
    xǁCircuitBreakerOpenǁ__init____mutmut_orig.__name__ = 'xǁCircuitBreakerOpenǁ__init__'


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
        args = [threshold, timeout, expected_exceptions]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerǁ__init____mutmut_mutants'), args, kwargs, self)
    
    def xǁCircuitBreakerǁ__init____mutmut_orig(
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
    
    def xǁCircuitBreakerǁ__init____mutmut_1(
        self,
        threshold: int = 4,
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
    
    def xǁCircuitBreakerǁ__init____mutmut_2(
        self,
        threshold: int = 3,
        timeout: float = 11.0,
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
    
    def xǁCircuitBreakerǁ__init____mutmut_3(
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
        self.threshold = None
        self.timeout = timeout
        self.expected_exceptions = expected_exceptions
        
        self.failures = 0
        self.successes = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_4(
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
        self.timeout = None
        self.expected_exceptions = expected_exceptions
        
        self.failures = 0
        self.successes = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_5(
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
        self.expected_exceptions = None
        
        self.failures = 0
        self.successes = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_6(
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
        
        self.failures = None
        self.successes = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_7(
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
        
        self.failures = 1
        self.successes = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_8(
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
        self.successes = None
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_9(
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
        self.successes = 1
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_10(
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
        self.last_failure_time: Optional[float] = ""
        self.state = CircuitState.CLOSED
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_11(
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
        self.state = None
        
        # For half-open test limiting
        self._half_open_attempts = 0
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_12(
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
        self._half_open_attempts = None
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_13(
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
        self._half_open_attempts = 1
        self._max_half_open_attempts = 1
    
    def xǁCircuitBreakerǁ__init____mutmut_14(
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
        self._max_half_open_attempts = None
    
    def xǁCircuitBreakerǁ__init____mutmut_15(
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
        self._max_half_open_attempts = 2
    
    xǁCircuitBreakerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerǁ__init____mutmut_1': xǁCircuitBreakerǁ__init____mutmut_1, 
        'xǁCircuitBreakerǁ__init____mutmut_2': xǁCircuitBreakerǁ__init____mutmut_2, 
        'xǁCircuitBreakerǁ__init____mutmut_3': xǁCircuitBreakerǁ__init____mutmut_3, 
        'xǁCircuitBreakerǁ__init____mutmut_4': xǁCircuitBreakerǁ__init____mutmut_4, 
        'xǁCircuitBreakerǁ__init____mutmut_5': xǁCircuitBreakerǁ__init____mutmut_5, 
        'xǁCircuitBreakerǁ__init____mutmut_6': xǁCircuitBreakerǁ__init____mutmut_6, 
        'xǁCircuitBreakerǁ__init____mutmut_7': xǁCircuitBreakerǁ__init____mutmut_7, 
        'xǁCircuitBreakerǁ__init____mutmut_8': xǁCircuitBreakerǁ__init____mutmut_8, 
        'xǁCircuitBreakerǁ__init____mutmut_9': xǁCircuitBreakerǁ__init____mutmut_9, 
        'xǁCircuitBreakerǁ__init____mutmut_10': xǁCircuitBreakerǁ__init____mutmut_10, 
        'xǁCircuitBreakerǁ__init____mutmut_11': xǁCircuitBreakerǁ__init____mutmut_11, 
        'xǁCircuitBreakerǁ__init____mutmut_12': xǁCircuitBreakerǁ__init____mutmut_12, 
        'xǁCircuitBreakerǁ__init____mutmut_13': xǁCircuitBreakerǁ__init____mutmut_13, 
        'xǁCircuitBreakerǁ__init____mutmut_14': xǁCircuitBreakerǁ__init____mutmut_14, 
        'xǁCircuitBreakerǁ__init____mutmut_15': xǁCircuitBreakerǁ__init____mutmut_15
    }
    xǁCircuitBreakerǁ__init____mutmut_orig.__name__ = 'xǁCircuitBreakerǁ__init__'
    
    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        args = [func, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerǁcall__mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerǁcall__mutmut_mutants'), args, kwargs, self)
    
    def xǁCircuitBreakerǁcall__mutmut_orig(self, func: Callable[..., T], *args, **kwargs) -> T:
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
    
    def xǁCircuitBreakerǁcall__mutmut_1(self, func: Callable[..., T], *args, **kwargs) -> T:
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
        
        if self.state != CircuitState.OPEN:
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
    
    def xǁCircuitBreakerǁcall__mutmut_2(self, func: Callable[..., T], *args, **kwargs) -> T:
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
                None
            )
        
        # Execute function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    def xǁCircuitBreakerǁcall__mutmut_3(self, func: Callable[..., T], *args, **kwargs) -> T:
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
            result = None
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    def xǁCircuitBreakerǁcall__mutmut_4(self, func: Callable[..., T], *args, **kwargs) -> T:
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
            result = func(**kwargs)
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    def xǁCircuitBreakerǁcall__mutmut_5(self, func: Callable[..., T], *args, **kwargs) -> T:
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
            result = func(*args, )
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    xǁCircuitBreakerǁcall__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerǁcall__mutmut_1': xǁCircuitBreakerǁcall__mutmut_1, 
        'xǁCircuitBreakerǁcall__mutmut_2': xǁCircuitBreakerǁcall__mutmut_2, 
        'xǁCircuitBreakerǁcall__mutmut_3': xǁCircuitBreakerǁcall__mutmut_3, 
        'xǁCircuitBreakerǁcall__mutmut_4': xǁCircuitBreakerǁcall__mutmut_4, 
        'xǁCircuitBreakerǁcall__mutmut_5': xǁCircuitBreakerǁcall__mutmut_5
    }
    xǁCircuitBreakerǁcall__mutmut_orig.__name__ = 'xǁCircuitBreakerǁcall'
    
    async def call_async(self, func: Callable[..., T], *args, **kwargs) -> T:
        args = [func, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerǁcall_async__mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerǁcall_async__mutmut_mutants'), args, kwargs, self)
    
    async def xǁCircuitBreakerǁcall_async__mutmut_orig(self, func: Callable[..., T], *args, **kwargs) -> T:
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
    
    async def xǁCircuitBreakerǁcall_async__mutmut_1(self, func: Callable[..., T], *args, **kwargs) -> T:
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
        
        if self.state != CircuitState.OPEN:
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
    
    async def xǁCircuitBreakerǁcall_async__mutmut_2(self, func: Callable[..., T], *args, **kwargs) -> T:
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
                None
            )
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    async def xǁCircuitBreakerǁcall_async__mutmut_3(self, func: Callable[..., T], *args, **kwargs) -> T:
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
            result = None
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    async def xǁCircuitBreakerǁcall_async__mutmut_4(self, func: Callable[..., T], *args, **kwargs) -> T:
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
            result = await func(**kwargs)
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    async def xǁCircuitBreakerǁcall_async__mutmut_5(self, func: Callable[..., T], *args, **kwargs) -> T:
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
            result = await func(*args, )
            self._on_success()
            return result
        except self.expected_exceptions as e:
            self._on_failure()
            raise
    
    xǁCircuitBreakerǁcall_async__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerǁcall_async__mutmut_1': xǁCircuitBreakerǁcall_async__mutmut_1, 
        'xǁCircuitBreakerǁcall_async__mutmut_2': xǁCircuitBreakerǁcall_async__mutmut_2, 
        'xǁCircuitBreakerǁcall_async__mutmut_3': xǁCircuitBreakerǁcall_async__mutmut_3, 
        'xǁCircuitBreakerǁcall_async__mutmut_4': xǁCircuitBreakerǁcall_async__mutmut_4, 
        'xǁCircuitBreakerǁcall_async__mutmut_5': xǁCircuitBreakerǁcall_async__mutmut_5
    }
    xǁCircuitBreakerǁcall_async__mutmut_orig.__name__ = 'xǁCircuitBreakerǁcall_async'
    
    def _check_and_transition(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerǁ_check_and_transition__mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerǁ_check_and_transition__mutmut_mutants'), args, kwargs, self)
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_orig(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("Circuit breaker: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 0
                self.successes = 0
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_1(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state != CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("Circuit breaker: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 0
                self.successes = 0
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_2(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info(None)
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 0
                self.successes = 0
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_3(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("XXCircuit breaker: OPEN -> HALF_OPENXX")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 0
                self.successes = 0
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_4(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("circuit breaker: open -> half_open")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 0
                self.successes = 0
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_5(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("CIRCUIT BREAKER: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 0
                self.successes = 0
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_6(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("Circuit breaker: OPEN -> HALF_OPEN")
                self.state = None
                self._half_open_attempts = 0
                self.successes = 0
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_7(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("Circuit breaker: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = None
                self.successes = 0
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_8(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("Circuit breaker: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 1
                self.successes = 0
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_9(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("Circuit breaker: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 0
                self.successes = None
    
    def xǁCircuitBreakerǁ_check_and_transition__mutmut_10(self) -> None:
        """Check state and perform transitions if needed."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("Circuit breaker: OPEN -> HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
                self._half_open_attempts = 0
                self.successes = 1
    
    xǁCircuitBreakerǁ_check_and_transition__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerǁ_check_and_transition__mutmut_1': xǁCircuitBreakerǁ_check_and_transition__mutmut_1, 
        'xǁCircuitBreakerǁ_check_and_transition__mutmut_2': xǁCircuitBreakerǁ_check_and_transition__mutmut_2, 
        'xǁCircuitBreakerǁ_check_and_transition__mutmut_3': xǁCircuitBreakerǁ_check_and_transition__mutmut_3, 
        'xǁCircuitBreakerǁ_check_and_transition__mutmut_4': xǁCircuitBreakerǁ_check_and_transition__mutmut_4, 
        'xǁCircuitBreakerǁ_check_and_transition__mutmut_5': xǁCircuitBreakerǁ_check_and_transition__mutmut_5, 
        'xǁCircuitBreakerǁ_check_and_transition__mutmut_6': xǁCircuitBreakerǁ_check_and_transition__mutmut_6, 
        'xǁCircuitBreakerǁ_check_and_transition__mutmut_7': xǁCircuitBreakerǁ_check_and_transition__mutmut_7, 
        'xǁCircuitBreakerǁ_check_and_transition__mutmut_8': xǁCircuitBreakerǁ_check_and_transition__mutmut_8, 
        'xǁCircuitBreakerǁ_check_and_transition__mutmut_9': xǁCircuitBreakerǁ_check_and_transition__mutmut_9, 
        'xǁCircuitBreakerǁ_check_and_transition__mutmut_10': xǁCircuitBreakerǁ_check_and_transition__mutmut_10
    }
    xǁCircuitBreakerǁ_check_and_transition__mutmut_orig.__name__ = 'xǁCircuitBreakerǁ_check_and_transition'
    
    def _should_attempt_reset(self) -> bool:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerǁ_should_attempt_reset__mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerǁ_should_attempt_reset__mutmut_mutants'), args, kwargs, self)
    
    def xǁCircuitBreakerǁ_should_attempt_reset__mutmut_orig(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) >= self.timeout
    
    def xǁCircuitBreakerǁ_should_attempt_reset__mutmut_1(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is not None:
            return True
        return (time.time() - self.last_failure_time) >= self.timeout
    
    def xǁCircuitBreakerǁ_should_attempt_reset__mutmut_2(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return False
        return (time.time() - self.last_failure_time) >= self.timeout
    
    def xǁCircuitBreakerǁ_should_attempt_reset__mutmut_3(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        return (time.time() + self.last_failure_time) >= self.timeout
    
    def xǁCircuitBreakerǁ_should_attempt_reset__mutmut_4(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) > self.timeout
    
    xǁCircuitBreakerǁ_should_attempt_reset__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerǁ_should_attempt_reset__mutmut_1': xǁCircuitBreakerǁ_should_attempt_reset__mutmut_1, 
        'xǁCircuitBreakerǁ_should_attempt_reset__mutmut_2': xǁCircuitBreakerǁ_should_attempt_reset__mutmut_2, 
        'xǁCircuitBreakerǁ_should_attempt_reset__mutmut_3': xǁCircuitBreakerǁ_should_attempt_reset__mutmut_3, 
        'xǁCircuitBreakerǁ_should_attempt_reset__mutmut_4': xǁCircuitBreakerǁ_should_attempt_reset__mutmut_4
    }
    xǁCircuitBreakerǁ_should_attempt_reset__mutmut_orig.__name__ = 'xǁCircuitBreakerǁ_should_attempt_reset'
    
    def _on_success(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerǁ_on_success__mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerǁ_on_success__mutmut_mutants'), args, kwargs, self)
    
    def xǁCircuitBreakerǁ_on_success__mutmut_orig(self) -> None:
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
    
    def xǁCircuitBreakerǁ_on_success__mutmut_1(self) -> None:
        """Handle successful call."""
        self.failures = None
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_2(self) -> None:
        """Handle successful call."""
        self.failures = 1
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_3(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state != CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_4(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes = 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_5(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes -= 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_6(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 2
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_7(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes > self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_8(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info(None)
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_9(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("XXCircuit breaker: HALF_OPEN -> CLOSEDXX")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_10(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("circuit breaker: half_open -> closed")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_11(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("CIRCUIT BREAKER: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_12(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = None
                self.successes = 0
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_13(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = None
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_14(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 1
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    def xǁCircuitBreakerǁ_on_success__mutmut_15(self) -> None:
        """Handle successful call."""
        self.failures = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self._max_half_open_attempts:
                logger.info("Circuit breaker: HALF_OPEN -> CLOSED")
                self.state = CircuitState.CLOSED
                self.successes = 0
        elif self.state != CircuitState.CLOSED:
            # Reset failure count on success
            pass
    
    xǁCircuitBreakerǁ_on_success__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerǁ_on_success__mutmut_1': xǁCircuitBreakerǁ_on_success__mutmut_1, 
        'xǁCircuitBreakerǁ_on_success__mutmut_2': xǁCircuitBreakerǁ_on_success__mutmut_2, 
        'xǁCircuitBreakerǁ_on_success__mutmut_3': xǁCircuitBreakerǁ_on_success__mutmut_3, 
        'xǁCircuitBreakerǁ_on_success__mutmut_4': xǁCircuitBreakerǁ_on_success__mutmut_4, 
        'xǁCircuitBreakerǁ_on_success__mutmut_5': xǁCircuitBreakerǁ_on_success__mutmut_5, 
        'xǁCircuitBreakerǁ_on_success__mutmut_6': xǁCircuitBreakerǁ_on_success__mutmut_6, 
        'xǁCircuitBreakerǁ_on_success__mutmut_7': xǁCircuitBreakerǁ_on_success__mutmut_7, 
        'xǁCircuitBreakerǁ_on_success__mutmut_8': xǁCircuitBreakerǁ_on_success__mutmut_8, 
        'xǁCircuitBreakerǁ_on_success__mutmut_9': xǁCircuitBreakerǁ_on_success__mutmut_9, 
        'xǁCircuitBreakerǁ_on_success__mutmut_10': xǁCircuitBreakerǁ_on_success__mutmut_10, 
        'xǁCircuitBreakerǁ_on_success__mutmut_11': xǁCircuitBreakerǁ_on_success__mutmut_11, 
        'xǁCircuitBreakerǁ_on_success__mutmut_12': xǁCircuitBreakerǁ_on_success__mutmut_12, 
        'xǁCircuitBreakerǁ_on_success__mutmut_13': xǁCircuitBreakerǁ_on_success__mutmut_13, 
        'xǁCircuitBreakerǁ_on_success__mutmut_14': xǁCircuitBreakerǁ_on_success__mutmut_14, 
        'xǁCircuitBreakerǁ_on_success__mutmut_15': xǁCircuitBreakerǁ_on_success__mutmut_15
    }
    xǁCircuitBreakerǁ_on_success__mutmut_orig.__name__ = 'xǁCircuitBreakerǁ_on_success'
    
    def _on_failure(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerǁ_on_failure__mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerǁ_on_failure__mutmut_mutants'), args, kwargs, self)
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_orig(self) -> None:
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
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_1(self) -> None:
        """Handle failed call."""
        self.failures = 1
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
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_2(self) -> None:
        """Handle failed call."""
        self.failures -= 1
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
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_3(self) -> None:
        """Handle failed call."""
        self.failures += 2
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
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_4(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = None
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_5(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state != CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_6(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning(None)
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_7(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("XXCircuit breaker: HALF_OPEN -> OPEN (test failed)XX")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_8(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("circuit breaker: half_open -> open (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_9(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("CIRCUIT BREAKER: HALF_OPEN -> OPEN (TEST FAILED)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_10(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = None
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_11(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts = 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_12(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts -= 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_13(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 2
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_14(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED or self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_15(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state != CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_16(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures > self.threshold:
            logger.warning(
                f"Circuit breaker: CLOSED -> OPEN ({self.failures} failures)"
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_17(self) -> None:
        """Handle failed call."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: HALF_OPEN -> OPEN (test failed)")
            self.state = CircuitState.OPEN
            self._half_open_attempts += 1
        elif self.state == CircuitState.CLOSED and self.failures >= self.threshold:
            logger.warning(
                None
            )
            self.state = CircuitState.OPEN
    
    def xǁCircuitBreakerǁ_on_failure__mutmut_18(self) -> None:
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
            self.state = None
    
    xǁCircuitBreakerǁ_on_failure__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerǁ_on_failure__mutmut_1': xǁCircuitBreakerǁ_on_failure__mutmut_1, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_2': xǁCircuitBreakerǁ_on_failure__mutmut_2, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_3': xǁCircuitBreakerǁ_on_failure__mutmut_3, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_4': xǁCircuitBreakerǁ_on_failure__mutmut_4, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_5': xǁCircuitBreakerǁ_on_failure__mutmut_5, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_6': xǁCircuitBreakerǁ_on_failure__mutmut_6, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_7': xǁCircuitBreakerǁ_on_failure__mutmut_7, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_8': xǁCircuitBreakerǁ_on_failure__mutmut_8, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_9': xǁCircuitBreakerǁ_on_failure__mutmut_9, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_10': xǁCircuitBreakerǁ_on_failure__mutmut_10, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_11': xǁCircuitBreakerǁ_on_failure__mutmut_11, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_12': xǁCircuitBreakerǁ_on_failure__mutmut_12, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_13': xǁCircuitBreakerǁ_on_failure__mutmut_13, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_14': xǁCircuitBreakerǁ_on_failure__mutmut_14, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_15': xǁCircuitBreakerǁ_on_failure__mutmut_15, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_16': xǁCircuitBreakerǁ_on_failure__mutmut_16, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_17': xǁCircuitBreakerǁ_on_failure__mutmut_17, 
        'xǁCircuitBreakerǁ_on_failure__mutmut_18': xǁCircuitBreakerǁ_on_failure__mutmut_18
    }
    xǁCircuitBreakerǁ_on_failure__mutmut_orig.__name__ = 'xǁCircuitBreakerǁ_on_failure'
    
    def reset(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerǁreset__mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerǁreset__mutmut_mutants'), args, kwargs, self)
    
    def xǁCircuitBreakerǁreset__mutmut_orig(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def xǁCircuitBreakerǁreset__mutmut_1(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = None
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def xǁCircuitBreakerǁreset__mutmut_2(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 1
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def xǁCircuitBreakerǁreset__mutmut_3(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = None
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def xǁCircuitBreakerǁreset__mutmut_4(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 1
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def xǁCircuitBreakerǁreset__mutmut_5(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = ""
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def xǁCircuitBreakerǁreset__mutmut_6(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.state = None
        self._half_open_attempts = 0
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def xǁCircuitBreakerǁreset__mutmut_7(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = None
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def xǁCircuitBreakerǁreset__mutmut_8(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 1
        logger.info("Circuit breaker manually reset to CLOSED")
    
    def xǁCircuitBreakerǁreset__mutmut_9(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info(None)
    
    def xǁCircuitBreakerǁreset__mutmut_10(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("XXCircuit breaker manually reset to CLOSEDXX")
    
    def xǁCircuitBreakerǁreset__mutmut_11(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("circuit breaker manually reset to closed")
    
    def xǁCircuitBreakerǁreset__mutmut_12(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._half_open_attempts = 0
        logger.info("CIRCUIT BREAKER MANUALLY RESET TO CLOSED")
    
    xǁCircuitBreakerǁreset__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerǁreset__mutmut_1': xǁCircuitBreakerǁreset__mutmut_1, 
        'xǁCircuitBreakerǁreset__mutmut_2': xǁCircuitBreakerǁreset__mutmut_2, 
        'xǁCircuitBreakerǁreset__mutmut_3': xǁCircuitBreakerǁreset__mutmut_3, 
        'xǁCircuitBreakerǁreset__mutmut_4': xǁCircuitBreakerǁreset__mutmut_4, 
        'xǁCircuitBreakerǁreset__mutmut_5': xǁCircuitBreakerǁreset__mutmut_5, 
        'xǁCircuitBreakerǁreset__mutmut_6': xǁCircuitBreakerǁreset__mutmut_6, 
        'xǁCircuitBreakerǁreset__mutmut_7': xǁCircuitBreakerǁreset__mutmut_7, 
        'xǁCircuitBreakerǁreset__mutmut_8': xǁCircuitBreakerǁreset__mutmut_8, 
        'xǁCircuitBreakerǁreset__mutmut_9': xǁCircuitBreakerǁreset__mutmut_9, 
        'xǁCircuitBreakerǁreset__mutmut_10': xǁCircuitBreakerǁreset__mutmut_10, 
        'xǁCircuitBreakerǁreset__mutmut_11': xǁCircuitBreakerǁreset__mutmut_11, 
        'xǁCircuitBreakerǁreset__mutmut_12': xǁCircuitBreakerǁreset__mutmut_12
    }
    xǁCircuitBreakerǁreset__mutmut_orig.__name__ = 'xǁCircuitBreakerǁreset'
    
    def get_state(self) -> CircuitState:
        """Get current circuit breaker state."""
        return self.state
    
    def get_stats(self) -> dict:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCircuitBreakerǁget_stats__mutmut_orig'), object.__getattribute__(self, 'xǁCircuitBreakerǁget_stats__mutmut_mutants'), args, kwargs, self)
    
    def xǁCircuitBreakerǁget_stats__mutmut_orig(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_1(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "XXstateXX": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_2(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "STATE": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_3(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "XXfailuresXX": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_4(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "FAILURES": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_5(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "XXsuccessesXX": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_6(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "SUCCESSES": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_7(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "XXlast_failure_timeXX": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_8(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "LAST_FAILURE_TIME": self.last_failure_time,
            "threshold": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_9(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "XXthresholdXX": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_10(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "THRESHOLD": self.threshold,
            "timeout": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_11(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "XXtimeoutXX": self.timeout,
        }
    
    def xǁCircuitBreakerǁget_stats__mutmut_12(self) -> dict:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failures": self.failures,
            "successes": self.successes,
            "last_failure_time": self.last_failure_time,
            "threshold": self.threshold,
            "TIMEOUT": self.timeout,
        }
    
    xǁCircuitBreakerǁget_stats__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCircuitBreakerǁget_stats__mutmut_1': xǁCircuitBreakerǁget_stats__mutmut_1, 
        'xǁCircuitBreakerǁget_stats__mutmut_2': xǁCircuitBreakerǁget_stats__mutmut_2, 
        'xǁCircuitBreakerǁget_stats__mutmut_3': xǁCircuitBreakerǁget_stats__mutmut_3, 
        'xǁCircuitBreakerǁget_stats__mutmut_4': xǁCircuitBreakerǁget_stats__mutmut_4, 
        'xǁCircuitBreakerǁget_stats__mutmut_5': xǁCircuitBreakerǁget_stats__mutmut_5, 
        'xǁCircuitBreakerǁget_stats__mutmut_6': xǁCircuitBreakerǁget_stats__mutmut_6, 
        'xǁCircuitBreakerǁget_stats__mutmut_7': xǁCircuitBreakerǁget_stats__mutmut_7, 
        'xǁCircuitBreakerǁget_stats__mutmut_8': xǁCircuitBreakerǁget_stats__mutmut_8, 
        'xǁCircuitBreakerǁget_stats__mutmut_9': xǁCircuitBreakerǁget_stats__mutmut_9, 
        'xǁCircuitBreakerǁget_stats__mutmut_10': xǁCircuitBreakerǁget_stats__mutmut_10, 
        'xǁCircuitBreakerǁget_stats__mutmut_11': xǁCircuitBreakerǁget_stats__mutmut_11, 
        'xǁCircuitBreakerǁget_stats__mutmut_12': xǁCircuitBreakerǁget_stats__mutmut_12
    }
    xǁCircuitBreakerǁget_stats__mutmut_orig.__name__ = 'xǁCircuitBreakerǁget_stats'


def circuit_breaker_decorator(
    threshold: int = 3,
    timeout: float = 10.0,
    expected_exceptions: tuple = (Exception,),
):
    args = [threshold, timeout, expected_exceptions]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_circuit_breaker_decorator__mutmut_orig, x_circuit_breaker_decorator__mutmut_mutants, args, kwargs, None)


def x_circuit_breaker_decorator__mutmut_orig(
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


def x_circuit_breaker_decorator__mutmut_1(
    threshold: int = 4,
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


def x_circuit_breaker_decorator__mutmut_2(
    threshold: int = 3,
    timeout: float = 11.0,
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


def x_circuit_breaker_decorator__mutmut_3(
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
    breaker = None
    
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


def x_circuit_breaker_decorator__mutmut_4(
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
    breaker = CircuitBreaker(None, timeout, expected_exceptions)
    
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


def x_circuit_breaker_decorator__mutmut_5(
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
    breaker = CircuitBreaker(threshold, None, expected_exceptions)
    
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


def x_circuit_breaker_decorator__mutmut_6(
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
    breaker = CircuitBreaker(threshold, timeout, None)
    
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


def x_circuit_breaker_decorator__mutmut_7(
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
    breaker = CircuitBreaker(timeout, expected_exceptions)
    
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


def x_circuit_breaker_decorator__mutmut_8(
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
    breaker = CircuitBreaker(threshold, expected_exceptions)
    
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


def x_circuit_breaker_decorator__mutmut_9(
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
    breaker = CircuitBreaker(threshold, timeout, )
    
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


def x_circuit_breaker_decorator__mutmut_10(
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
        wrapper.circuit_breaker = None
        async_wrapper.circuit_breaker = breaker
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper
    
    import asyncio
    return decorator


def x_circuit_breaker_decorator__mutmut_11(
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
        async_wrapper.circuit_breaker = None
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper
    
    import asyncio
    return decorator


def x_circuit_breaker_decorator__mutmut_12(
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
        
        if asyncio.iscoroutinefunction(None):
            return async_wrapper
        return wrapper
    
    import asyncio
    return decorator

x_circuit_breaker_decorator__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_circuit_breaker_decorator__mutmut_1': x_circuit_breaker_decorator__mutmut_1, 
    'x_circuit_breaker_decorator__mutmut_2': x_circuit_breaker_decorator__mutmut_2, 
    'x_circuit_breaker_decorator__mutmut_3': x_circuit_breaker_decorator__mutmut_3, 
    'x_circuit_breaker_decorator__mutmut_4': x_circuit_breaker_decorator__mutmut_4, 
    'x_circuit_breaker_decorator__mutmut_5': x_circuit_breaker_decorator__mutmut_5, 
    'x_circuit_breaker_decorator__mutmut_6': x_circuit_breaker_decorator__mutmut_6, 
    'x_circuit_breaker_decorator__mutmut_7': x_circuit_breaker_decorator__mutmut_7, 
    'x_circuit_breaker_decorator__mutmut_8': x_circuit_breaker_decorator__mutmut_8, 
    'x_circuit_breaker_decorator__mutmut_9': x_circuit_breaker_decorator__mutmut_9, 
    'x_circuit_breaker_decorator__mutmut_10': x_circuit_breaker_decorator__mutmut_10, 
    'x_circuit_breaker_decorator__mutmut_11': x_circuit_breaker_decorator__mutmut_11, 
    'x_circuit_breaker_decorator__mutmut_12': x_circuit_breaker_decorator__mutmut_12
}
x_circuit_breaker_decorator__mutmut_orig.__name__ = 'x_circuit_breaker_decorator'
