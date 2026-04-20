#!/usr/bin/env python3
"""
整合測試 - Kokoro Taiwan Proxy
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.taiwan_linguistic import TaiwanLinguisticEngine
from src.engines.ssml_parser import SSMLParser
from src.engines.text_splitter import TextSplitter
from src.config import MODEL_MAP, DEFAULT_VOICE, KOKORO_BACKEND_URL


class TestIntegration:
    """端到端整合測試"""

    def test_ssml_to_taiwan_pipeline(self):
        """SSML → 台灣化 → 切分"""
        ssml = "<speak><prosody rate='0.9'>今天天氣很好</prosody></speak>"
        # 1. SSML 解析
        parsed = SSMLParser.parse(ssml)
        assert parsed.is_ssml is True
        assert parsed.segments[0].speed == 0.9
        # 2. 台灣化
        text = TaiwanLinguisticEngine.apply_taiwan_accent(parsed.input_text)
        assert isinstance(text, str)
        # 3. 切分
        splitter = TextSplitter()
        chunks = splitter.split(text)
        assert len(chunks) >= 1

    def test_model_mapping(self):
        """模型代號映射"""
        assert MODEL_MAP["tts-1"] == "kokoro"
        assert MODEL_MAP["tts-1-hd"] == "kokoro"
        assert "custom-gentle" in MODEL_MAP

    def test_taiwan_accent_full_text(self):
        """完整台灣化流程"""
        text = "我要坐地鐵去看視頻順便丟垃圾"
        result = TaiwanLinguisticEngine.apply_taiwan_accent(text)
        assert "捷運" in result
        assert "影片" in result
        assert "ㄌㄜˋ ㄙㄜˋ" in result

    def test_ssml_english_blending(self):
        """英文混合音色映射"""
        ssml = "<speak>I love AI</speak>"
        parsed = SSMLParser.parse(ssml)
        text = TaiwanLinguisticEngine.add_english_spaces(parsed.input_text)
        assert "AI" in text

    def test_config_defaults(self):
        """設定檔預設值"""
        assert "localhost:8880" in KOKORO_BACKEND_URL
        assert DEFAULT_VOICE == "zf_xiaoxiao"
        assert "tts-1" in MODEL_MAP

    def test_circuit_breaker_import(self):
        """斷路器可正常 import"""
        from src.middleware.circuit_breaker import CircuitBreaker, CircuitState
        cb = CircuitBreaker(threshold=3, timeout=10.0)
        assert cb.state == CircuitState.CLOSED

    def test_redis_cache_import(self):
        """Redis 快取可正常 import"""
        from src.cache.redis_cache import RedisCache
        assert RedisCache is not None

    def test_full_pipeline_ssml_to_segments(self):
        """完整流程：SSML → 解析 → 台灣化 → 切分"""
        ssml = "<speak><prosody rate='0.85'>我要坐地鐵去看視頻</prosody></speak>"
        # 解析
        parsed = SSMLParser.parse(ssml)
        assert parsed.segments[0].speed == 0.85
        # 台灣化
        tw = TaiwanLinguisticEngine.apply_taiwan_accent(parsed.input_text)
        assert "捷運" in tw
        assert "影片" in tw
        # 切分
        splitter = TextSplitter()
        chunks = splitter.split(tw)
        assert len(chunks) >= 1

    def test_models_pydantic(self):
        """Pydantic 模型可正常 import"""
        from src.models import SpeechRequest
        req = SpeechRequest(model="tts-1", input="測試")
        assert req.model == "tts-1"
        assert req.input == "測試"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
