# QUOTA LOG AHVO2 - PEMAKAIAN MODEL FREE TIER
# Dicatat AHVO2-7 (T-18) tiap hari lomba. Format: timestamp | model | role | tokens/credits | action taken

## Header
- Lomba: UGREEN AI NAS Hackathon 2026
- Primary: NVIDIA Nemotron via NVIDIA NIM (rate limit ~40 req/min, no token billing)
- Fallback 1: OpenRouter free tier (~20 req/min, 50 req/day free models)
- Fallback 2: Ollama lokal (unlimited, butuh RAM/VRAM)

## Log Harian (Contoh Format)
```
2026-11-02 08:00 | NVIDIA Nemotron 3 Ultra | PM (planning) | ~5k tokens | OK
2026-11-02 08:30 | NVIDIA Nemotron 3 Ultra | RA (rules extract) | ~15k tokens | OK
2026-11-02 09:00 | NVIDIA Nemotron 3.5 Lightning | RA (bulk scan) | ~8k tokens | OK
2026-11-02 10:00 | NVIDIA Nemotron 3 Ultra | AR (blueprint) | ~12k tokens | OK
2026-11-02 14:00 | NVIDIA Nemotron 3 Ultra | DEV (coding M1) | ~25k tokens | OK
2026-11-02 18:00 | NVIDIA Nemotron 3 Ultra | QA (gate review) | ~10k tokens | OK
2026-11-02 20:00 | NVIDIA Nemotron 3.5 Lightning | PM (status) | ~3k tokens | OK
--- DAILY TOTAL NIM: ~78k tokens equivalent, ~85 requests ---
```

## Warning Thresholds (AHVO2-7 monitor via T-18)
- NIM: >70% rate limit (28 req/min sustained) → switch bulk work to OpenRouter
- OpenRouter free: >70% daily quota (35 req/day) → switch to Ollama
- Ollama: RAM/VRAM >85% → reduce context, batch smaller

## Action Log (Model Switching)
| Timestamp | From Model | To Model | Reason | Agent Affected |
|---|---|---|---|---|
| *Belum ada switching* | | | | |

## Quota Summary (Update tiap STATUS malam)
| Model | Requests Today | Est. Tokens | % Limit | Status |
|---|---|---|---|---|
| NVIDIA NIM (Nemotron) | 0 | 0 | 0% | READY |
| OpenRouter Free | 0 | 0 | 0% | READY |
| Ollama Local | 0 | 0 | 0% | READY (not running) |

## Catatan
- NIM free tier = rate-based (40 req/min), bukan token-based. Risiko utama = 429 (too many requests).
- Displin T-18: jangan retry ke 429, switch model via `hermes model` command.
- AHVO2-7 log ke file ini + kirim angka ke AHVO2-9 untuk ledger.
- Founder review di STATUS malam (20:00 WIB).