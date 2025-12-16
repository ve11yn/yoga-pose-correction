# YogaFlow AI - Startup Script (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   YogaFlow AI - Startup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kill any existing processes on ports 3000 and 8000
Write-Host "Checking for existing processes..." -ForegroundColor Yellow

# Kill processes on port 3000
$port3000 = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
if ($port3000) {
    $pid3000 = $port3000.OwningProcess
    Write-Host "Terminating process on port 3000 (PID: $pid3000)" -ForegroundColor Yellow
    Stop-Process -Id $pid3000 -Force -ErrorAction SilentlyContinue
}

# Kill processes on port 8000
$port8000 = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($port8000) {
    $pid8000 = $port8000.OwningProcess
    Write-Host "Terminating process on port 8000 (PID: $pid8000)" -ForegroundColor Yellow
    Stop-Process -Id $pid8000 -Force -ErrorAction SilentlyContinue
}

# Remove Next.js lock file if it exists
$lockFile = Join-Path $PSScriptRoot "frontend\.next\dev\lock"
if (Test-Path $lockFile) {
    Write-Host "Removing Next.js lock file..." -ForegroundColor Yellow
    Remove-Item $lockFile -Force -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Starting servers..." -ForegroundColor Green
Write-Host ""

# Get the script directory
$scriptDir = $PSScriptRoot

# Start Backend
$backendPath = Join-Path $scriptDir "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host 'Starting Backend...' -ForegroundColor Cyan; pip install -r requirements.txt; Write-Host ''; Write-Host 'Backend is starting...' -ForegroundColor Green; python main.py" -WindowStyle Normal

# Wait a moment before starting frontend
Start-Sleep -Seconds 2

# Start Frontend
$frontendPath = Join-Path $scriptDir "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'Starting Frontend...' -ForegroundColor Cyan; npm install; Write-Host ''; Write-Host 'Frontend is starting...' -ForegroundColor Green; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Servers are starting in new windows:" -ForegroundColor Green
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit this launcher..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
