# ROUND 2 SURVIVAL SPRINT — 24 JAM INTEGRASI iDX6011 Pro
# Sprint Plan: H-24 jam sebelum Round 2 testing day
# Tim: AHVO2 Full Team (9 agents + Founder)
# Target: Skill berjalan FLUENT di iDX6011 Pro, demo video recorded, submit ready

---

## 🎯 SPRINT GOAL

> **Skill Watchtower berjalan FLUENT di iDX6011 Pro (UGOS real), demo video 90s recorded, Skill Package final submitted ke Devpost.**

**Definition of Done:**
- [ ] Pipeline end-to-end jalan di iDX6011 Pro (real UGOS APIs)
- [ ] Zero P0 bugs, zero OOM, zero crash
- [ ] Demo video 90s recorded di hardware real
- [ ] Skill Package final uploaded ke Devpost
- [ ] Devpost form 100% complete, SUBMIT clicked

---

## ⏰ SPRINT TIMELINE (24 JAM)

```
JAM 0-2   : SETUP & HARDWARE VALIDATION
JAM 2-6   : UGOS API INTEGRATION (REAL)
JAM 6-10  : PIPELINE HARDENING (OOM, ERROR HANDLING)
JAM 10-14 : FULL PIPELINE TEST & BUG BURN
JAM 14-18 : DEMO VIDEO RECORDING (REAL HARDWARE)
JAM 18-22 : FINAL PACKAGE & SUBMIT PREP
JAM 22-24 : BUFFER & SUBMIT
```

---

## 📋 DETAILED SPRINT BACKLOG

### JAM 0-2: SETUP & HARDWARE VALIDATION

| Task ID | Task | Owner | Acceptance Criteria | Duration |
|---------|------|-------|---------------------|----------|
| R2-01 | Flash iDX6011 Pro, boot UGOS | OPS7 | Device boots, SSH accessible, UGOS version confirmed | 30 min |
| R2-02 | Test `ugos.surveillance.get_camera_list()` | DEV4 | Returns camera list with IDs, names, status | 30 min |
| R2-03 | Test `ugos.surveillance.get_event_records()` | DEV4 | Returns events with timestamp, type, confidence | 30 min |
| R2-03 | Test `ugos.video.extract_clip()` | DEV4 | Extracts clip ±30s, saves to /Security/ | 30 min |
| R2-04 | Test `ugos.knowledge.generate()` (Nemotron) | DEV4 | Returns AI reasoning, <5s latency | 30 min |
| R2-05 | Test `ugos.files.write()` + confirmation | DEV4 | Write works, confirmation prompt appears | 30 min |
| R2-06 | Document ALL actual API signatures | DEV4 | `references/ugos-real-api.md` complete | 30 min |
| R2-07 | Verify storage space, RAM, CPU | OPS7 | >1GB free RAM, >5GB free storage | 15 min |
| R2-08 | Setup monitoring (htop, log tail) | OPS7 | Real-time monitoring active | 15 min |

**Exit Criteria Jam 2:** All UGOS APIs validated, actual signatures documented, zero surprises.

---

### JAM 2-6: UGOS API INTEGRATION (REAL)

| Task ID | Task | Owner | Acceptance Criteria | Duration |
|---------|------|-------|---------------------|----------|
| R2-10 | Replace ScannerAgent mock → real `ugos.surveillance` | DEV4 | `query_events()` calls real API, returns real events | 60 min |
| R2-11 | Implement Hikvision/Dahua/Reolink filename parsers | DEV4 | Parses 3+ vendor formats correctly | 60 min |
| R2-12 | Implement NVR export folder scanner fallback | DEV4 | Scans /mnt/cameras/, extracts events from filenames | 60 min |
| R2-13 | Replace AnalyzerAgent mock → real `ugos.video.extract_clip()` | DEV4 | Extracts ±30s clips, handles codec errors | 60 min |
| R2-14 | Implement codec fallback (HEVC→copy full file) | DEV4 | HEVC files copied with timestamp metadata | 45 min |
| R2-15 | Replace ReporterAgent mock → real `ugos.knowledge.generate()` | DEV4 | Nemotron generates briefing, <10s | 60 min |
| R2-16 | Implement streaming HTML generator (yield) | DEV4 | `generate_streaming()` yields chunks, <50MB RAM | 60 min |
| R2-17 | Wire per-file UGOS confirmation flow | DEV4 | Sequential confirmations, progress shown | 45 min |
| R2-18 | Implement model fallback chain (NIM→OpenRouter→Ollama) | DEV4 | Auto-switch on 429/timeout, logged | 45 min |

**Exit Criteria Jam 6:** All agents call REAL UGOS APIs, zero mocks, fallback chains work.

---

### JAM 6-10: PIPELINE HARDENING

| Task ID | Task | Owner | Acceptance Criteria | Duration |
|---------|------|-------|---------------------|----------|
| R2-20 | Implement streaming HTML generator (yield chunks) | DEV4 | 500 events <50MB RAM, yields chunks | 60 min |
| R2-21 | Add comprehensive error handling (24 codes) | DEV4 | All error codes handled, user messages clear | 60 min |
| R2-22 | Implement model fallback chain (NIM→OpenRouter→Ollama) | DEV4 | Auto-switch on 429/timeout, logged | 45 min |
| R2-23 | Add input validation + sanitization | DEV4 | NLP injection prevented, path traversal blocked | 30 min |
| R2-23 | Add timeout handling (30s per API call) | DEV4 | No hanging, graceful timeout | 30 min |
| R2-24 | Add retry logic with exponential backoff | DEV4 | 3 retries, exponential backoff, jitter | 30 min |
| R2-25 | Add structured logging (JSON lines) | DEV4 | All operations logged, queryable | 30 min |
| R2-26 | Add health check endpoint | DEV4 | `/health` returns component status | 30 min |
| R2-27 | Add resource monitoring (RAM, CPU, disk) | OPS7 | Alerts at 80% RAM, 90% disk | 30 min |

**Exit Criteria Jam 10:** Zero unhandled exceptions, streaming works, monitoring active.

---

### JAM 10-14: FULL PIPELINE TEST & BUG BURN

| Task ID | Task | Owner | Acceptance Criteria | Duration |
|---------|------|-------|---------------------|----------|
| R2-30 | Test full pipeline: `watchtower --test "analyze last 24h"` | QA5 | End-to-end works, 16 events → 16 clips → HTML | 60 min |
| R2-31 | Test complex query: `"person detections yesterday 18-22 front door"` | QA5 | Filters work, correct events returned | 30 min |
| R2-32 | Test edge: empty events (no detections) | QA5 | "All quiet" message, no crash | 15 min |
| R2-33 | Test edge: codec failure (HEVC) | QA5 | Falls back to full file copy | 30 min |
| R2-34 | Test edge: permission denied | QA5 | Clear error, graceful degradation | 15 min |
| R2-35 | Test edge: disk full simulation | QA5 | Graceful error, no corruption | 30 min |
| R2-36 | Test edge: model timeout (30s) | QA5 | Falls back to next model | 30 min |
| R2-37 | Test edge: model rate limit (429) | QA5 | Switches to next provider | 30 min |
| R2-38 | Test edge: UGOS API down | QA5 | Falls back to NVR export parser | 30 min |
| R2-39 | Test confirmation: user declines clips | QA5 | Cancels gracefully, partial results | 15 min |
| R2-40 | Test confirmation: user declines briefing | QA5 | Cancels, clips preserved | 15 min |
| R2-41 | Load test: 100 events, 500 events | QA5 | <50MB RAM, <30s total | 60 min |
| R2-42 | Bug burn: fix ALL P0/P1 bugs | DEV4 | Zero P0, zero P1 remaining | 60 min |

**Exit Criteria Jam 14:** Zero P0/P1 bugs, all edge cases handled, load test passes.

---

### JAM 14-18: DEMO VIDEO RECORDING (REAL HARDWARE)

| Task ID | Task | Owner | Acceptance Criteria | Duration |
|---------|------|-------|---------------------|----------|
| R2-50 | Prepare demo script + shot list | DN6 | Shot list printed, commands ready | 15 min |
| R2-51 | Setup recording: OBS + microphone test | Founder | 1080p, clear audio, no notifications | 15 min |
| R2-52 | Record Shot 1: Hook (split screen) | Founder | 5s, clean, text readable | 10 min |
| R2-53 | Record Shot 2: Terminal query | Founder | `watchtower "analyze last 24h"` typed | 10 min |
| R2-54 | Record Shot 3: Event table scroll | Founder | 15s, highlight confidence/camera | 10 min |
| R2-55 | Record Shot 4: Extract clips + folder | Founder | Progress bar, folder opens, MP4s | 15 min |
| R2-56 | Record Shot 5: HTML briefing scroll | Founder | Scroll summary→timeline→play clip | 20 min |
| R2-57 | Record Shot 6: Closing card | Founder | Logo, tagline, QR, 5s hold | 10 min |
| R2-58 | Retake worst shot (1x max) | Founder | One retake max per shot | 15 min |
| R2-59 | Edit: DaVinci Resolve + import SRT | Founder | 90s, 1080p, captions burned | 60 min |
| R2-60 | Export: 1080p MP4, H.264, AAC | Founder | <100MB, YouTube ready | 15 min |
| R2-61 | Upload YouTube (Unlisted → Public) | Founder | Link copied, thumbnail set | 15 min |

**Exit Criteria Jam 18:** 90s demo video uploaded to YouTube, link in submission.

---

### JAM 18-22: FINAL PACKAGE & SUBMIT PREP

| Task ID | Task | Owner | Acceptance Criteria | Duration |
|---------|------|-------|---------------------|----------|
| R2-70 | Final Skill Package build (ZIP) | OPS7 | 37.9 KB, 21 files, skill.json, icon, screenshots | 30 min |
| R2-71 | Verify ZIP contents: skill.json, icon, screenshots | OPS7 | All required assets present | 15 min |
| R2-72 | Convert submission-copy.md → PDF (≤1MB, ≤500 words) | DN6 | PDF ≤1MB, word count ≤500 | 15 min |
| R2-73 | Final Devpost form fill (all fields) | Founder | All fields complete, AI disclosure checked | 30 min |
| R2-74 | Upload Skill Package ZIP to Devpost | Founder | Upload succeeds, file validated | 15 min |
| R2-75 | Upload YouTube video link to Devpost | Founder | Link works, video plays | 10 min |
| R2-76 | Upload GitHub repo link to Devpost | Founder | `https://github.com/atenks2026/watchtower` | 5 min |
| R2-77 | Final verification: all Devpost fields green | Founder | Zero red fields | 15 min |
| R2-78 | Create Release v1.0.0 on GitHub | OPS7 | Tag v1.0.0, release notes | 15 min |

**Exit Criteria Jam 22:** Devpost form 100% complete, all assets uploaded.

---

### JAM 22-24: BUFFER & SUBMIT

| Task ID | Task | Owner | Acceptance Criteria | Duration |
|---------|------|-------|---------------------|----------|
| R2-80 | Buffer: fix any last-minute bugs | DEV4 | Zero new bugs introduced | 60 min |
| R2-81 | Buffer: re-record video if needed | Founder | One re-record max | 30 min |
| R2-82 | Final Devpost review (checklist) | Founder | 47-item checklist all ✅ | 30 min |
| R2-83 | **CLICK SUBMIT** | **Founder** | **SUBMIT CONFIRMED** | **5 min** |
| R2-84 | Screenshot confirmation | Founder | Screenshot saved | 5 min |
| R2-85 | Team celebration 🎉 | All | - | 30 min |

---

## 🚨 RISK REGISTER & MITIGATION

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| UGOS Surveillance API different from assumed | HIGH | CRITICAL | Fallback: NVR export parser implemented | DEV4 |
| Video extraction fails on ARM | HIGH | HIGH | Fallback: full file copy + timestamp | DEV4 |
| OOM on HTML generation | HIGH | HIGH | Streaming generator implemented | DEV4 |
| Nemotron rate limit (429) | MEDIUM | HIGH | Fallback chain: NIM→OpenRouter→Ollama | DEV4 |
| Video codec unsupported (HEVC) | MEDIUM | HIGH | Fallback: full file copy + timestamp | DEV4 |
| UGOS confirmation per-file (not batch) | LOW | MEDIUM | Implemented sequential confirm | DEV4 |
| Real hardware demo fails | LOW | CRITICAL | Pre-recorded backup video ready | DN6 |
| Devpost submit fails (network) | LOW | CRITICAL | Submit 6hr buffer, retry logic | Founder |
| Skill Package validation fails | LOW | CRITICAL | Pre-validated with schema | OPS7 |

---

## 📊 DAILY STANDUP FORMAT (Every 2 Hours)

```
TIME: [HH:MM]
PM2: "Status check - all agents report in 30 seconds"
DEV4: "R2-XX done, R2-YY in progress, blocker: [X]"
QA5: "R2-XX passed, R2-YY failed: [detail]"
OPS7: "Hardware: RAM 45%, Disk 60%, CPU 30%"
DN6: "Video: Shot X done, Shot Y next"
LC8: "Legal: [any new risk]"
FI9: "Finance: [no change]"
PM2: "Next 2h focus: [priority]. Blockers resolved: [Y/N]"
```

---

## 🎯 SPRINT SUCCESS METRICS

| Metric | Target | Measurement |
|--------|--------|-------------|
| **P0 Bugs** | 0 | QA5 verification |
| **P1 Bugs** | 0 | QA5 verification |
| **Pipeline Success Rate** | 100% | 5/5 test runs pass |
| **Memory Usage** | <100MB | 500 events load test |
| **Pipeline Latency** | <30s | 500 events end-to-end |
| **Demo Video** | 90s ±5s | YouTube link valid |
| **Skill Package** | <10MB | ZIP validated |
| **Devpost Submit** | Before deadline | Screenshot confirmed |

---

## 🚨 ESCALATION PATH

```
Blocker found → DEV4 investigates (15 min)
         ↓
   Can't fix in 30 min → PM2 escalates to Founder
         ↓
   Founder decides: workaround / cut scope / accept risk
         ↓
   Decision logged in progress-log.md
         ↓
   Team continues parallel work
```

---

## 🎯 SPRINT SUCCESS = SUBMIT CONFIRMED

> **Definition of Sprint Success:** `git tag v1.0.0` pushed, Devpost SUBMIT clicked, screenshot saved, team celebrates.

---

*Sprint Plan v1.0 - Generated by AHVO2-PM | Round 2 Survival Sprint | 24 Hours to Glory*