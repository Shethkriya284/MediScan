@echo off
echo Starting MediScan Application with ngrok...
echo.

REM Start Flask app in a new window
start "Flask App" cmd /k python app.py

REM Wait for Flask to start
echo Waiting for Flask to start...
timeout /t 5 /nobreak >nul

REM Start ngrok in a new window
start "ngrok" cmd /k ngrok.exe http 5000

echo.
echo ========================================
echo Both services are starting!
echo ========================================
echo.
echo Flask App: Running on http://localhost:5000
echo ngrok: Check the ngrok window for your public URL
echo.
echo Look for the line that says:
echo Forwarding    https://xxxx.ngrok-free.app
echo.
echo Share that HTTPS URL with your group members!
echo.
echo Press any key to stop both services...
pause >nul

REM Kill Flask and ngrok when done
taskkill /FI "WINDOWTITLE eq Flask App*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq ngrok*" /F >nul 2>&1
taskkill /IM python.exe /F >nul 2>&1
taskkill /IM ngrok.exe /F >nul 2>&1

echo Services stopped.
