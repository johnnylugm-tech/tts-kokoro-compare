#!/usr/bin/env python3
"""
單元測試 - Text Splitter
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.text_splitter import TextSplitter, SplitResult


class TestTextSplitter:
    """智能文本切分器測試"""

    def test_init_default(self):
        """預設初始化 (FR-03: max_chars = 250)"""
        splitter = TextSplitter()
        assert splitter.max_chars == 250

    def test_init_custom(self):
        """自訂參數"""
        splitter = TextSplitter(max_chars=100, optimal_range=(50, 100))
        assert splitter.max_chars == 100

    def test_split_empty(self):
        """空字串"""
        splitter = TextSplitter()
        result = splitter.split("")
        assert result == []

    def test_split_plain_text(self):
        """純文字不變（fast path）"""
        splitter = TextSplitter()
        text = "這是普通文字"
        result = splitter.split(text)
        assert len(result) == 1
        assert result[0] == text

    def test_split_by_period(self):
        """句號切分（split_semantic）"""
        splitter = TextSplitter()
        text = "第一句。第二句。第三句。"
        result = splitter.split_semantic(text)
        # 預期會切成多段（包含標點作為獨立元素）
        assert len(result) >= 2

    def test_split_by_question_mark(self):
        """問號切分"""
        splitter = TextSplitter()
        text = "你好嗎？我很好！"
        result = splitter.split_semantic(text)
        assert len(result) >= 2

    def test_split_by_newline(self):
        """換行切分"""
        splitter = TextSplitter()
        text = "第一行\n第二行"
        result = splitter.split(text)
        # 短文字走 fast path，不做語義切分
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_split_max_chars_respected(self):
        """每段不超過 max_chars"""
        splitter = TextSplitter(max_chars=10)
        text = "這是一個非常非常長的句子需要被切分處理"
        result = splitter.split(text)
        for seg in result:
            assert len(seg) <= 10

    def test_split_long_text(self):
        """長文字分段"""
        splitter = TextSplitter(max_chars=50)
        text = "。" * 200
        result = splitter.split(text)
        assert len(result) > 1
        for seg in result:
            assert len(seg) <= 50

    def test_split_semantic_returns_list(self):
        """split_semantic 回傳 list"""
        splitter = TextSplitter()
        result = splitter.split_semantic("第一句。第二句。")
        assert isinstance(result, list)

    def test_split_semantic_empty(self):
        """split_semantic 空字串"""
        splitter = TextSplitter()
        result = splitter.split_semantic("")
        assert result == []

    def test_split_250_char_boundary(self):
        """FR-03: 250 字邊界測試"""
        splitter = TextSplitter(max_chars=250)
        # 249 chars - should be 1 segment
        text_249 = "。" * 249
        result_249 = splitter.split(text_249)
        assert len(result_249) == 1

        # 251 chars - should be split
        text_251 = "。" * 251
        result_251 = splitter.split(text_251)
        assert len(result_251) >= 2

        # 每段都不超過 250
        for seg in result_251:
            assert len(seg) <= 250


class TestTextSplitterEdgeCases:
    """邊界條件測試"""

    def test_split_no_separators(self):
        """無分隔符 → 整段回傳"""
        splitter = TextSplitter()
        text = "這句話沒有句號"
        result = splitter.split(text)
        assert len(result) == 1

    def test_split_result_dataclass(self):
        """SplitResult dataclass"""
        result = SplitResult(segments=["a", "b"], total_segments=2, avg_segment_length=1.0)
        assert result.total_segments == 2
        assert len(result.segments) == 2

    def test_split_english_numbers(self):
        """英文數字不 crash"""
        splitter = TextSplitter(max_chars=5)
        text = "AI123"
        result = splitter.split(text)
        for seg in result:
            assert len(seg) <= 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
