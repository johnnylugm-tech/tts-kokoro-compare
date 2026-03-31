# Kokoro Taiwan Proxy - 規格文件

## 1. 概述

**專案名稱**：`kokoro-taiwan-proxy`  
**目的**：基於 Kokoro-82M 之台灣中文最佳化語音合成 Proxy  
**Python 版本**：3.10+

## 2. 技術架構

- **框架**：FastAPI + httpx + uvicorn
- **後端**：Kokoro Docker 執行於 `http://localhost:8880/v1`
- **Proxy**：FastAPI 代理層，處理所有 SSML + 台灣化邏輯

## 3. 資料夾結構

```
kokoro-taiwan-proxy/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI 應用程式
│   ├── config.py            # 設定檔
│   ├── models.py            # Pydantic 模型
│   ├── routers/
│   │   ├── __init__.py
│   │   └── speech.py         # /v1/proxy/speech 端點
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── taiwan_linguistic.py   # 台灣化語言引擎
│   │   ├── ssml_parser.py         # SSML 解析器
│   │   ├── text_splitter.py       # 智能文本切分器
│   │   └── synthesis.py            # 合成引擎
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── circuit_breaker.py      # 斷路器
│   └── cache/
│       ├── __init__.py
│       └── redis_cache.py         # Redis 音訊快取
├── tests/
│   ├── __init__.py
│   ├── test_taiwan_linguistic.py
│   ├── test_ssml_parser.py
│   ├── test_text_splitter.py
│   └── test_integration.py
├── requirements.txt
├── README.md
└── SPEC.md
```

## 4. 核心模組規格

### 4.1 config.py

```python
KOKORO_BACKEND_URL = "http://localhost:8880/v1/audio/speech"
KOKORO_VOICES_URL = "http://localhost:8880/v1/audio/voices"
DEFAULT_VOICE = "zf_xiaoxiao"
DEFAULT_SPEED = 1.0
MAX_CHARS_PER_REQUEST = 500
REQUEST_TIMEOUT = 30.0
CIRCUIT_BREAKER_THRESHOLD = 3
CIRCUIT_BREAKER_TIMEOUT = 10.0
WARMUP_ENABLED = True
WARMUP_TEXT = "你好，測試中"

MODEL_MAP = {
    "tts-1": "kokoro",
    "tts-1-hd": "kokoro",
    "kokoro": "kokoro",
    "custom-gentle": "zf_xiaoxiao(0.8)+af_heart(0.2)",
}
```

### 4.2 engines/taiwan_linguistic.py

**LEXICON 映射表**：
```python
LEXICON = {
    "視頻": "影片",
    "地鐵": "捷運",
    "垃圾": "ㄌㄜˋ ㄙㄜˋ",
    "和": "ㄏㄢˋ",
    "菠蘿": "鳳梨",
    "吧": "啦",
    "什麼": "什麥",
}
```

**API**：
- `apply_taiwan_accent(text: str) -> str` - 應用台灣化口音
- `add_english_spaces(text: str) -> str` - 中英文混雜加空格
- `preprocess_for_tts(text: str) -> str` - 完整前處理流程
- `validate_text(text: str) -> tuple[bool, str]` - 文字驗證

### 4.3 engines/ssml_parser.py

**支援標籤**：

| 標籤 | 屬性 | 處理策略 |
|------|------|---------|
| `<speak>` | - | 根元素 |
| `<break>` | `time="500ms"` | 插入停頓 |
| `<prosody>` | `rate="0.9"` | 映射 speed |
| `<emphasis>` | `level="strong"` | 速率×1.1 |
| `<phoneme>` | `alphabet="ipa"` | 保留 |

**API**：
- `parse(ssml_string: str) -> ParsedSSML`
- `is_ssml(text: str) -> bool`
- `extract_plain_text(ssml_string: str) -> str`

### 4.4 engines/text_splitter.py

**三級切分邏輯**：
```
一級（句）：。？！!?\n
二級（子句）：；：（若>100字）
三級（詞組）：，（若仍>100字）
```

**規則**：
- 每段最多 500 字
- 最優區段 100-250 字
- 標點符號保留在段落尾端

**API**：
- `split(text: str, max_chars: int = 500) -> List[str]`
- `split_semantic(text: str, max_chars: int = None) -> List[str]`

### 4.5 engines/synthesis.py

**並行合成**：使用 `httpx.AsyncClient` 同時發出 N 個請求

**拼接**：MP3 直接串接

**API**：
- `synthesize(text, voice, speed, model) -> bytes`
- `synthesize_segments(segments, voice, model) -> bytes`
- `synthesize_ssml(ssml_text, voice, speed) -> bytes`
- `synthesize_text(text, voice, speed, model) -> bytes`

### 4.6 middleware/circuit_breaker.py

```python
class CircuitBreaker:
    states: closed, open, half-open
    threshold: 3 failures
    timeout: 10 seconds
```

### 4.7 routers/speech.py

**端點**：`POST /v1/proxy/speech`

**流程**：
1. 偵測是否為 SSML
2. SSML → 參數 + 文字
3. 台灣化文字處理
4. 模型代號映射
5. 智慧切分
6. 並行合成
7. 返回 MP3

### 4.8 main.py

**端點**：
- `GET /` - 根目錄
- `GET /health` - 健康檢查
- `GET /ready` - 就緒檢查
- `POST /v1/proxy/speech` - 語音合成
- `GET /v1/proxy/voices` - 音色列表
- `GET /health/circuit` - 斷路器狀態
- `POST /health/circuit/reset` - 重置斷路器

### 4.9 models.py

```python
class SpeechRequest(BaseModel):
    model: str = "tts-1"
    input: str
    voice: Optional[str] = None
    speed: Optional[float] = None
    response_format: str = "mp3"
```

## 5. 錯誤處理

| 錯誤情況 | 處理策略 |
|---------|---------|
| SSML 解析失敗 | fallback 純文字 |
| 後端錯誤 | HTTPException 503 |
| 電路熔斷開啟 | HTTPException 503 |
| 空輸入 | HTTPException 400 |
| 輸入過長 | HTTPException 400 |

## 6. 測試要求

每個 engine 至少 5 個測試案例：
- `test_taiwan_linguistic.py` - 12+ 測試
- `test_ssml_parser.py` - 18+ 測試
- `test_text_splitter.py` - 16+ 測試
- `test_integration.py` - 14+ 測試

## 7. 依賴

```
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
httpx>=0.24.0
pydub>=0.25.1
pytest>=7.4.0
pytest-asyncio>=0.21.0
redis>=4.6.0
pydantic>=2.0.0
```

## 8. 驗收標準

1. ✅ `pytest tests/ -v` 全數通過
2. ✅ `python -m src.main` 可啟動伺服器
3. ✅ 包含 `SPEC.md`
4. ✅ 包含 `README.md`
5. ✅ `curl http://localhost:8880/v1/audio/voices` 可取得音色
