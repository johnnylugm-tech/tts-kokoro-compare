#!/usr/bin/env python3
"""
單元測試 - SSML Parser
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.ssml_parser import SSMLParser, ParsedSSML, SSMLSegment


class TestSSMLParser:
    """SSML 解析器測試"""

    def test_is_ssml_true(self):
        """SSML 標籤 → True"""
        assert SSMLParser.is_ssml("<speak>hello</speak>") is True
        assert SSMLParser.is_ssml("<prosody rate='1.2'>text</prosody>") is True
        assert SSMLParser.is_ssml("<break time='500ms'/>") is True

    def test_is_ssml_false(self):
        """一般文字 → False"""
        assert SSMLParser.is_ssml("你好世界") is False
        assert SSMLParser.is_ssml("no tags") is False

    def test_is_ssml_empty(self):
        """空字串 → False"""
        assert SSMLParser.is_ssml("") is False

    def test_parse_returns_parsedssml(self):
        """parse() 回傳 ParsedSSML dataclass"""
        result = SSMLParser.parse("純文字")
        assert isinstance(result, ParsedSSML)

    def test_parse_plain_text(self):
        """純文字 → 直接回傳"""
        text = "這是普通文字"
        result = SSMLParser.parse(text)
        assert result.input_text == text
        assert result.speed == 1.0
        assert result.is_ssml is False

    def test_parse_simple_speak(self):
        """基本 <speak> 標籤"""
        result = SSMLParser.parse("<speak>文字內容</speak>")
        assert "文字內容" in result.input_text
        assert result.is_ssml is True

    def test_parse_with_prosody(self):
        """prosody rate 解析（speed 在 segment 上）"""
        result = SSMLParser.parse("<speak><prosody rate='0.9'>文字</prosody></speak>")
        assert result.segments[0].speed == 0.9
        assert result.is_ssml is True

    def test_parse_with_break(self):
        """break time → pause_chars"""
        result = SSMLParser.parse("<speak>A<break time='500ms'/>B</speak>")
        # pause_chars should appear in segments
        assert any(s.pause_chars for s in result.segments)

    def test_parse_with_emphasis(self):
        """emphasis → speed > 1.0"""
        result = SSMLParser.parse("<speak><emphasis>重要</emphasis></speak>")
        assert result.is_ssml is True
        emp_segs = [s for s in result.segments if s.text.strip() == "重要"]
        assert emp_segs[0].speed > 1.0

    def test_parse_phoneme(self):
        """phoneme 標籤"""
        result = SSMLParser.parse("<speak><phoneme alphabet='ipa' ph='ni3'>文字</phoneme></speak>")
        assert result.is_ssml is True

    def test_break_time_medium(self):
        """break time 700ms → 句號"""
        result = SSMLParser.parse("<speak>A<break time='700ms'/>B</speak>")
        assert any(s.pause_chars == "。" for s in result.segments)

    def test_break_time_long(self):
        """break time 1500ms → 省略號"""
        result = SSMLParser.parse("<speak>A<break time='1500ms'/>B</speak>")
        assert any("。" in s.pause_chars for s in result.segments)

    def test_multiple_segments(self):
        """多段 SSML"""
        result = SSMLParser.parse(
            "<speak>"
            "<prosody rate='0.8'>慢速</prosody>"
            "<prosody rate='1.2'>快速</prosody>"
            "</speak>"
        )
        speeds = {s.speed for s in result.segments if s.text.strip()}
        assert 0.8 in speeds
        assert 1.2 in speeds

    def test_strip_comments(self):
        """註解移除"""
        result = SSMLParser.parse("<speak>文字<!-- 註解 -->結尾</speak>")
        assert "註解" not in result.input_text

    def test_strip_xml_declaration(self):
        """XML 宣告移除"""
        result = SSMLParser.parse('<?xml version="1.0"?><speak>內容</speak>')
        assert "<?xml" not in result.input_text

    def test_invalid_xml_fallback(self):
        """無效 XML → fallback"""
        result = SSMLParser.parse("這是普通<invalid>文字")
        assert isinstance(result.input_text, str)

    def test_voice_tag_parsing(self):
        """FR-02: <voice name="xxx"> → 切換音色"""
        result = SSMLParser.parse('<speak><voice name="zf_yunxi">切換音色</voice></speak>')
        assert result.is_ssml is True
        # Check that voice attribute is set on the segment
        voice_segments = [s for s in result.segments if s.text.strip() == "切換音色"]
        assert len(voice_segments) > 0
        assert voice_segments[0].voice == "zf_yunxi"

    def test_voice_tag_multiple_switches(self):
        """多段 voice 切換"""
        result = SSMLParser.parse(
            '<speak>'
            '<voice name="zf_xiaoxiao">第一段</voice>'
            '<voice name="af_heart">第二段</voice>'
            '</speak>'
        )
        assert result.is_ssml is True
        segments_with_voice = [s for s in result.segments if s.voice is not None]
        assert len(segments_with_voice) >= 2

    def test_voice_tag_in_prosody(self):
        """voice 標籤在 prosody 內"""
        result = SSMLParser.parse(
            '<speak>'
            '<prosody rate="0.9">'
            '<voice name="zf_yunxi">語速和音色切換</voice>'
            '</prosody>'
            '</speak>'
        )
        assert result.is_ssml is True
        voice_segments = [s for s in result.segments if s.voice == "zf_yunxi"]
        assert len(voice_segments) > 0

    def test_voice_tag_attribute_alias(self):
        """voice 標籤也支援 voice= 屬性"""
        result = SSMLParser.parse('<speak><voice voice="af_heart">另一種音色</voice></speak>')
        assert result.is_ssml is True
        voice_segments = [s for s in result.segments if s.voice == "af_heart"]
        assert len(voice_segments) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
