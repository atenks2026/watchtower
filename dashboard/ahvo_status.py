#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AHVO2 - ahvo_status.py
Alat lapor status untuk 9 karyawan AI AHVO2. Semua agen (lewat Hermes) menjalankan
script ini setiap kali statusnya berubah; dashboard.html hanya membaca hasilnya.

ID: Panduan singkat untuk Founder:
  python ahvo_status.py demo        -> isi data contoh, langsung terlihat di dashboard
  python ahvo_status.py show        -> ringkasan kantor di terminal
  python ahvo_status.py reset       -> kembali ke kondisi kantor kosong
Data disimpan di state.json (satu-satunya sumber kebenaran dashboard).

Daftar karyawan (kunci = kode jabatan, dipakai di perintah):
  pm2=AHVO2-1 | ra2=AHVO2-2 | ar2=AHVO2-3 | dev2=AHVO2-4 | qa2=AHVO2-5
  dn2=AHVO2-6 | ops2=AHVO2-7 | lc2=AHVO2-8 | fi2=AHVO2-9

Contoh perintah untuk agen (EN, agar stabil dipakai Hermes):
  python ahvo_status.py set dev2 working -t T-07 -p 40 -m "Building upload feature"
  python ahvo_status.py task T-07 done
  python ahvo_status.py gate 3 fail "1 button 404"
  python ahvo_status.py log "Deploy preview v3 online"
  python ahvo_status.py phase F4
  python ahvo_status.py mission "UGREEN AI NAS Hackathon 2026"
  python ahvo_status.py deadline "2026-11-16 14:45"
"""
import argparse, json, os, re, sys, tempfile
from datetime import datetime

DIR   = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(DIR, "state.json")

AGENT_DEFS = [
    ("pm2",  "AHVO2-1", "PM  - Chief of Staff / Project Manager", "#4da3e0"),
    ("ra2",  "AHVO2-2", "RA  - Research Analyst",                "#2ecc71"),
    ("ar2",  "AHVO2-3", "AR  - Solution Architect",              "#a78bfa"),
    ("dev2", "AHVO2-4", "DEV - Lead Developer",                  "#ff9f43"),
    ("qa2",  "AHVO2-5", "QA  - QA Engineer (veto mutu)",         "#ff5d5d"),
    ("dn2",  "AHVO2-6", "DN  - Designer & Narrative",            "#f472b6"),
    ("ops2", "AHVO2-7", "OPS - Ops & DevOps",                    "#2dd4bf"),
    ("lc2",  "AHVO2-8", "LC  - Legal & Compliance Officer",     "#facc15"),
    ("fi2",  "AHVO2-9", "FI  - Finance & Tax Officer",          "#38bdf8"),
]

TASK_DEFS = [
    ("T-01", "Kickoff intake lomba",       "F1", "pm2"),
    ("T-02", "Bedah rubric penjurian",     "F1", "ra2"),
    ("T-03", "Generate 10 ide",            "F2", "ra2"),
    ("T-04", "Kartu skor + kunci ide",     "F2", "pm2"),
    ("T-05", "Blueprint arsitektur",       "F3", "ar2"),
    ("T-06", "Pecah jadi papan tugas",     "F3", "pm2"),
    ("T-07", "Implementasi fitur inti",    "F4", "dev2"),
    ("T-08", "Perbaikan bug temuan QA",    "F4", "dev2"),
    ("T-09", "Test plan + review diff",    "F4", "qa2"),
    ("T-10", "Quality gate 12 butir",      "F5", "qa2"),
    ("T-11", "Generator README",           "F4", "dev2"),
    ("T-12", "Copy submission",            "F4", "dn2"),
    ("T-13", "Script video 90 detik",      "F5", "dn2"),
    ("T-14", "Pitch 100 kata",             "F5", "dn2"),
    ("T-15", "Post-mortem",                "F7", "pm2"),
    ("T-19", "Legal & compliance check",   "F2", "lc2"),
    ("T-20", "Anggaran, hadiah & pajak",   "F1", "fi2"),
]

GATE_DEFS = [
    ("G1",  "Demo path jalan 2x berturut-turut"),
    ("G2",  "Muat di bawah 5 detik"),
    ("G3",  "Tanpa 404 / error konsol / placeholder"),
    ("G4",  "Pesan error manusiawi"),
    ("G5",  "Tampilan perangkat juri aman"),
    ("G6",  "README lengkap (what/run/screenshots)"),
    ("G7",  "Repo bebas rahasia"),
    ("G8",  "Form submission terisi penuh"),
    ("G9",  "Video durasi + audio oke"),
    ("G10", "Lisensi + atribusi rapi"),
    ("G11", "Checklist legal AHVO2-8 lolos (ToS, lisensi, privasi)"),
    ("G12", "Register biaya & bukti pajak terarsip AHVO2-9"),
]

AGENT_STATUSES  = ["working", "idle", "done", "blocked", "offline"]
TASK_STATUSES   = ["todo", "doing", "review", "done", "blocked"]
GATE_STATUSES   = ["pass", "fail", "pending"]
PHASES          = ["F0","F1","F2","F3","F4","F5","F6","F7"]


def now_iso():
    return datetime.now().isoformat(timespec="seconds")

def default_state():
    return {
        "meta": {"company": "AHVO2 - AI Hackathon Virtual Office 2", "mission": "", "phase": "F0",
                 "deadline": None, "updated_at": now_iso()},
        "agents": {k: {"name": n, "role": r, "color": c, "status": "offline",
                       "task": "", "progress": 0, "message": "", "updated_at": None}
                   for k, n, r, c in AGENT_DEFS},
        "tasks": [{"id": i, "title": t, "phase": p, "owner": o, "status": "todo"}
                  for i, t, p, o in TASK_DEFS],
        "gates": [{"id": i, "name": n, "status": "pending", "note": ""}
                  for i, n in GATE_DEFS],
        "log": [{"ts": now_iso(), "agent": "founder",
                 "event": "Kantor AHVO2 didirikan. Dashboard siap; jalankan 'python ahvo_status.py demo' untuk melihat contoh."}],
    }

def demo_state():
    from datetime import timedelta
    st = default_state()
    st["meta"].update({"mission": "[DEMO] UGREEN AI NAS Hackathon 2026", "phase": "F2",
                       "deadline": (datetime.now() + timedelta(hours=19, minutes=12)).isoformat(timespec="seconds")})
    live = {
        "pm2":   ("working", "T-01", 30,  3,   "Kickoff intake UGREEN; rules brief disusun, legal & finance gates dipasang."),
        "ra2":   ("working", "T-02", 45,  1,   "Mengekstrak rubric UGREEN: User Value, Innovation, Technical Quality, AI NAS Fit."),
        "ar2":   ("idle",    "",     0,   95,  "Menunggu rules brief & rubric selesai sebelum blueprint."),
        "dev2":  ("offline", "",     0,   24,  "Belum diaktifkan - menunggu ide terkunci & blueprint."),
        "qa2":   ("offline", "",     0,   12,  "Standby - gerbang mutu G1-G12 disiapkan."),
        "dn2":   ("offline", "",     0,   24,  "Standby - story sheet & demo script nanti."),
        "ops2":  ("working", "",     0,   8,   "Setup repo template, deploy hello-world, dashboard server."),
        "lc2":   ("idle",    "",     0,   210, "Menunggu ToS UGREEN dari RA untuk T-19."),
        "fi2":   ("idle",    "",     0,   12,  "Menunggu prize data dari RA untuk T-20."),
    }
    for k, (s, t, p, m, msg) in live.items():
        st["agents"][k].update({"status": s, "task": t, "progress": p,
                                "message": msg, "updated_at": minutes_ago(m)})
    tstat = {"T-01":"doing","T-02":"doing","T-03":"todo","T-04":"todo","T-05":"todo",
             "T-06":"todo","T-07":"todo","T-09":"todo","T-19":"todo","T-20":"todo"}
    for t in st["tasks"]:
        t["status"] = tstat.get(t["id"], "todo")
    st["log"] = [
        {"ts": minutes_ago(0.5), "agent": "pm2",  "event": "AHVO2 online. 9 agents ready. Target hari ini: Kickoff UGREEN AI NAS Hackathon 2026."},
        {"ts": minutes_ago(1),   "agent": "ops2", "event": "Setup repo template + deploy hello-world Vercel. URL live verified."},
        {"ts": minutes_ago(2),   "agent": "ops2", "event": "Dashboard server started on port 8018. state.json initialized."},
        {"ts": minutes_ago(3),   "agent": "ra2",  "event": "Started T-02: extracting UGREEN rules, rubric, eligibility, ToS links."},
        {"ts": minutes_ago(4),   "agent": "pm2",  "event": "T-01 started: master plan F0-F7 built, T-19/T-20 gates scheduled."}
    ]
    return st

def minutes_ago(m):
    from datetime import timedelta
    return (datetime.now() - timedelta(minutes=m)).isoformat(timespec="seconds")

def load():
    if not os.path.exists(STATE):
        return default_state()
    with open(STATE, encoding="utf-8") as f:
        return json.load(f)

def save(st):
    st["meta"]["updated_at"] = now_iso()
    st["log"] = st.get("log", [])[-500:]
    fd, tmp = tempfile.mkstemp(dir=DIR, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, STATE)

def add_log(st, agent, event):
    st.setdefault("log", []).append({"ts": now_iso(), "agent": agent, "event": event})

def fail(msg, hint=""):
    print("GAGAL: %s" % msg)
    if hint:
        print("Cara bener: %s" % hint)
    sys.exit(1)

def norm_task_id(raw):
    r = raw.strip().upper()
    if re.fullmatch(r"T-?\d{1,2}", r):
        return "T-%02d" % int(r.split("-")[1])
    return r

def norm_gate_id(raw):
    r = raw.strip().upper()
    m = re.fullmatch(r"G?-?\d{1,2}", r)
    return ("G%d" % int(re.sub(r"\D", "", r))) if m else r

# ---------------- subcommands ----------------
def cmd_set(a):
    st = load()
    key = a.agent.strip().lower()
    if key not in st["agents"]:
        fail("agent '%s' tidak dikenal" % a.agent,
             "pilihan sah (kode jabatan): %s" % ", ".join(st["agents"].keys()))
    ag = st["agents"][key]
    ag["status"] = a.status
    if a.task is not None:
        tid = norm_task_id(a.task)
        if tid and not any(t["id"] == tid for t in st["tasks"]):
            fail("tugas '%s' tidak ada di papan" % tid,
                 "lihat daftar: python ahvo_status.py show")
        ag["task"] = tid
    if a.progress is not None:
        if not 0 <= a.progress <= 100:
            fail("progres harus 0-100, dapat %d" % a.progress)
        ag["progress"] = a.progress
    if a.status == "done" and a.progress is None:
        ag["progress"] = 100
    if a.message:
        ag["message"] = " ".join(a.message)[:220]
    ag["updated_at"] = now_iso()
    task_str = ag.get("task") or ""
    msg_str = ag.get("message") or ""
    add_log(st, key, "STATUS set: %s%s%s" % (
        a.status.upper(),
        " pada %s (%d%%)" % (task_str, ag["progress"]) if task_str else "",
        " - %s" % msg_str if msg_str else ""))
    save(st)
    print("OKE: %s -> %s%s" % (ag["name"], a.status,
          " | %s %d%%" % (task_str, ag["progress"]) if task_str else ""))
    print("Dashboard akan menampilkan ini dalam 5 detik berikutnya.")

def cmd_task(a):
    st = load()
    tid = norm_task_id(a.id)
    task = next((t for t in st["tasks"] if t["id"] == tid), None)
    if not task:
        fail("tugas '%s' tidak ada di papan" % a.id,
             "lihat daftar: python ahvo_status.py show")
    task["status"] = a.status
    owner = st["agents"].get(task["owner"])
    if a.status == "doing" and owner and owner["status"] in ("idle", "offline", "done"):
        owner.update({"status": "working", "task": tid,
                      "message": "Mengerjakan %s: %s" % (tid, task["title"]),
                      "updated_at": now_iso()})
        add_log(st, task["owner"], "Mulai mengerjakan %s (auto-set dari TASK %s doing)." % (tid, tid))
    if a.status == "done" and owner and owner.get("task") == tid:
        owner.update({"status": "idle", "task": "", "progress": 100,
                      "message": "%s selesai; menunggu tugas berikutnya." % tid,
                      "updated_at": now_iso()})
    add_log(st, task["owner"], "TASK %s -> %s (%s)" % (tid, a.status.upper(), task["title"]))
    save(st)
    print("OKE: %s '%s' -> %s" % (tid, task["title"], a.status))
    if a.status == "doing":
        print("Catatan: agen pemilik (%s) ikut di-set working pada %s." % (task["owner"], tid))

def cmd_gate(a):
    st = load()
    gid = norm_gate_id(a.id)
    gate = next((g for g in st["gates"] if g["id"] == gid), None)
    if not gate:
        fail("gerbang '%s' tidak dikenal" % a.id,
             "pilihan sah: G1..G12 (boleh tulis angkanya saja, mis. 3)")
    gate["status"] = a.status
    gate["note"] = " ".join(a.note) if a.note else gate.get("note", "")
    if a.status == "fail":
        add_log(st, "qa2", "ALERT GATE FAIL %s: %s %s" % (gid, gate["name"], ("- " + gate["note"]) if gate["note"] else ""))
    else:
        add_log(st, "qa2", "GATE %s -> %s: %s" % (gid, a.status.upper(), gate["name"]))
    save(st)
    print("OKE: %s '%s' -> %s" % (gid, gate["name"], a.status))

def cmd_log(a):
    st = load()
    add_log(st, "founder", " ".join(a.message)[:220])
    save(st)
    print("OKE: 1 baris log ditambahkan.")

def cmd_phase(a):
    st = load()
    p = a.phase.strip().upper()
    if p not in PHASES:
        fail("fase '%s' tidak sah" % a.phase, "pilihan: F0..F7")
    old = st["meta"]["phase"]
    st["meta"]["phase"] = p
    add_log(st, "pm2", "FASE %s -> %s." % (old, p))
    save(st)
    print("OKE: fase kantor sekarang %s (sebelumnya %s)." % (p, old))

def cmd_mission(a):
    st = load()
    st["meta"]["mission"] = " ".join(a.name)[:120]
    add_log(st, "founder", "Misi lomba dicatat: %s" % st["meta"]["mission"])
    save(st)
    print("OKE: misi = %s" % st["meta"]["mission"])

def cmd_deadline(a):
    st = load()
    raw = " ".join(a.when).strip()
    dt = None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(raw, fmt); break
        except ValueError:
            pass
    if not dt:
        fail("format waktu '%s' tidak dikenali" % raw,
             'contoh benar: python ahvo_status.py deadline "2026-11-16 14:45"')
    st["meta"]["deadline"] = dt.isoformat(timespec="seconds")
    add_log(st, "pm2", "Deadline resmi dicatat: %s (waktu lokal)." % st["meta"]["deadline"])
    save(st)
    print("OKE: deadline = %s. Hitungan mundur dashboard mulai berjalan." % st["meta"]["deadline"])

def cmd_show(a):
    st = load()
    m = st["meta"]
    print("=" * 62)
    print(" %s | misi: %s | fase %s | deadline %s" % (
        m.get("company", "?"), m.get("mission") or "-", m.get("phase", "-"),
        m.get("deadline") or "-"))
    print("=" * 62)
    for t in st["tasks"]:
        ag = st["agents"].get(t["owner"], {})
        print(" %-5s [%-7s] %-28s %-9s %s" % (t["id"], t["status"], t["title"][:28], t["phase"], ag.get("name", t["owner"])))
    print("-" * 62)
    for k, ag in st["agents"].items():
        print(" %-6s %-9s %-8s tugas=%-5s prog=%3d%%  %s" % (
            ag["name"], ag["role"][:9], ag["status"], ag["task"] or "-", ag.get("progress", 0), (ag.get("message") or "")[:36]))
    n_done = sum(1 for t in st["tasks"] if t["status"] == "done")
    n_pass = sum(1 for g in st["gates"] if g["status"] == "pass")
    print("-" * 62)
    print(" tugas selesai %d/%d | gerbang PASS %d/%d" % (n_done, len(st["tasks"]), n_pass, len(st["gates"])))

def cmd_reset(a):
    save(default_state())
    print("OKE: state.json kembali ke kondisi awal (kantor kosong, semua agen offline).")

def cmd_demo(a):
    save(demo_state())
    print("OKE: data contoh ditulis ke state.json. Buka dashboard (python ahvo_serve.py)")
    print("     atau klik tombol 'Muat state.json manual'. Untuk menghapus: python ahvo_status.py reset")

# ---------------- parser ----------------
def main():
    ap = argparse.ArgumentParser(description="Pelapor status karyawan AI AHVO2")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("set", help="ubah status satu agen")
    s.add_argument("agent", help="pm2|ra2|ar2|dev2|qa2|dn2|ops2|lc2|fi2")
    s.add_argument("status", choices=AGENT_STATUSES)
    s.add_argument("-t", "--task", help="kode tugas, mis. T-07")
    s.add_argument("-p", "--progress", type=int, help="0-100")
    s.add_argument("-m", "--message", nargs="+", help="pesan singkat sedang apa")
    s.set_defaults(fn=cmd_set)

    s = sub.add_parser("task", help="ubah status satu tugas")
    s.add_argument("id", help="mis. T-07")
    s.add_argument("status", choices=TASK_STATUSES)
    s.set_defaults(fn=cmd_task)

    s = sub.add_parser("gate", help="ubah status gerbang mutu")
    s.add_argument("id", help="1..12 atau G1..G12")
    s.add_argument("status", choices=GATE_STATUSES)
    s.add_argument("note", nargs="*", help="catatan singkat (opsional)")
    s.set_defaults(fn=cmd_gate)

    s = sub.add_parser("log", help="tambah catatan aktivitas")
    s.add_argument("message", nargs="+")
    s.set_defaults(fn=cmd_log)

    s = sub.add_parser("phase", help="set fase lomba F0..F7")
    s.add_argument("phase")
    s.set_defaults(fn=cmd_phase)

    s = sub.add_parser("mission", help="set nama lomba/misi")
    s.add_argument("name", nargs="+")
    s.set_defaults(fn=cmd_mission)

    s = sub.add_parser("deadline", help='set deadline, mis. "2026-11-16 14:45"')
    s.add_argument("when", nargs="+")
    s.set_defaults(fn=cmd_deadline)

    s = sub.add_parser("show", help="ringkasan kantor di terminal")
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("reset", help="kembalikan ke kondisi awal")
    s.set_defaults(fn=cmd_reset)

    s = sub.add_parser("demo", help="isi data contoh")
    s.set_defaults(fn=cmd_demo)

    a = ap.parse_args()
    a.fn(a)

if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)