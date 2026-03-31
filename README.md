# Kokoro Taiwan Proxy

基於 Kokoro-82M 之台灣中文最佳化語音合成 Proxy

## 功能特色

- 🌏 **台灣化語言處理**：自動將中國大陸用語轉換為台灣習慣用語
- 📄 **SSML 支援**：完整支援 Speech Synthesis Markup Language
- ⚡ **並行合成**：多段落同時合成，加快 TTFB
- 🔄 **斷路器模式**：後端故障時自動保護系統
- 💾 **Redis 快取**：可選的音訊快取層（需啟用）
- 🔧 **OpenAI 相容 API**：提供與 OpenAI TTS API 相容的接口

## 快速開始

### 1. 安裝依賴

```bash
cd kokoro-taiwan-proxy
pip install -r requirements.txt
```

### 2. 啟動後端（Kokoro Docker）

確保 Kokoro TTS Docker 運行於 `http://localhost:8880/v1`

### 3. 啟動 Proxy 伺服器

```bash
python -m src.main
```

或使用 uvicorn：

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8881
```

### 4. 測試 API

#### 健康檢查
```bash
curl http://localhost:8881/health
```

#### 取得音色列表
```bash
curl http://localhost:8881/v1/proxy/voices
```

#### 語音合成（純文字）
```bash
curl -X POST http://localhost:8881/v1/proxy/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "你好，世界！",
    "voice": "zf_xiaoxiao",
    "speed": 1.0
  }' \
  --output audio.mp3
```

#### 語音合成（SSML）
```bash
curl -X POST http://localhost:8881/v1/proxy/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kokoro",
    "input": "<speak><emphasis level=\"strong\">重要</emphasis>訊息</speak>",
    "voice": "zf_xiaoxiao"
  }' \
  --output audio.mp3
```

## API 端點

### POST /v1/proxy/speech

主要語音合成端點

**請求體**：
```json
{
  "model": "tts-1",
  "input": "要合成的文字",
  "voice": "zf_xiaoxiao",
  "speed": 1.0,
  "response_format": "mp3"
}
```

**模型支援**：
- `tts-1` - 標準品質
- `tts-1-hd` - 高品質
- `kokoro` - Kokoro 模型
- `custom-gentle` - 溫和混合音色

### GET /v1/proxy/voices

取得可用音色列表

### GET /health

健康檢查端點

### GET /health/circuit

斷路器狀態

## 台灣化詞彙

自動轉換的詞彙包括：

| 中國用語 | 平時/普通話 | 台灣用語 |
|---------|-----------|---------|
| 視頻 | 视频 | 影片 |
| 地鐵 | 地铁 | 捷運 |
| 垃圾 | 垃圾 | ㄌㄜˋ ㄙㄜˋ |
| 和 | 和 | ㄏㄢˋ |
| 菠蘿 | 菠萝 | 鳳梨 |
| 吧 | 吧 | 啦 |

## SSML 支援

### 支援的標籤

| 標籤 | 屬性 | 說明 |
|------|------|------|
| `<speak>` | - | 根元素 |
| `<break>` | `time` | 停頓時間（ms/s） |
| `<prosody>` | `rate` | 語速調整 |
| `<emphasis>` | `level` | 強調程度 |
| `<phoneme>` | `alphabet`, `ph` | IPA 音標 |

### 範例

```xml
<speak>
  <prosody rate="0.9">這段話會比較慢</prosody>
  <break time="500ms"/>
  <emphasis level="strong">特別強調</emphasis>
</speak>
```

## 測試

```bash
pytest tests/ -v
```

## 架構

```
                    ┌─────────────────┐
                    │   FastAPI       │
                    │   /v1/proxy/speech │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
    │ SSML    │        │ 台灣化  │        │ 文本    │
    │ 解析器  │        │ 語言引擎│        │ 切分器  │
    └────┬────┘        └────┬────┘        └────┬────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼────────┐
                    │   並行合成引擎   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
    │ 斷路器  │        │ Redis   │        │ Kokoro  │
    │         │        │ 快取     │        │ 後端    │
    └─────────┘        └─────────┘        └─────────┘
```

## 環境變數

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `KOKORO_BACKEND_URL` | `http://localhost:8880/v1/audio/speech` | Kokoro 後端 URL |
| `KOKORO_VOICES_URL` | `http://localhost:8880/v1/audio/voices` | 音色列表 URL |
| `DEFAULT_VOICE` | `zf_xiaoxiao` | 預設音色 |
| `DEFAULT_SPEED` | `1.0` | 預設語速 |
| `REQUEST_TIMEOUT` | `30.0` | 請求超時（秒） |

## License

MIT
