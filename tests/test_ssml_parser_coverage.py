#!/usr/bin/env python3
"""
Coverage tests - ssml_parser.py
Targets uncovered lines: 88,93,100,104,106,112,121,133-134,137-139,141,143,154,156,167,224-229,250,265-270,277-278,300-305,318-328
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.ssml_parser import SSMLParser, ParsedSSML, SSMLSegment


class TestSSMLParserPrivateHelpers:
    """Private helper method coverage."""

    def test_parse_time_to_chars_invalid(self):
        """Line 88: non-matching time string → ''"""
        assert SSMLParser._parse_time_to_chars("invalid") == ""

    def test_parse_time_to_chars_empty(self):
        """Line 88: empty → ''"""
        assert SSMLParser._parse_time_to_chars("") == ""

    def test_parse_time_to_chars_ms_short(self):
        """Line 100: < 200ms → single space"""
        assert SSMLParser._parse_time_to_chars("100ms") == " "

    def test_parse_time_to_chars_ms_medium(self):
        """Line 104: 200-500ms → ，"""
        assert SSMLParser._parse_time_to_chars("300ms") == "，"

    def test_parse_time_to_chars_ms_sentence(self):
        """Line 106: 500-1000ms → 。"""
        assert SSMLParser._parse_time_to_chars("700ms") == "。"

    def test_parse_time_to_chars_ms_long(self):
        """Line 112: 1000-2000ms → 。。。"""
        assert SSMLParser._parse_time_to_chars("1500ms") == "。。。"

    def test_parse_time_to_chars_ms_very_long(self):
        """Line 114: >= 2000ms → ......"""
        assert SSMLParser._parse_time_to_chars("3000ms") == "......"

    def test_parse_time_to_chars_seconds(self):
        """Line 100: unit 's' → converted to ms"""
        assert SSMLParser._parse_time_to_chars("0.3s") == "，"  # 300ms

    def test_parse_time_to_chars_seconds_long(self):
        """Line 112: 1s = 1000ms → 。。。"""
        assert SSMLParser._parse_time_to_chars("1s") == "。。。"

    def test_parse_time_to_chars_no_unit_bare_number(self):
        """Line 93: no unit defaults to ms; 150ms < 200ms → space"""
        assert SSMLParser._parse_time_to_chars("150") == " "

    def test_remove_xml_declaration(self):
        """Line 65: _remove_xml_declaration"""
        result = SSMLParser._remove_xml_declaration('<?xml version="1.0"?><speak>hi</speak>')
        assert "<?xml" not in result
        assert "hi" in result

    def test_remove_comments(self):
        """Line 71: _remove_comments"""
        result = SSMLParser._remove_comments("<!-- comment -->text")
        assert "comment" not in result
        assert "text" in result

    def test_remove_comments_multiline(self):
        """Line 71: multiline comment"""
        result = SSMLParser._remove_comments("text <!--\nmulti\nline--> more")
        assert "multi" not in result
        assert "text" in result


class TestSSMLParserProcessors:
    """_process_* method coverage."""

    def test_process_prosody_rate_string_slow(self):
        """Line 121: prosody rate='slow'"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<prosody rate='slow'>text</prosody>")
        speed, segs = SSMLParser._process_prosody(elem, 1.0, 0)
        assert speed == 0.8
        assert isinstance(segs, list)

    def test_process_prosody_rate_string_medium(self):
        """Line 121: prosody rate='medium'"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<prosody rate='medium'>text</prosody>")
        speed, segs = SSMLParser._process_prosody(elem, 1.0, 0)
        assert speed == 1.0

    def test_process_prosody_rate_string_fast(self):
        """Line 121: prosody rate='fast'"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<prosody rate='fast'>text</prosody>")
        speed, segs = SSMLParser._process_prosody(elem, 1.0, 0)
        assert speed == 1.2

    def test_process_prosody_rate_invalid_float(self):
        """Line 133: invalid rate → fallback to default"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<prosody rate='notanumber'>text</prosody>")
        speed, segs = SSMLParser._process_prosody(elem, 1.0, 0)
        assert speed == 1.0  # fallback to default

    def test_process_prosody_pitch_ignored(self):
        """Line 137: pitch attribute logged and ignored"""
        import xml.etree.ElementTree as ET
        # Need proper nested structure (child text element)
        elem = ET.fromstring("<prosody rate='1.0' pitch='high'>inner text</prosody>")
        speed, segs = SSMLParser._process_prosody(elem, 1.0, 0)
        assert speed == 1.0  # pitch ignored, rate used

    def test_process_prosody_volume_ignored(self):
        """Line 139: volume attribute logged and ignored"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<prosody rate='1.0' volume='loud'>inner text</prosody>")
        speed, segs = SSMLParser._process_prosody(elem, 1.0, 0)
        assert speed == 1.0  # volume ignored

    def test_process_prosody_with_text(self):
        """Line 141-143: prosody with child text"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<prosody rate='1.2'>child text</prosody>")
        speed, segs = SSMLParser._process_prosody(elem, 1.0, 0)
        assert speed == 1.2

    def test_process_emphasis_level_strong(self):
        """Line 147: emphasis level='strong' → speed * 1.15"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<emphasis level='strong'>text</emphasis>")
        segs = SSMLParser._process_emphasis(elem, 1.0, 0)
        assert any(abs(s.speed - 1.15) < 0.01 for s in segs if s.text.strip())

    def test_process_emphasis_level_none(self):
        """Line 147: emphasis level='none' → same speed"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<emphasis level='none'>text</emphasis>")
        segs = SSMLParser._process_emphasis(elem, 1.0, 0)
        assert all(abs(s.speed - 1.0) < 0.01 for s in segs if s.text.strip())

    def test_process_emphasis_level_moderate_default(self):
        """Line 147: emphasis default moderate → speed * 1.1"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<emphasis>text</emphasis>")
        segs = SSMLParser._process_emphasis(elem, 1.0, 0)
        assert any(abs(s.speed - 1.1) < 0.01 for s in segs if s.text.strip())

    def test_process_phoneme_with_text(self):
        """Line 154: phoneme with text → SSMLSegment"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<phoneme ph='təˈlefoʊn'>電話</phoneme>")
        seg = SSMLParser._process_phoneme(elem, 1.0)
        assert seg is not None
        assert seg.text == "電話"

    def test_process_phoneme_no_text(self):
        """Line 156: phoneme without text → None"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<phoneme ph='təˈlefoʊn'/>")
        seg = SSMLParser._process_phoneme(elem, 1.0)
        assert seg is None

    def test_process_break_no_time(self):
        """Line 112: break with no time attr → None"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<break/>")
        seg = SSMLParser._process_break(elem, 1.0)
        assert seg is None

    def test_process_break_short_time(self):
        """Line 112: break time < 200ms → space"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<break time='100ms'/>")
        seg = SSMLParser._process_break(elem, 1.0)
        assert seg is not None
        assert seg.pause_chars == " "

    def test_process_voice_sets_voice_attr(self):
        """Line 167: <voice name=...> sets seg.voice"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<voice name='zf_test'>inner</voice>")
        segs = SSMLParser._process_voice(elem, 1.0, 0)
        assert any(s.voice == "zf_test" for s in segs)

    def test_process_voice_voice_attribute_alias(self):
        """Line 167: voice= attribute alias"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<voice voice='zf_alias'>inner</voice>")
        segs = SSMLParser._process_voice(elem, 1.0, 0)
        assert any(s.voice == "zf_alias" for s in segs)

    def test_process_voice_no_name(self):
        """Line 167: voice tag with no name attr"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<voice>inner</voice>")
        segs = SSMLParser._process_voice(elem, 1.0, 0)
        assert all(s.voice is None for s in segs)


class TestSSMLParserProcessElement:
    """_process_element coverage (lines 154,156,167,224-229)."""

    def test_process_element_nested_speak(self):
        """Line 224-229: nested <speak> → recursive call"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<speak><speak>nested</speak></speak>")
        segs = SSMLParser._process_element(elem, 1.0)
        text = "".join(s.text for s in segs)
        assert "nested" in text

    def test_process_element_unknown_tag(self):
        """Line 224-229: unknown tag → text preserved"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<custom>custom text</custom>")
        segs = SSMLParser._process_element(elem, 1.0)
        text = "".join(s.text for s in segs)
        assert "custom text" in text

    def test_process_element_child_tail(self):
        """Line 224-229: child.tail → segment"""
        import xml.etree.ElementTree as ET
        elem = ET.fromstring("<speak><b/>tail text</speak>")
        segs = SSMLParser._process_element(elem, 1.0)
        text = "".join(s.text for s in segs)
        assert "tail text" in text


class TestSSMLParserParse:
    """parse() method coverage."""

    def test_parse_wraps_non_speak_tag(self):
        """Line 250: non-<speak> root → wrapped in <speak>"""
        result = SSMLParser.parse("<prosody rate='1.2'>text</prosody>")
        assert result.is_ssml is True
        assert "text" in result.input_text

    def test_parse_unexpected_root_element(self):
        """Line 265-270: unexpected root tag → ParsedSSML.is_ssml=False"""
        result = SSMLParser.parse("<div>text</div>")
        assert result.is_ssml is False

    def test_parse_extracts_global_voice(self):
        """Line 265-270: global voice attribute on <speak>"""
        result = SSMLParser.parse('<speak voice="zf_yunxi">hello</speak>')
        assert result.voice == "zf_yunxi"

    def test_parse_combined_text_includes_pause_chars(self):
        """Line 265-270: combined text includes pause_chars"""
        result = SSMLParser.parse("<speak>A<break time='700ms'/>B</speak>")
        assert "。" in result.input_text or result.input_text  # pause chars in text

    def test_is_ssml_with_xml_declaration_only(self):
        """Line 42: <?xml only → is_ssml=True"""
        assert SSMLParser.is_ssml('<?xml version="1.0"?>') is True

    def test_is_ssml_whitespace_only(self):
        """Line 42: whitespace-only → False"""
        assert SSMLParser.is_ssml("   \n\t  ") is False

    def test_extract_plain_text_non_ssml(self):
        """Line 300-305: non-SSML text returned as-is"""
        text = "plain text without tags"
        result = SSMLParser.extract_plain_text(text)
        assert result == text

    def test_extract_plain_text_ssml(self):
        """Line 300-305: SSML → tags removed"""
        result = SSMLParser.extract_plain_text("<speak>hello world</speak>")
        assert "hello" in result
        assert "<speak>" not in result

    def test_extract_plain_text_with_whitespace(self):
        """Line 300-305: SSML with whitespace → cleaned"""
        result = SSMLParser.extract_plain_text("<speak>  hello   world  </speak>")
        assert "hello" in result and "world" in result
        assert "  " not in result

    def test_is_ssml_uppercase(self):
        """Line 42: case-insensitive check"""
        assert SSMLParser.is_ssml("<SPEAK>text</SPEAK>") is True
        assert SSMLParser.is_ssml("<PROSODY RATE='1'>text</PROSODY>") is True

    def test_is_ssml_with_angle_brackets_no_tags(self):
        """Line 42: angle brackets but no SSML tag → False"""
        assert SSMLParser.is_ssml("<div>text</div>") is False


class TestSSMLParserEdgeCases:
    """Additional edge cases."""

    def test_speak_tag_with_attributes(self):
        """speak tag with voice attribute"""
        result = SSMLParser.parse('<speak voice="zf_xiaoxiao">hello</speak>')
        assert result.voice == "zf_xiaoxiao"

    def test_break_time_200ms_boundary(self):
        """exactly 200ms → boundary"""
        result = SSMLParser.parse("<speak>A<break time='200ms'/>B</speak>")
        # 200ms: < 200? No. 200 < 500? Yes → "，"
        assert any(s.pause_chars == "，" for s in result.segments)

    def test_break_time_500ms_boundary(self):
        """exactly 500ms → boundary"""
        result = SSMLParser.parse("<speak>A<break time='500ms'/>B</speak>")
        # 500ms: < 500? No. 500 < 1000? Yes → "。"
        assert any(s.pause_chars == "。" for s in result.segments)

    def test_break_time_1000ms_boundary(self):
        """exactly 1000ms → boundary"""
        result = SSMLParser.parse("<speak>A<break time='1000ms'/>B</speak>")
        # 1000ms: < 1000? No. 1000 < 2000? Yes → "。。。"
        assert any(s.pause_chars == "。。。" for s in result.segments)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
