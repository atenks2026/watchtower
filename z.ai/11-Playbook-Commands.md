# PLAYBOOK COMMANDS - AHVO2 - PERINTAH JAM-PER-JAM UNTUG UGREEN AI NAS HACKATHON 2026
# (ID: Urutan perintah siap-tempel saat lomba berlangsung. Kolom owner = agent
#  yang dipanggil dengan perintah dari file ini. Waktu H dihitung dari jam mulai
#  resmi lomba; Round 1 deadline: 2026-11-16 14:45 WIB.)
# ============================================================================
# ====== MULAI SALIN DARI SINI ================================================
# ============================================================================

## F0 PREP (SEKARANG - SEBELUM LOMBA MULAI)
# Target: siap tarik pada H0
# Perintah untuk Founder (jalankan sekali sekarang):

# 1. Setup akun & lingkungan
# BRIEFING F0: "AHVO2-1, buat master plan F0 dari sekarang sampai H0. Owner: AHVO2-7."
# T-01 untuk AHVO2-7: setup akun Devpost, GitHub, NVIDIA NIM (build.nvidia.com), OpenRouter, Vercel/Netlify, template repo.

# 2. Verifikasi eligibility & rules
# "AHVO2-2, jalankan T-01 extract rules brief UGREEN. Forward ToS ke AHVO2-8, prize ke AHVO2-9."
# "AHVO2-8, jalankan T-19 legal check UGREEN ToS."
# "AHVO2-9, jalankan T-20 prize tracker UGREEN."

# 3. Template repo & deploy hello-world
# "AHVO2-7, buat template repo di GitHub: README stub, .gitignore, LICENSE MIT, .env.example, CHANGELOG.md. Deploy hello-world ke Vercel. Verifikasi URL live."

# 4. Hermes & UReQ test
# "HERMES, tempel UREQ-AHVO2.md, tunggu salam 'AHVO2 online. 9 agents ready.'"

## F1 KICKOFF (H0-H2) - LOMBA RESMI MULAI
# Perintah jam-per-jam:

# H0+0m: "NEW HACKATHON" → HERMES jalanin SOP-01 kickoff intake
# H0+30m: "AHVO2-2, T-02 rubric breakdown UGREEN. Output: criteria table + 10-item build checklist + 3 traps + eligibility solo Indo."
# H0+1h: "AHVO2-8, T-19 legal check UGREEN ToS. Output: legal checklist + verdict."
# H0+1h: "AHVO2-9, T-20 prize tracker. Output: ledger (target 0) + prize tracker + tax checklist Indo + US."
# H0+1.5h: "AHVO2-1, master plan F0-F7 adjusted to real time remaining. Mark T-19/T-20 gates."

## F2 RESEARCH & IDEASI (H2-H6)
# H2: "AHVO2-2+AHVO2-6, T-03 generate 10 ide UGREEN. Track: [dipilih nanti]. Capabilities: Files/Albums/Documents/Knowledge/Video/Surveillance. Constraints: solo, 48h build, free tier, Uliya standard."
# H3: "AHVO2-8, screen 10 ide untuk BLOCKER legal. Output: verdict per ide."
# H4: "HERMES/AHVO2-1, T-04 scoring 10 ide. Scorecard: Impact 30, Feas 25, Demo 20, Novelty 15, Theme 10. Rank top 3, rekomendasi 1 ide + 2 baris defense."
# H5: "FOUNDER: kunci 1 ide. MVP max 3 fitur inti. Sisanya daftar 'nanti'."
# H5: "AHVO2-1, catat keputusan scope ke memory. Update master plan."

## F3 ARSITEKTUR (H6-H10)
# H6: "AHVO2-3, T-05 blueprint UGOS Skill. Stack: Python/JS + uliya-skill-kit. Output: BLUEPRINT.md + SKILL.md skeleton + repo tree + milestones M0-Mn + fallback + license table."
# H7: "AHVO2-1, T-06 pecah blueprint jadi task board max 12 task. Owner, deadline, effort, acceptance. Tandai (DEMO) path. Include T-19/T-20 gates."
# H8: "AHVO2-6, T-11 story sheet: nama, tagline, hook, user, 3 fitur, demo flow 3 langkah. Disetujui Founder."
# H9: "AHVO2-4, M0: scaffold repo + deploy hello-world. URL live verified."

## F4 BUILD MVP (H10-H34) - INCREMENT TIAP ~4 JAM
# Pola berulang (ulangi sampai feature freeze H34):

# Increment M1 (H10-H14):
# "AHVO2-4, T-07 implement [task ID M1]. Acceptance: [dari task board]. HOW TO TEST ≤3 menit."
# "AHVO2-5, T-09 review increment M1. Test plan + diff verdict + bug list."
# "AHVO2-7, deploy M1. Verifikasi URL live."
# "AHVO2-1, update task board. STATUS."

# Increment M2 (H14-H18): ... (sama)
# Increment M3 (H18-H22): ...
# Increment M4 (H22-H26): ...
# Increment M5 (H26-H30): ...
# Increment M6 (H30-H34): ...

# H24 CHECKPOINT: "AHVO2-1, realita vs rencana. Potong scope urutan: fitur extra → polesan → backend depth. DEMO PATH TIDAK DIPOTONG. Founder approve. Update master plan."

# H30-H34: "AHVO2-6, T-12 submission copy draft + T-13 script video 90 detik (siap Round 2). Shot list ready."

## H34 FEATURE FREEZE
# "AHVO2-1, FEATURE FREEZE. No new features. Only bug fix & polish."
# "AHVO2-5, full review semua increment. Daftar bug P0/P1/P2."

## F5 QA & POLISH (H34-H42) - BUG BURN-DOWN + GATE 12 BUTIR
# H34-H38: "AHVO2-4, T-08 fix P0 bugs. AHVO2-5 verify each fix. Target: 0 P0."
# H38-H40: "AHVO2-4, fix P1 bugs (visible to judge). AHVO2-5 verify."
# H40-H42: "AHVO2-5, T-10 full Quality Gate 12 butir pada URL live + repo.
#   G1 Demo path 2× | G2 Load <5s | G3 No console error/placeholder | G4 Human error msg | G5 Judge device safe
#   G6 README complete | G7 Repo no secrets | G8 Form filled | G9 Video correct | G10 License clean
#   G11 AHVO2-8 legal PASS | G12 AHVO2-9 ledger PASS
#   Output: PASS/FAIL table + verdict READY TO SUBMIT: YES/NO."

# H36 COMPLIANCE FINAL: "AHVO2-8, final license/attribution check repo final. G11 update."
# H36: "AHVO2-9, final ledger close + archive bukti. G12 update."

## F6 DEMO & SUBMIT (H42-H48) - BUFFER 6 JAM NON-NEGOTIABLE
# H42: "AHVO2-6, final submission package: title, one-liner, what/how, pitch, AI disclosure (approved AHVO2-8)."
# H42: "FOUNDER: rekam video 90 detik per shot list AHVO2-6. Satu take per shot. Uji audio 10 detik dulu. Zoom 100%. Tutup tab lain."
# H44: "AHVO2-7, submission checklist: Devpost form semua field ✓, link repo publik ✓, link demo live ✓, video terunggah ✓, kategori ✓, persetujuan aturan ✓. Verifikasi SEMUA link via incognito."
# H44: "AHVO2-8, final cek lisensi/atribusi repo final."
# H44: "AHVO2-9, final ledger archive + paket bukti."
# H45 (DEADLINE - 6 JAM): "FOUNDER: TEKAN SUBMIT. AHVO2-7 arsipkan bukti konfirmasi + jam submit."
# H48: "MODE LOW-POWER: repo dibekukan sampai pengumuman."

## F7 POST-MORTEM (+24 JAM)
# "AHVO2-1, T-15 post-mortem UGREEN. Score 1-5: demo, story, rubric coverage, time mgmt, tech depth. What won/lost/surprised. 3 process changes + owner. Money note AHVO2-9 + legal note AHVO2-8. File ke 04-arsip."

## ROUND 2 (JIKA LOLOS FINALIS - 22-28 NOV NAS ACCESS, SUBMIT 30 NOV)
# Jika dipanggil finalis (email 21 Nov):
# F0-F3: Persiapan khusus NAS (sudah punya blueprint + skill package Round 1)
# F4: 1 hari testing di NAS iDX6011 Pro remote - install, test, polish Skill
# F5: Final Skill Package (ZIP) + Demo Video 3 menit (YouTube, English narration/subtitle)
# F6: Submit via private link sebelum 30 Nov 23:45 PT
# "AHVO2-1, adaptasi master plan Round 2. Compress F4 jadi 1 hari. Buffer 6 jam tetap."

## PERINTAH STANDBY (KETIKA TIDAK ADA LOMBA AKTIF)
# Pagi (08:00): "BRIEFING" → AHVO2-1 output fokus harian + task board + max 3 keputusan
# Siang: Panggil agent per ID + template tugas (T-07, T-09, dll)
# Malam (20:00): "STATUS" → ringkasan done/next/risks + arsip AHVO2-7
# Mingguan (Jumat 16:00): "POST-MORTEM mini + BUDGET CHECK" → pelajaran + posisi biaya

## PERINTAH DARURAT
# "/stop" → KILL SWITCH: hentikan semua aksi segera, simpan state ke file, lapor 3 baris.
# "WAR ROOM" → tampilkan fase, jam tersisa, top 3 prioritas, single next action per agent.
# "LEGAL CHECK" → AHVO2-8 jalanin T-19 untuk lomba saat ini.
# "BUDGET CHECK" → AHVO2-9 jalanin T-20 untuk lomba saat ini.
# "DASHBOARD" / "STATUS KANTOR" → AHVO2-7 jalankan `python ahvo_status.py show`, output format snapshot kantor.

# ====== SELESAI SALIN =======================================================