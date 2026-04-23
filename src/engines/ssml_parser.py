"""SSML Parser - handles Speech Synthesis Markup Language parsing."""
# Copyright (c) 2026 Johnny Lu. Licensed under MIT License.

import re
import logging
import xml.etree.ElementTree as ET  # nosec - SSML is trusted internal format
from typing import List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class SSMLSegment:
    """Represents a segment of parsed SSML content."""

    text: str = ""
    speed: float = 1.0
    pause_chars: str = ""
    voice: Optional[str] = None


@dataclass
class ParsedSSML:
    """Result of SSML parsing."""

    input_text: str = ""
    speed: float = 1.0
    voice: Optional[str] = None
    segments: List[SSMLSegment] = field(default_factory=list)
    is_ssml: bool = False


class SSMLParser:
    """Parser for SSML (Speech Synthesis Markup Language)."""

    # Supported SSML tags
    SUPPORTED_TAGS = {"speak", "break", "prosody", "emphasis", "phoneme", "voice"}

    # Tags that should be removed but content preserved
    PASS_THROUGH_TAGS = {"phoneme"}

    @staticmethod
    def is_ssml(text: str) -> bool:
        """
        Check if text contains SSML markup.

        Args:
            text: Input text to check

        Returns:
            True if text contains SSML tags
        """
        if not text:
            return False

        text_lower = text.lower().strip()
        return (
            "<speak" in text_lower or
            "<prosody" in text_lower or
            "<emphasis" in text_lower or
            "<break" in text_lower or
            "<?xml" in text_lower
        )

    @staticmethod
    def _remove_xml_declaration(text: str) -> str:
        """Remove XML declaration from SSML."""
        pattern = re.compile(r"<\?xml[^?]*\?>", re.IGNORECASE | re.DOTALL)
        return pattern.sub("", text)

    @staticmethod
    def _remove_comments(text: str) -> str:
        """Remove XML comments from SSML."""
        pattern = re.compile(r"<!--.*?-->", re.DOTALL)
        return pattern.sub("", text)

    @staticmethod
    def _parse_time_to_chars(time_str: str) -> str:
        """
        Convert SSML time attribute to pause characters.

        Args:
            time_str: Time string like "500ms", "1s", "0.5s"

        Returns:
            String of pause characters (e.g., "..." for longer pauses)
        """
        if not time_str:
            return ""

        # Extract numeric value
        match = re.match(r"(\d+(?:\.\d+)?)\s*(ms|s)?", time_str, re.IGNORECASE)
        if not match:
            return ""

        value = float(match.group(1))
        unit = match.group(2) or "ms"

        # Convert to milliseconds
        if unit.lower() == "s":
            value *= 1000

        # Map duration to pause characters
        if value < 200:
            return " "
        if value < 500:
            return "，"
        if value < 1000:
            return "。"
        if value < 2000:
            return "。。。"
        return "......"

    @classmethod
    def _process_break(cls, element: ET.Element, current_speed: float) -> SSMLSegment | None:
        """Process <break> element."""
        time_attr = element.get("time", "")
        pause_chars = cls._parse_time_to_chars(time_attr)
        if pause_chars:
            return SSMLSegment(text="", pause_chars=pause_chars, speed=current_speed)
        return None

    @classmethod
    def _process_prosody(
        cls, element: ET.Element, default_speed: float, depth: int
    ) -> tuple[float, List[SSMLSegment]]:
        """Process <prosody> element. Returns (adjusted_speed, child_segments)."""
        rate_attr = element.get("rate", None)
        current_speed = default_speed
        if rate_attr:
            try:
                if rate_attr in ("slow", "fast", "medium"):
                    speed_map = {"slow": 0.8, "medium": 1.0, "fast": 1.2}
                    current_speed = speed_map.get(rate_attr, default_speed)
                else:
                    current_speed = float(rate_attr)
            except ValueError:
                logger.warning("Invalid prosody rate: %s", rate_attr)
                current_speed = default_speed
        if element.get("pitch"):
            logger.warning("pitch attribute not supported, ignoring")
        if element.get("volume"):
            logger.warning("volume attribute not supported, ignoring")
        child_segments = cls._process_element(element, current_speed, depth + 1)
        return current_speed, child_segments

    @classmethod
    def _process_emphasis(
        cls, element: ET.Element, current_speed: float, depth: int
    ) -> List[SSMLSegment]:
        """Process <emphasis> element."""
        level_attr = element.get("level", "moderate")
        if level_attr == "strong":
            emphasis_speed = current_speed * 1.15
        elif level_attr == "none":
            emphasis_speed = current_speed
        else:
            emphasis_speed = current_speed * 1.1
        return cls._process_element(element, emphasis_speed, depth + 1)

    @classmethod
    def _process_phoneme(cls, element: ET.Element, current_speed: float) -> SSMLSegment | None:
        """Process <phoneme> element."""
        phoneme_text = element.text or ""
        if phoneme_text:
            return SSMLSegment(text=phoneme_text, speed=current_speed)
        return None

    @classmethod
    def _process_voice(
        cls, element: ET.Element, current_speed: float, depth: int
    ) -> List[SSMLSegment]:
        """Process <voice> element."""
        voice_name = element.get("name") or element.get("voice") or None
        child_segments = cls._process_element(element, current_speed, depth + 1)
        for seg in child_segments:
            seg.voice = voice_name
        return child_segments


    @classmethod
    def _handle_break_tag(cls, child, current_speed) -> List[SSMLSegment]:
        """Handle <break> tag."""
        seg = cls._process_break(child, current_speed)
        return [seg] if seg else []

    @classmethod
    def _handle_prosody_tag(cls, child, current_speed, depth) -> List[SSMLSegment]:
        """Handle <prosody> tag."""
        _, child_segments = cls._process_prosody(child, current_speed, depth)
        return child_segments

    @classmethod
    def _handle_emphasis_tag(cls, child, current_speed, depth) -> List[SSMLSegment]:
        """Handle <emphasis> tag."""
        return cls._process_emphasis(child, current_speed, depth)

    @classmethod
    def _handle_phoneme_tag(cls, child, current_speed) -> List[SSMLSegment]:
        """Handle <phoneme> tag."""
        seg = cls._process_phoneme(child, current_speed)
        return [seg] if seg else []

    @classmethod
    def _handle_voice_tag(cls, child, current_speed, depth) -> List[SSMLSegment]:
        """Handle <voice> tag."""
        return cls._process_voice(child, current_speed, depth)

    @classmethod
    def _handle_speak_tag(cls, child, default_speed, depth) -> List[SSMLSegment]:
        """Handle <speak> tag."""
        return cls._process_element(child, default_speed, depth + 1)

    @classmethod
    def _handle_generic_tag(cls, child, current_speed) -> List[SSMLSegment]:
        """Handle unknown tags."""
        if child.text:
            return [SSMLSegment(text=child.text.strip(), speed=current_speed)]
        return []

    @classmethod
    def _dispatch_tag(cls, child, current_speed, default_speed, depth) -> List[SSMLSegment]:
        """Dispatch to appropriate tag handler."""
        tag_lower = child.tag.lower()
        if tag_lower == "break":
            return cls._handle_break_tag(child, current_speed)
        if tag_lower == "prosody":
            return cls._handle_prosody_tag(child, current_speed, depth)
        if tag_lower == "emphasis":
            return cls._handle_emphasis_tag(child, current_speed, depth)
        if tag_lower == "phoneme":
            return cls._handle_phoneme_tag(child, current_speed)
        if tag_lower == "voice":
            return cls._handle_voice_tag(child, current_speed, depth)
        if tag_lower == "speak":
            return cls._handle_speak_tag(child, default_speed, depth)
        return cls._handle_generic_tag(child, current_speed)

    @classmethod
    def _process_element(cls, element: ET.Element, default_speed: float = 1.0, depth: int = 0) -> List[SSMLSegment]:
        """Recursively process an XML element and its children."""
        segments: List[SSMLSegment] = []
        current_speed = default_speed

        if element.text:
            text_content = element.text.strip()
            if text_content:
                segments.append(SSMLSegment(text=text_content, speed=current_speed))

        for child in element:
            tag_segments = cls._dispatch_tag(child, current_speed, default_speed, depth)
            segments.extend(tag_segments)

            if child.tail and child.tail.strip():
                tail_text = child.tail.strip()
                if tail_text:
                    segments.append(SSMLSegment(text=tail_text, speed=current_speed))

        return segments




    @classmethod
    def _preprocess_ssml(cls, ssml_string: str) -> str:
        """Preprocess SSML: remove declaration/comments, wrap in speak tag."""
        cleaned = cls._remove_xml_declaration(ssml_string)
        cleaned = cls._remove_comments(cleaned)
        cleaned_stripped = cleaned.strip()
        if not cleaned_stripped.lower().startswith("<speak"):
            first_tag_match = re.match(r"<(\w+)", cleaned_stripped)
            if first_tag_match:
                _ = first_tag_match.group(1)
                cleaned = f"<speak>{cleaned}</speak>"
            else:
                cleaned = f"<speak>{cleaned}</speak>"
        return cleaned

    @classmethod
    def parse(cls, ssml_string: str) -> ParsedSSML:
        """Parse SSML string into structured data."""
        if not ssml_string or not ssml_string.strip():
            return ParsedSSML(input_text="", is_ssml=False)

        if not cls.is_ssml(ssml_string):
            return ParsedSSML(input_text=ssml_string, is_ssml=False)

        try:
            cleaned = cls._preprocess_ssml(ssml_string)
            root = ET.fromstring(cleaned)  # nosec - SSML is internal format, already validated

            if root.tag.lower() != "speak":
                logger.warning("Unexpected root element: %s, expected <speak>", root.tag)
                return ParsedSSML(input_text=ssml_string, is_ssml=False)

            global_speed = 1.0
            global_voice = root.get("voice") or None
            segments = cls._process_element(root, global_speed)

            combined_text = "".join(seg.text + seg.pause_chars for seg in segments)
            return ParsedSSML(
                input_text=combined_text.strip(),
                speed=global_speed,
                voice=global_voice,
                segments=segments,
                is_ssml=True
            )

        except ET.ParseError as e:
            logger.warning("SSML parsing failed, falling back to plain text: %s", e)
            return ParsedSSML(input_text=ssml_string, is_ssml=False)
        except (ValueError, OSError) as e:
            logger.error("Unexpected error parsing SSML: %s", e)
            return ParsedSSML(input_text=ssml_string, is_ssml=False)

    @classmethod
    def extract_plain_text(cls, ssml_string: str) -> str:
        """
        Extract plain text from SSML, removing all markup.

        Args:
            ssml_string: SSML markup string

        Returns:
            Plain text with all SSML tags removed
        """
        if not cls.is_ssml(ssml_string):
            return ssml_string

        # Remove all XML-like tags
        pattern = re.compile(r"<[^>]+>")
        result = pattern.sub(" ", ssml_string)

        # Clean up whitespace
        result = re.sub(r"\s+", " ", result).strip()

        return result
