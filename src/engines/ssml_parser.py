"""SSML Parser - handles Speech Synthesis Markup Language parsing."""

import re
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any
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
        elif value < 500:
            return "，"
        elif value < 1000:
            return "。"
        elif value < 2000:
            return "。。。"
        else:
            return "......"

    @classmethod
    def _process_element(cls, element: ET.Element, default_speed: float = 1.0, depth: int = 0) -> List[SSMLSegment]:
        """
        Recursively process an XML element and its children.
        
        Args:
            element: XML element to process
            default_speed: Default speech speed
            depth: recursion depth for debugging
            
        Returns:
            List of SSMLSegment objects
        """
        segments: List[SSMLSegment] = []
        current_speed = default_speed
        
        # Get text content from the element itself (before any children)
        if element.text:
            text_content = element.text.strip()
            if text_content:
                segments.append(SSMLSegment(text=text_content, speed=current_speed))
        
        for child in element:
            tag_lower = child.tag.lower()
            
            if tag_lower == "break":
                # Handle break element
                time_attr = child.get("time", "")
                pause_chars = cls._parse_time_to_chars(time_attr)
                
                if pause_chars:
                    # Create a pause segment
                    segments.append(SSMLSegment(text="", pause_chars=pause_chars, speed=current_speed))
            
            elif tag_lower == "prosody":
                # Handle prosody element
                rate_attr = child.get("rate", None)
                
                # Parse speed adjustment
                if rate_attr:
                    try:
                        # rate can be "slow", "fast", "medium" or multiplier like "0.9", "1.2"
                        if rate_attr in ("slow", "fast", "medium"):
                            speed_map = {"slow": 0.8, "medium": 1.0, "fast": 1.2}
                            current_speed = speed_map.get(rate_attr, default_speed)
                        else:
                            current_speed = float(rate_attr)
                    except ValueError:
                        logger.warning(f"Invalid prosody rate: {rate_attr}")
                        current_speed = default_speed
                
                # Warn about unsupported attributes
                if child.get("pitch"):
                    logger.warning("pitch attribute not supported, ignoring")
                if child.get("volume"):
                    logger.warning("volume attribute not supported, ignoring")
                
                # Process children with adjusted speed
                child_segments = cls._process_element(child, current_speed, depth + 1)
                segments.extend(child_segments)
            
            elif tag_lower == "emphasis":
                # Handle emphasis element
                level_attr = child.get("level", "moderate")
                
                # Adjust speed based on emphasis level
                if level_attr == "strong":
                    emphasis_speed = current_speed * 1.15
                elif level_attr == "moderate":
                    emphasis_speed = current_speed * 1.1
                elif level_attr == "none":
                    emphasis_speed = current_speed
                else:
                    emphasis_speed = current_speed * 1.1
                
                # Process children with emphasis
                child_segments = cls._process_element(child, emphasis_speed, depth + 1)
                segments.extend(child_segments)
            
            elif tag_lower == "phoneme":
                # Preserve phoneme content (IPA notation)
                phoneme_text = child.text or ""
                if phoneme_text:
                    segments.append(SSMLSegment(text=phoneme_text, speed=current_speed))
            
            elif tag_lower == "voice":
                # Handle voice element - switch to specified voice
                voice_name = child.get("name") or child.get("voice") or None
                
                # Process children with potentially different voice
                child_segments = cls._process_element(child, current_speed, depth + 1)
                for seg in child_segments:
                    seg.voice = voice_name
                segments.extend(child_segments)
            
            elif tag_lower == "speak":
                # Root element, process children
                child_segments = cls._process_element(child, default_speed, depth + 1)
                segments.extend(child_segments)
            
            else:
                # Unknown tag, extract text content
                if child.text:
                    segments.append(SSMLSegment(text=child.text.strip(), speed=current_speed))
            
            # Handle tail text (text after the child element)
            if child.tail and child.tail.strip():
                tail_text = child.tail.strip()
                if tail_text:
                    segments.append(SSMLSegment(text=tail_text, speed=current_speed))
        
        return segments

    @classmethod
    def parse(cls, ssml_string: str) -> ParsedSSML:
        """
        Parse SSML string into structured data.
        
        Args:
            ssml_string: SSML markup string
            
        Returns:
            ParsedSSML object with parsed content
        """
        if not ssml_string or not ssml_string.strip():
            return ParsedSSML(input_text="", is_ssml=False)
        
        # Check if actually SSML
        if not cls.is_ssml(ssml_string):
            return ParsedSSML(input_text=ssml_string, is_ssml=False)
        
        try:
            # Preprocess: remove XML declaration and comments
            cleaned = cls._remove_xml_declaration(ssml_string)
            cleaned = cls._remove_comments(cleaned)
            
            # Wrap in speak tag if not present
            cleaned_stripped = cleaned.strip()
            if not cleaned_stripped.lower().startswith("<speak"):
                # Find first tag
                first_tag_match = re.match(r"<(\w+)", cleaned_stripped)
                if first_tag_match:
                    tag_name = first_tag_match.group(1)
                    cleaned = f"<speak>{cleaned}</speak>"
                else:
                    cleaned = f"<speak>{cleaned}</speak>"
            
            # Parse XML
            root = ET.fromstring(cleaned)
            
            # Check root element
            if root.tag.lower() != "speak":
                logger.warning(f"Unexpected root element: {root.tag}, expected <speak>")
                return ParsedSSML(input_text=ssml_string, is_ssml=False)
            
            # Extract global attributes
            global_speed = 1.0
            global_voice = root.get("voice") or None
            
            # Process the speak element
            segments = cls._process_element(root, global_speed)
            
            # Combine all text segments
            combined_text = ""
            for seg in segments:
                combined_text += seg.text + seg.pause_chars
            
            return ParsedSSML(
                input_text=combined_text.strip(),
                speed=global_speed,
                voice=global_voice,
                segments=segments,
                is_ssml=True
            )
            
        except ET.ParseError as e:
            logger.warning(f"SSML parsing failed, falling back to plain text: {e}")
            return ParsedSSML(input_text=ssml_string, is_ssml=False)
        except Exception as e:
            logger.error(f"Unexpected error parsing SSML: {e}")
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
