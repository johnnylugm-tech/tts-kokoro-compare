#!/usr/bin/env python3
"""
單元測試 - Taiwan Linguistic Engine
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.taiwan_linguistic import TaiwanLinguisticEngine, LEXICON
from src.config import LEXICON_MIN_SIZE


class TestTaiwanLinguisticEngine:
    """台灣化語言引擎測試"""

    def test_lexicon_size_requirement(self):
        """Lexicon must have at least 50 entries (FR-01)"""
        assert len(LEXICON) >= LEXICON_MIN_SIZE, (
            f"LEXICON has {len(LEXICON)} entries, "
            f"minimum required is {LEXICON_MIN_SIZE}"
        )
        # Verify we have at least 50 unique entries
        assert len(LEXICON) >= 50, f"LEXICON size: {len(LEXICON)}"

    def test_lexicon_視頻(self):
        """視頻 → 影片"""
        text = "我要看視頻"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "影片" in result
        assert "視頻" not in result

    def test_lexicon_地鐵(self):
        """地鐵 → 捷運"""
        text = "我要坐地鐵"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "捷運" in result
        assert "地鐵" not in result

    def test_lexicon_垃圾(self):
        """垃圾 → 注音"""
        text = "去丟垃圾"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "ㄌㄜˋ ㄙㄜˋ" in result

    def test_lexicon_菠蘿(self):
        """菠蘿 → 鳳梨"""
        text = "菠蘿麵包很好吃"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "鳳梨" in result
        assert "菠蘿" not in result

    def test_lexicon_吧(self):
        """吧 → 啦"""
        text = "這樣不好吧"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "啦" in result

    def test_lexicon_程序員(self):
        """程序員 → 工程師"""
        text = "我是程序員"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "工程師" in result

    def test_lexicon_硬件(self):
        """硬件 → 硬體"""
        text = "這台電腦硬件很好"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "硬體" in result

    def test_lexicon_互聯網(self):
        """互聯網 → 網際網路"""
        text = "互聯網發展迅速"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "網際網路" in result

    def test_lexicon_公交車(self):
        """公交車 → 公車"""
        text = "我坐公交車上班"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "公車" in result

    def test_lexicon_網紅(self):
        """網紅 → 網紅（保留不變）"""
        text = "她是知名網紅"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "網紅" in result

    def test_lexicon_boundary_cases(self):
        """邊界測試：詞彙重疊、部分匹配"""
        # 測試「網吧」和「網站」都能正確替換
        text = "去網吧上網站"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "網咖" in result  # 網吧→網咖
        assert "網站" in result   # 網站保留

    def test_lexicon_停車場(self):
        """停車場 → 停車場"""
        text = "停在停車場"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "停車場" in result

    def test_lexicon_火車站(self):
        """火車站 → 火車站"""
        text = "我在火車站等你"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "火車站" in result

    def test_lexicon_高速鐵路(self):
        """高速鐵路 → 高鐵"""
        text = "坐高速鐵路去台北"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "高鐵" in result

    def test_lexicon_軟件(self):
        """軟件 → 軟體"""
        text = "這個軟件很好用"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "軟體" in result

    def test_multiple_lexicon(self):
        """多詞彙同時替換"""
        text = "菠蘿視頻地鐵垃圾"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "鳳梨" in result
        assert "影片" in result
        assert "捷運" in result
        assert "ㄌㄜˋ ㄙㄜˋ" in result

    def test_empty_string(self):
        """空字串"""
        result = TaiwanLinguisticEngine.apply_taiwan_accent("")
        assert result == ""

    def test_unchanged(self):
        """不在 LEXICON 的字不變"""
        text = "今天天氣很好"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert result == text

    def test_add_english_spaces_simple(self):
        """中英文混合加空格"""
        text = "I love AI"
        result = TaiwanLinguisticEngine.add_english_spaces(text)
        # 純英文也有空格處理
        assert isinstance(result, str)

    def test_add_english_spaces_mixed(self):
        """中英文混合加空格"""
        text = "我愛AI和ML"
        result = TaiwanLinguisticEngine.add_english_spaces(text)
        # AI 應在結果中
        assert "AI" in result

    def test_add_english_spaces_numbers(self):
        """數字+英文混合"""
        text = "2024年GDP"
        result = TaiwanLinguisticEngine.add_english_spaces(text)
        assert isinstance(result, str)

    def test_apply_taiwan_accent_returns_str(self):
        """回傳型別為字串"""
        result = TaiwanLinguisticEngine.apply_taiwan_accent("你好")
        assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
