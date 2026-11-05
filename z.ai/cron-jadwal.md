# CRON JADWAL AHVO2 (Asia/Jakarta)
# Daftar penjadwalan otomatis yang harus terdaftar di Hermes Scheduler.
# Format: nama | jadwal (cron) | agent | tugas | keterangan

## Mingguan
scan-lomba-mingguan | 0 9 * * 1 | AHVO2-2 (RA) | T-17 | Scan Devpost, MLH, HackerEarth/Unstop untuk AI hackathon buka/tutup 30 hari ke depan. Output -> 01-lomba/scan-[YYYY-MM-DD].md

review-anggaran-mingguan | 0 16 * * 5 | AHVO2-9 (FI) | T-20 | Review ledger, quota-log, prize tracker. Update budget forecast.

## Harian (saat lomba aktif)
briefing-pagi | 0 8 * * * | AHVO2-1 (PM) | BRIEFING | Fokus harian + papan tugas + max 3 keputusan. Output ke dashboard + terminal.

status-malam | 0 20 * * * | AHVO2-1 (PM) | STATUS | Ringkasan done/next/risks + arsip ke 04-arsip.

## Alarm Deadline (otomatis dihitung dari meta.deadline state.json)
alarm-h-24 | (H-24 jam dari deadline) | AHVO2-1 (PM) | - | "ALARM H-24: 24 jam lagi. Cek scope, kuota, legal, finance."

alarm-h-6 | (H-6 jam dari deadline) | AHVO2-1 (PM) | - | "ALARM H-6: 6 jam buffer submit dimulai. Feature freeze harus sudah selesai."

## Perintah Manual (Founder ketik di Hermes)
# BRIEFING          -> AHVO2-1 output daily plan
# STATUS            -> AHVO2-1 output done/next/risks
# NEW HACKATHON     -> SOP-01 kickoff intake
# WAR ROOM          -> fase, jam, top 3 prioritas, next action per agent
# LEGAL CHECK       -> AHVO2-8 T-19
# BUDGET CHECK      -> AHVO2-9 T-20
# POST-MORTEM       -> AHVO2-1 T-15
# ONBOARDING        -> T-16 setup kantor sekali
# /stop             -> KILL SWITCH total

## Catatan Implementasi
- Hermes Scheduler (cron) jalan di background proses Hermes.
- Jika scheduler tidak tersedia, fallback: AHVO2-7 set alarm manual di kalender/telegram.
- Semua jam dalam Asia/Jakarta (WIB, UTC+7).
- Deadline UGREEN: 2026-11-16 14:45 WIB = 2026-11-15 23:45 PT.