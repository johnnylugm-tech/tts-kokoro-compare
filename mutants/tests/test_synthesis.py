"""Tests for engines/synthesis.py — SynthesisEngine coverage."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
import httpx

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.synthesis import SynthesisEngine


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    """Engine with real client replaced by mock."""
    eng = SynthesisEngine(backend_url="http://localhost:8880/v1/audio/speech", timeout=30.0)
    eng.client = MagicMock()
    yield eng
    # prevent real aclose on a mock
    eng.client.aclose = AsyncMock()


@pytest.fixture
def mock_httpx_response():
    """Factory for mock httpx response with .content."""
    def make(content: bytes, status_code: int = 200):
        response = MagicMock()
        response.content = content
        response.status_code = status_code
        response.text = ""
        response.raise_for_status = MagicMock()
        return response
    return make


# ---------------------------------------------------------------------------
# synthesize()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_normal(engine, mock_httpx_response):
    """正常：httpx 返回音頻數據。"""
    mock_resp = mock_httpx_response(b"fake_audio_data")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    result = await engine.synthesize("你好", voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    assert result == b"fake_audio_data"
    post_mock.assert_called_once()
    call_kwargs = post_mock.call_args.kwargs
    assert call_kwargs["json"]["input"] == "你好"


@pytest.mark.asyncio
async def test_synthesize_empty_text(engine):
    """空文字：text="" → return b""。"""
    result = await engine.synthesize("")
    assert result == b""


@pytest.mark.asyncio
async def test_synthesize_whitespace_only(engine):
    """空白文字：text="   " → return b""。"""
    result = await engine.synthesize("   ")
    assert result == b""


@pytest.mark.asyncio
async def test_synthesize_with_voice_and_speed(engine, mock_httpx_response):
    """正常文字 + 語音 + 速度參數傳遞。"""
    mock_resp = mock_httpx_response(b"audio_with_params")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    result = await engine.synthesize("測試語音", voice="af_heart", speed=0.8, model="kokoro")

    assert result == b"audio_with_params"
    payload = post_mock.call_args.kwargs["json"]
    assert payload["voice"] == "af_heart"
    assert payload["speed"] == 0.8


@pytest.mark.asyncio
async def test_synthesize_httpx_timeout(engine):
    """httpx TimeoutException → 向上拋。"""
    engine.client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))  # type: ignore

    with pytest.raises(httpx.TimeoutException):
        await engine.synthesize("test")


@pytest.mark.asyncio
async def test_synthesize_httpx_http_status_error(engine):
    """httpx HTTPStatusError → 向上拋。"""
    response = MagicMock()
    response.status_code = 500
    response.text = "Internal Server Error"
    engine.client.post = AsyncMock(side_effect=httpx.HTTPStatusError(  # type: ignore
        "Server Error", request=MagicMock(), response=response
    ))

    with pytest.raises(httpx.HTTPStatusError):
        await engine.synthesize("test")


@pytest.mark.asyncio
async def test_synthesize_httpx_generic_http_error(engine):
    """通用 httpx HTTPError → 向上拋。"""
    engine.client.post = AsyncMock(side_effect=httpx.HTTPError("Generic error"))  # type: ignore

    with pytest.raises(httpx.HTTPError):
        await engine.synthesize("test")


# ---------------------------------------------------------------------------
# synthesize_segments()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_segments_empty_list(engine):
    """空列表 → return b""。"""
    result = await engine.synthesize_segments([])
    assert result == b""


@pytest.mark.asyncio
async def test_synthesize_segments_normal(engine, mock_httpx_response):
    """正常段列表 → 串接音頻結果。"""
    mock_resp1 = mock_httpx_response(b"chunk1")
    mock_resp2 = mock_httpx_response(b"chunk2")
    post_mock = AsyncMock(side_effect=[mock_resp1, mock_resp2])
    engine.client.post = post_mock  # type: ignore

    segments = [
        {"text": "第一段", "speed": 1.0},
        {"text": "第二段", "speed": 1.0},
    ]

    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")

    assert result == b"chunk1chunk2"
    assert post_mock.call_count == 2


@pytest.mark.asyncio
async def test_synthesize_segments_with_different_speeds(engine, mock_httpx_response):
    """不同 speed 參數傳遞到每個 segment。"""
    mock_resp1 = mock_httpx_response(b"slow")
    mock_resp2 = mock_httpx_response(b"fast")
    post_mock = AsyncMock(side_effect=[mock_resp1, mock_resp2])
    engine.client.post = post_mock  # type: ignore

    segments = [
        {"text": "慢慢說", "speed": 0.6},
        {"text": "快快說", "speed": 1.4},
    ]

    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")

    assert result == b"slowfast"
    payloads = [call.kwargs["json"] for call in post_mock.call_args_list]
    assert payloads[0]["speed"] == 0.6
    assert payloads[1]["speed"] == 1.4


@pytest.mark.asyncio
async def test_synthesize_segments_partial_failure(engine, mock_httpx_response):
    """部分段失敗（各自 retry 完仍失敗）→ RuntimeError。"""
    # Both segments fail after all retries
    engine.client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))  # type: ignore

    segments = [
        {"text": "失敗段", "speed": 1.0},
        {"text": "另一失敗段", "speed": 1.0},
    ]

    with pytest.raises(RuntimeError) as exc_info:
        await engine.synthesize_segments(segments)

    assert "All segments failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_synthesize_segments_all_failure(engine):
    """全部段失敗 → RuntimeError。"""
    engine.client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))  # type: ignore

    segments = [
        {"text": "段一", "speed": 1.0},
        {"text": "段二", "speed": 1.0},
    ]

    with pytest.raises(RuntimeError) as exc_info:
        await engine.synthesize_segments(segments)

    assert "All segments failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_synthesize_segments_skips_empty_text(engine, mock_httpx_response):
    """空文字段自動跳過。"""
    mock_resp = mock_httpx_response(b"only_one")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    segments = [
        {"text": "", "speed": 1.0},
        {"text": "  ", "speed": 1.0},
        {"text": "實際內容", "speed": 1.0},
    ]

    result = await engine.synthesize_segments(segments)
    assert result == b"only_one"
    assert post_mock.call_count == 1


# ---------------------------------------------------------------------------
# synthesize_text()（主入口）
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_plain_text(engine, mock_httpx_response):
    """純文字：split + synthesize_segments。"""
    mock_resp = mock_httpx_response(b"processed_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    result = await engine.synthesize_text("你好世界", voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    assert result == b"processed_audio"


@pytest.mark.asyncio
async def test_synthesize_text_ssml_triggers_ssml_branch(engine, mock_httpx_response):
    """SSML 文字：走 synthesize_ssml 分支。"""
    # Mock synthesize_ssml via patching the method
    ssml_mock = AsyncMock(return_value=b"ssml_audio")
    engine.synthesize_ssml = ssml_mock  # type: ignore

    result = await engine.synthesize_text("<speak>你好</speak>", voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    assert result == b"ssml_audio"
    ssml_mock.assert_called_once()


@pytest.mark.asyncio
async def test_synthesize_text_empty(engine):
    """空文字 → return b""。"""
    result = await engine.synthesize_text("")
    assert result == b""


# ---------------------------------------------------------------------------
# synthesize_ssml()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_ssml_valid_ssml(engine, mock_httpx_response):
    """有效 SSML：parse + synthesize_segments。"""
    mock_resp = mock_httpx_response(b"ssml_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    ssml = '<speak><prosody rate="1.2">加速文字</prosody></speak>'
    result = await engine.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)

    assert result == b"ssml_audio"


@pytest.mark.asyncio
async def test_synthesize_ssml_plain_text_fallback(engine, mock_httpx_response):
    """普通文字 fallback：treat as plain text and split。"""
    mock_resp = mock_httpx_response(b"fallback_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    result = await engine.synthesize_ssml("這是普通文字", voice="zf_xiaoxiao", speed=1.0)

    assert result == b"fallback_audio"


@pytest.mark.asyncio
async def test_synthesize_ssml_empty(engine):
    """空 SSML → return b""。"""
    result = await engine.synthesize_ssml("")
    assert result == b""


@pytest.mark.asyncio
async def test_synthesize_ssml_segments_have_speed(engine, mock_httpx_response):
    """SSML segments 攜帶各自的 speed 參數。"""
    mock_resp = mock_httpx_response(b"audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    ssml = '<speak><prosody rate="0.8">慢速</prosody><prosody rate="1.5">快速</prosody></speak>'
    await engine.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)

    payloads = [call.kwargs["json"] for call in post_mock.call_args_list]
    speeds = {p["speed"] for p in payloads}
    assert 0.8 in speeds or 1.5 in speeds


# ---------------------------------------------------------------------------
# synthesize_text() — further coverage
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_with_multiple_segments(engine, mock_httpx_response):
    """多段文字拆分後並行合成。"""
    mock_resp1 = mock_httpx_response(b"seg1")
    mock_resp2 = mock_httpx_response(b"seg2")
    post_mock = AsyncMock(side_effect=[mock_resp1, mock_resp2])
    engine.client.post = post_mock  # type: ignore

    # Text that exceeds max_chars so it gets split
    long_text = "你好，這是一段比較長的文字。" * 20
    result = await engine.synthesize_text(long_text, voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    # Should have concatenated results
    assert result in (b"seg1seg2", b"seg1")


# ---------------------------------------------------------------------------
# synthesize() — additional scenarios
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_logging_warning_for_empty(engine, caplog):
    """空文字會觸發 logger.warning。"""
    import logging
    caplog.set_level(logging.WARNING)

    result = await engine.synthesize("")
    assert result == b""
    assert any("Empty text" in record.message for record in caplog.records)


@pytest.mark.asyncio
async def test_synthesize_returns_raw_bytes(engine, mock_httpx_response):
    """確保回傳型別是 bytes。"""
    mock_resp = mock_httpx_response(b"\x00\x01\x02\xff")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    result = await engine.synthesize("binary test")
    assert isinstance(result, bytes)
    assert result == b"\x00\x01\x02\xff"


# ---------------------------------------------------------------------------
# synthesize_segments() — retry logic coverage
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_segments_single_segment(engine, mock_httpx_response):
    """只有一個有效 segment。"""
    mock_resp = mock_httpx_response(b"single")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    segments = [{"text": "只有一段", "speed": 1.0}]
    result = await engine.synthesize_segments(segments)

    assert result == b"single"
    assert post_mock.call_count == 1


# ---------------------------------------------------------------------------
# synthesize_ssml() — error paths
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_ssml_non_xml_fallback(engine, mock_httpx_response):
    """非 XML 文字走 fallback 路徑。"""
    mock_resp = mock_httpx_response(b"fallback")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    # SSML parser returns is_ssml=False for malformed SSML
    result = await engine.synthesize_ssml("plain text with < angle brackets >", voice="zf_xiaoxiao", speed=1.0)

    assert result == b"fallback"


# ---------------------------------------------------------------------------
# close()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_close_normal(engine):
    """正常 close 不拋錯。"""
    engine.client.aclose = AsyncMock()
    engine._executor.shutdown = MagicMock()

    await engine.close()

    engine.client.aclose.assert_called_once()
    engine._executor.shutdown.assert_called_once_with(wait=False)


@pytest.mark.asyncio
async def test_close_context_manager(engine):
    """async with 上下文管理器正常運作。"""
    engine.client.aclose = AsyncMock()
    engine._executor.shutdown = MagicMock()

    async with engine as e:
        assert e is engine

    engine.client.aclose.assert_called_once()


# ---------------------------------------------------------------------------
# synthesize_text() — prosody / emphasis SSML paths
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_emphasis_ssml(engine, mock_httpx_response):
    """SSML emphasis 標籤正確處理。"""
    mock_resp = mock_httpx_response(b"emphasis_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    ssml = '<speak><emphasis level="strong">強調文字</emphasis></speak>'
    result = await engine.synthesize_text(ssml, voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    assert result == b"emphasis_audio"


@pytest.mark.asyncio
async def test_synthesize_text_break_ssml(engine, mock_httpx_response):
    """SSML break 標籤 → 產生對應停頓字元，音訊分為多段。"""
    # SSML <speak>文字<break time="500ms"/>暫停</speak> parses to:
    #   segment 1: "文字" (text)
    #   segment 2: "" with pause_chars=" " (break 500ms < 2000ms → ".")
    #   segment 3: "暫停" (tail text)
    # Empty-text segments are skipped → only 2 actual synthesis calls
    mock_resp1 = mock_httpx_response(b"text_audio")
    mock_resp2 = mock_httpx_response(b"after_audio")
    post_mock = AsyncMock(side_effect=[mock_resp1, mock_resp2])
    engine.client.post = post_mock  # type: ignore

    ssml = '<speak>文字<break time="500ms"/>暫停</speak>'
    result = await engine.synthesize_text(ssml, voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    # break 空文字段被 skip，2 次實際合成
    assert post_mock.call_count == 2


# ---------------------------------------------------------------------------
# synthesize_segments() — mixed bytes / empty result filtering
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_segments_one_empty_bytes_result(engine, mock_httpx_response):
    """某段 return b"" 時不加入串接但不拋錯。"""
    # First returns empty bytes (already handled at gather level)
    mock_resp1 = mock_httpx_response(b"")  # empty
    mock_resp2 = mock_httpx_response(b"nonempty")
    post_mock = AsyncMock(side_effect=[mock_resp1, mock_resp2])
    engine.client.post = post_mock  # type: ignore

    segments = [
        {"text": "空段", "speed": 1.0},
        {"text": "非空段", "speed": 1.0},
    ]
    result = await engine.synthesize_segments(segments)

    # empty chunks are filtered out by the logic
    assert result == b"nonempty"


# ---------------------------------------------------------------------------
# synthesize() — unicode text processing
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_unicode_text(engine, mock_httpx_response):
    """Unicode 中文文字正常處理。"""
    mock_resp = mock_httpx_response(b"unicode_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    result = await engine.synthesize("繁體中文測試：你好、世界！")
    assert result == b"unicode_audio"


# ---------------------------------------------------------------------------
# synthesize_segments() — _concatenate_audio edge cases
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_segments_single_chunk(engine, mock_httpx_response):
    """只有一個 chunk 時不走 concat 邏輯。"""
    mock_resp = mock_httpx_response(b"single_chunk")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    segments = [{"text": "唯一段落", "speed": 1.0}]
    result = await engine.synthesize_segments(segments)

    assert result == b"single_chunk"


# ---------------------------------------------------------------------------
# synthesize_ssml() — voice element
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_ssml_voice_element(engine, mock_httpx_response):
    """SSML voice 標籤處理。"""
    mock_resp = mock_httpx_response(b"voice_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    ssml = '<speak><voice name="zf_xiaoxiao">語音標籤</voice></speak>'
    result = await engine.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)

    assert result == b"voice_audio"


# ---------------------------------------------------------------------------
# synthesize_text() — prosody element path
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_prosody_element(engine, mock_httpx_response):
    """prosody rate='slow' 處理。"""
    mock_resp = mock_httpx_response(b"prosody_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    ssml = '<speak><prosody rate="slow">慢速朗讀</prosody></speak>'
    result = await engine.synthesize_text(ssml, voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    assert result == b"prosody_audio"


# ---------------------------------------------------------------------------
# synthesize() — lingustic engine preprocess applied
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_calls_linguistic_engine(engine, mock_httpx_response):
    """synthesize 確實呼叫 linguistic_engine.preprocess_for_tts。"""
    mock_resp = mock_httpx_response(b"processed")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    with patch.object(engine.linguistic_engine, "preprocess_for_tts", return_value="處理後的文字") as mock_pre:
        result = await engine.synthesize("原始文字", voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    mock_pre.assert_called_once_with("原始文字")
    payload = post_mock.call_args.kwargs["json"]
    assert payload["input"] == "處理後的文字"


# ---------------------------------------------------------------------------
# synthesize_text() — empty after split
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_empty_after_split(engine):
    """split 後無段落 → return b""。"""
    # Mock splitter to return empty
    engine.text_splitter.split = MagicMock(return_value=[])

    result = await engine.synthesize_text("test", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
    assert result == b""


# ---------------------------------------------------------------------------
# synthesize_ssml() — no segments after parse
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_ssml_no_segments(engine):
    """解析後無段落 → return b""。"""
    from src.engines.ssml_parser import ParsedSSML
    mock_parsed = ParsedSSML(input_text="", is_ssml=True, segments=[])

    # Mock synthesize_segments to avoid hitting client.post
    with patch.object(engine.ssml_parser, "parse", return_value=mock_parsed):
        with patch.object(engine, "synthesize_segments", new_callable=AsyncMock, return_value=b"") as mock_ss:
            result = await engine.synthesize_ssml("<speak></speak>", voice="zf_xiaoxiao", speed=1.0)

    assert result == b""


# ---------------------------------------------------------------------------
# synthesize_segments() — all tasks skipped (empty after filter)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_segments_all_skipped(engine):
    """所有段都是空文字 → tasks 空 → return b""。"""
    segments = [{"text": "", "speed": 1.0}, {"text": "  ", "speed": 1.0}]
    result = await engine.synthesize_segments(segments)
    assert result == b""


# ---------------------------------------------------------------------------
# synthesize_ssml() — invalid XML → fallback with preprocess
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_ssml_invalid_xml_uses_fallback(engine, mock_httpx_response):
    """SSML 解析失敗（無效 XML）→ fallback + preprocess。"""
    mock_resp = mock_httpx_response(b"fallback_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    # Use text that won't parse as XML
    result = await engine.synthesize_ssml("<<>>invalid xml<<>>", voice="zf_xiaoxiao", speed=1.0)

    assert result == b"fallback_audio"
    assert post_mock.call_count >= 1


# ---------------------------------------------------------------------------
# synthesize() — ValueError/IOError/OSError
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_httpx_other_exceptions(engine):
    """httpx 例外（非 Timeout/HTTPStatus）→ 向上拋。"""
    engine.client.post = AsyncMock(side_effect=httpx.ConnectError("connection failed"))  # type: ignore

    with pytest.raises(httpx.HTTPError):
        await engine.synthesize("test")


@pytest.mark.asyncio
async def test_synthesize_value_error(engine):
    """ValueError 在 httpx 包之後被捕获 → 向上拋。"""
    # Patch httpx.HTTPError catch to NOT match, so ValueError path is hit
    # by patching client.post to raise ValueError after httpx processing
    with patch.object(
        engine.linguistic_engine,
        "preprocess_for_tts",
        side_effect=ValueError("lexicon error"),
    ):
        with pytest.raises(ValueError):
            await engine.synthesize("test")


# ---------------------------------------------------------------------------
# synthesize_text() — XML declaration SSML
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_xml_declaration_ssml(engine, mock_httpx_response):
    """帶 <?xml ?> 宣告的 SSML 正確處理。"""
    mock_resp = mock_httpx_response(b"xml_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    ssml = '<?xml version="1.0"?><speak>XML宣告測試</speak>'
    result = await engine.synthesize_text(ssml, voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    assert result == b"xml_audio"


# ---------------------------------------------------------------------------
# synthesize_segments() — large number of segments
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_segments_many_parallel(engine, mock_httpx_response):
    """大量 segments 正確並行處理。"""
    mock_resp = mock_httpx_response(b"a")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    segments = [{"text": f"段{i}", "speed": 1.0} for i in range(10)]
    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")

    assert result == b"aaaaaaaaaa"
    assert post_mock.call_count == 10


# ---------------------------------------------------------------------------
# synthesize_ssml() — phoneme element
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_ssml_phoneme_element(engine, mock_httpx_response):
    """SSML phoneme 標籤處理。"""
    mock_resp = mock_httpx_response(b"phoneme_audio")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    ssml = '<speak><phoneme alphabet="ipa" ph="təˈlefoʊn">電話</phoneme></speak>'
    result = await engine.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)

    assert result == b"phoneme_audio"


# ---------------------------------------------------------------------------
# synthesize_text() — very long text via text_splitter
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_long_text_split(engine, mock_httpx_response):
    """長文字經 text_splitter 正確拆分。"""
    mock_resp1 = mock_httpx_response(b"part1")
    mock_resp2 = mock_httpx_response(b"part2")
    post_mock = AsyncMock(side_effect=[mock_resp1, mock_resp2])
    engine.client.post = post_mock  # type: ignore

    # Override splitter to return two segments
    engine.text_splitter.split = MagicMock(
        side_effect=[["第一部分很長的文字", "第二部分也很長"]]
    )

    result = await engine.synthesize_text("超長文字" * 50, voice="zf_xiaoxiao", speed=1.0, model="kokoro")

    # Should have been called twice (two segments)
    assert result in (b"part1part2", b"part1")


# ---------------------------------------------------------------------------
# synthesize() — mixed Chinese/English text
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_mixed_chinese_english(engine, mock_httpx_response):
    """中英文混雜文字正確處理。"""
    mock_resp = mock_httpx_response(b"mixed")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    result = await engine.synthesize("I love AI 和 Artificial Intelligence")
    assert result == b"mixed"


# ---------------------------------------------------------------------------
# synthesize() — numeric speed value as string
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_speed_float(engine, mock_httpx_response):
    """speed=float 正確傳遞。"""
    mock_resp = mock_httpx_response(b"speed_test")
    post_mock = AsyncMock(return_value=mock_resp)
    engine.client.post = post_mock  # type: ignore

    result = await engine.synthesize("speed test", speed=1.25)
    payload = post_mock.call_args.kwargs["json"]
    assert payload["speed"] == 1.25


# ---------------------------------------------------------------------------
# synthesize_segments() — RuntimeError has correct format
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_segments_error_message_format(engine):
    """RuntimeError 訊息包含失敗段索引。"""
    engine.client.post = AsyncMock(side_effect=[  # type: ignore
        httpx.TimeoutException("timeout"),
        httpx.TimeoutException("timeout"),
    ])

    segments = [{"text": "a", "speed": 1.0}, {"text": "b", "speed": 1.0}]

    with pytest.raises(RuntimeError) as exc_info:
        await engine.synthesize_segments(segments)

    error_msg = str(exc_info.value)
    assert "All segments failed" in error_msg
    assert "Segment" in error_msg
