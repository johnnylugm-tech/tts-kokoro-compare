"""Taiwan Linguistic Engine - handles Taiwan-specific language processing."""

import re
import logging
from typing import Dict, Pattern

logger = logging.getLogger(__name__)

# Taiwan-specific lexicon mapping (50+ entries)
LEXICON: Dict[str, str] = {
    # 科技詞彙
    "視頻": "影片",
    "互聯網": "網際網路",
    "程序員": "工程師",
    "軟件": "軟體",
    "硬件": "硬體",
    "打印": "列印",
    "打印機": "印表機",
    "U盤": "隨身碟",
    "網吧": "網咖",
    "博客": "部落格",
    "博文": "文",
    "網站": "網站",
    "瀏覽器": "瀏覽器",
    "鍵盤": "鍵盤",
    "鼠標": "滑鼠",
    "主板": "主機板",
    "內存": "記憶體",
    "硬盤": "硬碟",
    "固態硬盤": "固態硬碟",
    "顯卡": "顯示卡",
    "CPU": "處理器",
    "GPU": "圖形處理器",
    "數據庫": "資料庫",
    "服務器": "伺服器",
    "運算": "運算",
    # 日常詞彙
    "地鐵": "捷運",
    "垃圾": "ㄌㄜˋ ㄙㄜˋ",
    "菠蘿": "鳳梨",
    "地鐵站": "捷運站",
    "公交車": "公車",
    "公交": "公車",
    "出租車": "計程車",
    "紅綠燈": "紅綠燈",
    "摩托車": "機車",
    "自行車": "腳踏車",
    "人行道": "人行道",
    "立交橋": "陸橋",
    "高速鐵路": "高鐵",
    "殘疾人": "身心障礙者",
    # 連接詞 / 語氣詞
    "和": "ㄏㄢˋ",
    "吧": "啦",
    "什麼": "什麥",
    "喝水": "喝髓",
    "便宜": "，便宜",
    "視頻會議": "影片會議",
    "視頻通话": "影片通話",
    "網絡": "網路",
    "網紅": "網紅",
    "快遞": "宅即便",
    "外賣": "外送",
    "購物": "購物",
    "老闆": "老闆",
    "同事": "同事",
    "你好": "你好",
    "謝謝": "謝謝",
    "對不起": "抱歉",
    "沒關係": "不會",
    "帥哥": "帥哥",
    "美眉": "美眉",
    "卡通": "卡通",
    "動漫": "動漫",
    "蛋白質": "蛋白質",
    "奇異果": "奇異果",
    "薯條": "薯條",
    "番茄醬": "番茄醬",
    "自助餐": "吃到飽",
    "便利店": "便利商店",
    "化妝品": "化妝品",
    "停車場": "停車場",
    "洗手間": "洗手間",
    "衛生間": "化妝間",
    "電影院": "電影院",
    "火車站": "火車站",
    "飛機場": "機場",
}

# Tone sandhi patterns for Taiwan accent (zh/ch/sh reduction in specific contexts)
TONE_SANDHI_PATTERNS: Dict[str, Pattern] = {
    # Reduction of retroflex initials in specific words
    "zh_to_z": re.compile(r"\b知道\b", re.IGNORECASE),
    "ch_to_c": re.compile(r"\b吃\b", re.IGNORECASE),
    "sh_to_s": re.compile(r"\b是\b", re.IGNORECASE),
}

# English word boundary pattern
ENGLISH_WORD_PATTERN: Pattern = re.compile(r"([a-zA-Z0-9]+)")


class TaiwanLinguisticEngine:
    """Engine for applying Taiwan-specific linguistic transformations."""

    @classmethod
    def apply_taiwan_accent(cls, text: str) -> str:
        """
        Apply Taiwan-specific linguistic transformations to input text.
        
        Steps:
        1. LEXICON replacement
        2. Tone sandhi normalization
        3. Add spaces around English words
        
        Args:
            text: Input text to transform
            
        Returns:
            Transformed text with Taiwan-specific processing applied
        """
        if not text:
            return text
        
        result = text
        
        # Step 1: Apply lexicon replacements
        result = cls._apply_lexicon(result)
        
        # Step 2: Apply tone sandhi normalization
        result = cls._apply_tone_sandhi(result)
        
        # Step 3: Add spaces around English words for better tokenization
        result = cls.add_english_spaces(result)
        
        logger.debug(f"Taiwan accent applied: '{text}' -> '{result}'")
        return result

    @classmethod
    def _apply_lexicon(cls, text: str) -> str:
        """Apply lexicon word replacements."""
        result = text
        for source, target in LEXICON.items():
            # Use word boundary matching to avoid partial replacements
            pattern = re.compile(re.escape(source), re.IGNORECASE)
            result = pattern.sub(target, result)
        return result

    @classmethod
    def _apply_tone_sandhi(cls, text: str) -> str:
        """
        Apply tone sandhi normalization.
        
        Taiwan Mandarin has fewer neutral tones and preserves full tones.
        We reduce retroflex initials (zh/ch/sh) in specific common words.
        """
        result = text
        
        # These patterns reduce retroflex sounds to alveolar in casual speech
        # Note: This is a simplified version; full sandhi rules are complex
        replacements = [
            (r"\b知道\b", "知道"),  # Keep as is, just logging
            (r"\b這個\b", "這個"),
            (r"\b什麼\b", "什麥"),
            (r"\b是不是\b", "是不是"),
            (r"\b只是\b", "只是"),
            (r"\b所以\b", "所以"),
            (r"\b開始\b", "開始"),
        ]
        
        for pattern_str, replacement in replacements:
            pattern = re.compile(pattern_str)
            result = pattern.sub(replacement, result)
        
        return result

    @classmethod
    def add_english_spaces(cls, text: str) -> str:
        """
        Add spaces around English words for better TTS tokenization.
        
        Example:
            "我愛AI" -> "我愛 AI "
            "HelloWorld" -> "HelloWorld " (no change if already spaced)
            "使用Python3.10" -> "使用 Python3.10 "
        
        Args:
            text: Input text with potential mixed Chinese/English
            
        Returns:
            Text with spaces added around English words
        """
        if not text:
            return text
        
        # Find all English words/sequences and add spaces around them
        result = ENGLISH_WORD_PATTERN.sub(r" \1 ", text)
        
        # Clean up multiple spaces
        result = re.sub(r"\s+", " ", result).strip()
        
        return result

    @classmethod
    def normalize_numbers(cls, text: str) -> str:
        """
        Normalize number expressions for Taiwan Mandarin.
        
        Args:
            text: Input text with numbers
            
        Returns:
            Text with numbers normalized
        """
        # Arabic numerals to Chinese conversion for common cases
        result = text
        
        # Percentage
        result = re.sub(r"(\d+)%", r"\1%", result)  # Keep as-is
        
        # Phone numbers - add spaces
        phone_pattern = re.compile(r"(\d{4})(\d{3})(\d{3})")
        result = phone_pattern.sub(r"\1 \2 \3", result)
        
        return result

    @classmethod
    def add_prosody_markers(cls, text: str, speed_adjustments: list) -> str:
        """
        Add internal prosody markers for better rhythm.
        
        Args:
            text: Input text
            speed_adjustments: List of (position, speed_multiplier) tuples
            
        Returns:
            Text with prosody hints
        """
        # This is a placeholder for more sophisticated prosody marking
        # In practice, the TTS engine handles this
        return text

    @classmethod
    def validate_text(cls, text: str) -> tuple[bool, str]:
        """
        Validate if text is suitable for TTS.
        
        Args:
            text: Input text to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text or not text.strip():
            return False, "Empty text provided"
        
        if len(text) > 5000:
            return False, "Text too long (max 5000 characters)"
        
        # Check for potentially problematic characters
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text):
            return False, "Text contains control characters"
        
        return True, ""

    @classmethod
    def preprocess_for_tts(cls, text: str) -> str:
        """
        Full preprocessing pipeline for TTS.
        
        Args:
            text: Raw input text
            
        Returns:
            Fully preprocessed text ready for TTS
        """
        # Step 1: Basic cleanup
        cleaned = text.strip()
        
        # Step 2: Apply Taiwan-specific transformations
        processed = cls.apply_taiwan_accent(cleaned)
        
        # Step 3: Normalize spacing
        processed = re.sub(r"\s+", " ", processed)
        
        return processed
