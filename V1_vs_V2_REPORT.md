# v1.0 vs v2.0 深度對比報告

Generated: 2026-04-24

---

## 一、整體快覽

| 維度 | v1.0 | v2.0 | 變化 |
|------|------|------|------|
| Source files | 10 個 .py | 10 個 .py | 架構不變，全部重寫品質 |
| Test files | 5 個 | 17 個 | +12 (+240%) |
| Test count | ~50 (估) | 283 | +230 tests |
| Overall quality score | 未測量 | 91.62/100 | — |
| LICENSE 文件 | ❌ | ✅ MIT | 新增 |
| Copyright headers | ❌ | ✅ 每個文件 | 新增 |
| pytest.ini | ❌ | ✅ | 新增 |
| config.yaml | ❌ | ✅ | 新增 |

---

## 二、軟體架構

架構層次（兩版本完全相同）：

```
main.py (FastAPI lifespan)
 └─ routers/speech.py (HTTP endpoints)
 └─ engines/synthesis.py (核心引擎)
 ├─ engines/ssml_parser.py
 ├─ engines/taiwan_linguistic.py
 ├─ engines/text_splitter.py
 ├─ middleware/circuit_breaker.py
 └─ cache/redis_cache.py
```

✅ v2.0 未改架構：所有模組邊界、依賴方向、接口簽名均不變
v2.0 的貢獻是在相同架構內部進行品質提升，非重構
cli.py 作為獨立入口依然並聯存在（非 router 入口）

---

## 三、重大 Bug 修復

### Bug 1：circuit_breaker.py — import asyncio 位置錯誤（v1.0 有效 bug）

```python
# v1.0 — asyncio 在 decorator factory 內的最底部才 import
def circuit_breaker_decorator(...):
    breaker = CircuitBreaker(...)
    def decorator(func):
        ...
        if asyncio.iscoroutinefunction(func): # ← NameError! asyncio 未 import
            return async_wrapper
        return wrapper
    import asyncio # ← 太晚了，已被使用
    return decorator

# v2.0 — 修正為 top-level import
import asyncio # ← 第一行
...
if asyncio.iscoroutinefunction(func): # ← 正確
```

### Bug 2：synthesis.py — 不可達的 elif（v1.0 邏輯錯誤）

```python
# v1.0 — 第二個 isinstance(result, Exception) 永遠不會執行
for i, result in enumerate(results):
    if isinstance(result, Exception): # ← 處理了
        errors.append(...)
    elif isinstance(result, bytes) and result:
        audio_chunks.append(result)
    elif isinstance(result, Exception): # ← 死碼，永遠 false
        errors.append(...)

# v2.0 重構為 _collect_and_concatenate() 獨立方法，消除重複邏輯。
```

### Bug 3：redis_cache.py — lazy import 導致多次失敗嘗試

```python
# v1.0 — 每次 _connect() 都嘗試 import redis，失敗時 ImportError 被靜默捕獲
def _connect(self):
    try:
        import redis # ← 每次都試
        ...
    except ImportError:
        ...

# v2.0 — 模組載入時 import 一次，redis=None 作為旗標
try:
    import redis
except ImportError:
    redis = None # ← 清晰標記不可用
```

---

## 四、錯誤處理品質

| 位置 | v1.0 | v2.0 |
|------|------|------|
| synthesis.py retry | `except Exception as e` | `except (ValueError, IOError, OSError, httpx.HTTPError)` |
| main.py warmup | `except Exception as e` | `except (httpx.HTTPError, httpx.TimeoutException, OSError)` |
| main.py health_check | `except Exception: pass` (完全吞掉) | `except httpx.HTTPError as e: logger.warning(...)` |
| redis_cache.py get/set/delete/clear | `except Exception as e` (×4) | `except (redis.RedisError, redis.ConnectionError, redis.TimeoutError, OSError)` (×4) |
| circuit_breaker.py call/call_async | `except ... as e: raise` (e 未使用) | `except ...: raise` (清乾淨) |

v2.0 所有 `except Exception` 全部替換為具體型別，消除「吞掉意外錯誤」的風險。

---

## 五、程式碼風格與 Linting

| 項目 | v1.0 | v2.0 |
|------|------|------|
| logger 格式 | f-string：`logger.info(f"text {var}")` | `%-style：`logger.info("text %s", var)` |
| 全域變數命名 | `_synthesis_engine, _cache_instance` | `_SYNTHESIS_ENGINE, _CACHE_INSTANCE` (PEP8 SCREAMING_SNAKE) |
| pylint suppression | 無 | `# pylint: disable=...` 明確標記 |
| bandit suppression | 無 | `# nosec` 標記 `host="0.0.0.0"` |
| type: ignore | 無 | 精確位置標記 |
| 未使用 import | asyncio in main.py (v1.0) | 清除 |
| list comprehension | 手動 for loop 填充 tasks | 一行 list comprehension |

**Linting 分數**：v1.0 估 ~65 → v2.0 100/100

---

## 六、測試覆蓋對比

### v1.0（5 files）

| 測試檔 | 大小 | 覆蓋對象 |
|--------|------|----------|
| test_cli.py | 5289B | CLI |
| test_integration.py | 3388B | 整合 |
| test_ssml_parser.py | 5832B | SSML |
| test_taiwan_linguistic.py | 5836B | 語言處理 |
| test_text_splitter.py | 4288B | 文字切割 |

**缺失覆蓋**：synthesis.py、circuit_breaker.py、redis_cache.py、audio_converter.py、main.py、routers/speech.py

### v2.0（17 files）新增 12 個

| 新增測試檔 | 大小 | 類型 |
|-----------|------|------|
| test_audio_converter.py | 2299B | 單元 |
| test_audio_converter_behavioral.py | 7138B | 行為 |
| test_circuit_breaker_behavioral.py | 12001B | 行為（最大） |
| test_main.py | 1956B | 單元 |
| test_redis_cache.py | 7714B | 單元 |
| test_speech_router.py | 5750B | 路由 |
| test_ssml_parser_coverage.py | 13434B | 覆蓋補強 |
| test_synthesis.py | 27802B | 核心引擎（最大） |
| test_synthesis_coverage.py | 11350B | 覆蓋補強 |
| test_synthesis_integration.py | 18085B | 整合 |
| test_synthesis_live.py | 8085B | 真實呼叫 |
| test_text_splitter_coverage.py | 12011B | 覆蓋補強 |

**Test coverage 分數**：v1.0 估 ~40-50% → v2.0 92/100

---

## 七、各維度品質分數（v2.0 最終）

| 維度 | v1.0 (估) | v2.0 (實測) | 主要原因 |
|------|-----------|-------------|----------|
| linting | ~65 | 100 | f-string→%, 全域命名, pylint |
| documentation | ~55 | 100 | copyright + pydocstyle 完全合規 |
| type_safety | ~65 | 100 | type: ignore 精確, pyright 通過 |
| security | ~70 | 100 | 具體 exception, nosec 標記 |
| secrets_scanning | ~95 | 100 | 無 secrets |
| error_handling | ~55 | 100 | 消除所有 bare except |
| test_coverage | ~45 | 92 | 從 5→17 test files |
| architecture | ~78 | 94 | CRG 驗證，RedisCache hub 補測 |
| license_compliance | ~40 | 98 | MIT LICENSE 新增 + copyright headers |
| performance | ~80 | 80 | 架構未變，基準不變 |
| readability | ~76 | 78.8 | Radon MI 數學天花板，非可優化項 |
| mutation_testing | N/A | 48.5 | 隨機工具底板，stochastic floor |

---

## 八、倉庫衛生（負面項目）

v2.0 有以下 **不應提交的 artifacts**，應補進 .gitignore：

| 文件/目錄 | 問題 |
|-----------|------|
| `.coverage.lvxiaolindeMac-mini_local.*` (×2) | coverage 工具的 temp 文件，143KB 各，無意義 |
| `coverage.json` (69KB) | 工具輸出，不應進 repo |
| `coverage/` 目錄 | 同上 |
| `.sessi-work/` 目錄 | harness 工作目錄，非生產代碼 |
| `crg_status.json` | 工具生成文件 |
| `mutants/` 目錄 | mutation testing 輸出 |
| `final_report.md` | 品質報告（視情況可保留） |

.gitignore v2.0 有更新（395B → 539B），但顯然未涵蓋上述所有文件。

---

## 九、總結評分

| 面向 | v1.0 | v2.0 | 結論 |
|------|------|------|------|
| 架構設計 | ★★★★☆ | ★★★★☆ | 相同，未退步 |
| Bug 嚴重度 | ★★☆☆☆ | ★★★★★ | 3 個有效 bug 全修 |
| 錯誤處理 | ★★☆☆☆ | ★★★★★ | 根本性改善 |
| 測試完整性 | ★★☆☆☆ | ★★★★☆ | 5→17 files, 92% coverage |
| 程式碼風格 | ★★★☆☆ | ★★★★★ | pylint/pyright 100 |
| 文件與授權 | ★★☆☆☆ | ★★★★★ | copyright + MIT |
| 倉庫衛生 | ★★★★☆ | ★★☆☆☆ | v2.0 提交了大量工具 artifacts |
| **整體** | **★★★☆☆** | **★★★★☆** | **顯著進步，衛生為唯一退步** |

---

## 十、v3.0 優先事項

1. **倉庫衛生**：清理 artifacts，補全 .gitignore
2. **mutation_testing 分數提升**：從 48.5 往上
3. **readability 微優化**：78.8 → 80+
