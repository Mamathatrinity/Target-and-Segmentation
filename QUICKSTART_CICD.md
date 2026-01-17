# Quick Start Guide - CI/CD-Ready Framework

## ✅ Framework is Ready for CI/CD!

Your test automation framework has been **completely refactored** from MCP Server to **standard Python libraries** (Playwright, requests, pyodbc).

---

## 🚀 Get Started in 3 Steps

### Step 1: Setup Environment
```powershell
# Run the setup script (installs everything)
.\setup_cicd.ps1
```

### Step 2: Configure Credentials
Edit `config/.env` file with your actual credentials:
```env
# Application URLs
APP_URL=https://ce-ts-dev.trinitylifesciences.com
API_BASE_URL=https://app-hcptargetandsegmentation-api-dev.azurewebsites.net/api/v1

# Test User Credentials
TEST_USER_EMAIL=your-email@trinitylifesciences.com
TEST_USER_PASSWORD=your-password

# Database Connection
DB_SERVER=your-sql-server.database.windows.net
DB_NAME=your-database-name
DB_USER=your-db-username
DB_PASSWORD=your-db-password
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### Step 3: Run Tests
```powershell
# Run first positive test
pytest tests/ui/test_login.py::test_pos_001_successful_login_with_all_validations -v -s

# Run all 3 positive tests
pytest tests/ui/test_login.py -v -s
```

---

## 📋 What Changed?

| **Before (MCP Server)** | **After (Standard Libraries)** |
|-------------------------|-------------------------------|
| ❌ Only works in VS Code | ✅ Works anywhere (local, CI/CD, Docker) |
| ❌ Manual interaction needed | ✅ Fully automated |
| ❌ Can't run in pipelines | ✅ Ready for GitHub Actions, Azure DevOps |
| ❌ Custom MCP tools | ✅ Industry-standard Playwright, requests, pyodbc |

---

## 🔧 Commands

### Local Testing:
```powershell
# Run with visible browser
pytest tests/ui/test_login.py -v -s

# Run in headless mode (no browser window)
pytest tests/ui/test_login.py --headless -v

# Run with Firefox instead of Chromium
pytest tests/ui/test_login.py --browser=firefox -v

# Generate HTML report
pytest tests/ui/test_login.py --html=reports/report.html --self-contained-html

# Run with slow motion (500ms delay per action)
pytest tests/ui/test_login.py --slowmo=500 -v
```

### CI/CD Deployment:

**GitHub Actions:**
1. Push code to GitHub
2. Pipeline runs automatically (`.github/workflows/test.yml`)
3. Runs on Chromium + Firefox
4. Reports uploaded as artifacts

**Azure DevOps:**
1. Push code to Azure Repos
2. Pipeline runs automatically (`azure-pipelines.yml`)
3. Results published to Test Results tab
4. Screenshots saved on failures

---

## 📁 File Structure

```
framework/
├── api_helpers/
│   └── api_helper.py          ← Handles API requests (requests library)
├── db_helpers/
│   └── db_helper.py           ← Handles DB queries (pyodbc library)
└── page_objects/
    ├── base_page.py           ← Uses Playwright Page object
    └── login_page.py          ← All page objects refactored

tests/
├── conftest.py                ← Standard Playwright fixtures
└── ui/
    └── test_login.py          ← 3 positive tests ready

.github/workflows/test.yml     ← GitHub Actions pipeline
azure-pipelines.yml            ← Azure DevOps pipeline
setup_cicd.ps1                 ← One-command setup script
```

---

## ✅ Tests Implemented (3 of 8 Positive Cases)

1. ✅ **TC_LOGIN_POS_001** - Successful Login (UI + API + DB validations)
2. ✅ **TC_LOGIN_POS_002** - Login with Stay Signed In (UI + API)
3. ✅ **TC_LOGIN_POS_003** - Login After Session Timeout (UI + API + DB)
4. ⏳ TC_LOGIN_POS_004 - Admin User (pending)
5. ⏳ TC_LOGIN_POS_005 - Regular User (pending)
6. ⏳ TC_LOGIN_POS_006 - Brand Selection (pending)
7. ⏳ TC_LOGIN_POS_007 - First-Time Login (pending)
8. ⏳ TC_LOGIN_POS_008 - Logout & Re-login (pending)

---

## 🎯 Next Actions

1. **Update credentials** in `config/.env`
2. **Run setup script**: `.\setup_cicd.ps1`
3. **Test the framework**: `pytest tests/ui/test_login.py::test_pos_001 -v -s`
4. **Verify all 3 tests pass**
5. **Deploy to CI/CD** (GitHub/Azure) when ready

---

## 💡 Key Benefits

✅ **Agent handles everything** - Playwright automates browser, API, DB operations  
✅ **CI/CD ready** - Runs in GitHub Actions, Azure DevOps, Jenkins, etc.  
✅ **Headless execution** - No GUI needed for automation  
✅ **Parallel tests** - Run multiple tests simultaneously  
✅ **Cross-browser** - Test on Chromium, Firefox, WebKit  
✅ **Screenshots on failure** - Automatic debugging aid  
✅ **Standard tooling** - Easy for teams to understand  

---

## 🆘 Troubleshooting

**Issue: Playwright not found**
```powershell
playwright install chromium
playwright install-deps
```

**Issue: ODBC Driver error**
```powershell
# Windows: Download ODBC Driver 17 for SQL Server
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

**Issue: Import errors**
```powershell
# Ensure you're in virtual environment
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 📚 Documentation

- **Full refactor details**: [REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md)
- **Test case documentation**: [TEST_CASES_LOGIN.md](TEST_CASES_LOGIN.md)
- **Validation matrix**: [LOGIN_VALIDATION_MATRIX.md](LOGIN_VALIDATION_MATRIX.md)

---

**Framework Status: ✅ CI/CD READY - All agent-based, fully automated!**
