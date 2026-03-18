$ErrorActionPreference = "Stop"
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "🚀 Launching InsightPulse AI Fullstack Supreme..." -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# 1. Kill any existing instances on port 8000 and 3000 to cleanly restart
Write-Host "Clearing ports 8000 and 3000..." -ForegroundColor Yellow
$backendProcess = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($backendProcess) {
    Stop-Process -Id $backendProcess.OwningProcess -Force -ErrorAction SilentlyContinue
}
$frontendProcess = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($frontendProcess) {
    Stop-Process -Id $frontendProcess.OwningProcess -Force -ErrorAction SilentlyContinue
}

# 2. Start Backend
Write-Host "Starting FastAPI Backend Engine in background..." -ForegroundColor Magenta
Start-Process -NoNewWindow -FilePath "python.exe" -ArgumentList "-m uvicorn backend:app --host 0.0.0.0 --port 8000 --reload" -WorkingDirectory "c:\Users\Soumoditya Das\Downloads\GFG kolkata\InsightPulse_AI"

# Wait for backend
Start-Sleep -Seconds 4

# 3. Start Frontend
Write-Host "Starting Next.js Frontend Framework in background..." -ForegroundColor Green
Start-Process -NoNewWindow -FilePath "npm.cmd" -ArgumentList "run dev" -WorkingDirectory "c:\Users\Soumoditya Das\Downloads\GFG kolkata\frontend_extracted"

# Give frontend time to initialize
Write-Host "Waiting for Next.js to compile (this might take ~10 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
Write-Host "All systems GO! Launching in Chrome... Prepare for absolute SCI-FI glory!" -ForegroundColor Cyan

Start-Process "chrome.exe" "http://localhost:3000"
Write-Host "If Chrome didn't open automatically, just visit http://localhost:3000" -ForegroundColor Gray
