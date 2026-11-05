@echo off
REM AHVO2 - Mulai Dashboard Mission Control
REM Jalankan dari folder AHVO2 root
cd /d "%~dp0"
echo ============================================================
echo  AHVO2 MISSION CONTROL - Dashboard Server
echo ============================================================
echo Menjalankan: python dashboard\ahvo_serve.py
echo Dashboard akan terbuka di http://localhost:8018
echo Biarkan jendela ini terbuka selama memantau.
echo Tekan Ctrl+C untuk berhenti.
echo ============================================================
python dashboard\ahvo_serve.py
pause