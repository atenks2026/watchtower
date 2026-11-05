# STORY SHEET - WATCHTOWER
# AHVO2-6 (DN) Output - T-11
# Untuk: Demo video 90s, Submission copy, README, Pitch

---

## 1. IDENTITAS PRODUK

| Atribut | Nilai |
|---|---|
| **Nama Skill** | `watchtower` |
| **Display Name** | Watchtower — AI Security Analyzer |
| **Tagline** | *Turn unwatched footage into actionable security intelligence.* |
| **One-Liner** | Natural language query → cross-camera anomaly detection → HTML security briefing with video clips. |
| **Hook (10 detik)** | **"You have cameras. But who's watching the footage?"** |
| **Track** | Surveillance / Open Innovation |

---

## 2. TARGET USER & PROBLEM

| User Persona | Pain Point | Watchtower Solution |
|---|---|---|
| **Homeowner** | 5 kamera, 24/7 recording, **0 menit review** per hari | "Analyze last 24h" → 30 detik baca briefing |
| **SMB Owner** | Gudang/tokko punya CCTV tapi **tidak punya security team** | Otomatis flag anomali: orang asing, kendaraan tidak dikenal |
| **Elderly Care** | Anak khawatir orang tua di rumah sendirian | Daily security briefing dikirim ke WhatsApp/email |
| **Airbnb Host** | Tamu check-out, **siapa review footage?** | "Generate briefing for last guest stay" → bukti kerusakan/kehilangan |

**Core Insight**: 90% footage CCTV **tidak pernah ditonton** sampai ada insiden. Watchtower = "AI yang nontonin buat kamu."

---

## 3. 3 FITUR INTI (MVP)

| # | Fitur | User Value | Demo Moment (Visual) |
|---|---|---|---|
| **1** | **Query Events** | "Show me person detections last 24h" → instant list dengan timestamp & kamera | Ketik natural language → tabel event muncul <2 detik |
| **2** | **Extract Clips** | Otomatis potong video ±30s di sekitar event → save ke folder /Security/ | Klik "Extract" → progress bar → folder buka, 10 clip siap diputar |
| **3** | **Generate Briefing** | HTML report lengkap: summary, timeline, embedded clips, rekomendasi | Klik "Generate" → browser buka HTML, video play inline, threat level warna-warni |

---

## 4. DEMO FLOW (90 DETIK - 3 LANGKAH)

### Detik 0-10: HOOK
> **Visual**: Split screen — kiri: grid 4 kamera CCTV (footage cepat), kanan: teks "24 jam footage. 0 menit ditonton."
> **Voice**: "You have cameras. But who's watching the footage? Meet Watchtower."

### Detik 10-25: CONTEXT
> **Visual**: Dashboard Watchtower di terminal/UGOS. User ketik: `watchtower "analyze last 24 hours"`
> **Voice**: "Natural language query. Cross-camera. No complex setup."

### Detik 25-55: DEMO STEP 1 — QUERY EVENTS
> **Visual**: Output tabel: `14:32 | Cam-Front | Person | 94% | Unknown individual`
> `16:15 | Cam-Garage | Vehicle | 87% | White sedan`
> `18:44 | Cam-Backyard | Motion | 72% | Cat`
> **Voice**: "Instant event list. Timestamp. Camera. Confidence. Filterable."

### Detik 55-75: DEMO STEP 2 — EXTRACT CLIPS
> **Visual**: User ketik `watchtower extract --all`. Progress bar. Folder `/Security/2026-11-02/` terbuka. 10 file MP4.
> **Voice**: "One command extracts clips around every event. ±30 seconds. Batch approval. Ready to review."

### Detik 75-85: DEMO STEP 3 — GENERATE BRIEFING
> **Visual**: Browser buka `security_briefing_20261102_1430.html`. Executive Summary: "3 Anomalies Detected". Timeline visual. Embedded video play inline. Threat level badges (Critical/High/Medium).
> **Voice**: "AI-generated briefing. Executive summary. Timeline. Playable clips. Recommendations."

### Detik 85-90: CLOSING
> **Visual**: Logo Watchtower + "Built on UGOS. Local. Private. Yours." + QR ke Skills Hub.
> **Voice**: "Watchtower. AI that watches so you don't have to. On UGREEN Skills Hub soon."

---

## 5. SHOT LIST (Untuk Recording)

| Shot # | Duration | Visual | Audio Cue | Notes |
|---|---|---|---|---|
| 1 | 5s | Split screen: 4 cam grid vs "0 min watched" | "You have cameras..." | Static graphic, zoom ke teks |
| 2 | 5s | Terminal: `watchtower "analyze last 24h"` | "Natural language query..." | Type effect, enter |
| 3 | 10s | Output tabel event (scroll) | "Instant event list..." | Highlight confidence %, camera |
| 4 | 10s | `watchtower extract --all` + progress + folder open | "One command extracts..." | Show MP4 thumbnails |
| 5 | 15s | Browser: HTML briefing scroll (summary → timeline → play clip) | "AI-generated briefing..." | Play video inline, show threat badge |
| 6 | 5s | Closing card: Watchtower logo + UGOS badge + Skills Hub QR | "Watchtower. AI that watches..." | Hold 3s, fade out |

**Recording Tips**:
1. **Record per shot** — bukan sekali jalan. Retake shot terburuk 1x max.
2. **Audio test 10 detik** dulu — pastikan mic jelas, no background noise.
3. **Zoom 100%** — teks terminal & browser harus terbaca di mobile.
4. **Tutup tab lain** — notifikasi off, desktop bersih.
5. **Dummy data realistis** — jangan "test test", gunakan nama kamera nyata (Front Door, Garage, Backyard).

---

## 6. SUBMISSION COPY (Devpost)

### Title Options
1. **Watchtower: AI Security Analyzer for UGREEN NAS** (58 chars)
2. **Watchtower — Turn Footage into Intelligence** (44 chars) ⭐ **Recommended**

### One-Liner (≤200 chars)
> Watchtower transforms unwatched CCTV footage into actionable security briefings using natural language queries, cross-camera anomaly detection, and AI-generated HTML reports with embedded video clips — all running locally on your UGREEN NAS.

### What It Does (≤150 words)
> Most security cameras record 24/7, but footage is rarely reviewed until after an incident. Watchtower changes that. Using UGOS capabilities (Surveillance, Video, Knowledge, Files), it lets you ask questions like "Show me all person detections last night" and instantly returns a structured event list. One click extracts ±30-second clips around every event. Another click generates a beautiful HTML security briefing with executive summary, visual timeline, playable video clips, and AI-powered recommendations — all running locally on your UGREEN AI NAS with zero cloud dependency. Built for homeowners, SMBs, and anyone who wants to actually use their security footage.

### How We Built It (≤150 words)
> **Stack**: Python + UGREEN uliya-skill-kit (official Skill framework). **AI Model**: NVIDIA Nemotron 3 Ultra via NIM (free tier) for reasoning and multimodal analysis. **UGOS Capabilities Chained**: Surveillance (query events) → Video (extract clips) → Knowledge (AI reasoning) → Files (save clips & HTML report). **Architecture**: 3 expert agents (Scanner, Analyzer, Reporter) orchestrated via Uliya standard. **Privacy**: 100% local processing, face recognition opt-in only, no external API calls. **Compliance**: UGOS confirmation gates for all write operations, UU PDP/GDPR/BIPA ready.

### Challenges
> 1. **UGOS Surveillance capability assumptions** — designed fallback to NVR export parsing if live query unavailable.
> 2. **Video clip extraction accuracy** — implemented codec fallback (copy full file + timestamp metadata).
> 3. **Write confirmation UX** — designed batch approval for multiple clips to meet UGOS requirements smoothly.

### What's Next
> 1. Face recognition module (opt-in, BIPA/GDPR/UU PDP compliant).
> 2. Scheduled briefings via UGOS cron (when supported).
> 3. Mobile push notifications for critical anomalies.
> 4. Multi-site dashboard for property managers.

---

## 7. PITCH PARAGRAPH (100 kata - untuk Forms/Social)

> **Watchtower** turns your security cameras from passive recorders into active intelligence. Ask "What happened last night?" in plain English — get an instant event list, extracted video clips, and an AI-generated HTML briefing with timeline and recommendations. Built on UGREEN UGOS: Surveillance → Video → Knowledge → Files chained in 3 expert agents. Runs 100% locally on your NAS. No cloud. No subscriptions. Your footage, your intelligence. **Coming to UGREEN Skills Hub.**

---

## 8. README STRUCTURE (Untuk Repo)

| Section | Content |
|---|---|
| **Badge Row** | UGOS Skill, MIT License, Python 3.10+, UGREEN NAS |
| **Hero** | Name, tagline, one-liner, screenshot HTML briefing |
| **Quickstart** | 3 commands: install → authorize → `watchtower "analyze last 24h"` |
| **Architecture** | Mermaid diagram: 3 agents → 4 capabilities |
| **Capabilities** | Table: query_events, extract_clips, generate_briefing |
| **Example Queries** | 5 natural language examples |
| **Privacy** | Local processing, face rec opt-in, UU PDP/GDPR |
| **Roadmap** | Face rec, scheduled briefings, mobile push |
| **License** | MIT + attributions |

---

*Story Sheet v1.0 — AHVO2-6 (DN) — Approved for Demo Video & Submission*
*Next: AHVO2-4 (DEV) M0 Scaffold → M1 Scanner Agent*