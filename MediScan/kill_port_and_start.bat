@echo off
echo ========================================
echo  Killing Port 5001 and Starting Server
echo ========================================
echo.

echo Step 1: Finding process on port 5001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5001') do (
    echo Found PID: %%a
    echo Killing process...
    taskkill /F /PID %%a 2>nul
)

echo.
echo Step 2: Waiting 2 seconds...
timeout /t 2 /nobreak >nul

echo.
echo Step 3: Starting Flask server...
python app.py

pause
