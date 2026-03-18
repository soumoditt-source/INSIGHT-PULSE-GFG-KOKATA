# InsightPulse AI - Universal Launch Script
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host " INSIGHTPULSE AI: J.A.R.V.I.S. INTELLIGENCE SYSTEM " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

Write-Host "`n[1/3] Clearing old ports (3000, 8000)..." -ForegroundColor Yellow
npx kill-port 3000
npx kill-port 8000

Write-Host "`n[2/3] Initializing Data Core Backend (FastAPI - Port 8000)..." -ForegroundColor Green
$backendPath = "c:\Users\Soumoditya Das\Downloads\GFG kolkata\InsightPulse_AI"
Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$backendPath'; Write-Host '--- BACKEND LOGS ---'; uvicorn backend:app --host 0.0.0.0 --port 8000 --reload`""

Write-Host "`n[3/3] Initializing Visual Interface (Next.js - Port 3000)..." -ForegroundColor Green
$frontendPath = "c:\Users\Soumoditya Das\Downloads\GFG kolkata\frontend_extracted"
Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$frontendPath'; Write-Host '--- FRONTEND LOGS ---'; npx next dev -H 127.0.0.1`""

Write-Host "`nALL SYSTEMS ONLINE! 🚀" -ForegroundColor Cyan
Write-Host "Frontend: http://127.0.0.1:3000" -ForegroundColor White
Write-Host "Backend:  http://127.0.0.1:8000/docs" -ForegroundColor White

Write-Host "`n[4/4] Launching Google Chrome prototype (waiting for Next.js cold start)..." -ForegroundColor Yellow
Start-Sleep -Seconds 12
Start-Process "chrome.exe" -ArgumentList "http://127.0.0.1:3000" -ErrorAction SilentlyContinue

Write-Host "`nYou can close this window. Check the two new terminal windows for server logs." -ForegroundColor Gray
