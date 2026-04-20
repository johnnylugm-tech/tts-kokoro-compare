#!/usr/bin/env python3
"""
單元測試 - CLI Tool (FR-07)
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.cli import parse_args, read_input, synthesize, main_async


class TestCLIArguments:
    """CLI 參數解析測試 (FR-07)"""

    def test_parse_basic_input(self):
        """基本文字輸入"""
        with patch("sys.argv", ["tts-v610", "-i", "你好世界", "-o", "output.mp3"]):
            args = parse_args()
            assert args.input == "你好世界"
            assert args.output == "output.mp3"

    def test_parse_voice_blend(self):
        """音色混合配方"""
        with patch("sys.argv", ["tts-v610", "-i", "測試", "-v", "zf_xiaoxiao(0.8)+af_heart(0.2)", "-o", "out.mp3"]):
            args = parse_args()
            assert args.voice == "zf_xiaoxiao(0.8)+af_heart(0.2)"

    def test_parse_ssml_flag(self):
        """SSML 模式"""
        with patch("sys.argv", ["tts-v610", "--ssml", "-i", "<speak>文字</speak>", "-o", "out.mp3"]):
            args = parse_args()
            assert args.ssml is True
            assert "<speak>" in args.input

    def test_parse_file_input(self):
        """檔案輸入模式"""
        with patch("sys.argv", ["tts-v610", "--file", "input.txt", "-o", "output/"]):
            args = parse_args()
            assert args.file == "input.txt"
            assert args.output == "output/"

    def test_parse_speed(self):
        """語速參數"""
        with patch("sys.argv", ["tts-v610", "-i", "快速", "-s", "1.5", "-o", "out.mp3"]):
            args = parse_args()
            assert args.speed == 1.5

    def test_parse_wav_format(self):
        """WAV 格式"""
        with patch("sys.argv", ["tts-v610", "-i", "測試", "-f", "wav", "-o", "out.wav"]):
            args = parse_args()
            assert args.format == "wav"

    def test_parse_backend_url(self):
        """自訂後端 URL"""
        with patch("sys.argv", ["tts-v610", "-i", "測", "--backend", "http://custom:9999/v1", "-o", "out.mp3"]):
            args = parse_args()
            assert args.backend == "http://custom:9999/v1"

    def test_parse_defaults(self):
        """預設值檢查"""
        with patch("sys.argv", ["tts-v610", "-i", "測試", "-o", "out.mp3"]):
            args = parse_args()
            assert args.voice == "zf_xiaoxiao"
            assert args.speed == 1.0
            assert args.format == "mp3"
            assert args.ssml is False


class TestCLIInputReading:
    """CLI 輸入讀取測試"""

    def test_read_input_from_arg(self):
        """從 CLI 參數讀取"""
        args = MagicMock()
        args.input = "測試文字"
        args.file = None
        result = read_input(args)
        assert result == "測試文字"

    def test_read_input_from_file(self, tmp_path):
        """從檔案讀取"""
        test_file = tmp_path / "input.txt"
        test_file.write_text("檔案內容", encoding="utf-8")
        
        args = MagicMock()
        args.input = None
        args.file = str(test_file)
        
        result = read_input(args)
        assert result == "檔案內容"

    def test_read_input_file_not_found(self):
        """檔案不存在"""
        args = MagicMock()
        args.input = None
        args.file = "/nonexistent/file.txt"
        
        with pytest.raises(FileNotFoundError):
            read_input(args)

    def test_read_input_empty_input(self):
        """空白輸入：is not None 所以回傳空字串"""
        args = MagicMock()
        args.input = ""
        args.file = None

        # empty string is not None → returns "" directly
        result = read_input(args)
        assert result == ""



class TestSynthesize:
    """合成邏輯測試"""

    @pytest.mark.asyncio
    async def test_synthesize_plain_text(self):
        """一般文字合成"""
        mock_engine = AsyncMock()
        mock_engine.synthesize_text.return_value = b"fake_audio_data"
        
        result = await synthesize(mock_engine, "測試", "zf_xiaoxiao", 1.0, False)
        
        mock_engine.synthesize_text.assert_called_once()
        assert result == b"fake_audio_data"

    @pytest.mark.asyncio
    async def test_synthesize_ssml(self):
        """SSML 模式合成"""
        mock_engine = AsyncMock()
        mock_engine.synthesize_ssml.return_value = b"ssml_audio"
        
        ssml = "<speak><prosody rate='0.9'>測試</prosody></speak>"
        result = await synthesize(mock_engine, ssml, "zf_xiaoxiao", 1.0, True)
        
        mock_engine.synthesize_ssml.assert_called_once()
        assert result == b"ssml_audio"

    @pytest.mark.asyncio
    async def test_synthesize_empty_result(self):
        """空音訊結果 → main_async 會在 caller 層處理，不在 synthesize() 拋異常"""
        mock_engine = AsyncMock()
        mock_engine.synthesize_text.return_value = b""
        # synthesize() 本身不拋異常，回傳 b""
        # caller (main_async) 會檢查並回傳錯誤碼 1
        result = await synthesize(mock_engine, "測", "zf_xiaoxiao", 1.0, False)
        assert result == b""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
