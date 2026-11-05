# RUBRIC BREAKDOWN - SURVEILLANCE TRACK / WATCHTOWER
# AHVO2-2 (RA) Output - T-02
# Sumber: UGREEN Official Rules, Devpost, Starter Kit, Skills Hub
# Label: VERIFIED / ASSUMPTION

---

## 1. JUDGING CRITERIA (Official - 4 Kriteria, asumsi bobot ~25% each)

| Kriteria | Deskripsi Resmi | Bobot Estimasi | Watchtower Mapping |
|---|---|---|---|
| **User Value** | Does the Skill solve a clear user problem? Does it give users a clear workflow, useful feedback, and a real result? | ~25% | **Hook**: "Kamera ada, tapi footage tidak pernah di-review" → Watchtower = "Security briefing otomatis" |
| **Innovation & Differentiation** | Does the Skill offer a new function, interaction, or workflow that is different from common AI tools and existing solutions? | ~25% | **First** surveillance automation skill di Skills Hub. Vendor analytics = camera-level real-time. Watchtower = NAS-level post-processing + natural language + HTML briefing |
| **Technical Quality** | Do the core and repeat-use cases work? Does the Skill handle errors and edge cases? Does it manage data, permissions, credentials, outside services, and versions well? Do the docs and dependencies support install, setup, removal, and testing? | ~25% | 3 CLI caps, confirmation gates, error handling, offline-first, no external deps |
| **AI NAS Fit & Validation** | Do UGREEN AI NAS features add real value to the Skill? Does the Skill use NAS resources well? | ~25% | **Chain 4 capabilities**: Surveillance → Video → Knowledge → Files. Local processing, privacy-first |

---

## 2. 10-ITEM BUILD CHECKLIST (Criteria → Feature/Artifact)

| # | Kriteria | Build Artifact / Feature | Demo Evidence |
|---|---|---|---|
| 1 | User Value | **Natural language query**: "Show anomalies last 24h" | User ketik/voice → instant event list |
| 2 | User Value | **Actionable output**: HTML Security Briefing dengan video clips | User baca report → lihat clips → paham situasi |
| 3 | User Value | **Clear workflow**: Query → Extract → Briefing (3 langkah) | Demo 90s: 3 langkah selesai |
| 4 | Innovation | **First surveillance automation skill** | Skills Hub search: 0 hasil "surveillance analysis" |
| 5 | Innovation | **NAS-level post-processing** (vs camera-level) | Cross-camera, cross-vendor, historical |
| 6 | Innovation | **Natural language interface** (vs rule-based config) | "Show me..." bukan setup tripwire di NVR |
| 7 | Technical Quality | **3 CLI capabilities** registered & working | `query_events`, `extract_clips`, `generate_briefing` |
| 8 | Technical Quality | **Confirmation gates** sebelum write (UGOS requirement) | User approve sebelum save clips/report |
| 9 | Technical Quality | **Error handling**: low confidence, codec fail, permission denied | Graceful degradation, user feedback |
| 10 | AI NAS Fit | **4 Capabilities Chained**: Surveillance→Video→Knowledge→Files | Diagram alur di README + live demo |

---

## 3. TOP 3 TRAPS (Teams Akan Miss)

| # | Trap | Deskripsi | Watchtower Mitigasi |
|---|---|---|---|
| **1** | **Mengira UGOS Surveillance = Real-time Detection** | Banyak tim akan coba bikin "real-time alert" tapi UGOS skill **hanya on-demand** (no scheduled triggers, no webhooks). Forum Devpost confirm: skill hanya jalan saat user request. | Watchtower = **Post-incident analysis** ("Analyze last 24h"), bukan real-time. Design for on-demand. |
| **2** | **Write Operations Tanpa Confirmation** | UGOS **wajib user confirmation** per write action (copy, move, write). Tim yang auto-write akan fail compliance. Forum: "How often is user asked to approve?" | Setiap `extract_clips` & `generate_briefing` → **explicit confirmation prompt**. Batch approval UX. |
| **3** | **Menggunakan Custom Scripts/Binaries** | Rules: "Custom executable scripts, general-purpose programming runtimes, and unauthorized direct access to NAS resources are not supported." | **Python + uliya-skill-kit only**. No ffmpeg binary, no custom vision model. Pakai UGOS `ug-video` capabilities. |

---

## 4. ELIGIBILITY RISKS - SOLO INDONESIAN PARTICIPANT

| Risk | Status | Mitigasi |
|---|---|---|
| **Team size** | ✅ OK | Solo (1 human + AI agents) = eligible individual |
| **Indonesia eligible** | ✅ OK | Explicit di Asia-Pacific list |
| **AI Team disclosure** | 🟡 ASSUMPTION | Devpost rules tidak explicit larang AI agents. AHVO2-8: disclosure wording ready untuk submission copy. |
| **Pre-existing code** | ✅ OK | Watchtower baru, core workflow developed during hackathon |
| **Organization entry** | ✅ OK | Individual entry, bukan org |

---

## 5. SURVEILLANCE TRACK SPECIFIC REQUIREMENTS

| Requirement | Watchtower Compliance |
|---|---|
| **Use Surveillance capability** | ✅ `query camera events` → core feature #1 |
| **Use authorized footage** | ✅ User approve folder access, confirmation per clip |
| **Organize/search/extract/summarize** | ✅ Query → Extract clips → Summarize in HTML briefing |
| **Chain with other capabilities** | ✅ Surveillance → Video → Knowledge → Files |

---

## 6. WATCHTOWER FIT SCORE (Internal)

| Kriteria | Fit 1-10 | Notes |
|---|---|---|
| User Value | 9 | Real pain point: "cameras but no time to review" |
| Innovation | 9 | First in Skills Hub, NAS-level vs camera-level |
| Technical Quality | 8 | Clear scope, 3 caps, confirmation gates |
| AI NAS Fit | 10 | 4 capabilities chained, local processing, privacy |
| **Rata-rata** | **9.0** | **Sangat kuat untuk menang** |

---

## 7. RECOMMENDATION UNTUK BUILD

**Priority Order (Demo Path First)**:
1. **M1**: `query_events` — Surveillance query → event list (foundation)
2. **M2**: `extract_clips` — Video extract ±30s → save to /Security/ (visual wow)
3. **M3**: `generate_briefing` — Knowledge → HTML report dengan embedded clips (completeness)
4. **M4**: CLI Integration — Natural language parsing, help, error messages
5. **M5**: HTML Polish — Template, timeline, threat levels, video playback
6. **M6**: E2E Polish — Confirmation gates, error handling, README, README

**Deferred**: Face recognition (opt-in), Auto-organize (high risk write), Scheduled triggers (not supported).

---

*Dokumen ini output T-02 — AHVO2-2 (RA) complete.*
*Next: T-05 Blueprint (AHVO2-3 AR) setelah Legal/Finance gates done.*