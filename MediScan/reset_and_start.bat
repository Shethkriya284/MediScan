@echo off
echo Stopping Python processes...
taskkill /F /IM python.exe 2>nul

echo Waiting for processes to close...
timeout /t 3 /nobreak >nul

echo Deleting old database...
del instance\mediscan.db 2>nul

echo Starting server with fresh database...
python app.py

pause
