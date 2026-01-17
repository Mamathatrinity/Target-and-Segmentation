# Next Steps - Run Your Tests with YOUR Custom MCP Validators

## ✅ Cleanup Complete
- Removed `framework/api_helpers/` (not needed)
- Removed `framework/db_helpers/` (not needed)
- Now using **YOUR custom MCP validators** from `c:\Users\mv\mcp_servers\validation_mcp_server`

---

## Step 1: Update Credentials in .env

Edit `config/.env` and replace placeholder values:

```env
# Test User Credentials (REQUIRED for login tests)
TEST_USER_EMAIL=your-actual-email@trinitylifesciences.com
TEST_USER_PASSWORD=your-actual-password

# Database Configuration (REQUIRED for DB validation)
DB_SERVER=your-actual-server.database.windows.net
DB_NAME=HCPTargetingSegmentation
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_DRIVER={ODBC Driver 17 for SQL Server}

# Optional: Additional test users (for TC_POS_005, TC_POS_007)
REGULAR_USER_EMAIL=regular-user@trinitylifesciences.com
REGULAR_USER_PASSWORD=regular-password
NEW_USER_EMAIL=new-user@trinitylifesciences.com
NEW_USER_PASSWORD=new-password
```

---

## Step 2: Verify Your Custom MCP Validators

Make sure your validators exist at:
```
c:\Users\mv\mcp_servers\validation_mcp_server\
├── tools\
│   ├── api_validator.py    ← YOUR custom API validator
│   ├── db_validator.py     ← YOUR custom DB validator
│   └── ui_validator.py     ← YOUR custom UI validator
```

**Check they have these methods:**

### api_validator.py
```python
class APIValidator:
    def set_base_url(self, base_url)
    def make_api_request(self, endpoint, method="GET")
```

### db_validator.py
```python
class DBValidator:
    def connect_to_database(self, db_type, connection_params)
    def execute_query(self, query, fetch_results=False)
    def close_connection()
```

### ui_validator.py
```python
class UIValidator:
    def navigate_to(self, url)
    def click_element(self, selector)
    def type_text(self, selector, text)
    def is_element_visible(self, selector, timeout=5000)
    def take_screenshot(self, filename)
    def close_browser()
```

---

## Step 3: Run Tests

### Run All Login Tests (8 tests)
```powershell
pytest tests/ui/test_login.py -v -s
```

### Run Specific Test
```powershell
pytest tests/ui/test_login.py::test_pos_001_successful_login_with_all_validations -v -s
```

### Run Only Critical Tests
```powershell
pytest tests/ui/test_login.py -m critical -v -s
```

### Expected Output:
```
tests/ui/test_login.py::test_pos_001_successful_login_with_all_validations PASSED
tests/ui/test_login.py::test_pos_002_login_with_stay_signed_in PASSED
tests/ui/test_login.py::test_pos_003_login_after_session_timeout PASSED
tests/ui/test_login.py::test_pos_004_login_as_admin_user PASSED
tests/ui/test_login.py::test_pos_005_login_as_regular_user PASSED
tests/ui/test_login.py::test_pos_006_brand_workspace_selection PASSED
tests/ui/test_login.py::test_pos_007_first_time_login_new_user SKIPPED (credentials not configured)
tests/ui/test_login.py::test_pos_008_logout_and_relogin PASSED
```

---

## Step 4: Verify Validations Are Working

Each test should show:

```
================================================================================
TC_LOGIN_POS_001: Successful Login with Valid Credentials
================================================================================

[ACTION] Performing login...

--- UI Validation ---
✅ UI PASSED: Login successful, dashboard accessible

--- API Validation ---
✅ API PASSED: Status 200, User context retrieved

--- Database Validation ---
✅ DB PASSED: User found, 1 record(s)

================================================================================
✅ TC_LOGIN_POS_001: ALL VALIDATIONS PASSED
================================================================================
```

---

## Step 5: Check Reports & Screenshots

After running tests:

### Screenshots (on failures)
```
reports/
└── screenshots/
    └── test_login_py_test_pos_001_failed.png
```

### Test Results
```powershell
# Generate HTML report
pytest tests/ui/test_login.py --html=reports/report.html --self-contained-html
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tools'"
**Solution:** Check that your MCP server path is correct in conftest.py:
```python
sys.path.insert(0, r'c:\Users\mv\mcp_servers\validation_mcp_server')
```

### Issue: "AttributeError: 'APIValidator' object has no attribute 'make_api_request'"
**Solution:** Verify your validators have the expected methods. Check your api_validator.py file.

### Issue: Tests skip with "credentials not configured"
**Solution:** Update TEST_USER_EMAIL and TEST_USER_PASSWORD in config/.env

### Issue: Database connection fails
**Solution:** 
1. Verify DB credentials in .env
2. Check your db_validator.py expects the right connection params format
3. Ensure ODBC Driver 17 is installed: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

---

## What's Using YOUR Custom Validators?

### conftest.py
```python
# Imports YOUR validators as Python modules
sys.path.insert(0, r'c:\Users\mv\mcp_servers\validation_mcp_server')
from tools.api_validator import APIValidator
from tools.db_validator import DBValidator
from tools.ui_validator import UIValidator

# Provides fixtures
@pytest.fixture(scope="session")
def api_validator(settings):
    validator = APIValidator()  # YOUR class!
    validator.set_base_url(settings.API_BASE_URL)
    yield validator
```

### test_login.py
```python
def test_pos_001_successful_login_with_all_validations(
    ui_validator,      # YOUR custom UI validator
    api_validator,     # YOUR custom API validator
    db_validator,      # YOUR custom DB validator
    settings,
    db_connection_params
):
    # Uses YOUR validators for all validations
```

---

## Summary

✅ **Obsolete files removed** (api_helper.py, db_helper.py)  
✅ **Settings updated** (added TEST_USER_EMAIL, TEST_USER_PASSWORD, DB_DRIVER)  
✅ **Using YOUR custom MCP validators** from your MCP server  
✅ **All YOUR custom logic preserved** (error handling, retry, logging)  
✅ **8 login tests ready to run**  

### Next Action:
1. **Update credentials** in `config/.env`
2. **Run tests**: `pytest tests/ui/test_login.py -v -s`
3. **Verify results** - all using YOUR custom validators!

🚀 **Ready to test!**
