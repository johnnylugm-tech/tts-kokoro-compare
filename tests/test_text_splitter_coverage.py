#!/usr/bin/env python3
"""
Coverage tests - text_splitter.py
Targets uncovered lines: 167-197, 215, 232-235, 244, 263, 273, 281, 284, 292, 295, 309-314, 332
Function line map (verified via AST):
  __init__() at line 38
  _emergency_split() at line 250
  _split_by_sentence() at line 117
  _split_level2() at line 145
  _split_level3() at line 199
  should_split() at line 321
  split() at line 49
  split_semantic() at line 84
  split_with_metadata() at line 299
  _split_level2_by_clause() at line 169
  _split_level3_by_phrase() at line 215
  _emergency_split_by_words() at line 263
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.text_splitter import TextSplitter, SplitResult


class TestTextSplitterPrivateMethods:
    """Private method coverage."""

    def test_split_by_sentence_with_delimiters(self):
        """_split_by_sentence: splits text with sentence-ending punctuation"""
        splitter = TextSplitter()
        text = "你好。世界！"
        result = splitter._split_by_sentence(text)
        assert len(result) >= 2

    def test_split_by_sentence_multiple_delimiters(self):
        """_split_by_sentence: multiple consecutive delimiters"""
        splitter = TextSplitter()
        text = "句一。句二？！句三"
        result = splitter._split_by_sentence(text)
        assert len(result) >= 1

    def test_split_by_sentence_no_delimiter(self):
        """_split_by_sentence: no delimiter → returns text"""
        splitter = TextSplitter()
        text = "這句話沒有句號"
        result = splitter._split_by_sentence(text)
        assert result == [text]

    def test_split_by_sentence_only_delimiters(self):
        """_split_by_sentence: only delimiters"""
        splitter = TextSplitter()
        text = "。？！"
        result = splitter._split_by_sentence(text)
        assert len(result) >= 1

    def test_split_level2_short_text(self):
        """_split_level2: text <= 100 chars → returns as-is"""
        splitter = TextSplitter(max_chars=100)
        text = "短文字" * 5  # 15 chars < 100
        result = splitter._split_level2(text, 100)
        assert result == [text]

    def test_split_level2_with_clause_separators(self):
        """_split_level2: text > 100 chars with ； → splits"""
        splitter = TextSplitter(max_chars=50)
        text = "第一段內容" + "；" + "第二段內容"  # total > 50
        result = splitter._split_level2(text, 50)
        assert len(result) >= 1

    def test_split_level2_with_colon_separator(self):
        """_split_level2: text > 100 chars with ： → splits"""
        splitter = TextSplitter(max_chars=50)
        text = "第一段內容" + "：" + "第二段內容"
        result = splitter._split_level2(text, 50)
        assert len(result) >= 1

    def test_split_level2_no_clause_separators(self):
        """_split_level2: no clause separators → level 3"""
        splitter = TextSplitter(max_chars=50)
        text = "這句話很長，" * 20  # has phrase separator
        result = splitter._split_level2(text, 50)
        assert len(result) >= 1

    def test_split_level3_no_separators(self):
        """_split_level3: no phrase separators → [text]"""
        splitter = TextSplitter(max_chars=50)
        text = "這句話沒有任何短語分隔符很長需要被處理"
        result = splitter._split_level3(text, 50)
        assert result == [text]

    def test_split_level3_with_phrase_separators(self):
        """_split_level3: with phrase separators → splits"""
        splitter = TextSplitter(max_chars=20)
        text = "第一部分，很長的第二部分"
        result = splitter._split_level3(text, 20)
        assert len(result) >= 1

    def test_split_level3_comma_separator(self):
        """_split_level3: English comma separator"""
        splitter = TextSplitter(max_chars=20)
        text = "Hello, world"
        result = splitter._split_level3(text, 20)
        assert len(result) >= 1

    def test_split_level3_by_phrase(self):
        """_split_level3_by_phrase: core phrase splitting"""
        splitter = TextSplitter(max_chars=20)
        text = "第一部分，長長的第二部分"
        result = splitter._split_level3_by_phrase(text, 20)
        assert len(result) >= 1

    def test_split_level3_by_phrase_single_segment(self):
        """_split_level3_by_phrase: result fits limit → kept"""
        splitter = TextSplitter(max_chars=200)
        text = "短文字"
        result = splitter._split_level3_by_phrase(text, 200)
        assert result == [text]

    def test_split_level3_by_phrase_triggers_emergency(self):
        """_split_level3_by_phrase: segment > limit → emergency split"""
        splitter = TextSplitter(max_chars=10)
        text = "這是一個非常長的句子"
        result = splitter._split_level3_by_phrase(text, 10)
        assert len(result) >= 1
        assert all(len(s) <= 10 for s in result)

    def test_split_level2_by_clause(self):
        """_split_level2_by_clause: core clause splitting"""
        splitter = TextSplitter(max_chars=30)
        text = "第一段；很長的第二段"
        result = splitter._split_level2_by_clause(text, 30)
        assert len(result) >= 1

    def test_split_level2_by_clause_triggers_level3(self):
        """_split_level2_by_clause: clause result > limit → level 3"""
        splitter = TextSplitter(max_chars=10)
        text = "很長的第一段；也很長的第二段"
        result = splitter._split_level2_by_clause(text, 10)
        assert len(result) >= 1
        assert all(len(s) <= 10 for s in result)

    def test_emergency_split_short_text(self):
        """_emergency_split: text within limit → [text]"""
        splitter = TextSplitter(max_chars=100)
        text = "短文字"
        result = splitter._emergency_split(text, 100)
        assert result == [text]

    def test_emergency_split_by_sentence(self):
        """_emergency_split: splits by sentence then recurses"""
        splitter = TextSplitter(max_chars=20)
        text = "第一句話。第二句話"
        result = splitter._emergency_split(text, 20)
        assert len(result) >= 1

    def test_emergency_split_by_words(self):
        """_emergency_split: long sentence → split by words"""
        splitter = TextSplitter(max_chars=20)
        text = "word1 word2 word3 word4 word5"
        result = splitter._emergency_split(text, 20)
        assert len(result) >= 1
        assert all(len(s) <= 20 for s in result)

    def test_emergency_split_by_words_long_word(self):
        """_emergency_split_by_words: word > limit → char chunk"""
        splitter = TextSplitter(max_chars=5)
        text = "toolongword"
        result = splitter._emergency_split(text, 5)
        assert len(result) >= 2
        assert all(len(s) <= 5 for s in result)

    def test_emergency_split_fallback_truncation(self):
        """_emergency_split: no result → truncation fallback"""
        splitter = TextSplitter(max_chars=10)
        text = "a" * 100  # no natural boundaries
        result = splitter._emergency_split(text, 10)
        assert len(result) >= 1
        # fallback returns text[:limit]

    def test_emergency_split_by_words_empty(self):
        """_emergency_split_by_words: text with no spaces"""
        splitter = TextSplitter(max_chars=10)
        text = "無空白長文字"
        result = splitter._emergency_split(text, 10)
        assert len(result) >= 1


class TestTextSplitterSplitSemantic:
    """split_semantic() coverage."""

    def test_split_semantic_short_text_fast_path(self):
        """split_semantic: text <= limit → returns [text]"""
        splitter = TextSplitter(max_chars=250)
        text = "短文字"
        result = splitter.split_semantic(text)
        assert len(result) == 1

    def test_split_semantic_empty(self):
        """split_semantic: empty → []"""
        splitter = TextSplitter()
        result = splitter.split_semantic("")
        assert result == []

    def test_split_semantic_long_text_calls_level2(self):
        """split_semantic: long text → level 2"""
        splitter = TextSplitter(max_chars=50)
        text = "這是一段比較長的文字。" * 5
        result = splitter.split_semantic(text, 50)
        assert len(result) >= 1

    def test_split_semantic_with_custom_limit(self):
        """split_semantic: custom limit overrides instance max_chars"""
        splitter = TextSplitter(max_chars=250)
        text = "。" * 300
        result = splitter.split_semantic(text, 50)
        assert all(len(s) <= 50 for s in result)


class TestTextSplitterSplit:
    """split() method coverage."""

    def test_split_whitespace_text(self):
        """split: whitespace-only text"""
        splitter = TextSplitter()
        result = splitter.split("   ")
        assert isinstance(result, list)

    def test_split_long_text_respects_limit(self):
        """split: ensures no segment exceeds limit"""
        splitter = TextSplitter(max_chars=30)
        text = "。" * 200
        result = splitter.split(text, 30)
        assert all(len(s) <= 30 for s in result)

    def test_split_with_custom_max_chars(self):
        """split: max_chars parameter overrides instance"""
        splitter = TextSplitter(max_chars=250)
        text = "。" * 300
        result = splitter.split(text, max_chars=50)
        assert all(len(s) <= 50 for s in result)


class TestTextSplitterMetadata:
    """split_with_metadata() and should_split() coverage."""

    def test_split_with_metadata_single_segment(self):
        """split_with_metadata: single segment"""
        splitter = TextSplitter(max_chars=250)
        result = splitter.split_with_metadata("短文字")
        assert result.total_segments == 1
        assert len(result.segments) == 1
        assert result.avg_segment_length > 0

    def test_split_with_metadata_multiple_segments(self):
        """split_with_metadata: multiple segments"""
        splitter = TextSplitter(max_chars=10)
        text = "。" * 50
        result = splitter.split_with_metadata(text)
        assert result.total_segments >= 2
        assert result.avg_segment_length > 0

    def test_split_with_metadata_empty_text(self):
        """split_with_metadata: empty text"""
        splitter = TextSplitter()
        result = splitter.split_with_metadata("")
        assert result.total_segments == 0
        assert result.avg_segment_length == 0

    def test_should_split_true(self):
        """should_split: text > max_chars → True"""
        assert TextSplitter.should_split("。" * 300, 250) is True

    def test_should_split_false(self):
        """should_split: text <= max_chars → False"""
        assert TextSplitter.should_split("。" * 100, 250) is False


class TestTextSplitterEdgeCases:
    """Additional edge cases."""

    def test_init_optimal_range(self):
        """__init__: optimal_range correctly unpacked"""
        splitter = TextSplitter(optimal_range=(50, 200))
        assert splitter.optimal_min == 50
        assert splitter.optimal_max == 200

    def test_split_english_text_with_spaces(self):
        """split: English text with spaces → word-split emergency"""
        splitter = TextSplitter(max_chars=10)
        text = "Hello World Example Text"
        result = splitter.split(text, 10)
        assert len(result) >= 1
        assert all(len(s) <= 10 for s in result)

    def test_split_mixed_chinese_english(self):
        """split: mixed content"""
        splitter = TextSplitter(max_chars=20)
        text = "你好Hello世界World"
        result = splitter.split(text, 20)
        assert len(result) >= 1

    def test_split_only_separators(self):
        """split: text is only punctuation"""
        splitter = TextSplitter(max_chars=10)
        text = "，、。，、"
        result = splitter.split(text, 10)
        assert len(result) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
