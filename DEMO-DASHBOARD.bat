@echo off
REM AHVO2 - Demo Dashboard (isi data contoh)
REM Jalankan dari folder AHVO2 root
cd /d "%~dp0"
echo ============================================================
echo  AHVO2 DEMO DASHBOARD
echo ============================================================
echo Mengisi state.json dengan data contoh...
python dashboard\ahvo_status.py demo
echo.
echo Data contoh ditulis. Sekarang jalankan MULAI-DASHBOARD.bat
echo atau buka dashboard\dashboard.html manual (perlu server).
echo ============================================================
pause