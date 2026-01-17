# Login Module - Validation Feasibility Matrix

## Quick Reference: Which Validations Are Possible?

✅ = Feasible and will be automated  
❌ = Not feasible or not applicable

---

## POSITIVE SCENARIOS (8 Test Cases)

| Test Case ID | Test Name | UI | API | Database |
|--------------|-----------|----|----|----------|
| TC_LOGIN_POS_001 | Successful Login with Valid Credentials | ✅ | ✅ | ✅ |
| TC_LOGIN_POS_002 | Successful Login with "Stay Signed In" | ✅ | ✅ | ❌ |
| TC_LOGIN_POS_003 | Login After Session Timeout | ✅ | ✅ | ✅ |
| TC_LOGIN_POS_004 | Login as Admin User | ✅ | ✅ | ✅ |
| TC_LOGIN_POS_005 | Login as Regular User | ✅ | ✅ | ✅ |
| TC_LOGIN_POS_006 | Brand/Workspace Selection | ✅ | ✅ | ✅ |
| TC_LOGIN_POS_007 | First-Time Login (New User) | ✅ | ✅ | ✅ |
| TC_LOGIN_POS_008 | Logout and Re-login | ✅ | ✅ | ✅ |

**Summary:** 8 UI + 8 API + 7 Database = **23 validations**

---

## NEGATIVE SCENARIOS (6 Automatable Test Cases)

| Test Case ID | Test Name | UI | API | Database | Reason for No API/DB |
|--------------|-----------|----|----|----------|---------------------|
| TC_LOGIN_NEG_001 | Invalid Email Address | ✅ | ❌ | ❌ | Microsoft SSO handles, never reaches app |
| TC_LOGIN_NEG_002 | Incorrect Password | ✅ | ❌ | ❌ | Fails at Microsoft level |
| TC_LOGIN_NEG_003 | Empty Email Field | ✅ | ❌ | ❌ | Client-side validation only |
| TC_LOGIN_NEG_004 | Empty Password Field | ✅ | ❌ | ❌ | Client-side validation only |
| TC_LOGIN_NEG_010 | Unauthorized User (No App Access) | ✅ | ✅ | ✅ | **Microsoft succeeds, app denies** |
| TC_LOGIN_NEG_011 | Special Characters in Email | ✅ | ❌ | ❌ | Microsoft SSO handles validation |

**Summary:** 6 UI + 1 API + 1 Database = **8 validations**

---

## EDGE CASES (7 Test Cases)

| Test Case ID | Test Name | UI | API | Database | Notes |
|--------------|-----------|----|----|----------|-------|
| TC_LOGIN_EDGE_001 | Very Long Email (256+ chars) | ✅ | ❌ | ❌ | Client-side validation |
| TC_LOGIN_EDGE_002 | Browser Back Button After Login | ✅ | ✅ | ❌ | Session validation only |
| TC_LOGIN_EDGE_003 | Multiple Browser Tabs | ✅ | ✅ | ❌ | Shared session token |
| TC_LOGIN_EDGE_004 | Server Downtime | ✅ | ✅ | ❌ | DB down, can't validate |
| TC_LOGIN_EDGE_005 | Concurrent Sessions (Multiple Devices) | ✅ | ✅ | ✅ | Session tracking |
| TC_LOGIN_EDGE_006 | Token Refresh During Active Session | ✅ | ✅ | ❌ | In-memory token refresh |
| TC_LOGIN_EDGE_007 | Cross-Browser Testing | ✅ | ❌ | ❌ | UI compatibility test |

**Summary:** 7 UI + 5 API + 1 Database = **13 validations**

---

## SECURITY & PERFORMANCE (5 Test Cases)

| Test Case ID | Test Name | UI | API | Database | Notes |
|--------------|-----------|----|----|----------|-------|
| TC_LOGIN_SEC_001 | Password Not Visible in Network | ✅ | ✅ | ❌ | HTTPS verification |
| TC_LOGIN_SEC_002 | JWT Token Security | ✅ | ✅ | ❌ | Token decode & validation |
| TC_LOGIN_SEC_003 | Session Timeout Enforcement | ✅ | ✅ | ✅ | Session expiry tracking |
| TC_LOGIN_PERF_001 | Login Page Load Time | ✅ | ❌ | ❌ | Performance test only |
| TC_LOGIN_PERF_002 | Authentication Response Time | ✅ | ✅ | ❌ | API performance test |

**Summary:** 5 UI + 4 API + 1 Database = **10 validations**

---

## OVERALL SUMMARY

### Total Validations Across All 26 Automatable Test Cases

| Validation Type | Count | Percentage |
|----------------|-------|------------|
| **UI Validations** | 26 | 100% of all tests |
| **API Validations** | 18 | 69% of all tests |
| **Database Validations** | 10 | 38% of all tests |
| **Total Validation Points** | **54** | - |

---

## Why Some Validations Are Not Feasible

### 🚫 Negative Test Cases (Limited API/DB Validation)

**Problem:** Microsoft Azure AD SSO handles authentication

- Invalid credentials fail at Microsoft level
- Application never receives the authentication request
- No API calls made to our application
- No database interaction occurs

**Exception:** TC_LOGIN_NEG_010 (Unauthorized User)
- Microsoft authentication **succeeds**
- User gets valid Microsoft token
- Application then checks if user has access
- This is where we can validate API (403 error) and Database (user not in Users table)

### 🚫 Edge Cases (Variable Validation)

**Limited DB Validation Because:**
- Token refresh happens in-memory (no DB logging)
- Multiple tabs share same session (single DB entry)
- Server downtime means DB unavailable
- Cross-browser is UI compatibility only

### 🚫 Security Tests (No DB Validation)

**Why:**
- Token validation is API-level (decode JWT in code)
- Password encryption handled by Microsoft
- HTTPS is transport layer (no DB)

---

## Database Tables Involved (10 Validations)

When database validation IS possible, these are the tables/fields we'll check:

| Table | Fields Validated | Test Cases |
|-------|-----------------|------------|
| **Users** | last_login_date, Role, last_selected_brand, created_date | POS_001, 003, 004, 005, 006, 007 |
| **Sessions** | login_time, logout_time, device_info, session_status | POS_003, 008, EDGE_005, SEC_003 |
| **Users** (Negative) | User existence check (COUNT = 0) | NEG_010 |

---

## API Endpoints Involved (18 Validations)

| Endpoint | Purpose | Used In |
|----------|---------|---------|
| **/api/v1/get_user_context/** | User authentication, roles, permissions | POS_001-008, NEG_010 |
| **/api/v1/sankey_chart/** | Brand-specific data (for brand selection test) | POS_006 |
| **/api/v1/cohorts/{brand_id}/** | Brand data validation | POS_006 |
| **JWT Token** | Token validation (decode, expiry check) | POS_002, 003, 008, EDGE_002-006, SEC_002, 003 |

---

## Test Implementation Priority

### Phase 1: Critical Positive Tests (High ROI)
- ✅ TC_LOGIN_POS_001: Successful Login (all 3 validations)
- ✅ TC_LOGIN_POS_004: Admin Login (all 3 validations)
- ✅ TC_LOGIN_POS_005: User Login (all 3 validations)
- ✅ TC_LOGIN_POS_008: Logout & Re-login (all 3 validations)

**4 tests × 3 validations each = 12 validation points**

### Phase 2: Essential Negative & Edge Cases
- ✅ TC_LOGIN_NEG_001-004: Invalid inputs (UI only)
- ✅ TC_LOGIN_NEG_010: Unauthorized user (all 3 validations)
- ✅ TC_LOGIN_EDGE_002-003: Browser behavior (UI + API)

**7 tests with 10 validation points**

### Phase 3: Advanced Scenarios
- ✅ TC_LOGIN_POS_002, 003, 006, 007: Session & brand management
- ✅ TC_LOGIN_EDGE_001, 004-007: Edge cases
- ✅ TC_LOGIN_SEC_001-003, PERF_001-002: Security & performance

**15 tests with 32 validation points**

---

**Document Status:** ✅ Updated  
**Total Test Cases:** 26 automatable  
**Total Validation Points:** 54 (26 UI + 18 API + 10 Database)
