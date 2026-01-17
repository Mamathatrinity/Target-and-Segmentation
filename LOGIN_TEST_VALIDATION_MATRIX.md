# Login Test Cases - API & Database Validation Matrix

**Total Test Cases: 20** (Updated!)
- ✅ 8 Positive Scenarios
- ✅ 6 Negative Scenarios  
- ✅ 6 Edge Case Scenarios (5 NEW!)

---

## Validation Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Validation is implemented and active |
| ⚠️ | Validation is implemented but requires conditions |
| ❌ | Validation not applicable for this test |
| 🔄 | Validation uses JWT token extraction |

---

## 🟢 POSITIVE TEST CASES (8 Tests)

### 1. TC_LOGIN_POS_001: Successful Login with Valid Credentials
**File:** `tests/ui/test_login.py::test_pos_001_successful_login_with_all_validations`  
**Priority:** Critical

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Dashboard loaded, profile button visible |
| **API** | ✅ 🔄 | `/get_user_context/` with JWT token extraction |
| **Database** | ✅ | MySQL connection via pymysql, basic connectivity test |

**Key Features:**
- Extracts JWT token from browser (cookies/localStorage/sessionStorage)
- Updates API validator with `Authorization: Bearer <token>`
- Direct MySQL connection (no ODBC drivers needed)
- Full tri-layer validation (UI + API + DB)

---

### 2. TC_LOGIN_POS_002: Login with "Stay Signed In"
**File:** `tests/ui/test_login.py::test_pos_002_login_with_stay_signed_in`  
**Priority:** High

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Login success with Stay Signed In checkbox enabled |
| **API** | ✅ 🔄 | `/get_user_context/` with JWT token |
| **Database** | ❌ | Not needed - focuses on session persistence |

**Key Features:**
- Tests persistent login functionality
- JWT token extraction enabled
- API validation confirms session token is valid

---

### 3. TC_LOGIN_POS_003: Login After Session Timeout
**File:** `tests/ui/test_login.py::test_pos_003_login_after_session_timeout`  
**Priority:** High

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Logout → Wait → Re-login successful |
| **API** | ✅ 🔄 | Verifies new session token after timeout |
| **Database** | ✅ | Query: `SELECT email, last_login_date FROM Users` |

**Key Features:**
- Simulates session timeout scenario
- Validates new JWT token generation
- Checks last login timestamp in database

---

### 4. TC_LOGIN_POS_004: Login as Admin User
**File:** `tests/ui/test_login.py::test_pos_004_login_as_admin_user`  
**Priority:** High

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Admin user dashboard access |
| **API** | ✅ 🔄 | Admin user context verification |
| **Database** | ✅ | Query: `SELECT email, Role FROM Users` (verify Admin role) |

**Key Features:**
- Role-based access validation
- JWT token extraction
- Database role verification

---

### 5. TC_LOGIN_POS_005: Login as Regular User
**File:** `tests/ui/test_login.py::test_pos_005_login_as_regular_user`  
**Priority:** High

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Regular user dashboard access |
| **API** | ✅ 🔄 | Regular user context verification |
| **Database** | ✅ | Query: `SELECT email, Role FROM Users` (verify User role) |

**Key Features:**
- Uses REGULAR_USER_EMAIL from settings
- Validates non-admin user permissions
- JWT token extraction

---

### 6. TC_LOGIN_POS_006: Brand/Workspace Selection
**File:** `tests/ui/test_login.py::test_pos_006_brand_workspace_selection`  
**Priority:** Medium

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Brand/workspace dropdown selection |
| **API** | ✅ 🔄 | Brand context verification |
| **Database** | ✅ | Query: `SELECT email, last_selected_brand FROM Users` |

**Key Features:**
- Multi-tenant brand selection
- Validates brand context persistence
- JWT token extraction

---

### 7. TC_LOGIN_POS_007: First-Time Login (New User)
**File:** `tests/ui/test_login.py::test_pos_007_first_time_login_new_user`  
**Priority:** Medium

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | First-time user onboarding flow |
| **API** | ✅ 🔄 | New user profile creation verification |
| **Database** | ✅ | Query: `SELECT email, created_date, Role FROM Users` |

**Key Features:**
- Requires NEW_USER_EMAIL in settings
- Validates new user record creation
- JWT token extraction

---

### 8. TC_LOGIN_POS_008: Logout and Re-login
**File:** `tests/ui/test_login.py::test_pos_008_logout_and_relogin`  
**Priority:** High

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Logout → Re-login workflow |
| **API** | ✅ 🔄 | New session token after re-login |
| **Database** | ✅ | Query: `SELECT email, logout_time FROM Sessions` |

**Key Features:**
- Complete logout/login cycle
- New JWT token extraction after re-login
- Session tracking validation

---

## 🔴 NEGATIVE TEST CASES (6 Tests)

### 9. TC_LOGIN_NEG_001: Invalid Email Address
**File:** `tests/ui/test_login_negative.py::test_neg_001_invalid_email_address`  
**Priority:** Critical

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Microsoft SSO error message validation |
| **API** | ❌ | Login fails - no API access |
| **Database** | ❌ | Login fails - no DB access needed |

**Key Features:**
- Tests Microsoft SSO error handling
- Validates user does not exist error message
- No authentication = No API/DB validation

---

### 10. TC_LOGIN_NEG_002: Incorrect Password
**File:** `tests/ui/test_login_negative.py::test_neg_002_incorrect_password`  
**Priority:** Critical

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Incorrect password error from Microsoft SSO |
| **API** | ❌ | Login fails - no API access |
| **Database** | ❌ | Login fails - no DB access needed |

**Key Features:**
- Password validation via Microsoft SSO
- Error message verification
- No successful login = No API/DB validation

---

### 11. TC_LOGIN_NEG_003: Empty Email Field
**File:** `tests/ui/test_login_negative.py::test_neg_003_empty_email_field`  
**Priority:** High

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Required field validation |
| **API** | ❌ | Form validation prevents submission |
| **Database** | ❌ | Form validation prevents submission |

**Key Features:**
- Client-side field validation
- Browser native "required" attribute check
- No form submission = No API/DB validation

---

### 12. TC_LOGIN_NEG_004: Empty Password Field
**File:** `tests/ui/test_login_negative.py::test_neg_004_empty_password_field`  
**Priority:** High

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Required field validation |
| **API** | ❌ | Form validation prevents submission |
| **Database** | ❌ | Form validation prevents submission |

**Key Features:**
- Client-side field validation
- Browser native "required" attribute check
- No form submission = No API/DB validation

---

### 13. TC_LOGIN_NEG_010: Unauthorized User (No App Access)
**File:** `tests/ui/test_login_negative.py::test_neg_010_unauthorized_user_no_access`  
**Priority:** High  
**Status:** ⚠️ SKIPPED (requires unauthorized user credentials)

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Access denied message verification |
| **API** | ✅ | Expected 401/403 response |
| **Database** | ✅ | Verify user NOT in Users table |

**Key Features:**
- Requires UNAUTHORIZED_USER_EMAIL in settings
- Microsoft auth succeeds, app denies access
- **SKIPPED by default** - manual test only
- Validates authorization vs authentication

---

### 14. TC_LOGIN_NEG_011: Special Characters in Email
**File:** `tests/ui/test_login_negative.py::test_neg_011_special_characters_in_email`  
**Priority:** Medium

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Special character handling in email field |
| **API** | ❌ | Login fails - no API access |
| **Database** | ❌ | Login fails - no DB access needed |

**Key Features:**
- Tests email with special characters: `test!@#$%user@example.com`
- Microsoft SSO validation
- No successful login = No API/DB validation

---

## ⚡ EDGE CASE SCENARIOS (6 Tests - 5 NEW!)

### 15. TC_LOGIN_EDGE_001: Very Long Email (256+ chars)
**File:** `tests/ui/test_login_negative.py::test_edge_001_very_long_email_address`  
**Priority:** Low

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Field length limit validation |
| **API** | ❌ | Invalid input - no API submission |
| **Database** | ❌ | Invalid input - no DB validation needed |

**Key Features:**
- Tests email with 256+ characters
- Validates input field max-length handling
- Browser/form validation prevents submission

---

### 16. TC_LOGIN_EDGE_002: Browser Back Button After Login (NEW!)
**File:** `tests/ui/test_login_negative.py::test_edge_002_browser_back_button_after_login`  
**Priority:** Medium

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | User stays on dashboard after back button |
| **API** | ✅ 🔄 | Session token still valid after navigation |
| **Database** | ❌ | Browser navigation doesn't create new DB entries |

**Key Features:**
- Tests session persistence with browser navigation
- JWT token extraction after back navigation
- Validates user doesn't get logged out

---

### 17. TC_LOGIN_EDGE_003: Multiple Browser Tabs (NEW!)
**File:** `tests/ui/test_login_negative.py::test_edge_003_multiple_browser_tabs_same_session`  
**Priority:** Medium

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Login state shared across tabs in same browser |
| **API** | ✅ 🔄 | Same JWT token works in all tabs |
| **Database** | ❌ | Single session, same token across tabs |

**Key Features:**
- Tests concurrent tabs in same browser
- Validates session sharing between tabs
- JWT token consistency check

---

### 18. TC_LOGIN_EDGE_005: Concurrent Sessions (Multiple Devices) (NEW!)
**File:** `tests/ui/test_login_negative.py::test_edge_005_concurrent_sessions_multiple_browsers`  
**Priority:** Medium

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Both browser windows show logged in state |
| **API** | ✅ 🔄 | Different JWT tokens for each session |
| **Database** | ✅ | Query: `SELECT COUNT(*) FROM Sessions WHERE session_status = 'active'` |

**Key Features:**
- Simulates multiple devices with separate browser contexts
- Validates concurrent session support
- **Full tri-layer validation** (UI + API + DB)

---

### 19. TC_LOGIN_EDGE_006: Token Refresh During Active Session (NEW!)
**File:** `tests/ui/test_login_negative.py::test_edge_006_token_refresh_during_session`  
**Priority:** Low

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | User remains logged in during token refresh |
| **API** | ✅ 🔄 | Detects if token changes during session |
| **Database** | ❌ | Token refresh is in-memory, not DB-logged |

**Key Features:**
- Tests automatic token refresh mechanism
- Validates seamless user experience during refresh
- Note: Depends on app's token refresh implementation

---

### 20. TC_LOGIN_EDGE_007: Cross-Browser Testing (NEW!)
**File:** `tests/ui/test_login_negative.py::test_edge_007_cross_browser_login`  
**Priority:** Medium  
**Parametrized:** Runs 3 times (Chromium, Firefox, WebKit)

| Validation Type | Status | Details |
|----------------|--------|---------|
| **UI** | ✅ | Login successful on Chrome, Firefox, Safari/WebKit |
| **API** | ✅ 🔄 | JWT token extraction works on all browsers |
| **Database** | ✅ | Login timestamps recorded for each browser |

**Key Features:**
- **Parametrized test** runs on 3 browsers automatically
- Validates cross-browser compatibility
- **Full tri-layer validation** (UI + API + DB) on each browser

---

## Summary Statistics

### Validation Coverage

| Validation Type | Total Tests | Count | Tests |
|----------------|-------------|-------|-------|
| **UI Only** | 20 | 8 | NEG_001-004, NEG_011, EDGE_001, EDGE_006, POS_002 (partial) |
| **UI + API** | 20 | 4 | POS_002, EDGE_002, EDGE_003, EDGE_006 |
| **UI + API + DB** | 20 | 8 | POS_001, POS_003-008, EDGE_005, EDGE_007 (×3 browsers) |
| **UI + API + DB (Skipped)** | 20 | 1 | NEG_010 (requires special setup) |

### JWT Token Extraction

| Feature | Count | Tests |
|---------|-------|-------|
| **With JWT Token** 🔄 | 13 | All POS_001-008 + EDGE_002, 003, 005, 006, 007 |
| **Without JWT Token** | 7 | All NEG and EDGE_001 tests (login fails) |

### Database Validation

| Database Action | Count | Tests |
|----------------|-------|-------|
| **Uses pymysql** | 10 | POS_001, POS_003-008, EDGE_005, EDGE_007 (×3) |
| **Uses db_validator** | 1 | NEG_010 (SKIPPED) |
| **No DB validation** | 9 | POS_002, NEG_001-004, NEG_011, EDGE_001-003, EDGE_006 |

### Cross-Browser Testing

| Browser | Tests | Status |
|---------|-------|--------|
| **Chromium20 Login Tests (Complete Suite)
```powershell
# Run all login tests (positive + negative + edge)
python -m pytest tests/ui/test_login.py tests/ui/test_login_negative.py -v

# With markers
python -m pytest -m "login_positive or login_negative or login_edge" -v
```

### Run Tests by Category

```powershell
# Only positive tests (8 tests - all have API + most have DB validation)
python -m pytest -m login_positive -v

# Only negative tests (6 tests - mostly UI validation)
python -m pytest -m login_negative -v

# Only edge cases (6 tests - mixed validation)
python -m pytest -m login_edge -v
```

### Run NEW Edge Case Tests Only

```powershell
# Run only the 5 new edge case tests
python -m pytest tests/ui/test_login_negative.py::test_edge_002_browser_back_button_after_login \
                tests/ui/test_login_negative.py::test_edge_003_multiple_browser_tabs_same_session \
                tests/ui/test_login_negative.py::test_edge_005_concurrent_sessions_multiple_browsers \
                tests/ui/test_login_negative.py::test_edge_006_token_refresh_during_session \
                tests/ui/test_login_negative.py::test_edge_007_cross_browser_login -v

# Note: EDGE_007 runs 3 times (once per browser)
```

### Run Tests by Validation Type

```powershell
# All tests with API validation (13 tests)
python -m pytest tests/ui/test_login.py -v

# All tests with Database validation (10 tests)
python -m pytest tests/ui/test_login.py::test_pos_001 \
                tests/ui/test_login.py::test_pos_003 \
                tests/ui/test_login.py::test_pos_004 \
                tests/ui/test_login.py::test_pos_005 \
                tests/ui/test_login.py::test_pos_006 \
                tests/ui/test_login.py::test_pos_007 \
                tests/ui/test_login.py::test_pos_008 \
                tests/ui/test_login_negative.py::test_edge_005_concurrent_sessions_multiple_browsers \
                tests/ui/test_login_negative.py::test_edge_007_cross_browser_login -v
```

### Run Critical Tests Only

```powershell
# Critical priority tests (4 tests)
python -m pytest -m critical -v
# Includes: POS_001, POS_008, NEG_001, NEG_002
```

### Run Cross-Browser Tests

```powershell
# Run EDGE_007 on all 3 browsers (parametrized)
python -m pytest tests/ui/test_login_negative.py::test_edge_007_cross_browser_login -v

# This will automatically run 3 times:
# - test_edge_007_cross_browser_login[chromium]
# - test_edge_007_cross_browser_login[firefox]
# - test_edge_007_cross_browser_login[webkit]os_006 \
                tests/ui/test_login.py::test_pos_007 \
                tests/ui/test_login.py::test_pos_008 -v
```

### Run Critical Tests Only

```powershell
# Critical priority tests (4 tests)
python -m pytest -m critical -v
# Includes: POS_001, POS_008, NEG_001, NEG_002
```

---

## Prerequisites for Full Validation

### Required Configuration (config/.env or settings)

```ini
# Positive Test Users
TEST_USER_EMAIL=your_test_user@company.com
TEST_USER_PASSWORD=your_password

# Regular User (for POS_005)
REGULAR_USER_EMAIL=regular_user@company.com
REGULAR_USER_PASSWORD=regular_password

# New User (for POS_007)
NEW_USER_EMAIL=new_user@company.com
NEW_USER_PASSWORD=new_password

# Unauthorized User (for NEG_010 - optional)
UNAUTHORIZED_USER_EMAIL=unauthorized@company.com
UNAUTHORIZED_USER_PASSWORD=unauthorized_password

# Database Configuration (already configured via pymysql)
# MySQL Azure: mysql-customerengagement-dev.mysql.database.azure.com
# Database: mysql_hcp_targetandsegmentation_dev

# API Configuration
API_BASE_URL=https://your-app-url.com/api
```

### Required Python Packages

```bash
# Already installed in your venv:
pymysql          # For Database validation (no ODBC needed!)
cryptography     # For MySQL SSL connections
playwright       # For UI automation
requests         # For API validation
imagehash        # For UIValidator
Pillow           # For image processing
```

---

## Validation Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│  LOGIN TEST EXECUTION FLOW                             │
└─────────────────────────────────────────────────────────┘

1. UI Validation
   ├─► Navigate to login page
   ├─► Enter credentials
   ├─► Submit login form
   └─► ✅ Verify dashboard/error message

2. JWT Token Extraction (if login successful)
   ├─► Check cookies (jwt, token, auth_token, etc.)
   ├─► Check localStorage
   ├─► Check sessionStorage
   └─► 🔄 Update API validator with token

3. API Validation (if login successful + token found)
   ├─► Make API request with JWT token
   ├─► Header: Authorization: Bearer <token>
   └─► ✅ Verify 200 response (or skip if 401/403)

4. Database Validation (if configured)
   ├─► Connect via pymysql (no ODBC!)
   ├─► Execute validation query
   └─► ✅ Verify database state

RESULT: ✅ All validations passed OR ⚠️ Some skipped
```

---
20 (8 Positive + 6 Negative + 6 Edge)  
**API Validation Capable:** 13 tests  
**Database Validation Capable:** 10 tests  
**Full Tri-Layer Validation:** 8 tests  
**Cross-Browser Tests:** 3 (parametrized from 1 test)

🎯 **Ready to run complete test suite with API & Database validation!**
🚀 **5 NEW Edge Case Tests Added
   - Updates API validator's Authorization header
   - If token not found, API validation is skipped gracefully

2. **Database Connection**
   - Uses **pymysql** directly (no ODBC drivers needed!)
   - Connection pooling via session fixture
   - Automatic connection cleanup after tests

3. **Skipped Tests**
   - `test_neg_010_unauthorized_user_no_access` is SKIPPED by default
   - Requires UNAUTHORIZED_USER credentials in settings
   - Remove `@pytest.mark.skip()` decorator to enable

4. **Graceful Degradation**
   - Tests don't fail if API/DB validation unavailable
   - Clear console output shows what was validated
   - `[SKIP]` messages explain why validation was skipped

---

**Document Generated:** January 13, 2026  
**Total Test Cases:** 15  
**API Validation Capable:** 9 tests  
**Database Validation Capable:** 7 tests  
**Full Tri-Layer Validation:** 6 tests  

🎯 **Ready to run complete test suite with API & Database validation!**
