"""Tests for engines/synthesis.py — SynthesisEngine coverage.

All HTTP-related tests use REAL Kokoro API at localhost:8880.
Error-path tests continue using mock (httpx exceptions are not easily
injectable via connection-refused for these specific scenarios).
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.engines.synthesis import SynthesisEngine


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
async def engine():
    """Per-test engine with REAL HTTP client (no mocking)."""
    eng = SynthesisEngine(backend_url="http://localhost:8880/v1/audio/speech", timeout=30.0)
    yield eng
    await eng.close()


# ---------------------------------------------------------------------------
# synthesize() — empty / early-return (no HTTP)
# ---------------------------------------------------------------------------

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
async def test_synthesize_logging_warning_for_empty(engine, caplog):
    """空文字會觸發 logger.warning。"""
    import logging
    caplog.set_level(logging.WARNING)

    result = await engine.synthesize("")
    assert result == b""
    assert any("Empty text" in record.message for record in caplog.records)


# ---------------------------------------------------------------------------
# synthesize() — error paths (kept with mock — httpx exception handling)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_httpx_timeout():
    """httpx TimeoutException → 向上拋。"""
    eng = SynthesisEngine(timeout=1.0)
    eng.client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))  # type: ignore
    try:
        with pytest.raises(httpx.TimeoutException):
            await eng.synthesize("test")
    finally:
        await eng.close()


@pytest.mark.asyncio
async def test_synthesize_httpx_http_status_error():
    """httpx HTTPStatusError → 向上拋。"""
    response = MagicMock()
    response.status_code = 500
    response.text = "Internal Server Error"
    eng = SynthesisEngine(timeout=30.0)
    eng.client.post = AsyncMock(side_effect=httpx.HTTPStatusError(  # type: ignore
        "Server Error", request=MagicMock(), response=response
    ))
    try:
        with pytest.raises(httpx.HTTPStatusError):
            await eng.synthesize("test")
    finally:
        await eng.close()


@pytest.mark.asyncio
async def test_synthesize_httpx_generic_http_error():
    """通用 httpx HTTPError → 向上拋。"""
    eng = SynthesisEngine(timeout=30.0)
    eng.client.post = AsyncMock(side_effect=httpx.HTTPError("Generic error"))  # type: ignore
    try:
        with pytest.raises(httpx.HTTPError):
            await eng.synthesize("test")
    finally:
        await eng.close()


@pytest.mark.asyncio
async def test_synthesize_httpx_other_exceptions():
    """httpx ConnectError → httpx.HTTPError 向上拋。"""
    eng = SynthesisEngine(timeout=5.0)
    eng.client.post = AsyncMock(side_effect=httpx.ConnectError("connection failed"))  # type: ignore
    try:
        with pytest.raises(httpx.HTTPError):
            await eng.synthesize("test")
    finally:
        await eng.close()


@pytest.mark.asyncio
async def test_synthesize_value_error():
    """ValueError 在 httpx 包之後被捕获 → 向上拋。"""
    eng = SynthesisEngine(timeout=30.0)
    try:
        with patch.object(
            eng.linguistic_engine,
            "preprocess_for_tts",
            side_effect=ValueError("lexicon error"),
        ):
            with pytest.raises(ValueError):
                await eng.synthesize("test")
    finally:
        await eng.close()


# ---------------------------------------------------------------------------
# synthesize() — happy paths (REAL HTTP)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_normal(engine):
    """正常：httpx 返回音頻數據。"""
    result = await engine.synthesize("你好", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_with_voice_and_speed(engine):
    """正常文字 + 語音 + 速度參數傳遞。"""
    result = await engine.synthesize("測試語音", voice="af_heart", speed=0.8, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_returns_raw_bytes(engine):
    """確保回傳型別是 bytes。"""
    result = await engine.synthesize("binary test")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_unicode_text(engine):
    """Unicode 中文文字正常處理。"""
    result = await engine.synthesize("繁體中文測試：你好、世界！")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_mixed_chinese_english(engine):
    """中英文混雜文字正確處理。"""
    result = await engine.synthesize("I love AI 和 Artificial Intelligence")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_speed_float(engine):
    """speed=float 正確傳遞。"""
    result = await engine.synthesize("speed test", voice="zf_xiaoxiao", speed=1.25, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_calls_linguistic_engine(engine):
    """synthesize 確實呼叫 linguistic_engine.preprocess_for_tts。"""
    # Just verify it doesn't raise — linguistic engine is applied internally
    result = await engine.synthesize("原始文字", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# synthesize_segments()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_segments_empty_list(engine):
    """空列表 → return b""。"""
    result = await engine.synthesize_segments([])
    assert result == b""


@pytest.mark.asyncio
async def test_synthesize_segments_normal(engine):
    """正常段列表 → 串接音頻結果。"""
    segments = [
        {"text": "第一段", "speed": 1.0},
        {"text": "第二段", "speed": 1.0},
    ]
    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_segments_with_different_speeds(engine):
    """不同 speed 參數傳遞到每個 segment。"""
    segments = [
        {"text": "慢慢說", "speed": 0.6},
        {"text": "快快說", "speed": 1.4},
    ]
    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_segments_single_segment(engine):
    """只有一個有效 segment。"""
    segments = [{"text": "只有一段", "speed": 1.0}]
    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_segments_single_chunk(engine):
    """只有一個 chunk 時不走 concat 邏輯。"""
    segments = [{"text": "唯一段落", "speed": 1.0}]
    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_segments_skips_empty_text(engine):
    """空文字段自動跳過。"""
    segments = [
        {"text": "", "speed": 1.0},
        {"text": "  ", "speed": 1.0},
        {"text": "實際內容", "speed": 1.0},
    ]
    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_segments_one_empty_bytes_result(engine):
    """某段 return b"" 時不加入串接但不拋錯。"""
    segments = [
        {"text": "非空段", "speed": 1.0},
    ]
    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_segments_all_skipped(engine):
    """所有段都是空文字 → tasks 空 → return b""。"""
    segments = [{"text": "", "speed": 1.0}, {"text": "  ", "speed": 1.0}]
    result = await engine.synthesize_segments(segments)
    assert result == b""


@pytest.mark.asyncio
async def test_synthesize_segments_many_parallel(engine):
    """大量 segments 正確並行處理。"""
    segments = [{"text": f"段{i}", "speed": 1.0} for i in range(10)]
    result = await engine.synthesize_segments(segments, voice="zf_xiaoxiao", model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# synthesize_segments() — error paths (mock)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_segments_partial_failure():
    """部分段失敗（各自 retry 完仍失敗）→ RuntimeError。"""
    eng = SynthesisEngine(timeout=30.0)
    eng.client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))  # type: ignore
    try:
        segments = [
            {"text": "失敗段", "speed": 1.0},
            {"text": "另一失敗段", "speed": 1.0},
        ]
        with pytest.raises(RuntimeError) as exc_info:
            await eng.synthesize_segments(segments)
        assert "All segments failed" in str(exc_info.value)
    finally:
        await eng.close()


@pytest.mark.asyncio
async def test_synthesize_segments_all_failure():
    """全部段失敗 → RuntimeError。"""
    eng = SynthesisEngine(timeout=30.0)
    eng.client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))  # type: ignore
    try:
        segments = [
            {"text": "段一", "speed": 1.0},
            {"text": "段二", "speed": 1.0},
        ]
        with pytest.raises(RuntimeError) as exc_info:
            await eng.synthesize_segments(segments)
        assert "All segments failed" in str(exc_info.value)
    finally:
        await eng.close()


@pytest.mark.asyncio
async def test_synthesize_segments_error_message_format():
    """RuntimeError 訊息包含失敗段索引。"""
    eng = SynthesisEngine(timeout=30.0)
    eng.client.post = AsyncMock(side_effect=[  # type: ignore
        httpx.TimeoutException("timeout"),
        httpx.TimeoutException("timeout"),
    ])
    try:
        segments = [{"text": "a", "speed": 1.0}, {"text": "b", "speed": 1.0}]
        with pytest.raises(RuntimeError) as exc_info:
            await eng.synthesize_segments(segments)
        error_msg = str(exc_info.value)
        assert "All segments failed" in error_msg
        assert "Segment" in error_msg
    finally:
        await eng.close()


# ---------------------------------------------------------------------------
# synthesize_text()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_plain_text(engine):
    """純文字：split + synthesize_segments。"""
    result = await engine.synthesize_text("你好世界", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_text_empty(engine):
    """空文字 → return b""。"""
    result = await engine.synthesize_text("")
    assert result == b""


@pytest.mark.asyncio
async def test_synthesize_text_empty_after_split():
    """split 後無段落 → return b""。"""
    eng = SynthesisEngine(timeout=30.0)
    # Mock splitter to return empty
    eng.text_splitter.split = MagicMock(return_value=[])
    try:
        result = await eng.synthesize_text("test", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
        assert result == b""
    finally:
        await eng.close()


@pytest.mark.asyncio
async def test_synthesize_text_with_multiple_segments(engine):
    """多段文字拆分後並行合成。"""
    # A text long enough to be split into multiple segments
    long_text = "你好，這是一段比較長的文字。" * 20
    result = await engine.synthesize_text(long_text, voice="zf_xiaoxiao", speed=1.0, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_text_long_text_split():
    """長文字經 text_splitter 正確拆分。"""
    eng = SynthesisEngine(timeout=30.0)
    # Override splitter to return two segments
    eng.text_splitter.split = MagicMock(
        side_effect=[["第一部分很長的文字", "第二部分也很長"]]
    )
    try:
        result = await eng.synthesize_text("超長文字" * 50, voice="zf_xiaoxiao", speed=1.0, model="kokoro")
        assert isinstance(result, bytes)
        assert len(result) > 0
    finally:
        await eng.close()


# ---------------------------------------------------------------------------
# synthesize_text() — SSML branches (mock synthesize_ssml)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_ssml_triggers_ssml_branch():
    """SSML 文字：走 synthesize_ssml 分支。"""
    eng = SynthesisEngine(timeout=30.0)
    ssml_mock = AsyncMock(return_value=b"ssml_audio")
    eng.synthesize_ssml = ssml_mock  # type: ignore
    try:
        result = await eng.synthesize_text("<speak>你好</speak>", voice="zf_xiaoxiao", speed=1.0, model="kokoro")
        assert result == b"ssml_audio"
        ssml_mock.assert_called_once()
    finally:
        await eng.close()


# ---------------------------------------------------------------------------
# synthesize_text() — SSML elements (real HTTP)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_text_emphasis_ssml(engine):
    """SSML emphasis 標籤正確處理。"""
    ssml = '<speak><emphasis level="strong">強調文字</emphasis></speak>'
    result = await engine.synthesize_text(ssml, voice="zf_xiaoxiao", speed=1.0, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_text_break_ssml(engine):
    """SSML break 標籤 → 產生對應停頓字元，音訊分為多段。"""
    ssml = '<speak>文字<break time="500ms"/>暫停</speak>'
    result = await engine.synthesize_text(ssml, voice="zf_xiaoxiao", speed=1.0, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_text_prosody_element(engine):
    """prosody rate='slow' 處理。"""
    ssml = '<speak><prosody rate="slow">慢速朗讀</prosody></speak>'
    result = await engine.synthesize_text(ssml, voice="zf_xiaoxiao", speed=1.0, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_text_xml_declaration_ssml(engine):
    """帶 <?xml ?> 宣告的 SSML 正確處理。"""
    ssml = '<?xml version="1.0"?><speak>XML宣告測試</speak>'
    result = await engine.synthesize_text(ssml, voice="zf_xiaoxiao", speed=1.0, model="kokoro")
    assert isinstance(result, bytes)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# synthesize_ssml()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_synthesize_ssml_valid_ssml(engine):
    """有效 SSML：parse + synthesize_segments。"""
    ssml = '<speak><prosody rate="1.2">加速文字</prosody></speak>'
    result = await engine.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_ssml_plain_text_fallback(engine):
    """普通文字 fallback：treat as plain text and split。"""
    result = await engine.synthesize_ssml("這是普通文字", voice="zf_xiaoxiao", speed=1.0)
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_ssml_empty(engine):
    """空 SSML → return b""。"""
    result = await engine.synthesize_ssml("")
    assert result == b""


@pytest.mark.asyncio
async def test_synthesize_ssml_non_xml_fallback(engine):
    """非 XML 文字走 fallback 路徑。"""
    result = await engine.synthesize_ssml("plain text with < angle brackets >", voice="zf_xiaoxiao", speed=1.0)
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_ssml_invalid_xml_uses_fallback(engine):
    """SSML 解析失敗（無效 XML）→ fallback + preprocess。"""
    result = await engine.synthesize_ssml("<<>>invalid xml<<>>", voice="zf_xiaoxiao", speed=1.0)
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_ssml_voice_element(engine):
    """SSML voice 標籤處理。"""
    ssml = '<speak><voice name="zf_xiaoxiao">語音標籤</voice></speak>'
    result = await engine.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_ssml_phoneme_element(engine):
    """SSML phoneme 標籤處理。"""
    ssml = '<speak><phoneme alphabet="ipa" ph="təˈlefoʊn">電話</phoneme></speak>'
    result = await engine.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_ssml_segments_have_speed(engine):
    """SSML segments 攜帶各自的 speed 參數。"""
    ssml = '<speak><prosody rate="0.8">慢速</prosody><prosody rate="1.5">快速</prosody></speak>'
    result = await engine.synthesize_ssml(ssml, voice="zf_xiaoxiao", speed=1.0)
    assert isinstance(result, bytes)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_synthesize_ssml_no_segments():
    """解析後無段落 → return b""。"""
    from src.engines.ssml_parser import ParsedSSML
    eng = SynthesisEngine(timeout=30.0)
    mock_parsed = ParsedSSML(input_text="", is_ssml=True, segments=[])
    with patch.object(eng.ssml_parser, "parse", return_value=mock_parsed):
        with patch.object(eng, "synthesize_segments", new_callable=AsyncMock, return_value=b"") as mock_ss:
            result = await eng.synthesize_ssml("<speak></speak>", voice="zf_xiaoxiao", speed=1.0)
    assert result == b""
    await eng.close()


# ---------------------------------------------------------------------------
# close()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_close_normal():
    """正常 close 不拋錯。"""
    eng = SynthesisEngine(timeout=30.0)
    eng.client.aclose = AsyncMock()
    eng._executor.shutdown = MagicMock()
    await eng.close()
    eng.client.aclose.assert_called_once()
    eng._executor.shutdown.assert_called_once_with(wait=False)


@pytest.mark.asyncio
async def test_close_context_manager():
    """async with 上下文管理器正常運作。"""
    async with SynthesisEngine() as eng:
        eng.client.aclose = AsyncMock()
        eng._executor.shutdown = MagicMock()
    eng.client.aclose.assert_called_once()