# Non-interactive Render deployment helper for AirTraffic
# Usage: run in PowerShell: .\scripts\deploy_render_headless.ps1

Push-Location .
$remote = git config --get remote.origin.url 2>$null
if (-not $remote) { Write-Host 'Cannot detect git remote. Please open https://dashboard.render.com/new and select your repo.' -ForegroundColor Yellow; Pop-Location; exit 0 }

$importUrl = "https://dashboard.render.com/new?repo=${remote}"
Write-Host "Opening Render import page: $importUrl" -ForegroundColor Cyan
try { Start-Process $importUrl } catch { Write-Host "Please open: $importUrl" -ForegroundColor Yellow }

Write-Host "\nFollow these manual steps in the Render UI:" -ForegroundColor Green
Write-Host "1) Create Web Service (backend)" -ForegroundColor Cyan
Write-Host "   - Name: aeroshield-backend" -NoNewline; Write-Host ""; Write-Host "   - Environment: Docker or Python" -NoNewline; Write-Host ""; Write-Host "   - Root Directory: (repo root)" -NoNewline; Write-Host ""; Write-Host "   - Build Command: pip install -r requirements.txt" -NoNewline; Write-Host ""; Write-Host "   - Start Command: gunicorn backend.server:app --bind 0.0.0.0:$PORT --workers 2" -NoNewline; Write-Host ""; Write-Host "   - Health check path: /api/status" -NoNewline; Write-Host ""

Write-Host "2) Create Static Site (frontend)" -ForegroundColor Cyan
Write-Host "   - Name: aeroshield-frontend" -NoNewline; Write-Host ""; Write-Host "   - Root Directory: frontend" -NoNewline; Write-Host ""; Write-Host "   - Build Command: npm install && npm run build" -NoNewline; Write-Host ""; Write-Host "   - Publish Directory: dist" -NoNewline; Write-Host ""; Write-Host "   - Env vars (set after backend deploy):" -NoNewline; Write-Host ""; Write-Host "       VITE_API_BASE_URL = https://<your-backend-host>" -NoNewline; Write-Host ""; Write-Host "       VITE_BASE_PATH = /" -NoNewline; Write-Host ""

Write-Host "After both services are built, re-deploy frontend with the backend URL set to make the app live." -ForegroundColor Green
Pop-Location
