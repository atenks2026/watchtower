# SETUP GUIDE AHVO2 - UGREEN AI NAS Hackathon 2026
# Panduan instalasi "gedung kantor" AHVO2. Ikuti berurutan.

## 1. STRUKTUR FOLDER (Sudah Dibuat Otomatis)
```
AHVO2/
├── 00-ureq/           # UREQ master context
├── 01-lomba/
│   └── ugreen-ai-nas-hackathon-2026/  # Arsip per lomba
├── 02-repo/           # Workspace kode (clone dari GitHub)
├── 03-prompts/        # Folder prompts (isi dari z.ai/ ke sini)
├── 04-arsip/          # Post-mortem, template, ledger, quota-log
├── 05-rahasia/        # .env asli, catatan key (TIDAK ikut repo)
├── z.ai/              # File master: blueprint, agent profiles, task lib, playbook, dashboard, config
└── dashboard/         # Mission Control: dashboard.html, state.json, ahvo_status.py, ahvo_serve.py
```

## 2. AKUN YANG HARUS DIBUAT (Manual oleh Founder)
| Layanan | URL | Kegunaan |
|---|---|---|
| Devpost | https://devpost.com | Daftar lomba, submit |
| GitHub | https://github.com | Repo kode, deploy |
| NVIDIA NIM | https://build.nvidia.com | API Key Nemotron (gratis) |
| OpenRouter | https://openrouter.ai | API Key cadangan (gratis) |
| Vercel/Netlify | https://vercel.com / https://netlify.com | Hosting gratis |
| Telegram (opsional) | @BotFather | Bot notifikasi Gateway |

## 3. SIMPAN API KEY (Manual oleh Founder)
1. Salin `05-rahasia/ahvo2.env.example` → `05-rahasia/.env`
2. Isi nilai-nilai:
   - `NVIDIA_API_KEY` (wajib, dari build.nvidia.com)
   - `OPENROUTER_API_KEY` (cadangan)
   - `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (opsional)
   - `GITHUB_TOKEN`, `VERCEL_TOKEN` (opsional, untuk auto-deploy)
3. **JANGAN PERNAH** paste key di chat, commit ke repo, atau screenshot.

## 4. PASANG HERMES AGENT
1. Unduh Hermes Agent Desktop dari situs resmi (Nous Research).
2. Install di Windows/Mac/Linux.
3. Buka Hermes → Settings → Models → Add Custom Provider (OpenAI-compatible):
   - **Name**: NVIDIA NIM
   - **Base URL**: `https://integrate.api.nvidia.com/v1`
   - **API Key**: `NVIDIA_API_KEY` dari .env
   - **Models**: Pilih `nvidia/nemotron-3-ultra-550b-a55b` (utama)
4. Tambahkan provider cadangan OpenRouter:
   - **Name**: OpenRouter
   - **Base URL**: `https://openrouter.ai/api/v1`
   - **API Key**: `OPENROUTER_API_KEY`
5. Test: kirim "Halo" → pastikan jawab muncul.

## 5. JALANKAN ONBOARDING (Sekali Saja)
Di Hermes, buat sesi baru, paste **seluruh isi** `00-ureq/UREQ-AHVO2.md`, lalu ketik:
```
ONBOARDING
```
Hermes akan:
1. Validasi struktur folder (sudah ada)
2. Convert 8 SOP jadi Hermes skills
3. Register cron jobs (lihat `z.ai/cron-jadwal.md`)
4. Test semua fasilitas (skills, subagent, memory, cron, web fetch, file write, code execution, dashboard CLI, plugins)
5. Verifikasi model setup (NIM, OpenRouter, Ollama)
6. Buat file arsip kosong: `ide-andalan.md`, `quota-log.md`, `ledger.md`
7. Laporkan hal manual yang harus Founder lakukan (akun, API key, Telegram)

## 6. JALANKAN DASHBOARD MISSION CONTROL
```bash
cd AHVO2/dashboard
python ahvo_status.py demo      # isi data contoh
python ahvo_serve.py            # buka http://localhost:8018 otomatis
```
Biarkan terminal `ahvo_serve.py` terbuka saat memantau. Dashboard auto-refresh 5 detik.

## 7. MULAI LOMBA UGREEN
Di Hermes (sesi yang sudah ONBOARDING), ketik:
```
NEW HACKATHON
```
AHVO2-1 akan meminta data lomba (sudah di-hardcode di UREQ untuk UGREEN), lalu menjalankan SOP-01 kickoff otomatis.

## 8. CEK SETUP OTOMATIS
```bash
cd AHVO2/z.ai
python check_setup.py
```
Output harus semua PASS. Jika ada FAIL, ikuti petunjuk perbaikannya.

## 9. FILE PENTING UNTUK DIPAHAMI
| File | Fungsi |
|---|---|
| `00-ureq/UREQ-AHVO2.md` | Konteks master - paste di awal sesi Hermes |
| `z.ai/AHVO2-Blueprint.md` | Blueprint lengkap perusahaan AHVO2 |
| `z.ai/01-Agent-AHVO2-1-PM.md` s/d `09-Agent-AHVO2-9-FI.md` | Profil 9 agent (kontrak kerja) |
| `z.ai/10-Task-Prompt-Library.md` | 20 template tugas (T-01..T-20) |
| `z.ai/11-Playbook-Commands.md` | Perintah jam-per-jam saat lomba |
| `z.ai/12-Agent-Monitor-Dashboard.md` | Standing order dashboard |
| `dashboard/dashboard.html` | Mission Control UI |
| `dashboard/ahvo_status.py` | CLI update status agen |
| `dashboard/ahvo_serve.py` | Server dashboard port 8018 |

## 10. TROUBLESHOOTING CEPAT
| Gejala | Penyebab | Solusi |
|---|---|---|
| Dashboard "STALE" | Agen tidak nulis state.json >2 menit | Ingatkan: "Update your status via ahvo_status.py now" |
| Model error 429 | Rate limit NIM | Switch: `python ahvo_status.py log "Switch to OpenRouter"` lalu ganti model di Hermes |
| Deploy gagal | Vercel/Netlify config | Cek `vercel.json` / `netlify.toml`, pastikan env vars diset |
| Key bocor di repo | .gitignore salah | Tambah `.env` ke .gitignore, rotasi key, `git filter-branch` |
| Kuota habis | Free tier limit | Jenjang: Nemotron → OpenRouter free → Ollama local |

## 11. EMERGENCY: KILL SWITCH
Ketik `/stop` di Hermes → semua agent hentikan kerja, simpan state, lapor 3 baris.
Tidak ada agent lanjut kerja sampai Founder resume eksplisit.

---

**Estimasi Waktu Setup Total:** 30-45 menit (termasuk bikin akun).
**Deadline UGREEN:** 2026-11-16 14:45 WIB (Round 1 submission).
**Waktu Tersisa:** ~14 hari — cukup untuk 2-3 siklus build penuh.

*Selamat membangun, Founder. AHVO2 siap tempur.*