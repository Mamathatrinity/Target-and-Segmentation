# Setup Script for CI/CD-Ready Test Automation Framework
# Trinity HCP Targeting & Segmentation Application
# Run this script to set up the framework for local testing or CI/CD

# Stop on errors
$ErrorActionPreference = "Stop"

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "Trinity Test Automation - Setup Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Step 1: Create virtual environment
Write-Host "`n[1/6] Creating Python virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   Virtual environment already exists. Skipping..." -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "   ✅ Virtual environment created" -ForegroundColor Green
}

# Step 2: Activate virtual environment
Write-Host "`n[2/6] Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
Write-Host "   ✅ Virtual environment activated" -ForegroundColor Green

# Step 3: Upgrade pip
Write-Host "`n[3/6] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null
Write-Host "   ✅ Pip upgraded" -ForegroundColor Green

# Step 4: Install Python dependencies
Write-Host "`n[4/6] Installing Python packages..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "   ✅ Python packages installed" -ForegroundColor Green

# Step 5: Install Playwright browsers
Write-Host "`n[5/6] Installing Playwright browsers..." -ForegroundColor Yellow
Write-Host "   This may take several minutes..." -ForegroundColor Gray
playwright install chromium firefox
playwright install-deps
Write-Host "   ✅ Playwright browsers installed" -ForegroundColor Green

# Step 6: Create directories
Write-Host "`n[6/6] Creating necessary directories..." -ForegroundColor Yellow
$directories = @("reports", "reports/screenshots", "reports/videos", "logs")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "   Created: $dir" -ForegroundColor Gray
    }
}
Write-Host "   ✅ Directories created" -ForegroundColor Green

# Verify .env file
Write-Host "`n[Configuration Check]" -ForegroundColor Yellow
if (Test-Path "config\.env") {
    Write-Host "   ✅ .env file exists" -ForegroundColor Green
    Write-Host "   Please ensure all credentials are configured:" -ForegroundColor Cyan
    Write-Host "      - TEST_USER_EMAIL" -ForegroundColor Gray
    Write-Host "      - TEST_USER_PASSWORD" -ForegroundColor Gray
    Write-Host "      - DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD" -ForegroundColor Gray
} else {
    Write-Host "   ⚠️  .env file not found!" -ForegroundColor Red
    Write-Host "   Please create config\.env with your credentials" -ForegroundColor Yellow
}

# Display next steps
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. Configure config\.env with your credentials" -ForegroundColor White
Write-Host "2. Run tests:" -ForegroundColor White
Write-Host "   pytest tests/ui/test_login.py -v -s" -ForegroundColor Gray
Write-Host "3. Run in headless mode:" -ForegroundColor White
Write-Host "   pytest tests/ui/test_login.py --headless -v" -ForegroundColor Gray
Write-Host "4. Run with specific browser:" -ForegroundColor White
Write-Host "   pytest tests/ui/test_login.py --browser=firefox -v" -ForegroundColor Gray
Write-Host "5. Run with HTML report:" -ForegroundColor White
Write-Host "   pytest tests/ui/test_login.py --html=reports/report.html --self-contained-html" -ForegroundColor Gray

Write-Host "`nFor CI/CD:" -ForegroundColor Cyan
Write-Host "- GitHub Actions: .github/workflows/test.yml" -ForegroundColor Gray
Write-Host "- Azure DevOps: azure-pipelines.yml" -ForegroundColor Gray

Write-Host "`n"
