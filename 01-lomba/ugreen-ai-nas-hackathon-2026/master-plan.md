# MASTER PLAN - WATCHTOWER (UGREEN AI NAS Hackathon 2026)
# F1 KICKOFF Output - AHVO2-1 (PM)
# Deadline: 2026-11-16 14:45 WIB (Round 1 Submission)
# Ide: Watchtower - AI Security Analyzer
# Track: Surveillance / Open Innovation

---

## 1. TIMELINE OVERVIEW (Dari Sekarang ke Deadline)

**Hari Tersisa**: ~14 hari (14 x 24 jam = 336 jam)
**Buffer Submit**: 6 jam (NON-NEGOTIABLE) → **Effective Deadline: 2026-11-16 08:45 WIB**

| Fase | Window (WIB) | Durasi | Focus |
|---|---|---|---|
| **F1 KICKOFF** | Sekarang - H+2j | 2 jam | Rules brief final, Legal/Finance gates, Master plan lock |
| **F2 IDEASI** | H+2j - H+6j | 4 jam | **SKIP** - Ide sudah terkunci (Watchtower) |
| **F3 ARSITEKTUR** | H+6j - H+10j | 4 jam | Blueprint Watchtower, SKILL.md skeleton, Task board, Story sheet |
| **F4 BUILD MVP** | H+10j - H+34j | 24 jam | 6 Increment (M1-M6) ~4 jam each, Deploy live tiap increment |
| **H+24j CHECKPOINT** | H+24j | 1 jam | Scope review, burn-down, quota check |
| **H+34j FEATURE FREEZE** | H+34j | - | No new features, bug fix only |
| **F5 QA & POLISH** | H+34j - H+42j | 8 jam | Bug burn-down P0→P1, Gate 12 butir (G11 Legal, G12 Finance) |
| **F6 DEMO & SUBMIT** | H+42j - H+48j | 6 jam | Video 90s, README, Devpost copy, Submit (buffer 6 jam) |
| **F7 POST-MORTEM** | +24 jam post-submit | 1 jam | Retro, lessons, archive |

---

## 2. WATCHTOWER - 3 FITUR INTI (MVP CAP)

| # | Fitur | CLI Capability | UGOS Capabilities | Demo Moment |
|---|---|---|---|---|
| **1** | **Query Events** | `query_events` | Surveillance (query camera events) + Files (list footage) | "Show me all person detections last 24h" |
| **2** | **Extract Clips** | `extract_clips` | Video (extract clips ±30s around events) + Files (save to /Security/) | "Save clips for all anomalies" |
| **3** | **Generate Briefing** | `generate_briefing` | Knowledge (AI analyze patterns → narrative) + Files (write HTML report) | "Generate security briefing" → HTML dengan embedded clips |

**Deferred (Post-Hackathon)**:
- `organize_security` (auto-move clips to dated folders) — high risk write ops
- Face recognition module (opt-in, privacy warning)
- Scheduled triggers (not supported by UGOS currently)

---

## 3. TASK BOARD (12 TASKS MAX)

| ID | Task | Phase | Owner | Effort | Acceptance Criteria | Status |
|---|---|---|---|---|---|---|
| **T-01** | Kickoff Watchtower | F1 | PM2 | S | Master plan done, Legal/Finance gates locked | **DOING** |
| **T-02** | Rubric Breakdown Surveillance | F1 | RA2 | S | Criteria mapped to 3 features, traps identified | **DOING** |
| **T-19** | Legal Finalize Watchtower | F1 | LC8 | S | Face rec opt-in, privacy notice, vendor EULA cleared | **DOING** |
| **T-20** | Finance Finalize | F1 | FI9 | S | Prize tracker, W-8BEN action item, tax verified | **DOING** |
| **T-05** | Blueprint Watchtower | F3 | AR3 | M | Stack, 3 expert agents, SKILL.md skeleton, fallback, license table | TODO |
| **T-06** | Task Breakdown | F3 | PM2 | S | 6 increments M1-M6, demo-path marked, gates scheduled | TODO |
| **T-11** | Story Sheet | F3 | DN6 | S | Name, tagline, hook, 3 features, demo flow 3 steps | TODO |
| **M1** | Scanner Agent (Surveillance Query) | F4 | DEV4 | M | `query_events` works: input timeframe → output event list with timestamps | TODO |
| **M2** | Analyzer Agent (Vision VLM) | F4 | DEV4 | M | `extract_clips` works: event list → video clips ±30s saved to /Security/ | TODO |
| **M3** | Reporter Agent (Knowledge Briefing) | F4 | DEV4 | M | `generate_briefing` works: events → HTML report dengan embedded clips | TODO |
| **M4** | CLI Integration & Search | F4 | DEV4 | S | 3 CLI caps registered, natural language parsing, help text | TODO |
| **M5** | HTML Briefing Polish | F4 | DEV4+DN6 | S | Report template, embedded video playback, timeline, threat levels | TODO |
| **M6** | End-to-End Polish | F4 | DEV4+QA5 | S | Full flow tested, error handling, confirmation gates, README | TODO |
| **T-09** | Test Plan & Review | F4 | QA5 | M | Each increment: test plan + diff review + bug list | TODO |
| **T-10** | Quality Gate 12 Butir | F5 | QA5 | L | G1-G12 PASS, G11 Legal, G12 Finance verified | TODO |
| **T-12** | Submission Copy | F5 | DN6 | S | Devpost title, what/how, challenges, AI disclosure | TODO |
| **T-13** | Demo Video Script | F5 | DN6 | S | 90s script, shot list, recording tips | TODO |
| **T-15** | Post-Mortem | F7 | PM2 | S | Scores, lessons, 3 process changes | TODO |

**Demo-Path Tasks (Priority)**: M1, M2, M3, M4, M5, M6, T-09, T-10
**Compliance Gates**: T-19 (G11), T-20 (G12) — **MUST PASS before F5**

---

## 4. GATES & CHECKPOINTS

| Gate | Owner | When | Criteria |
|---|---|---|---|
| **G11 Legal** | LC8 | F1 (now) + F5 (pre-submit) | Face rec opt-in, privacy notice, vendor EULA, UU PDP, no reverse engineering |
| **G12 Finance** | FI9 | F1 (now) + F5 (pre-submit) | Prize tracker, W-8BEN action, tax verified, $0 cost |
| **H+24 Checkpoint** | PM2 | H+24j | Scope vs reality, quota check, burn-down rate |
| **Feature Freeze** | PM2 | H+34j | No new features, demo-path locked |
| **Quality Gate** | QA5 | F5 | G1-G12 all PASS, 0 P0 bugs |

---

## 5. RISK REGISTER (Top 5)

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| 1 | **UGOS Surveillance capability limited** (can't query events as expected) | Medium | High | Fallback: parse NVR export files (MP4 + timestamp naming), manual folder scan | AR3/DEV4 |
| 2 | **Video extraction fails** (codec, seek accuracy) | Medium | High | Fallback: copy full file + timestamp metadata, user manual trim | DEV4 |
| 3 | **Vision VLM accuracy low** (false positives) | Medium | Medium | Confidence threshold, flag low-confidence for manual review | DEV4 |
| 4 | **Write approvals per file** (UGOS requires per-action approval) | High | Medium | Batch approval UX, clear confirmation messages | DEV4/DN6 |
| 5 | **W-8BEN not ready at win** | Low | Critical | **Founder action NOW** — download, fill, save ready | Founder/FI9 |

---

## 6. MODEL ROUTING (Per Watchtower Needs)

| Task Type | Model | Reason |
|---|---|---|
| Architecture/Blueprint (AR3) | Nemotron 3 Ultra | Complex reasoning, stack decisions |
| Code Implementation (DEV4) | Nemotron 3 Ultra | Coding capability, UGOS SDK patterns |
| Vision Analysis (Analyzer Agent) | Nemotron 3.5 Super VL | Multimodal - video frame analysis |
| Bulk Research (RA2) | Nemotron 3.5 Lightning | Fast, high-volume |
| Legal/Finance Analysis (LC8/FI9) | Nemotron 3 Ultra | Precision reasoning |
| Narrative/Copy (DN6) | Nemotron 3 Ultra | Creative writing, hook crafting |

**Fallback Chain**: NIM → OpenRouter (Llama 3.1 70B) → Ollama (Nemotron local)

---

## 7. CRON SHIFT ACTIVATION

Shift schedule aktif per `z.ai/cron-shift-schedule.md`:
- **PM2**: :00 start, 4h work / 1h break
- **RA2**: :05 start, 4h work / 1h break
- **AR3**: :10 start, 4h work / 1h break
- **DEV4**: :15 start, 4h work / 1h break
- **QA5**: :20 start, 4h work / 1h break
- **DN6**: :25 start, 4h work / 1h break
- **OPS7**: :30 start, 4h work / 1h break (dashboard always on)
- **LC8**: :35 start, 4h work / 1h break
- **FI9**: :40 start, 4h work / 1h break

**Daily**: BRIEFING 08:00, STATUS 20:00 (Asia/Jakarta)
**Weekly**: Contest Scan Mon 09:00 (RA2), Budget Review Fri 16:00 (FI9)
**Alarms**: H-24, H-6 auto-trigger

---

## 8. IMMEDIATE NEXT ACTIONS (Next 2 Hours)

| Action | Owner | Command/Deliverable |
|---|---|---|
| **1. Rubric Breakdown Surveillance** | RA2 | Output: criteria table + 10-item build checklist + 3 traps + Watchtower fit |
| **2. Legal Finalize** | LC8 | Output: Face rec opt-in spec, privacy notice draft, vendor EULA clearance note |
| **3. Finance Finalize** | FI9 | Output: W-8BEN template download link for Founder, tax rate verified |
| **4. Blueprint Start** | AR3 | After RA2/LC8/FI9 done: Watchtower blueprint (3 expert agents, SKILL.md skeleton) |
| **5. Repo Template** | OPS7 | GitHub repo init, hello-world deploy Vercel, URL live verified |

---

## 9. FOUNDER ACTION REQUIRED (URGENT)

| # | Action | Deadline | Link |
|---|---|---|---|
| **1** | **Download & fill Form W-8BEN** (IRS) | **SEKARANG** (before win) | https://www.irs.gov/forms-pubs/about-form-w-8ben |
| **2** | Siapkan: KTP/Paspor, NPWP, Bank details (SWIFT/BIC) | SEKARANG | - |
| **3** | Approve blueprint (F3) | H+6j (~8 jam) | Review di Hermes |
| **4** | Approve scope cut (H+24 checkpoint) | H+24j | Review di Hermes |
| **5** | Record demo video | H+42j | Follow DN6 shot list |
| **6** | Click Submit | H+48j - 6h buffer | Devpost |

---

## 10. DASHBOARD STATUS

- **Phase**: F1 KICKOFF
- **Mission**: UGREEN AI NAS Hackathon 2026 - Watchtower (Surveillance)
- **Deadline**: 2026-11-16 14:45 WIB (Countdown active)
- **Active Agents**: PM2, RA2, LC8, FI9, OPS7 (5/9 working)
- **Gates**: G11 Legal (DOING), G12 Finance (DOING)

---

*Master Plan v1.0 — AHVO2-1 (PM) — Auto-generated from SOP-01 Kickoff*
*Next Update: H+2j (F1 Complete) atau saat Blocker muncul*