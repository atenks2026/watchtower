# CRON JADWAL AHVO2 - SHIFT OTOMATIS 4 JAM KERJA / 1 JAM ISTIRAHAT
# Berjalan saat Hermes aktif, berhenti saat Hermes mati.
# Zona waktu: Asia/Jakarta (WIB, UTC+7)
# Job codes: pm2, ra2, ar2, dev2, qa2, dn2, ops2, lc2, fi2

## KONSEP SHIFT
# Setiap agent bekerja 4 jam, istirahat 1 jam, berulang.
# Shift bergilir (staggered) supaya selalu ada agent yang working.
# Founder hanya butuh approve keputusan kunci, tidak handle shift.

## JADWAL CRON (format: menit jam hari bulan minggu)

### SHIFT MANAGEMENT - AHVO2-1 (PM) mengatur
# Setiap 5 menit cek status & trigger shift change jika perlu
*/5 * * * * | AHVO2-1 (PM) | SHIFT_CHECK | python dashboard/ahvo_status.py show | cek agent idle >60min & auto-assign next task

# Shift boundary alarms (Founder tidak perlu manual)
0 */5 * * * | AHVO2-1 (PM) | SHIFT_ALARM | "SHIFT CHANGE: 4 jam kerja selesai, 1 jam istirahat dimulai" | notify all agents
0 * * * * | AHVO2-7 (OPS) | HEARTBEAT | python dashboard/ahvo_status.py log "Heartbeat: AHVO2 alive, shift running" | dashboard stay live

### AGENT-SPECIFIC CRON (staggered start times)

# AHVO2-1 PM: Start at :00, work 4h, break 1h
0 0,5,10,15,20 * * * | AHVO2-1 | SHIFT_START | set pm2 working -t "T-XX" -p 10 -m "Shift mulai: review board, assign tasks"
0 1,6,11,16,21 * * * | AHVO2-1 | SHIFT_BREAK | set pm2 idle -t "" -p 0 -m "Istirahat 1 jam (shift break)"
0 2,7,12,17,22 * * * | AHVO2-1 | SHIFT_RESUME | set pm2 working -t "T-XX" -p 10 -m "Shift lanjut: monitor burn-down, escalate blockers"

# AHVO2-2 RA: Start at :05, work 4h, break 1h (offset 5 menit)
5 0,5,10,15,20 * * * | AHVO2-2 | SHIFT_START | set ra2 working -t "T-XX" -p 10 -m "Shift mulai: research, fact-check, idea gen"
5 1,6,11,16,21 * * * | AHVO2-2 | SHIFT_BREAK | set ra2 idle -t "" -p 0 -m "Istirahat 1 jam"
5 2,7,12,17,22 * * * | AHVO2-2 | SHIFT_RESUME | set ra2 working -t "T-XX" -p 10 -m "Shift lanjut: verify facts, update rules brief"

# AHVO2-3 AR: Start at :10, work 4h, break 1h (offset 10 menit)
10 0,5,10,15,20 * * * | AHVO2-3 | SHIFT_START | set ar2 working -t "T-XX" -p 10 -m "Shift mulai: blueprint, architecture, stack decisions"
10 1,6,11,16,21 * * * | AHVO2-3 | SHIFT_BREAK | set ar2 idle -t "" -p 0 -m "Istirahat 1 jam"
10 2,7,12,17,22 * * * | AHVO2-3 | SHIFT_RESUME | set ar2 working -t "T-XX" -p 10 -m "Shift lanjut: refine blueprint, license tags"

# AHVO2-4 DEV: Start at :15, work 4h, break 1h (offset 15 menit)
15 0,5,10,15,20 * * * | AHVO2-4 | SHIFT_START | set dev2 working -t "T-XX" -p 10 -m "Shift mulai: implement increment, self-test, commit"
15 1,6,11,16,21 * * * | AHVO2-4 | SHIFT_BREAK | set dev2 idle -t "" -p 0 -m "Istirahat 1 jam"
15 2,7,12,17,22 * * * | AHVO2-4 | SHIFT_RESUME | set dev2 working -t "T-XX" -p 10 -m "Shift lanjut: next increment, bug fixes"

# AHVO2-5 QA: Start at :20, work 4h, break 1h (offset 20 menit)
20 0,5,10,15,20 * * * | AHVO2-5 | SHIFT_START | set qa2 working -t "T-XX" -p 10 -m "Shift mulai: review diff, test plan, gate check"
20 1,6,11,16,21 * * * | AHVO2-5 | SHIFT_BREAK | set qa2 idle -t "" -p 0 -m "Istirahat 1 jam"
20 2,7,12,17,22 * * * | AHVO2-5 | SHIFT_RESUME | set qa2 working -t "T-XX" -p 10 -m "Shift lanjut: gate run, bug triage"

# AHVO2-6 DN: Start at :25, work 4h, break 1h (offset 25 menit)
25 0,5,10,15,20 * * * | AHVO2-6 | SHIFT_START | set dn2 working -t "T-XX" -p 10 -m "Shift mulai: story sheet, demo script, copy"
25 1,6,11,16,21 * * * | AHVO2-6 | SHIFT_BREAK | set dn2 idle -t "" -p 0 -m "Istirahat 1 jam"
25 2,7,12,17,22 * * * | AHVO2-6 | SHIFT_RESUME | set dn2 working -t "T-XX" -p 10 -m "Shift lanjut: README, pitch, visuals"

# AHVO2-7 OPS: Start at :30, work 4h, break 1h (offset 30 menit) - ALWAYS ON for dashboard
30 0,5,10,15,20 * * * | AHVO2-7 | SHIFT_START | set ops2 working -t "T-XX" -p 10 -m "Shift mulai: deploy, repo, dashboard server, submission prep"
30 1,6,11,16,21 * * * | AHVO2-7 | SHIFT_BREAK | set ops2 idle -t "" -p 0 -m "Istirahat 1 jam (dashboard keep running)"
30 2,7,12,17,22 * * * | AHVO2-7 | SHIFT_RESUME | set ops2 working -t "T-XX" -p 10 -m "Shift lanjut: verify links, archive state"

# AHVO2-8 LC: Start at :35, work 4h, break 1h (offset 35 menit)
35 0,5,10,15,20 * * * | AHVO2-8 | SHIFT_START | set lc2 working -t "T-XX" -p 10 -m "Shift mulai: legal check T-19, license table, disclosure"
35 1,6,11,16,21 * * * | AHVO2-8 | SHIFT_BREAK | set lc2 idle -t "" -p 0 -m "Istirahat 1 jam"
35 2,7,12,17,22 * * * | AHVO2-8 | SHIFT_RESUME | set lc2 working -t "T-XX" -p 10 -m "Shift lanjut: final compliance, G11 update"

# AHVO2-9 FI: Start at :40, work 4h, break 1h (offset 40 menit)
40 0,5,10,15,20 * * * | AHVO2-9 | SHIFT_START | set fi2 working -t "T-XX" -p 10 -m "Shift mulai: ledger T-20, prize tracker, tax checklist"
40 1,6,11,16,21 * * * | AHVO2-9 | SHIFT_BREAK | set fi2 idle -t "" -p 0 -m "Istirahat 1 jam"
40 2,7,12,17,22 * * * | AHVO2-9 | SHIFT_RESUME | set fi2 working -t "T-XX" -p 10 -m "Shift lanjut: final finance, G12 update"

### DAILY MANAGEMENT
0 8 * * * | AHVO2-1 | BRIEFING | "BRIEFING" | Founder gets daily plan + 3 decisions max
0 20 * * * | AHVO2-1 | STATUS | "STATUS" | Ringkasan done/next/risks + archive

### WEEKLY
0 9 * * 1 | AHVO2-2 | SCAN_LOMBA | T-17 | Weekly contest scan (Devpost, MLH, HackerEarth)
0 16 * * 5 | AHVO2-9 | REVIEW_BUDGET | T-20 | Weekly budget/quota review

### DEADLINE ALARMS (auto-calculated from state.json deadline)
# H-24 dan H-6 trigger oleh AHVO2-1 via shift check logic

## IMPLEMENTASI DI HERMES
# 1. Paste UREQ-AHVO2.md di Hermes
# 2. Ketik ONBOARDING → Hermes register cron jobs di atas
# 3. Cron jalan di background proses Hermes
# 4. Saat Hermes close → cron stop, agent "offline"
# 5. Saat Hermes open → cron resume, agent "working" per jadwal

## FALLBACK JIKA HERMES CRON TIDAK TERSEDIA
# AHVO2-7 jalanin manual via Windows Task Scheduler / cron Linux:
# schtasks /create /tn "AHVO2_ShiftCheck" /tr "python D:\OneDrive\2026 - 1drive\.AHVO\AHVO2\dashboard\ahvo_status.py show" /sc minute /mo 5
# Atau gunakan systemd timer di Linux.

## SHIFT HANDOFF PROTOCOL (Setiap ganti shift)
1. Agent outgoing: `python ahvo_status.py set <job> idle -t "T-XX" -p <progress> -m "Handoff: <next step untuk incoming>"`
2. Agent incoming: `python ahvo_status.py set <job> working -t "T-XX" -p <progress> -m "Resume: <lanjut dari progress X%>"`
3. AHVO2-1 update task board: `python ahvo_status.py task T-XX doing` (auto-set owner working)
4. Log: `python ahvo_status.py log "SHIFT HANDOFF: <agent> -> <agent>, task T-XX, progress X%"`

## MONITORING DASHBOARD
- Buka http://localhost:8018 (MULAI-DASHBOARD.bat)
- Card agent: status BEKERJA/SIAGA/SELESAI/TERBLOKIR/OFFLINE
- "updated X mnt lalu" → kuning >30min, merah >60min
- LIVE/STALE indicator: STALE = tidak ada agent update >2 menit saat jam kerja

## EMERGENCY OVERRIDE
# Founder ketik di Hermes:
# /stop → semua agent stop immediate, save state, report 3 lines
# WAR ROOM → tampilkan fase, jam, top 3 prioritas, next action per agent
# LEGAL CHECK / BUDGET CHECK → bypass shift, jalankan T-19/T-20 langsung