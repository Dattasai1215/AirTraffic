# Render deployment helper for AirTraffic
# Usage: Open PowerShell and run: .\scripts\deploy_render.ps1
# This script helps you import the repo into Render and provides curl templates
# It does NOT upload your API key anywhere. You can cancel at any prompt.

function Read-SecretEnv {
    param([string]$Name)
    $val = [System.Environment]::GetEnvironmentVariable($Name, 'User')
    if (-not $val) {
        $val = Read-Host -Prompt "Enter $Name (will not be stored by this script)"
    }
    return $val
}

Write-Host "This helper will guide you to create two Render services (backend web + frontend static site)." -ForegroundColor Cyan

# Detect GitHub repo URL
Push-Location .
$remote = git config --get remote.origin.url 2>$null
if (-not $remote) { $remote = Read-Host 'Cannot detect git remote. Paste your GitHub repo URL' }
Write-Host "Detected repo: $remote" -ForegroundColor Green

# Ask for Render API key (optional; only needed for API automation)
$renderApiKey = Read-SecretEnv -Name 'RENDER_API_KEY'
if (-not $renderApiKey) {
    Write-Host "No RENDER_API_KEY provided. The script will open the Render import page in your browser for manual import." -ForegroundColor Yellow
}

# Open Render import page (manual path)
try {
    $importUrl = "https://dashboard.render.com/new?repo=${remote}"
    Write-Host "Opening Render import page: $importUrl" -ForegroundColor Cyan
    Start-Process $importUrl
} catch {
    Write-Host "Unable to open browser automatically. Please visit: https://dashboard.render.com/new and select your repo." -ForegroundColor Yellow
}

Write-Host "\nAfter importing the repo into Render, create two services as follows in the Render UI:" -ForegroundColor Cyan
Write-Host "1) Web Service (backend)" -ForegroundColor Green
Write-Host "   - Name: aeroshield-backend" -NoNewline; Write-Host ""; Write-Host "   - Environment: Docker (or Python)" -NoNewline; Write-Host ""; Write-Host "   - Root Directory: (repo root)" -NoNewline; Write-Host ""; Write-Host "   - Build Command: pip install -r requirements.txt" -NoNewline; Write-Host ""; Write-Host "   - Start Command: gunicorn backend.server:app --bind 0.0.0.0:$PORT --workers 2" -NoNewline; Write-Host ""; Write-Host "   - Health check path: /api/status" -NoNewline; Write-Host ""

Write-Host "2) Static Site (frontend)" -ForegroundColor Green
Write-Host "   - Name: aeroshield-frontend" -NoNewline; Write-Host ""; Write-Host "   - Root Directory: frontend" -NoNewline; Write-Host ""; Write-Host "   - Build Command: npm install && npm run build" -NoNewline; Write-Host ""; Write-Host "   - Publish Directory: dist" -NoNewline; Write-Host ""; Write-Host "   - Set env var: VITE_API_BASE_URL=https://<your-backend-host>" -NoNewline; Write-Host ""; Write-Host "   - Set env var: VITE_BASE_PATH=/ (or /AirTraffic/ for GitHub Pages)" -NoNewline; Write-Host ""

if ($renderApiKey) {
    Write-Host "\nYou provided a Render API key. The script can optionally set environment variables for an existing service if you provide the service ID." -ForegroundColor Cyan
    $setEnv = Read-Host 'Do you want to set env vars via the API now? (y/n)'
    if ($setEnv -match '^[Yy]') {
        $serviceId = Read-Host 'Enter the Render service ID (example: srv-xxxx). Leave blank to skip'
        if ($serviceId) {
            $backendUrl = Read-Host 'Enter the public backend URL (https://...)'
            $envTemplate = @{
                key = 'VITE_API_BASE_URL'
                value = $backendUrl
                secure = $false
            }
            $payload = @{
                envVars = @($envTemplate)
            } | ConvertTo-Json -Depth 5

            $headers = @{
                Authorization = "Bearer $renderApiKey"
                'Content-Type' = 'application/json'
            }

            $apiUrl = "https://api.render.com/v1/services/$serviceId/env-vars"
            Write-Host "Setting env var via Render API: $apiUrl" -ForegroundColor Cyan
            $resp = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers $headers -Body $payload -ErrorAction SilentlyContinue
            if ($resp) { Write-Host "Environment variable set. Response: $($resp | ConvertTo-Json -Depth 2)" -ForegroundColor Green }
            else { Write-Host "API call failed. You may need to set env vars manually in Render UI." -ForegroundColor Red }
        }
    }
}

Write-Host "\nDone. After Render builds both services, set the frontend env var `VITE_API_BASE_URL` to your backend URL and rebuild if necessary." -ForegroundColor Cyan

Pop-Location
