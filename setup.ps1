# Setup Script for Target and Segmentation Automation Project
Write-Host "
========================================" -ForegroundColor Cyan
Write-Host " Target & Segmentation Automation Setup" -ForegroundColor Cyan
Write-Host "========================================
" -ForegroundColor Cyan

# Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "
[2/5] Installing Python packages..." -ForegroundColor Yellow
pip install -r requirements.txt

# Install Playwright browsers
Write-Host "
[3/5] Installing Playwright browsers..." -ForegroundColor Yellow
playwright install chromium

# Setup environment
Write-Host "
[4/5] Setting up environment..." -ForegroundColor Yellow
if (!(Test-Path "config\.env")) {
    Copy-Item "config\.env.example" "config\.env"
    Write-Host "Created config\.env - Please update with your settings!" -ForegroundColor Green
}

# Test configuration
Write-Host "
[5/5] Verifying setup..." -ForegroundColor Yellow
pytest --collect-only

Write-Host "
========================================" -ForegroundColor Green
Write-Host " Setup Complete!" -ForegroundColor Green
Write-Host "========================================
" -ForegroundColor Green

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit config\.env with your credentials"
Write-Host "2. Run: pytest -m smoke"
Write-Host "3. Use @validation-server in Copilot Chat"
Write-Host "
See QUICKSTART.md for more info
"
