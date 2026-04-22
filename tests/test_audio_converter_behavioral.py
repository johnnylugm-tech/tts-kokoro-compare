"""Behavioral tests for audio_converter — designed to KILL mutations.

These tests verify actual behavior with mock subprocess,
so mutations that change logic will cause test failures.
"""

import pytest
import sys
import os
import importlib
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.audio_converter import (
    convert_mp3_to_wav,
    convert_wav_to_mp3,
    is_ffmpeg_available,
    get_audio_info,
)


class TestConvertMp3ToWav:
    """Mutations that change conversion logic should FAIL here."""

    def test_returns_true_on_success(self, tmp_path):
        """Mutation: if return True is removed → test FAILS"""
        input_file = tmp_path / "in.mp3"
        input_file.touch()
        output_file = tmp_path / "out.wav"
        with patch("src.audio_converter.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = convert_mp3_to_wav(str(input_file), str(output_file))
            assert result is True

    def test_returns_false_when_subprocess_fails(self, tmp_path):
        """Mutation: if returncode check is removed → test FAILS"""
        input_file = tmp_path / "in.mp3"
        input_file.touch()
        output_file = tmp_path / "out.wav"
        with patch("src.audio_converter.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            result = convert_mp3_to_wav(str(input_file), str(output_file))
            assert result is False  # This would FAIL if mutation removes the if check

    def test_returns_false_when_input_missing(self, tmp_path):
        """Mutation: if input exists check is removed → test FAILS"""
        result = convert_mp3_to_wav(
            str(tmp_path / "nonexistent.mp3"),
            str(tmp_path / "out.wav")
        )
        assert result is False

    def test_subprocess_called_with_correct_args(self, tmp_path):
        """Mutation: if ffmpeg args are changed → test FAILS"""
        input_file = tmp_path / "in.mp3"
        input_file.touch()
        output_file = tmp_path / "out.wav"
        with patch("src.audio_converter.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            convert_mp3_to_wav(str(input_file), str(output_file))
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert "-i" in args
            assert "-acodec" in args
            assert "pcm_s16le" in args

    def test_subprocess_not_called_when_input_missing(self, tmp_path):
        """Mutation: if input exists check is removed → test FAILS"""
        with patch("src.audio_converter.subprocess.run") as mock_run:
            convert_mp3_to_wav(
                str(tmp_path / "nonexistent.mp3"),
                str(tmp_path / "out.wav")
            )
            mock_run.assert_not_called()


class TestConvertWavToMp3:
    """Mutations in wav→mp3 should be caught here."""

    def test_returns_true_on_success(self, tmp_path):
        """Mutation: if return True removed → test FAILS"""
        input_file = tmp_path / "in.wav"
        input_file.touch()
        output_file = tmp_path / "out.mp3"
        with patch("src.audio_converter.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = convert_wav_to_mp3(str(input_file), str(output_file))
            assert result is True

    def test_returns_false_when_subprocess_fails(self, tmp_path):
        """Mutation: if returncode check removed → test FAILS"""
        input_file = tmp_path / "in.wav"
        input_file.touch()
        output_file = tmp_path / "out.mp3"
        with patch("src.audio_converter.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            result = convert_wav_to_mp3(str(input_file), str(output_file))
            assert result is False

    def test_custom_bitrate_passed_to_subprocess(self, tmp_path):
        """Mutation: if bitrate param changed → test FAILS"""
        input_file = tmp_path / "in.wav"
        input_file.touch()
        output_file = tmp_path / "out.mp3"
        with patch("src.audio_converter.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            convert_wav_to_mp3(str(input_file), str(output_file), bitrate="320k")
            args = mock_run.call_args[0][0]
            assert "320k" in args


class TestIsFFmpegAvailable:
    """Mutations that change availability check should FAIL here."""

    def test_returns_true_when_ffmpeg_present(self):
        """Mutation: if shutil.which result check inverted → test FAILS"""
        with patch("src.audio_converter.shutil.which", return_value="/usr/bin/ffmpeg"):
            importlib.reload(__import__('src.audio_converter'))
            from src.audio_converter import is_ffmpeg_available
            result = is_ffmpeg_available()
            assert result is True

    def test_returns_false_when_ffmpeg_missing(self):
        """Mutation: if shutil.which result inverted → test FAILS"""
        with patch("src.audio_converter.shutil.which", return_value=None):
            with patch("src.audio_converter.FFMPEG_PATH", None):
                importlib.reload(__import__('src.audio_converter'))
                from src.audio_converter import is_ffmpeg_available
                result = is_ffmpeg_available()
                assert result is False


class TestGetAudioInfo:
    """Mutations in json parsing should FAIL here."""

    def test_returns_none_when_ffprobe_missing(self, tmp_path):
        """Mutation: if ffprobe_path check removed → test FAILS"""
        with patch("src.audio_converter.shutil.which", return_value=None):
            result = get_audio_info(str(tmp_path / "test.wav"))
            assert result is None

    def test_returns_dict_with_correct_keys_on_success(self, tmp_path):
        """Mutation: if any field extraction removed → test FAILS"""
        with patch("src.audio_converter.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"format":{"format_name":"wav","duration":"1.5","bit_rate":"44100","size":"10000"},"streams":[]}'
            )
            info = get_audio_info(str(tmp_path / "test.wav"))
            assert info is not None
            assert info["format"] == "wav"
            assert info["duration"] == 1.5
            assert info["bitrate"] == "44100"

    def test_handles_missing_audio_stream(self, tmp_path):
        """Mutation: if audio_stream lookup fails → test FAILS"""
        with patch("src.audio_converter.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"format":{"format_name":"wav","duration":"1.0"},"streams":[]}'
            )
            info = get_audio_info(str(tmp_path / "test.wav"))
            assert info is not None
            assert info.get("codec") is None
            assert info.get("sample_rate") is None
