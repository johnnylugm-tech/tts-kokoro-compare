"""Test audio converter with mocked ffmpeg."""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.audio_converter import (
    get_ffmpeg_path,
    convert_mp3_to_wav,
    convert_wav_to_mp3,
    is_ffmpeg_available,
    get_audio_info,
)
from unittest.mock import patch


class TestAudioConverterHelpers:
    def test_is_ffmpeg_available(self):
        """Check ffmpeg availability status."""
        available = is_ffmpeg_available()
        assert isinstance(available, bool)

    def test_get_ffmpeg_path_returns_string(self):
        """get_ffmpeg_path returns a string path."""
        path = get_ffmpeg_path()
        assert isinstance(path, str)
        assert len(path) > 0

    def test_get_ffmpeg_path_consistent(self):
        """get_ffmpeg_path is deterministic."""
        p1 = get_ffmpeg_path()
        p2 = get_ffmpeg_path()
        assert p1 == p2


class TestConvertMp3ToWav:
    def test_convert_nonexistent_file_returns_false(self, tmp_path):
        """Missing input returns False."""
        result = convert_mp3_to_wav(
            str(tmp_path / "nonexistent.mp3"),
            str(tmp_path / "output.wav"),
        )
        assert result is False

    def test_convert_wav_to_mp3_nonexistent_returns_false(self, tmp_path):
        """Missing input returns False."""
        result = convert_wav_to_mp3(
            str(tmp_path / "nonexistent.wav"),
            str(tmp_path / "output.mp3"),
        )
        assert result is False


class TestAudioConverterIntegration:
    def test_module_imports_correctly(self):
        """All public functions are importable."""
        from src.audio_converter import (
            get_ffmpeg_path,
            is_ffmpeg_available,
            convert_mp3_to_wav,
            convert_wav_to_mp3,
            get_audio_info,
        )
        assert callable(get_ffmpeg_path)
        assert callable(is_ffmpeg_available)
        assert callable(convert_mp3_to_wav)
        assert callable(convert_wav_to_mp3)

    def test_get_audio_info_nonexistent_returns_none(self, tmp_path):
        """Nonexistent file → None."""
        info = get_audio_info(str(tmp_path / "does_not_exist.wav"))
        assert info is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])