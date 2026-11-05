# TASK BREAKDOWN - WATCHTOWER (from Blueprint)
# AHVO2-1 (PM) Output - T-06
# Source: Blueprint v1.0 (AHVO2-3 AR)
# Max 12 open tasks, demo-path marked, compliance gates included

---

## TASK BOARD (12 Tasks)

| ID | Task | Phase | Owner | Effort | Acceptance Criteria | Demo-Path |
|---|---|---|---|---|---|---|
| **T-01** | Kickoff Watchtower | F1 | PM2 | S | Master plan done, Legal/Finance gates locked | ❌ |
| **T-02** | Rubric Breakdown Surveillance | F1 | RA2 | S | Criteria mapped to 3 features, traps identified | ❌ |
| **T-19** | Legal Finalize Watchtower | F1 | LC8 | S | Face rec opt-in, privacy notice, vendor EULA cleared | ❌ |
| **T-20** | Finance Finalize | F1 | FI9 | S | Prize tracker, W-8BEN action item, tax verified | ❌ |
| **T-05** | Blueprint Watchtower | F3 | AR3 | M | Stack, 3 expert agents, SKILL.md skeleton, fallback, license table | ❌ |
| **T-06** | Task Breakdown | F3 | PM2 | S | 6 increments M1-M6, demo-path marked, gates scheduled | ❌ |
| **T-11** | Story Sheet | F3 | DN6 | S | Name, tagline, hook, 3 features, demo flow 3 steps | ❌ |
| **M1** | **Scanner Agent (Surveillance Query)** | F4 | DEV4 | M | `query_events` works: input timeframe → output event list with timestamps | ✅ **DEMO** |
| **M2** | **Analyzer Agent (Vision VLM + Clips)** | F4 | DEV4 | M | `extract_clips` works: event list → video clips ±30s saved to /Security/ | ✅ **DEMO** |
| **M3** | **Reporter Agent (Knowledge Briefing)** | F4 | DEV4 | M | `generate_briefing` works: events → HTML report dengan embedded clips | ✅ **DEMO** |
| **M4** | **CLI Integration & Search** | F4 | DEV4 | S | 3 CLI caps registered, natural language parsing, help text | ✅ **DEMO** |
| **M5** | **HTML Briefing Polish** | F4 | DEV4+DN6 | S | Report template, timeline, threat levels, video playback | ✅ **DEMO** |
| **M6** | **End-to-End Polish** | F4 | DEV4+QA5 | S | Full flow tested, error handling, confirmation gates, README | ✅ **DEMO** |
| **T-09** | Test Plan & Review | F4 | QA5 | M | Each increment: test plan + diff review + bug list | ❌ |
| **T-10** | Quality Gate 12 Butir | F5 | QA5 | L | G1-G12 PASS, G11 Legal, G12 Finance verified | ❌ |
| **T-12** | Submission Copy | F5 | DN6 | S | Devpost title, what/how, challenges, AI disclosure | ❌ |
| **T-13** | Demo Video Script | F5 | DN6 | S | 90s script, shot list, recording tips | ❌ |
| **T-15** | Post-Mortem | F7 | PM2 | S | Scores, lessons, 3 process changes | ❌ |

---

## DEMO PATH (Priority Order - NEVER CUT)

```
M1 → M2 → M3 → M4 → M5 → M6
     ↓      ↓      ↓      ↓      ↓      ↓
  Query   Clip    Brief   CLI     HTML   E2E
 Events  Extract Gen.    Parse  Polish  Test
```

**Rule**: Jika scope cut needed (H+24 checkpoint), urutan potong:
1. M5 Polish (bisa minimal template)
2. M4 CLI Integration (bisa basic parsing)
3. **M1-M3 CORE JANGAN DIPISANGKAN** — ini demo path

---

## MILESTONE DETAIL (Per Increment ~4 Jam)

### M0 - Scaffold (H+10j, sebelum M1)
| Item | Detail |
|---|---|
| **Repo** | GitHub: `AHVO2/watchtower` (private → public at submit) |
| **Structure** | `watchtower/` + `references/` per blueprint |
| **SKILL.md** | Skeleton dengan frontmatter + section headers |
| **CLI Entry** | `python -m watchtower --help` works |
| **Deploy** | Vercel preview URL live (simulated CLI demo) |
| **Owner** | OPS7 + DEV4 |
| **Done Criteria** | `git clone` → `pip install -e .` → `watchtower --help` → success |

### M1 - Scanner Agent (H+10j to H+14j)
| Item | Detail |
|---|---|
| **Capability** | `watchtower.query_events` registered |
| **Input Parsing** | Natural language → timeframe (last 24h, yesterday, custom), filters (camera, event_type) |
| **UGOS Call** | Surveillance capability: query events (mock untuk Round 1) |
| **Output** | Structured: `[{ts, camera_id, event_type, confidence, metadata}]` |
| **Error Cases** | No events, capability unavailable, invalid timeframe |
| **Test** | Query "last 24h" → returns mock event list |
| **Owner** | DEV4 |
| **QA** | T-09: Test plan (happy + 5 edge), diff review |

### M2 - Analyzer Agent (H+14j to H+18j)
| Item | Detail |
|---|---|
| **Capability** | `watchtower.extract_clips` registered |
| **Input** | Event list dari M1 |
| **UGOS Call** | Video capability: extract clips ±30s. Files: write to `/Security/YYYY-MM-DD/` |
| **Confirmation** | **Batch approval prompt** sebelum write multiple clips |
| **Output** | Clip files + metadata JSON |
| **Fallback** | Codec fail → copy full file + timestamp in filename |
| **Test** | Extract 3 clips → saved to /Security/, confirmation works |
| **Owner** | DEV4 |
| **QA** | T-09: Test plan, diff review |

### M3 - Reporter Agent (H+18j to H+22j)
| Item | Detail |
|---|---|
| **Capability** | `watchtower.generate_briefing` registered |
| **Input** | Events + clips metadata |
| **UGOS Call** | Knowledge (Nemotron) → reasoning. Files: write HTML |
| **Confirmation** | **Single approval** sebelum write HTML report |
| **Output** | `security_briefing_YYYYMMDD_HHMM.html` |
| **Template** | Executive Summary, Timeline, Embedded Clips, Per-Camera, Recommendations |
| **Test** | Generate briefing → HTML opens, clips play inline |
| **Owner** | DEV4 |
| **QA** | T-09: Test plan, diff review |

### M4 - CLI Integration (H+22j to H+26j)
| Item | Detail |
|---|---|
| **Natural Language Parsing** | "Analyze last 24h" → auto-detect capability chain |
| **Help Text** | `watchtower --help` shows 3 capabilities + examples |
| **Error Messages** | Human-readable: "No events found. Try: watchtower 'last 48 hours'" |
| **Progress Feedback** | Spinner/status untuk long operations |
| **Owner** | DEV4 |
| **QA** | T-09: Test plan, diff review |

### M5 - HTML Polish (H+26j to H+30j)
| Item | Detail |
|---|---|
| **Template** | Responsive HTML5, CSS embedded, dark/light mode |
| **Timeline** | Visual chronological events (CSS/JS) |
| **Video Playback** | HTML5 `<video>` tags, inline play, thumbnail preview |
| **Threat Levels** | Color-coded: Critical/High/Medium/Low/Info |
| **Per-Camera Summary** | Expandable sections per camera |
| **Owner** | DEV4 + DN6 (design) |
| **QA** | T-09: Test plan, diff review |

### M6 - E2E Polish (H+30j to H+34j)
| Item | Detail |
|---|---|
| **Full Flow Test** | "Analyze last 24h" → events → clips → briefing → zero manual steps |
| **Confirmation Gates** | All write ops: batch clips approval, single briefing approval |
| **Error Handling** | All matrix scenarios (empty, corrupt, permission, timeout) |
| **README** | Quickstart 3 commands, architecture diagram (mermaid), screenshots, env vars |
| **Skill Package** | ZIP < 10MB, < 100 files, SKILL.md + references/ |
| **Owner** | DEV4 + QA5 |
| **QA** | T-09: Final test plan, T-10: Quality Gate 12 butir |

---

## COMPLIANCE GATES (Scheduled)

| Gate | Task | Phase | Owner | When |
|---|---|---|---|---|
| **G11 Legal** | T-19 | F1 (done) + F5 | LC8 | Pre-submit re-verify |
| **G12 Finance** | T-20 | F1 (done) + F5 | FI9 | Pre-submit re-verify |
| **H+24 Checkpoint** | - | F4 | PM2 | Scope vs reality, quota, burn-down |
| **Feature Freeze** | - | F4 | PM2 | H+34j — no new features after |
| **Quality Gate** | T-10 | F5 | QA5 | All G1-G12 PASS, 0 P0 |

---

## RESOURCE ALLOCATION (Per Shift)

| Agent | Primary Task | Shift Hours |
|---|---|---|
| **DEV4** | M1→M6 sequential | 24 jam total (6 increments × 4 jam) |
| **QA5** | T-09 per increment + T-10 final | 8 jam review + 4 jam final gate |
| **DN6** | T-11, M5, T-12, T-13 | 4 jam story + 4 jam HTML + 4 jam copy/video |
| **OPS7** | M0 repo, deploy, M6 package, submit | 4 jam setup + 4 jam package/submit |
| **PM2** | T-06, T-06 board sync, H+24 checkpoint, H+34 freeze | 2 jam planning + 2 jam monitoring |
| **LC8/FI9** | T-19/T-20 re-verify at F5 | 1 jam each |
| **RA2/AR3** | Standby (done F1/F3) | Available for consultation |

---

*Task Breakdown v1.0 — AHVO2-1 (PM) — Ready for F4 Build*
*Next: AHVO2-7 (OPS) M0 Scaffold + Deploy Hello-World*