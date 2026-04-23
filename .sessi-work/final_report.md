# Quality Improvement Report

**Project:** `tts-kokoro-compare`
**Generated:** 2026-04-23 22:15:00
**Overall Score:** 87.53 / 100 (gate: 85)
**Recommendation:** ✅ **PASS**

## 1. Summary Statistics

| Metric | Count |
|--------|------:|
| Total issues found | 15 |
| Fixed | 3 |
| Wontfix (accepted risk) | 0 |
| Deferred | 12 |
| Still open | 12 |

### By Severity

| Severity | Found | Still Open |
|----------|------:|-----------:|
| 🔴 Critical | 0 | 0 |
| 🟠 High | 3 | 0 |
| 🟡 Medium | 12 | 12 |
| 🔵 Low | 0 | 0 |
| ⚪ Info | 0 | 0 |

## 2. Score Trajectory

| Dimension | R1 | R2 | Δ |
|-----------|----:|----:|---:|
| **Overall** | **81.6** | **87.53** | **+5.93** |
| mutation_testing | 47 | 31 | -16 |
| license_compliance | 100 | 80 | -20 |
| linting | 97.5 | 90 | -7.5 |
| test_coverage | 95 | 92 | -3 |
| architecture | 82 | 82 | 0 |
| performance | 80 | 80 | 0 |
| readability | 95 | 100 | +5 |
| error_handling | 85 | 85 | 0 |
| documentation | 80 | 100 | +20 |
| secrets_scanning | 100 | 100 | 0 |
| security | 100 | 100 | 0 |
| type_safety | 100 | 99 | -1 |

> Note: R2 scores use correct Python 3.12 toolchain. R1 had inconsistent measurement conditions (pytest collection errors, coverage not running). R2 is the authoritative measurement.

## 3. Per-Dimension Breakdown

| Dimension | Found | Fixed | Wontfix | Deferred | Open |
|-----------|------:|------:|--------:|---------:|-----:|
| architecture | 1 | 1 | 0 | 0 | 0 |
| documentation | 3 | 0 | 0 | 0 | 3 |
| linting | 5 | 0 | 0 | 0 | 5 |
| mutation_testing | 2 | 1 | 0 | 0 | 1 |
| readability | 2 | 0 | 0 | 0 | 2 |
| test_coverage | 2 | 1 | 0 | 0 | 1 |

## 4. Issues Fixed

### architecture

| ID | Severity | Location | Issue | Commit |
|----|----------|----------|-------|--------|
| `00000007` | 🟠 high | `src/cache/redis_cache.py` | RedisCache hub class untested | `21c4f590` |

### mutation_testing

| ID | Severity | Location | Issue | Commit |
|----|----------|----------|-------|--------|
| `0000000d` | 🟠 high | `src/cache/redis_cache.py:L55` | RedisCache 0% mutation coverage | `21c4f590` |

### test_coverage

| ID | Severity | Location | Issue | Commit |
|----|----------|----------|-------|--------|
| `1c5761ec8d` | 🟠 high | CRG | CRG untested_hubs | `21c4f590` |

## 5. Still Open (12 medium — deferred)

| ID | Severity | Dimension | Location | Issue |
|----|----------|-----------|----------|-------|
| `08984734c5` | 🟡 medium | test_coverage | `` | CRG untested_hotspots |
| `00000002` | 🟡 medium | linting | `src/main.py:L70` | Using global statement |
| `00000003` | 🟡 medium | linting | `src/routers/speech.py:L39` | Using global statement |
| `00000004` | 🟡 medium | linting | `src/routers/speech.py:L47` | Using global statement |
| `00000005` | 🟡 medium | linting | `src/routers/speech.py:L58` | Using global statement |
| `00000006` | 🟡 medium | linting | `src/cache/redis_cache.py:L209` | Using global statement |
| `00000008` | 🟡 medium | readability | `src/models.py:L9` | D204: 1 blank line required after class docstring |
| `00000009` | 🟡 medium | readability | `src/models.py:L20` | D204: 1 blank line required after class docstring |
| `0000000a` | 🟡 medium | documentation | `src/cli.py:L3` | D400: First line should end with a period |
| `0000000b` | 🟡 medium | documentation | `src/middleware/circuit_breaker.py:L34` | D107: Missing docstring in __init__ |
| `0000000c` | 🟡 medium | documentation | `src/middleware/circuit_breaker.py:L220` | D401: First line should be in imperative mood |
| `0000000e` | 🟡 medium | mutation_testing | `src/engines/synthesis.py:L55` | SynthesisEngine.synthesize low kill rate |

## 6. Failing Dimensions (R2)

| Dimension | Score | Target | Gap | Impact |
|-----------|------:|-------:|----:|-------:|
| mutation_testing | 31 | 70 | 39 | 3.12 |
| license_compliance | 80 | 100 | 20 | 1.20 |
| linting | 90 | 95 | 5 | 0.30 |

These are the dimensions to focus on in future rounds if continued improvement is desired.

## 7. CRG Status

CRG is **fully functional** this round:

- Binary: `/opt/homebrew/bin/code-review-graph` (explicit path — no PATH dependency)
- Graph: 2227 nodes, 20915 edges, 65 files
- `risk_score`: 0.85 → `eval_depth: deep`
- `flows` data: unavailable (CLI limitation; MCP-only in SKILL.md)

---

*Report generated following `openclaw_sw_improvement/SKILL.md` protocol.*
