@echo off
echo ========================================
echo    YogaFlow AI - Startup Script
echo ========================================
echo.

REM Kill any existing processes on ports 3000 and 8000
echo Checking for existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    echo Terminating process on port 3000 (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Terminating process on port 8000 (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

REM Remove Next.js lock file if it exists
if exist "frontend\.next\dev\lock" (
    echo Removing Next.js lock file...
    del /F /Q "frontend\.next\dev\lock" >nul 2>&1
)

echo.
echo Starting servers...
echo.

REM Start Backend
start "YogaFlow Backend" cmd /k "cd /d %~dp0backend && echo Starting Backend... && pip install -r requirements.txt && echo. && echo Backend is starting... && python main.py"

REM Wait a moment before starting frontend
timeout /t 2 /nobreak >nul

REM Start Frontend
start "YogaFlow Frontend" cmd /k "cd /d %~dp0frontend && echo Starting Frontend... && npm install && echo. && echo Frontend is starting... && npm run dev"

echo.
echo ========================================
echo Servers are starting in new windows:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit this launcher...
pause >nul
