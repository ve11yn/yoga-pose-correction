@echo off
echo Starting YogaFlow AI...
echo.

start cmd /k "cd backend && echo Starting Backend... && pip install -r requirements.txt && python main.py"
start cmd /k "cd frontend && echo Starting Frontend... && npm install && npm run dev"

echo Servers are starting in new windows.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this launcher...
pause >nul
