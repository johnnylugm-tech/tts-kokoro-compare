"""Text Splitter - intelligent text segmentation for TTS."""

import re
import logging
from typing import List, Tuple
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
class SplitResult:
    """Result of text splitting operation."""
    segments: List[str]
    total_segments: int
    avg_segment_length: float


class TextSplitter:
    """
    Intelligent text splitter with 3-level recursive segmentation.
    
    Level 1 (Sentence): 。？！!?\n
    Level 2 (Clause): ；： (if segment > 100 chars)
    Level 3 (Phrase): ， (if still > 100 chars)
    """
    
    # Primary sentence ending punctuation (Chinese and English)
    SENTENCE_ENDINGS = r"([。？！!?\n]+)"
    
    # Clause separators (used when segment is too long)
    CLAUSE_SEPARATORS = r"([；：])"
    
    # Phrase separators (final fallback)
    PHRASE_SEPARATORS = r"([，。,、])"
    
    def __init__(self, max_chars: int = 250, optimal_range: Tuple[int, int] = (100, 250)):
        args = [max_chars, optimal_range]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTextSplitterǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁTextSplitterǁ__init____mutmut_mutants'), args, kwargs, self)
    
    def xǁTextSplitterǁ__init____mutmut_orig(self, max_chars: int = 250, optimal_range: Tuple[int, int] = (100, 250)):
        """
        Initialize text splitter.
        
        Args:
            max_chars: Maximum characters per segment
            optimal_range: Optimal character range for segments (min, max)
        """
        self.max_chars = max_chars
        self.optimal_min, self.optimal_max = optimal_range
    
    def xǁTextSplitterǁ__init____mutmut_1(self, max_chars: int = 251, optimal_range: Tuple[int, int] = (100, 250)):
        """
        Initialize text splitter.
        
        Args:
            max_chars: Maximum characters per segment
            optimal_range: Optimal character range for segments (min, max)
        """
        self.max_chars = max_chars
        self.optimal_min, self.optimal_max = optimal_range
    
    def xǁTextSplitterǁ__init____mutmut_2(self, max_chars: int = 250, optimal_range: Tuple[int, int] = (100, 250)):
        """
        Initialize text splitter.
        
        Args:
            max_chars: Maximum characters per segment
            optimal_range: Optimal character range for segments (min, max)
        """
        self.max_chars = None
        self.optimal_min, self.optimal_max = optimal_range
    
    def xǁTextSplitterǁ__init____mutmut_3(self, max_chars: int = 250, optimal_range: Tuple[int, int] = (100, 250)):
        """
        Initialize text splitter.
        
        Args:
            max_chars: Maximum characters per segment
            optimal_range: Optimal character range for segments (min, max)
        """
        self.max_chars = max_chars
        self.optimal_min, self.optimal_max = None
    
    xǁTextSplitterǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTextSplitterǁ__init____mutmut_1': xǁTextSplitterǁ__init____mutmut_1, 
        'xǁTextSplitterǁ__init____mutmut_2': xǁTextSplitterǁ__init____mutmut_2, 
        'xǁTextSplitterǁ__init____mutmut_3': xǁTextSplitterǁ__init____mutmut_3
    }
    xǁTextSplitterǁ__init____mutmut_orig.__name__ = 'xǁTextSplitterǁ__init__'

    def split(self, text: str, max_chars: int = None) -> List[str]:
        args = [text, max_chars]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTextSplitterǁsplit__mutmut_orig'), object.__getattribute__(self, 'xǁTextSplitterǁsplit__mutmut_mutants'), args, kwargs, self)

    def xǁTextSplitterǁsplit__mutmut_orig(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_1(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_2(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = None
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_3(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars and self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_4(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) < limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_5(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = None
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_6(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(None, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_7(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, None)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_8(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_9(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, )
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_10(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = None
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_11(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) < limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_12(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(None)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_13(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = None
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_14(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(None, limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_15(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, None)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_16(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(limit)
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_17(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, )
                final_segments.extend(emergency)
        
        return final_segments

    def xǁTextSplitterǁsplit__mutmut_18(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text into segments respecting the maximum character limit.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment (overrides instance default)
            
        Returns:
            List of text segments
        """
        if not text:
            return []
        
        limit = max_chars or self.max_chars
        
        # Fast path: text is already within limit
        if len(text) <= limit:
            return [text]
        
        # Use semantic splitting
        segments = self.split_semantic(text, limit)
        
        # Final cleanup: ensure no segment exceeds limit
        final_segments = []
        for seg in segments:
            if len(seg) <= limit:
                final_segments.append(seg)
            else:
                # Emergency split by character count
                emergency = self._emergency_split(seg, limit)
                final_segments.extend(None)
        
        return final_segments
    
    xǁTextSplitterǁsplit__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTextSplitterǁsplit__mutmut_1': xǁTextSplitterǁsplit__mutmut_1, 
        'xǁTextSplitterǁsplit__mutmut_2': xǁTextSplitterǁsplit__mutmut_2, 
        'xǁTextSplitterǁsplit__mutmut_3': xǁTextSplitterǁsplit__mutmut_3, 
        'xǁTextSplitterǁsplit__mutmut_4': xǁTextSplitterǁsplit__mutmut_4, 
        'xǁTextSplitterǁsplit__mutmut_5': xǁTextSplitterǁsplit__mutmut_5, 
        'xǁTextSplitterǁsplit__mutmut_6': xǁTextSplitterǁsplit__mutmut_6, 
        'xǁTextSplitterǁsplit__mutmut_7': xǁTextSplitterǁsplit__mutmut_7, 
        'xǁTextSplitterǁsplit__mutmut_8': xǁTextSplitterǁsplit__mutmut_8, 
        'xǁTextSplitterǁsplit__mutmut_9': xǁTextSplitterǁsplit__mutmut_9, 
        'xǁTextSplitterǁsplit__mutmut_10': xǁTextSplitterǁsplit__mutmut_10, 
        'xǁTextSplitterǁsplit__mutmut_11': xǁTextSplitterǁsplit__mutmut_11, 
        'xǁTextSplitterǁsplit__mutmut_12': xǁTextSplitterǁsplit__mutmut_12, 
        'xǁTextSplitterǁsplit__mutmut_13': xǁTextSplitterǁsplit__mutmut_13, 
        'xǁTextSplitterǁsplit__mutmut_14': xǁTextSplitterǁsplit__mutmut_14, 
        'xǁTextSplitterǁsplit__mutmut_15': xǁTextSplitterǁsplit__mutmut_15, 
        'xǁTextSplitterǁsplit__mutmut_16': xǁTextSplitterǁsplit__mutmut_16, 
        'xǁTextSplitterǁsplit__mutmut_17': xǁTextSplitterǁsplit__mutmut_17, 
        'xǁTextSplitterǁsplit__mutmut_18': xǁTextSplitterǁsplit__mutmut_18
    }
    xǁTextSplitterǁsplit__mutmut_orig.__name__ = 'xǁTextSplitterǁsplit'

    def split_semantic(self, text: str, max_chars: int = None) -> List[str]:
        args = [text, max_chars]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTextSplitterǁsplit_semantic__mutmut_orig'), object.__getattribute__(self, 'xǁTextSplitterǁsplit_semantic__mutmut_mutants'), args, kwargs, self)

    def xǁTextSplitterǁsplit_semantic__mutmut_orig(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_1(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = None
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_2(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars and self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_3(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = None
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_4(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(None)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_5(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = None
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_6(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = None
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_7(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_8(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                break
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_9(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) < limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_10(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(None)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_11(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(None)
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_12(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(None, limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_13(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, None))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_14(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(limit))
        
        return result

    def xǁTextSplitterǁsplit_semantic__mutmut_15(self, text: str, max_chars: int = None) -> List[str]:
        """
        Split text using 3-level recursive semantic segmentation.
        
        Args:
            text: Input text to split
            max_chars: Maximum characters per segment
            
        Returns:
            List of semantically segmented text
        """
        limit = max_chars or self.max_chars
        
        # Level 1: Split by sentence endings
        segments = self._split_by_sentence(text)
        
        # Process each segment
        result: List[str] = []
        
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            
            # If within limit, add directly
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Level 2: Split by clause separators
                result.extend(self._split_level2(seg, ))
        
        return result
    
    xǁTextSplitterǁsplit_semantic__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTextSplitterǁsplit_semantic__mutmut_1': xǁTextSplitterǁsplit_semantic__mutmut_1, 
        'xǁTextSplitterǁsplit_semantic__mutmut_2': xǁTextSplitterǁsplit_semantic__mutmut_2, 
        'xǁTextSplitterǁsplit_semantic__mutmut_3': xǁTextSplitterǁsplit_semantic__mutmut_3, 
        'xǁTextSplitterǁsplit_semantic__mutmut_4': xǁTextSplitterǁsplit_semantic__mutmut_4, 
        'xǁTextSplitterǁsplit_semantic__mutmut_5': xǁTextSplitterǁsplit_semantic__mutmut_5, 
        'xǁTextSplitterǁsplit_semantic__mutmut_6': xǁTextSplitterǁsplit_semantic__mutmut_6, 
        'xǁTextSplitterǁsplit_semantic__mutmut_7': xǁTextSplitterǁsplit_semantic__mutmut_7, 
        'xǁTextSplitterǁsplit_semantic__mutmut_8': xǁTextSplitterǁsplit_semantic__mutmut_8, 
        'xǁTextSplitterǁsplit_semantic__mutmut_9': xǁTextSplitterǁsplit_semantic__mutmut_9, 
        'xǁTextSplitterǁsplit_semantic__mutmut_10': xǁTextSplitterǁsplit_semantic__mutmut_10, 
        'xǁTextSplitterǁsplit_semantic__mutmut_11': xǁTextSplitterǁsplit_semantic__mutmut_11, 
        'xǁTextSplitterǁsplit_semantic__mutmut_12': xǁTextSplitterǁsplit_semantic__mutmut_12, 
        'xǁTextSplitterǁsplit_semantic__mutmut_13': xǁTextSplitterǁsplit_semantic__mutmut_13, 
        'xǁTextSplitterǁsplit_semantic__mutmut_14': xǁTextSplitterǁsplit_semantic__mutmut_14, 
        'xǁTextSplitterǁsplit_semantic__mutmut_15': xǁTextSplitterǁsplit_semantic__mutmut_15
    }
    xǁTextSplitterǁsplit_semantic__mutmut_orig.__name__ = 'xǁTextSplitterǁsplit_semantic'

    def _split_by_sentence(self, text: str) -> List[str]:
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTextSplitterǁ_split_by_sentence__mutmut_orig'), object.__getattribute__(self, 'xǁTextSplitterǁ_split_by_sentence__mutmut_mutants'), args, kwargs, self)

    def xǁTextSplitterǁ_split_by_sentence__mutmut_orig(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_1(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = None
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_2(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(None)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_3(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = None

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_4(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(None)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_5(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = None
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_6(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = None

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_7(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = "XXXX"

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_8(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_9(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                break

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_10(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(None, part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_11(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", None):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_12(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_13(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", ):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_14(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"XX[。？！!?\n]+$XX", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_15(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(None)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_16(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = None
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_17(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(None)
                buffer = part

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_18(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = None

        if buffer:
            result.append(buffer)

        return result if result else [text]

    def xǁTextSplitterǁ_split_by_sentence__mutmut_19(self, text: str) -> List[str]:
        """Split text by sentence-ending punctuation."""
        pattern = re.compile(self.SENTENCE_ENDINGS)
        parts = pattern.split(text)

        result: List[str] = []
        buffer = ""

        for part in parts:
            if not part:
                continue

            if re.match(r"[。？！!?\n]+$", part):
                # Delimiter: flush previous buffer, start new buffer with delimiter
                if buffer:
                    result.append(buffer)
                buffer = part
            else:
                # Regular text
                if buffer:
                    result.append(buffer)
                buffer = part

        if buffer:
            result.append(None)

        return result if result else [text]
    
    xǁTextSplitterǁ_split_by_sentence__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTextSplitterǁ_split_by_sentence__mutmut_1': xǁTextSplitterǁ_split_by_sentence__mutmut_1, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_2': xǁTextSplitterǁ_split_by_sentence__mutmut_2, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_3': xǁTextSplitterǁ_split_by_sentence__mutmut_3, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_4': xǁTextSplitterǁ_split_by_sentence__mutmut_4, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_5': xǁTextSplitterǁ_split_by_sentence__mutmut_5, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_6': xǁTextSplitterǁ_split_by_sentence__mutmut_6, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_7': xǁTextSplitterǁ_split_by_sentence__mutmut_7, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_8': xǁTextSplitterǁ_split_by_sentence__mutmut_8, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_9': xǁTextSplitterǁ_split_by_sentence__mutmut_9, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_10': xǁTextSplitterǁ_split_by_sentence__mutmut_10, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_11': xǁTextSplitterǁ_split_by_sentence__mutmut_11, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_12': xǁTextSplitterǁ_split_by_sentence__mutmut_12, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_13': xǁTextSplitterǁ_split_by_sentence__mutmut_13, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_14': xǁTextSplitterǁ_split_by_sentence__mutmut_14, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_15': xǁTextSplitterǁ_split_by_sentence__mutmut_15, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_16': xǁTextSplitterǁ_split_by_sentence__mutmut_16, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_17': xǁTextSplitterǁ_split_by_sentence__mutmut_17, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_18': xǁTextSplitterǁ_split_by_sentence__mutmut_18, 
        'xǁTextSplitterǁ_split_by_sentence__mutmut_19': xǁTextSplitterǁ_split_by_sentence__mutmut_19
    }
    xǁTextSplitterǁ_split_by_sentence__mutmut_orig.__name__ = 'xǁTextSplitterǁ_split_by_sentence'

    def _split_level2(self, text: str, limit: int) -> List[str]:
        args = [text, limit]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTextSplitterǁ_split_level2__mutmut_orig'), object.__getattribute__(self, 'xǁTextSplitterǁ_split_level2__mutmut_mutants'), args, kwargs, self)

    def xǁTextSplitterǁ_split_level2__mutmut_orig(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_1(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) < 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_2(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 101:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_3(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text or "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_4(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "XX；XX" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_5(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_6(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "XX：XX" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_7(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_8(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(None, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_9(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, None)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_10(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_11(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, )
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_12(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = None
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_13(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(None)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_14(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = None
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_15(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(None)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_16(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = None
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_17(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = None
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_18(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = "XXXX"
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_19(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_20(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                break
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_21(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part not in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_22(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("XX；XX", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_23(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "XX：XX"):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_24(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer = part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_25(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer -= part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_26(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer or len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_27(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) - len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_28(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) >= limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_29(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(None)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_30(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = None
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_31(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = "XXXX"
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_32(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer = part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_33(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer -= part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_34(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(None)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_35(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = None
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_36(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) < limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_37(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(None)
            else:
                final_result.extend(self._split_level3(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_38(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(None)
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_39(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(None, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_40(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, None))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_41(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level2__mutmut_42(self, text: str, limit: int) -> List[str]:
        """
        Level 2 splitting: split by clause separators if text > 100 chars.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Only use clause splitting if text is significantly over 100 chars
        if len(text) <= 100:
            # Just return as-is, let level 3 handle it
            return [text]
        
        # Check if has clause separators
        if "；" not in text and "：" not in text:
            # No clause separators, go to level 3
            return self._split_level3(text, limit)
        
        # Split by clause separators
        pattern = re.compile(self.CLAUSE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("；", "："):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If segments are still too long, go to level 3
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, ))
        
        return final_result if final_result else [text]
    
    xǁTextSplitterǁ_split_level2__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTextSplitterǁ_split_level2__mutmut_1': xǁTextSplitterǁ_split_level2__mutmut_1, 
        'xǁTextSplitterǁ_split_level2__mutmut_2': xǁTextSplitterǁ_split_level2__mutmut_2, 
        'xǁTextSplitterǁ_split_level2__mutmut_3': xǁTextSplitterǁ_split_level2__mutmut_3, 
        'xǁTextSplitterǁ_split_level2__mutmut_4': xǁTextSplitterǁ_split_level2__mutmut_4, 
        'xǁTextSplitterǁ_split_level2__mutmut_5': xǁTextSplitterǁ_split_level2__mutmut_5, 
        'xǁTextSplitterǁ_split_level2__mutmut_6': xǁTextSplitterǁ_split_level2__mutmut_6, 
        'xǁTextSplitterǁ_split_level2__mutmut_7': xǁTextSplitterǁ_split_level2__mutmut_7, 
        'xǁTextSplitterǁ_split_level2__mutmut_8': xǁTextSplitterǁ_split_level2__mutmut_8, 
        'xǁTextSplitterǁ_split_level2__mutmut_9': xǁTextSplitterǁ_split_level2__mutmut_9, 
        'xǁTextSplitterǁ_split_level2__mutmut_10': xǁTextSplitterǁ_split_level2__mutmut_10, 
        'xǁTextSplitterǁ_split_level2__mutmut_11': xǁTextSplitterǁ_split_level2__mutmut_11, 
        'xǁTextSplitterǁ_split_level2__mutmut_12': xǁTextSplitterǁ_split_level2__mutmut_12, 
        'xǁTextSplitterǁ_split_level2__mutmut_13': xǁTextSplitterǁ_split_level2__mutmut_13, 
        'xǁTextSplitterǁ_split_level2__mutmut_14': xǁTextSplitterǁ_split_level2__mutmut_14, 
        'xǁTextSplitterǁ_split_level2__mutmut_15': xǁTextSplitterǁ_split_level2__mutmut_15, 
        'xǁTextSplitterǁ_split_level2__mutmut_16': xǁTextSplitterǁ_split_level2__mutmut_16, 
        'xǁTextSplitterǁ_split_level2__mutmut_17': xǁTextSplitterǁ_split_level2__mutmut_17, 
        'xǁTextSplitterǁ_split_level2__mutmut_18': xǁTextSplitterǁ_split_level2__mutmut_18, 
        'xǁTextSplitterǁ_split_level2__mutmut_19': xǁTextSplitterǁ_split_level2__mutmut_19, 
        'xǁTextSplitterǁ_split_level2__mutmut_20': xǁTextSplitterǁ_split_level2__mutmut_20, 
        'xǁTextSplitterǁ_split_level2__mutmut_21': xǁTextSplitterǁ_split_level2__mutmut_21, 
        'xǁTextSplitterǁ_split_level2__mutmut_22': xǁTextSplitterǁ_split_level2__mutmut_22, 
        'xǁTextSplitterǁ_split_level2__mutmut_23': xǁTextSplitterǁ_split_level2__mutmut_23, 
        'xǁTextSplitterǁ_split_level2__mutmut_24': xǁTextSplitterǁ_split_level2__mutmut_24, 
        'xǁTextSplitterǁ_split_level2__mutmut_25': xǁTextSplitterǁ_split_level2__mutmut_25, 
        'xǁTextSplitterǁ_split_level2__mutmut_26': xǁTextSplitterǁ_split_level2__mutmut_26, 
        'xǁTextSplitterǁ_split_level2__mutmut_27': xǁTextSplitterǁ_split_level2__mutmut_27, 
        'xǁTextSplitterǁ_split_level2__mutmut_28': xǁTextSplitterǁ_split_level2__mutmut_28, 
        'xǁTextSplitterǁ_split_level2__mutmut_29': xǁTextSplitterǁ_split_level2__mutmut_29, 
        'xǁTextSplitterǁ_split_level2__mutmut_30': xǁTextSplitterǁ_split_level2__mutmut_30, 
        'xǁTextSplitterǁ_split_level2__mutmut_31': xǁTextSplitterǁ_split_level2__mutmut_31, 
        'xǁTextSplitterǁ_split_level2__mutmut_32': xǁTextSplitterǁ_split_level2__mutmut_32, 
        'xǁTextSplitterǁ_split_level2__mutmut_33': xǁTextSplitterǁ_split_level2__mutmut_33, 
        'xǁTextSplitterǁ_split_level2__mutmut_34': xǁTextSplitterǁ_split_level2__mutmut_34, 
        'xǁTextSplitterǁ_split_level2__mutmut_35': xǁTextSplitterǁ_split_level2__mutmut_35, 
        'xǁTextSplitterǁ_split_level2__mutmut_36': xǁTextSplitterǁ_split_level2__mutmut_36, 
        'xǁTextSplitterǁ_split_level2__mutmut_37': xǁTextSplitterǁ_split_level2__mutmut_37, 
        'xǁTextSplitterǁ_split_level2__mutmut_38': xǁTextSplitterǁ_split_level2__mutmut_38, 
        'xǁTextSplitterǁ_split_level2__mutmut_39': xǁTextSplitterǁ_split_level2__mutmut_39, 
        'xǁTextSplitterǁ_split_level2__mutmut_40': xǁTextSplitterǁ_split_level2__mutmut_40, 
        'xǁTextSplitterǁ_split_level2__mutmut_41': xǁTextSplitterǁ_split_level2__mutmut_41, 
        'xǁTextSplitterǁ_split_level2__mutmut_42': xǁTextSplitterǁ_split_level2__mutmut_42
    }
    xǁTextSplitterǁ_split_level2__mutmut_orig.__name__ = 'xǁTextSplitterǁ_split_level2'

    def _split_level3(self, text: str, limit: int) -> List[str]:
        args = [text, limit]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTextSplitterǁ_split_level3__mutmut_orig'), object.__getattribute__(self, 'xǁTextSplitterǁ_split_level3__mutmut_mutants'), args, kwargs, self)

    def xǁTextSplitterǁ_split_level3__mutmut_orig(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_1(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = None
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_2(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(None)
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_3(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c not in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_4(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "XX，。、,XX")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_5(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_6(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = None
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_7(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(None)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_8(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = None
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_9(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(None)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_10(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = None
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_11(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = None
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_12(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = "XXXX"
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_13(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_14(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                break
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_15(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part not in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_16(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("XX，XX", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_17(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "XX。XX", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_18(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "XX、XX", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_19(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", "XX,XX"):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_20(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer = part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_21(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer -= part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_22(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer or len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_23(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) - len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_24(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) >= limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_25(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(None)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_26(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = None
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_27(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = "XXXX"
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_28(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer = part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_29(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer -= part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_30(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(None)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_31(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = None
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_32(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) < limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_33(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(None)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_34(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(None)
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_35(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(None, limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_36(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, None))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_37(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(limit))
        
        return final_result if final_result else [text]

    def xǁTextSplitterǁ_split_level3__mutmut_38(self, text: str, limit: int) -> List[str]:
        """
        Level 3 splitting: split by phrase separators.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        # Check if has phrase separators
        has_separators = any(c in text for c in "，。、,")
        
        if not has_separators:
            # No phrase separators, return as is (emergency split will handle)
            return [text]
        
        # Split by phrase separators
        pattern = re.compile(self.PHRASE_SEPARATORS)
        parts = pattern.split(text)
        
        result: List[str] = []
        buffer = ""
        
        for part in parts:
            if not part:
                continue
            
            if part in ("，", "。", "、", ","):
                # Attach separator to buffer
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        
        if buffer:
            result.append(buffer)
        
        # If still too long, emergency split
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, ))
        
        return final_result if final_result else [text]
    
    xǁTextSplitterǁ_split_level3__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTextSplitterǁ_split_level3__mutmut_1': xǁTextSplitterǁ_split_level3__mutmut_1, 
        'xǁTextSplitterǁ_split_level3__mutmut_2': xǁTextSplitterǁ_split_level3__mutmut_2, 
        'xǁTextSplitterǁ_split_level3__mutmut_3': xǁTextSplitterǁ_split_level3__mutmut_3, 
        'xǁTextSplitterǁ_split_level3__mutmut_4': xǁTextSplitterǁ_split_level3__mutmut_4, 
        'xǁTextSplitterǁ_split_level3__mutmut_5': xǁTextSplitterǁ_split_level3__mutmut_5, 
        'xǁTextSplitterǁ_split_level3__mutmut_6': xǁTextSplitterǁ_split_level3__mutmut_6, 
        'xǁTextSplitterǁ_split_level3__mutmut_7': xǁTextSplitterǁ_split_level3__mutmut_7, 
        'xǁTextSplitterǁ_split_level3__mutmut_8': xǁTextSplitterǁ_split_level3__mutmut_8, 
        'xǁTextSplitterǁ_split_level3__mutmut_9': xǁTextSplitterǁ_split_level3__mutmut_9, 
        'xǁTextSplitterǁ_split_level3__mutmut_10': xǁTextSplitterǁ_split_level3__mutmut_10, 
        'xǁTextSplitterǁ_split_level3__mutmut_11': xǁTextSplitterǁ_split_level3__mutmut_11, 
        'xǁTextSplitterǁ_split_level3__mutmut_12': xǁTextSplitterǁ_split_level3__mutmut_12, 
        'xǁTextSplitterǁ_split_level3__mutmut_13': xǁTextSplitterǁ_split_level3__mutmut_13, 
        'xǁTextSplitterǁ_split_level3__mutmut_14': xǁTextSplitterǁ_split_level3__mutmut_14, 
        'xǁTextSplitterǁ_split_level3__mutmut_15': xǁTextSplitterǁ_split_level3__mutmut_15, 
        'xǁTextSplitterǁ_split_level3__mutmut_16': xǁTextSplitterǁ_split_level3__mutmut_16, 
        'xǁTextSplitterǁ_split_level3__mutmut_17': xǁTextSplitterǁ_split_level3__mutmut_17, 
        'xǁTextSplitterǁ_split_level3__mutmut_18': xǁTextSplitterǁ_split_level3__mutmut_18, 
        'xǁTextSplitterǁ_split_level3__mutmut_19': xǁTextSplitterǁ_split_level3__mutmut_19, 
        'xǁTextSplitterǁ_split_level3__mutmut_20': xǁTextSplitterǁ_split_level3__mutmut_20, 
        'xǁTextSplitterǁ_split_level3__mutmut_21': xǁTextSplitterǁ_split_level3__mutmut_21, 
        'xǁTextSplitterǁ_split_level3__mutmut_22': xǁTextSplitterǁ_split_level3__mutmut_22, 
        'xǁTextSplitterǁ_split_level3__mutmut_23': xǁTextSplitterǁ_split_level3__mutmut_23, 
        'xǁTextSplitterǁ_split_level3__mutmut_24': xǁTextSplitterǁ_split_level3__mutmut_24, 
        'xǁTextSplitterǁ_split_level3__mutmut_25': xǁTextSplitterǁ_split_level3__mutmut_25, 
        'xǁTextSplitterǁ_split_level3__mutmut_26': xǁTextSplitterǁ_split_level3__mutmut_26, 
        'xǁTextSplitterǁ_split_level3__mutmut_27': xǁTextSplitterǁ_split_level3__mutmut_27, 
        'xǁTextSplitterǁ_split_level3__mutmut_28': xǁTextSplitterǁ_split_level3__mutmut_28, 
        'xǁTextSplitterǁ_split_level3__mutmut_29': xǁTextSplitterǁ_split_level3__mutmut_29, 
        'xǁTextSplitterǁ_split_level3__mutmut_30': xǁTextSplitterǁ_split_level3__mutmut_30, 
        'xǁTextSplitterǁ_split_level3__mutmut_31': xǁTextSplitterǁ_split_level3__mutmut_31, 
        'xǁTextSplitterǁ_split_level3__mutmut_32': xǁTextSplitterǁ_split_level3__mutmut_32, 
        'xǁTextSplitterǁ_split_level3__mutmut_33': xǁTextSplitterǁ_split_level3__mutmut_33, 
        'xǁTextSplitterǁ_split_level3__mutmut_34': xǁTextSplitterǁ_split_level3__mutmut_34, 
        'xǁTextSplitterǁ_split_level3__mutmut_35': xǁTextSplitterǁ_split_level3__mutmut_35, 
        'xǁTextSplitterǁ_split_level3__mutmut_36': xǁTextSplitterǁ_split_level3__mutmut_36, 
        'xǁTextSplitterǁ_split_level3__mutmut_37': xǁTextSplitterǁ_split_level3__mutmut_37, 
        'xǁTextSplitterǁ_split_level3__mutmut_38': xǁTextSplitterǁ_split_level3__mutmut_38
    }
    xǁTextSplitterǁ_split_level3__mutmut_orig.__name__ = 'xǁTextSplitterǁ_split_level3'

    def _emergency_split(self, text: str, limit: int) -> List[str]:
        args = [text, limit]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTextSplitterǁ_emergency_split__mutmut_orig'), object.__getattribute__(self, 'xǁTextSplitterǁ_emergency_split__mutmut_mutants'), args, kwargs, self)

    def xǁTextSplitterǁ_emergency_split__mutmut_orig(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_1(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) < limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_2(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = None
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_3(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = None
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_4(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(None)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_5(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) < limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_6(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(None)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_7(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = None
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_8(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = None
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_9(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = "XXXX"
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_10(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) - 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_11(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) - len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_12(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 2 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_13(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 < limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_14(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = None
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_15(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " - word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_16(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer - " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_17(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + "XX XX" + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_18(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(None)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_19(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) >= limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_20(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(None, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_21(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, None, limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_22(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), None):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_23(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_24(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_25(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), ):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_26(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(1, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_27(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = None
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_28(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i - limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_29(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(None)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_30(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = None
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_31(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = "XXXX"
                        else:
                            buffer = word
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_32(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = None
                
                if buffer:
                    result.append(buffer)
        
        return result if result else [text[:limit]]

    def xǁTextSplitterǁ_emergency_split__mutmut_33(self, text: str, limit: int) -> List[str]:
        """
        Emergency split: break by character count without regard for semantics.
        Used only when no other splitting method works.
        
        Args:
            text: Text to split
            limit: Maximum characters per segment
            
        Returns:
            List of segments
        """
        if len(text) <= limit:
            return [text]
        
        result: List[str] = []
        
        # Try to split at natural boundaries
        # First, try sentence endings
        segments = self._split_by_sentence(text)
        
        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                # Split by words (space-separated)
                words = seg.split()
                buffer = ""
                
                for word in words:
                    if len(buffer) + len(word) + 1 <= limit:
                        buffer = (buffer + " " + word).strip()
                    else:
                        if buffer:
                            result.append(buffer)
                        if len(word) > limit:
                            # Split long word by chars
                            for i in range(0, len(word), limit):
                                chunk = word[i:i+limit]
                                result.append(chunk)
                            buffer = ""
                        else:
                            buffer = word
                
                if buffer:
                    result.append(None)
        
        return result if result else [text[:limit]]
    
    xǁTextSplitterǁ_emergency_split__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTextSplitterǁ_emergency_split__mutmut_1': xǁTextSplitterǁ_emergency_split__mutmut_1, 
        'xǁTextSplitterǁ_emergency_split__mutmut_2': xǁTextSplitterǁ_emergency_split__mutmut_2, 
        'xǁTextSplitterǁ_emergency_split__mutmut_3': xǁTextSplitterǁ_emergency_split__mutmut_3, 
        'xǁTextSplitterǁ_emergency_split__mutmut_4': xǁTextSplitterǁ_emergency_split__mutmut_4, 
        'xǁTextSplitterǁ_emergency_split__mutmut_5': xǁTextSplitterǁ_emergency_split__mutmut_5, 
        'xǁTextSplitterǁ_emergency_split__mutmut_6': xǁTextSplitterǁ_emergency_split__mutmut_6, 
        'xǁTextSplitterǁ_emergency_split__mutmut_7': xǁTextSplitterǁ_emergency_split__mutmut_7, 
        'xǁTextSplitterǁ_emergency_split__mutmut_8': xǁTextSplitterǁ_emergency_split__mutmut_8, 
        'xǁTextSplitterǁ_emergency_split__mutmut_9': xǁTextSplitterǁ_emergency_split__mutmut_9, 
        'xǁTextSplitterǁ_emergency_split__mutmut_10': xǁTextSplitterǁ_emergency_split__mutmut_10, 
        'xǁTextSplitterǁ_emergency_split__mutmut_11': xǁTextSplitterǁ_emergency_split__mutmut_11, 
        'xǁTextSplitterǁ_emergency_split__mutmut_12': xǁTextSplitterǁ_emergency_split__mutmut_12, 
        'xǁTextSplitterǁ_emergency_split__mutmut_13': xǁTextSplitterǁ_emergency_split__mutmut_13, 
        'xǁTextSplitterǁ_emergency_split__mutmut_14': xǁTextSplitterǁ_emergency_split__mutmut_14, 
        'xǁTextSplitterǁ_emergency_split__mutmut_15': xǁTextSplitterǁ_emergency_split__mutmut_15, 
        'xǁTextSplitterǁ_emergency_split__mutmut_16': xǁTextSplitterǁ_emergency_split__mutmut_16, 
        'xǁTextSplitterǁ_emergency_split__mutmut_17': xǁTextSplitterǁ_emergency_split__mutmut_17, 
        'xǁTextSplitterǁ_emergency_split__mutmut_18': xǁTextSplitterǁ_emergency_split__mutmut_18, 
        'xǁTextSplitterǁ_emergency_split__mutmut_19': xǁTextSplitterǁ_emergency_split__mutmut_19, 
        'xǁTextSplitterǁ_emergency_split__mutmut_20': xǁTextSplitterǁ_emergency_split__mutmut_20, 
        'xǁTextSplitterǁ_emergency_split__mutmut_21': xǁTextSplitterǁ_emergency_split__mutmut_21, 
        'xǁTextSplitterǁ_emergency_split__mutmut_22': xǁTextSplitterǁ_emergency_split__mutmut_22, 
        'xǁTextSplitterǁ_emergency_split__mutmut_23': xǁTextSplitterǁ_emergency_split__mutmut_23, 
        'xǁTextSplitterǁ_emergency_split__mutmut_24': xǁTextSplitterǁ_emergency_split__mutmut_24, 
        'xǁTextSplitterǁ_emergency_split__mutmut_25': xǁTextSplitterǁ_emergency_split__mutmut_25, 
        'xǁTextSplitterǁ_emergency_split__mutmut_26': xǁTextSplitterǁ_emergency_split__mutmut_26, 
        'xǁTextSplitterǁ_emergency_split__mutmut_27': xǁTextSplitterǁ_emergency_split__mutmut_27, 
        'xǁTextSplitterǁ_emergency_split__mutmut_28': xǁTextSplitterǁ_emergency_split__mutmut_28, 
        'xǁTextSplitterǁ_emergency_split__mutmut_29': xǁTextSplitterǁ_emergency_split__mutmut_29, 
        'xǁTextSplitterǁ_emergency_split__mutmut_30': xǁTextSplitterǁ_emergency_split__mutmut_30, 
        'xǁTextSplitterǁ_emergency_split__mutmut_31': xǁTextSplitterǁ_emergency_split__mutmut_31, 
        'xǁTextSplitterǁ_emergency_split__mutmut_32': xǁTextSplitterǁ_emergency_split__mutmut_32, 
        'xǁTextSplitterǁ_emergency_split__mutmut_33': xǁTextSplitterǁ_emergency_split__mutmut_33
    }
    xǁTextSplitterǁ_emergency_split__mutmut_orig.__name__ = 'xǁTextSplitterǁ_emergency_split'

    def split_with_metadata(self, text: str) -> SplitResult:
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTextSplitterǁsplit_with_metadata__mutmut_orig'), object.__getattribute__(self, 'xǁTextSplitterǁsplit_with_metadata__mutmut_mutants'), args, kwargs, self)

    def xǁTextSplitterǁsplit_with_metadata__mutmut_orig(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_1(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = None
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_2(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(None)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_3(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = None
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_4(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(None)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_5(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = None
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_6(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars * len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_7(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 1
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_8(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=None,
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_9(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            total_segments=None,
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_10(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            avg_segment_length=None
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_11(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            total_segments=len(segments),
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_12(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            avg_segment_length=avg_length
        )

    def xǁTextSplitterǁsplit_with_metadata__mutmut_13(self, text: str) -> SplitResult:
        """
        Split text and return with metadata.
        
        Args:
            text: Input text to split
            
        Returns:
            SplitResult with segments and statistics
        """
        segments = self.split(text)
        
        total_chars = sum(len(s) for s in segments)
        avg_length = total_chars / len(segments) if segments else 0
        
        return SplitResult(
            segments=segments,
            total_segments=len(segments),
            )
    
    xǁTextSplitterǁsplit_with_metadata__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTextSplitterǁsplit_with_metadata__mutmut_1': xǁTextSplitterǁsplit_with_metadata__mutmut_1, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_2': xǁTextSplitterǁsplit_with_metadata__mutmut_2, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_3': xǁTextSplitterǁsplit_with_metadata__mutmut_3, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_4': xǁTextSplitterǁsplit_with_metadata__mutmut_4, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_5': xǁTextSplitterǁsplit_with_metadata__mutmut_5, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_6': xǁTextSplitterǁsplit_with_metadata__mutmut_6, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_7': xǁTextSplitterǁsplit_with_metadata__mutmut_7, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_8': xǁTextSplitterǁsplit_with_metadata__mutmut_8, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_9': xǁTextSplitterǁsplit_with_metadata__mutmut_9, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_10': xǁTextSplitterǁsplit_with_metadata__mutmut_10, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_11': xǁTextSplitterǁsplit_with_metadata__mutmut_11, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_12': xǁTextSplitterǁsplit_with_metadata__mutmut_12, 
        'xǁTextSplitterǁsplit_with_metadata__mutmut_13': xǁTextSplitterǁsplit_with_metadata__mutmut_13
    }
    xǁTextSplitterǁsplit_with_metadata__mutmut_orig.__name__ = 'xǁTextSplitterǁsplit_with_metadata'

    @staticmethod
    def should_split(text: str, max_chars: int) -> bool:
        """
        Determine if text should be split.
        
        Args:
            text: Text to check
            max_chars: Maximum characters before splitting
            
        Returns:
            True if text should be split
        """
        return len(text) > max_chars
