"""Text Splitter - intelligent text segmentation for TTS."""
# Copyright (c) 2026 Johnny Lu. Licensed under MIT License.

import re
import logging
from typing import List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


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
        """
        Initialize text splitter.

        Args:
            max_chars: Maximum characters per segment
            optimal_range: Optimal character range for segments (min, max)
        """
        self.max_chars = max_chars
        self.optimal_min, self.optimal_max = optimal_range

    def split(self, text: str, max_chars: Optional[int] = None) -> List[str]:
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

    def split_semantic(self, text: str, max_chars: Optional[int] = None) -> List[str]:
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

    def _split_by_sentence(self, text: str) -> List[str]:
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

    def _split_level2(self, text: str, limit: int) -> List[str]:
        """Level 2: split by clause separators if text > 100 chars."""
        if len(text) <= 100:
            return [text]

        if "；" not in text and "：" not in text:
            return self._split_level3(text, limit)

        return self._split_level2_by_clause(text, limit)

    def _split_level2_by_clause(self, text: str, limit: int) -> List[str]:
        """Core clause-splitting logic."""
        parts = re.compile(self.CLAUSE_SEPARATORS).split(text)
        result = self._collect_clause_parts(parts, limit)
        return self._finalize_segments(result, limit)

    def _collect_clause_parts(self, parts: list, limit: int) -> List[str]:
        """Collect clause parts into segments."""
        result: List[str] = []
        buffer = ""
        for part in parts:
            if not part:
                continue
            if part in ("；", "："):
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        if buffer:
            result.append(buffer)
        return result

    def _finalize_segments(self, result: List[str], limit: int) -> List[str]:
        """Finalize segments, escalating oversized ones."""
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._split_level3(seg, limit))
        return final_result if final_result else result

    def _split_level3(self, text: str, limit: int) -> List[str]:
        """Level 3: split by phrase separators."""
        has_separators = any(c in text for c in "，。、,")
        if not has_separators:
            return [text]

        return self._split_level3_by_phrase(text, limit)

    def _split_level3_by_phrase(self, text: str, limit: int) -> List[str]:
        """Core phrase-splitting logic."""
        parts = re.compile(self.PHRASE_SEPARATORS).split(text)
        result = self._collect_phrase_parts(parts, limit)
        return self._finalize_phrase_segments(result, limit)

    def _collect_phrase_parts(self, parts: list, limit: int) -> List[str]:
        """Collect phrase parts into segments."""
        result: List[str] = []
        buffer = ""
        for part in parts:
            if not part:
                continue
            if part in ("，", "。", "、", ","):
                buffer += part
            else:
                if buffer and len(buffer) + len(part) > limit:
                    result.append(buffer)
                    buffer = ""
                buffer += part
        if buffer:
            result.append(buffer)
        return result

    def _finalize_phrase_segments(self, result: List[str], limit: int) -> List[str]:
        """Finalize phrase segments, escalating oversized ones."""
        final_result: List[str] = []
        for seg in result:
            if len(seg) <= limit:
                final_result.append(seg)
            else:
                final_result.extend(self._emergency_split(seg, limit))
        return final_result if final_result else result

    def _emergency_split(self, text: str, limit: int) -> List[str]:
        """Emergency split: break by character count without regard for semantics."""
        if len(text) <= limit:
            return [text]

        segments = self._split_by_sentence(text)
        result: List[str] = []

        for seg in segments:
            if len(seg) <= limit:
                result.append(seg)
            else:
                result.extend(self._emergency_split_by_words(seg, limit))

        return result if result else [text[:limit]]

    def _emergency_split_by_words(self, text: str, limit: int) -> List[str]:
        """Split a too-long segment by words."""
        words = text.split()
        result: List[str] = []
        buffer = ""

        for word in words:
            if len(buffer) + len(word) + 1 <= limit:
                buffer = (buffer + " " + word).strip()
            else:
                if buffer:
                    result.append(buffer)
                if len(word) > limit:
                    for i in range(0, len(word), limit):
                        result.append(word[i:i+limit])
                    buffer = ""
                else:
                    buffer = word

        if buffer:
            result.append(buffer)

        return result

    def split_with_metadata(self, text: str) -> SplitResult:
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
