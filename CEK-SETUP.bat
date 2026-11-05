@echo off
REM AHVO2 - Cek Setup Otomatis
REM Jalankan dari folder AHVO2 root: D:\OneDrive\2026 - 1drive\.AHVO\AHVO2
cd /d "%~dp0"
echo ============================================================
echo  AHVO2 SETUP CHECK - UGREEN AI NAS Hackathon 2026
echo ============================================================
python z.ai\check_setup.py
echo.
pause