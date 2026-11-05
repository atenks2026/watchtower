# BLUEPRINT - WATCHTOWER (AI Security Analyzer)
# AHVO2-3 (AR) Output - T-05
# Ide: Watchtower - NAS-level Security Briefing Generator
# Track: Surveillance / Open Innovation
# Stack: Python + uliya-skill-kit (UGOS Official)

---

## 1. STACK TEKNIS

| Layer | Technology | Justification |
|---|---|---|
| **Language** | Python 3.10+ | UGOS Skill Creation Tool support, uliya-skill-kit native |
| **Skill Framework** | uliya-skill-kit (UGREEN Official) | Required by hackathon, handles CLI registration, agent orchestration |
| **AI Model** | NVIDIA Nemotron 3 Ultra (via NIM) | Primary: reasoning, code, VLM fallback. Free tier NIM. |
| **Fallback Model** | Nemotron 3.5 Super VL (multimodal) | Video frame analysis untuk Analyzer Agent |
| **Local Fallback** | Ollama (Nemotron 3 Ultra quantized) | Zero cost, privacy, no rate limit |
| **Deployment** | Skill Package ZIP (SKILL.md + references/) | Round 1: Pre-test package. Round 2: Install di NAS iDX6011 Pro |
| **Testing** | Local Python + UGOS simulator (starter kit) | No NAS needed Round 1 |

**No External Dependencies**: No pip packages beyond stdlib + uliya-skill-kit. No binaries, no external APIs.

---

## 2. ARSITEKTUR EXPERT AGENTS (3 Agents)

```
┌─────────────────────────────────────────────────────────────┐
│                    WATCHTOWER SKILL                         │
│  (User Natural Language → UGOS CLI → Expert Agents)         │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
       │  SCANNER    │ │  ANALYZER   │ │  REPORTER   │
       │   AGENT     │ │   AGENT     │ │   AGENT     │
       └─────────────┘ └─────────────┘ └─────────────┘
              │               │               │
              ▼               ▼               ▼
       UGOS Surveillance   UGOS Video       UGOS Knowledge
       (query events)      (extract clips)  (reason + write)
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                       UGOS Files
                       (save clips, write HTML)
```

### 2.1 Scanner Agent (Query Events)
| Aspek | Detail |
|---|---|
| **Role** | Terima natural language query → parse timeframe/filters → call UGOS Surveillance |
| **Input** | User query: "Show anomalies last 24h", "Person detections yesterday 18:00-22:00" |
| **UGOS Capability** | `Surveillance` → query camera events (motion, person, vehicle, etc.) |
| **Output** | Structured event list: `[{timestamp, camera_id, event_type, confidence, metadata}]` |
| **Error Handling** | No events found → clear message. Surveillance unavailable → fallback to Files scan. |

### 2.2 Analyzer Agent (Extract Clips)
| Aspek | Detail |
|---|---|
| **Role** | Terima event list → extract video clips ±30s around each event → save to /Security/ |
| **Input** | Event list dari Scanner Agent |
| **UGOS Capability** | `Video` → extract clips (seek to timestamp, duration). `Files` → write to `/Security/YYYY-MM-DD/` |
| **Output** | Clip files + metadata: `[{clip_path, event_ref, start_time, end_time, camera_id}]` |
| **Confirmation** | **WAJIB**: User approve sebelum write (UGOS requirement). Batch approval untuk multiple clips. |
| **Fallback** | Jika extract gagal (codec/seek) → copy full file + timestamp metadata di nama file. |

### 2.3 Reporter Agent (Generate Briefing)
| Aspek | Detail |
|---|---|
| **Role** | Terima events + clips → AI reasoning → generate HTML Security Briefing |
| **Input** | Events + clip metadata + user context (home/away, priority zones) |
| **UGOS Capability** | `Knowledge` → LLM reasoning (Nemotron). `Files` → write HTML report. |
| **Output** | `security_briefing_YYYYMMDD_HHMM.html` dengan: |
| | - Executive Summary (threat level, anomaly count) |
| | - Timeline visual (chronological events) |
| | - Embedded video clips (HTML5 `<video>` tags, play inline) |
| | - Per-camera summary |
| | - Recommendations (review zones, adjust sensitivity) |
| **Confirmation** | **WAJIB**: User approve sebelum write HTML report. |

---

## 3. CLI CAPABILITIES (UGOS Registered)

| Capability ID | Name | Description | Inputs | Confirmation |
|---|---|---|---|---|
| `watchtower.query_events` | Query Security Events | Natural language query untuk camera events | `query` (string), `timeframe` (optional), `filters` (optional) | No (read-only) |
| `watchtower.extract_clips` | Extract Event Clips | Extract video clips around events | `events` (array), `padding_seconds` (default 30), `output_folder` | **YES** (write) |
| `watchtower.generate_briefing` | Generate Security Briefing | AI-generated HTML report dengan clips | `events` (array), `clips` (array), `template` (optional) | **YES** (write) |

**Natural Language Triggers** (Examples):
- "Analyze security for last 24 hours"
- "Show me all person detections yesterday"
- "Generate security briefing for front door camera last week"
- "Extract clips for all vehicle detections today"

---

## 4. SKILL.MD SKELETON (Frontmatter + Sections)

```yaml
---
name: watchtower
description: "AI Security Analyzer: Natural language query → cross-camera anomaly detection → HTML security briefing with video clips. Turns unwatched footage into actionable security intelligence."
version: "1.0.0"
author: "AHVO2 Team"
license: "MIT"
tags: [surveillance, security, video-analysis, home-automation]
ugos_capabilities: [surveillance, video, knowledge, files]
---
```

**Sections Required**:
1. **User Goal** — "Help homeowners understand what their cameras actually recorded without watching hours of footage"
2. **Required Inputs** — Authorized footage folder, timeframe, optional filters (camera, event type)
3. **Supported CLI Capabilities** — 3 capabilities detailed above with examples
4. **Expert Agent Orchestration Workflow** — Scanner → Analyzer → Reporter (sequential, each uses previous output)
5. **Completion/Failure Handling** — 
   - Success: HTML report path + clip folder path
   - No events: "No security events found in timeframe. All quiet."
   - Partial failure: "Clips extracted but briefing generation failed: [reason]. Clips saved at [path]."
   - Permission denied: "User declined confirmation for [action]. Operation cancelled."
6. **Privacy & Security** — Face recognition opt-in only, local processing, no external calls

---

## 5. REPO STRUCTURE

```
watchtower/
├── SKILL.md                    # Required: frontmatter + all sections above
├── README.md                   # Conversational: for whom, how to use, example queries
├── references/
│   ├── extraction_schema.md    # JSON schema untuk event/clip/briefing structure
│   ├── prompt_templates.md     # Few-shot prompts untuk 3 expert agents
│   ├── privacy_notice.md       # Face recognition opt-in, UU PDP/GDPR/BIPA compliance
│   ├── error_handling.md       # Failure modes & recovery per agent
│   └── license_table.md        # Dependencies: uliya-skill-kit (UGREEN), Nemotron (NVIDIA)
└── (no scripts, no binaries, no external deps)
```

---

## 6. MILESTONES (M1-M6, Setiap ~4 Jam, Runnable)

| Milestone | Focus | Deliverable | Runnable Criteria |
|---|---|---|---|
| **M0** | Scaffold | Repo init, SKILL.md skeleton, hello-world CLI | `python -m watchtower --help` works |
| **M1** | Scanner Agent | `query_events` capability registered, returns mock events | Query "test" → structured event list |
| **M2** | Analyzer Agent | `extract_clips` capability, extracts ±30s clips (mock video) | Clips saved to /Security/, confirmation prompt works |
| **M3** | Reporter Agent | `generate_briefing` capability, generates HTML with embedded clips | HTML opens in browser, clips playable |
| **M4** | CLI Integration | 3 capabilities unified, natural language parsing, help text | `watchtower "analyze last 24h"` runs full flow |
| **M5** | Polish | HTML template, timeline, threat levels, video playback, error handling | Full flow works, edge cases handled |
| **M6** | E2E & Docs | README, README screenshots, README architecture diagram, README quickstart | Zero P0 bugs, README complete, Skill Package ZIP <10MB |

**Deploy Live at M1**: Vercel/Netlify preview URL untuk CLI demo (simulated).

---

## 7. FALLBACK PLAN (Per External Dependency)

| Dependency | Risk | Fallback |
|---|---|---|
| **NVIDIA NIM (Nemotron)** | Rate limit 429 / quota habis | Switch to OpenRouter (Llama 3.1 70B) → Ollama local |
| **UGOS Surveillance capability** | Tidak support query events seperti diharapkan | Fallback: Parse NVR export folder (MP4 + timestamp naming convention) via Files scan |
| **UGOS Video extract** | Codec tidak support / seek inaccurate | Fallback: Copy full file + rename dengan timestamp metadata |
| **UGOS Knowledge (LLM)** | Model tidak available | Fallback: Template-based briefing (no AI reasoning) — static sections only |
| **Write approvals** | User cancel confirmation | Graceful cancel: "Operation cancelled by user. Partial results at [path]." |

---

## 8. LICENSE TABLE

| Dependency | License | OK? | Attribution Needed |
|---|---|---|---|
| uliya-skill-kit | UGREEN Official (Apache-2.0 equivalent) | ✅ | Yes - "Built with UGREEN UGOS Skill Creation Tool" |
| NVIDIA Nemotron (via NIM) | NVIDIA License (Free tier) | ✅ | Yes - "Powered by NVIDIA Nemotron" |
| Python stdlib | PSF License | ✅ | No |
| **Skill Code (Watchtower)** | **MIT** (chosen by team) | ✅ | **Yes - "Copyright 2026 AHVO2 Team, MIT License"** |

**Third-party Disclosure**: None beyond above. No external pip packages, no binaries, no external APIs.

---

## 9. ERROR HANDLING MATRIX

| Scenario | Agent | Detection | Recovery | User Message |
|---|---|---|---|---|
| No events found | Scanner | Empty result | Return empty list + suggestion | "No security events found in timeframe. Try wider range or check camera status." |
| Surveillance capability unavailable | Scanner | Exception | Fallback to Files scan (NVR export folder) | "Live query unavailable. Scanning footage folder instead..." |
| Clip extraction failed (codec) | Analyzer | Exception | Copy full file + timestamp metadata | "Could not extract clip. Full recording saved at [path] with timestamp." |
| User declines confirmation | Analyzer/Reporter | User input = no | Cancel operation, return partial | "Operation cancelled. [X] clips saved at [path]." |
| LLM reasoning failed | Reporter | Exception/timeout | Template-based briefing (static) | "AI briefing unavailable. Generated standard report template." |
| HTML report write failed | Reporter | Exception | Save as Markdown fallback | "HTML write failed. Report saved as Markdown at [path]." |

---

## 10. PERFORMANCE TARGETS

| Metric | Target |
|---|---|
| Query events (100 events) | < 3 seconds |
| Extract 10 clips (±30s each) | < 10 seconds (depends on NAS I/O) |
| Generate briefing (10 events) | < 5 seconds (LLM) |
| Skill Package ZIP size | < 2 MB (well under 10 MB limit) |
| Files in package | < 20 (well under 100 limit) |
| Memory usage (NAS iDX6011 Pro) | < 512 MB RAM |

---

## 11. TEST CASES (Core + Edge)

### Core Test Cases (Harus PASS)
1. **Happy Path**: "Analyze last 24h" → events → clips → HTML briefing → user satisfied
2. **Empty Result**: "Analyze last hour" (no events) → clear message "All quiet"
3. **Confirmation Flow**: User declines clip extraction → graceful cancel, no partial writes

### Edge Cases (Harus HANDLE)
1. **Mixed Cameras**: Hikvision + Dahua + Uniview footage in same folder → all processed
2. **Large Timeframe**: "Analyze last 30 days" → batch processing, progress feedback
3. **Corrupt Video File**: One file unreadable → skip + log + continue others
4. **Permission Denied**: Folder not authorized → clear error + guide to authorize
5. **LLM Timeout**: Nemotron slow → fallback to template briefing

---

*Blueprint v1.0 — AHVO2-3 (AR) — Ready for T-06 Task Breakdown (AHVO2-1 PM)*
*Next: AHVO2-1 pecah jadi Task Board (T-06) + AHVO2-6 Story Sheet (T-11)*