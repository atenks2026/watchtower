#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AHVO2 - check_setup.py
Pemeriksa kesiapan otomatis kantor AHVO2.
Jalankan: python check_setup.py
Output: tabel PASS/FAIL per item. Semua harus PASS sebelum lomba.
"""
import os, sys, json, subprocess, shutil
from pathlib import Path

BASE = Path(__file__).parent.parent  # AHVO2 root
Z_AI = BASE / "z.ai"
DASHBOARD = BASE / "dashboard"
SECRETS = BASE / "05-rahasia"
UREQ = BASE / "00-ureq"

checks = []

def ok(msg): checks.append(("PASS", msg))
def fail(msg): checks.append(("FAIL", msg))
def warn(msg): checks.append(("WARN", msg))

# 1. Struktur folder
for d in ["00-ureq", "01-lomba", "02-repo", "03-prompts", "04-arsip", "05-rahasia", "z.ai", "dashboard"]:
    if (BASE / d).exists():
        ok(f"Folder {d} exists")
    else:
        fail(f"Folder {d} MISSING")

# 2. File kunci z.ai
key_files = [
    "AHVO2-Blueprint.md",
    "01-Agent-AHVO2-1-PM.md", "02-Agent-AHVO2-2-RA.md", "03-Agent-AHVO2-3-AR.md",
    "04-Agent-AHVO2-4-DEV.md", "05-Agent-AHVO2-5-QA.md", "06-Agent-AHVO2-6-DN.md",
    "07-Agent-AHVO2-7-OPS.md", "08-Agent-AHVO2-8-LC.md", "09-Agent-AHVO2-9-FI.md",
    "10-Task-Prompt-Library.md", "11-Playbook-Commands.md", "12-Agent-Monitor-Dashboard.md",
    "models-nemotron.json", "cron-jadwal.md", "SETUP-GUIDE.md"
]
for f in key_files:
    if (Z_AI / f).exists():
        ok(f"z.ai/{f}")
    else:
        fail(f"z.ai/{f} MISSING")

# 3. UREQ master
if (UREQ / "UREQ-AHVO2.md").exists():
    ok("00-ureq/UREQ-AHVO2.md")
else:
    fail("00-ureq/UREQ-AHVO2.md MISSING")

# 4. Dashboard files
for f in ["dashboard.html", "state.json", "ahvo_status.py", "ahvo_serve.py"]:
    if (DASHBOARD / f).exists():
        ok(f"dashboard/{f}")
    else:
        fail(f"dashboard/{f} MISSING")

# 5. .env.example
if (SECRETS / "ahvo2.env.example").exists():
    ok("05-rahasia/ahvo2.env.example")
else:
    fail("05-rahasia/ahvo2.env.example MISSING")

# 6. .env actual (tidak wajib di sini, tapi cek apakah ada)
env_path = SECRETS / ".env"
if env_path.exists():
    ok("05-rahasia/.env EXISTS (remember: never commit this)")
    # cek isi minimal
    content = env_path.read_text(encoding="utf-8")
    if "NVIDIA_API_KEY" in content and "your_nvidia_nim_api_key_here" not in content:
        ok("  -> NVIDIA_API_KEY terisi")
    else:
        warn("  -> NVIDIA_API_KEY BELUM terisi / masih placeholder")
    if "OPENROUTER_API_KEY" in content and "your_openrouter_api_key_here" not in content:
        ok("  -> OPENROUTER_API_KEY terisi")
    else:
        warn("  -> OPENROUTER_API_KEY BELUM terisi / masih placeholder")
else:
    warn("05-rahasia/.env BELUM ADA (salin dari ahvo2.env.example dan isi)")

# 7. Python & dependencies
try:
    py_version = subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip()
    ok(f"Python: {py_version}")
except Exception as e:
    fail(f"Python check failed: {e}")

# 8. Git
if shutil.which("git"):
    ok("Git tersedia")
else:
    warn("Git tidak ditemukan (diperlukan untuk repo/deploy)")

# 9. Node (untuk Vercel/Netlify CLI)
if shutil.which("node"):
    ok("Node.js tersedia")
else:
    warn("Node.js tidak ditemukan (diperlukan untuk Vercel/Netlify CLI deploy)")

# 10. Models config valid JSON
try:
    with open(Z_AI / "models-nemotron.json", encoding="utf-8") as f:
        json.load(f)
    ok("models-nemotron.json valid JSON")
except Exception as e:
    fail(f"models-nemotron.json INVALID: {e}")

# 11. Dashboard CLI works
try:
    result = subprocess.run([sys.executable, str(DASHBOARD / "ahvo_status.py"), "show"],
                           capture_output=True, text=True, cwd=str(DASHBOARD), timeout=10)
    if result.returncode == 0:
        ok("ahvo_status.py runs OK")
    else:
        fail(f"ahvo_status.py error: {result.stderr[:200]}")
except Exception as e:
    fail(f"ahvo_status.py failed: {e}")

# 12. Dashboard server imports
try:
    import http.server, socketserver, threading, webbrowser
    ok("Dashboard server dependencies available (stdlib)")
except Exception as e:
    fail(f"Dashboard server deps missing: {e}")

# 13. Hermes Agent check (optional - bisa dicek manual)
# Tidak bisa otomatis cek apakah Hermes terinstall & terkonfigurasi
warn("CEK MANUAL: Hermes Agent terinstall & terhubung ke NVIDIA NIM + OpenRouter?")

# 14. Devpost account & UGREEN registration
warn("CEK MANUAL: Akun Devpost aktif & sudah daftar UGREEN AI NAS Hackathon 2026?")

# 15. GitHub repo template ready
warn("CEK MANUAL: Template repo GitHub siap (README, .gitignore, LICENSE, .env.example, CHANGELOG)?")

# Print results
print("=" * 70)
print(" AHVO2 SETUP CHECK - UGREEN AI NAS Hackathon 2026")
print("=" * 70)
for status, msg in checks:
    icon = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}[status]
    print(f" {icon} [{status}] {msg}")

passed = sum(1 for s,_ in checks if s == "PASS")
failed = sum(1 for s,_ in checks if s == "FAIL")
warned = sum(1 for s,_ in checks if s == "WARN")
total = len(checks)

print("-" * 70)
print(f" TOTAL: {total} | PASS: {passed} | FAIL: {failed} | WARN: {warned}")
print("=" * 70)

if failed > 0:
    print("\n❌ SETUP BELUM SIAP - Perbaiki FAIL items di atas sebelum lomba.")
    sys.exit(1)
else:
    print("\n✅ SETUP SIAP - Semua critical checks PASS. WARN items cek manual.")
    sys.exit(0)