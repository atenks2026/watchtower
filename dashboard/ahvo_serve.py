#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AHVO2 - ahvo_serve.py
Server mini tanpa dependensi untuk dashboard Mission Control AHVO2.

ID: Cara pakai (Founder):
  python ahvo_serve.py            -> buka http://localhost:8018 otomatis
  python ahvo_serve.py 9000       -> pakai port lain
Biarkan terminal ini terbuka selama kamu memantau. Tekan Ctrl+C untuk berhenti.
Data tidak dikirim ke internet; semua berjalan di komputermu sendiri (gratis).
"""
import http.server, os, socketserver, sys, threading, webbrowser

DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kw):
        super().__init__(*args, directory=DIR, **kw)

    def do_GET(self):
        # root path -> serve dashboard.html (default landing page)
        if self.path in ("/", ""):
            self.path = "/dashboard.html"
        return super().do_GET()

    def end_headers(self):
        # cegah cache supaya dashboard selalu membaca state.json terbaru
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # diamkan log akses agar terminal bersih

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8018
    url = "http://localhost:%d" % port
    try:
        srv = socketserver.ThreadingTCPServer(("127.0.0.1", port), Handler)
    except OSError:
        print("GAGAL: port %d sedang dipakai. Coba: python ahvo_serve.py %d"
              % (port, port + 1))
        sys.exit(1)
    srv.allow_reuse_address = True
    print("=" * 60)
    print(" AHVO2 - AI Hackathon Virtual Office 2 | Mission Control")
    print(" Dashboard : %s" % url)
    print(" Folder    : %s" % DIR)
    print(" Ctrl+C untuk berhenti. Biarkan jalan selama memantau.")
    print("=" * 60)
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dimatikan. Sampai jumpa di shift berikutnya.")

if __name__ == "__main__":
    main()