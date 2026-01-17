# Login Module - Test Cases

## Module: Microsoft SSO Authentication for Trinity HCP Targeting & Segmentation
**Application URL:** https://ce-ts-dev.trinitylifesciences.com/  
**Authentication Type:** Microsoft Azure AD Single Sign-On (SSO)  
**Date:** January 12, 2026

---

## Test Scenarios Overview

| Category | Total Test Cases |
|----------|-----------------|
| Positive Scenarios | 8 |
| Negative Scenarios | 12 |
| Edge Cases | 7 |
| Security & Performance | 5 |
| **TOTAL** | **32** |

---

## 1. POSITIVE SCENARIOS (8 Test Cases)

### TC_LOGIN_POS_001: Successful Login with Valid Credentials
**Priority:** Critical  
**Test Type:** UI, API  

**Pre-conditions:**
- User has valid Microsoft account
- User has access to Trinity HCP application
- Application is accessible

**Test Steps:**
1. Navigate to https://ce-ts-dev.trinitylifesciences.com/
2. Verify redirect to Microsoft SSO login page
3. Enter valid email address
4. Click "Next" button
5. Enter valid password
6. Click "Sign in" button
7. Handle "Stay signed in?" prompt (click "No")
8. Wait for redirect back to application

**Expected Results:**
- User successfully redirects to Microsoft SSO page
- Email and password fields accept input
- User is authenticated successfully
- Application redirects to Universe Summary dashboard
- Profile button is visible with user initials
- No error messages displayed

**Validations:**
- ✅ **UI:** Profile button visible, dashboard loaded, correct user name displayed
- ✅ **API:** GET /api/v1/get_user_context/ returns 200 with user details, roles, permissions
- ✅ **Database:** User login timestamp updated in Users table (last_login_date field)

---

### TC_LOGIN_POS_002: Successful Login with "Stay Signed In" Option
**Priority:** High  
**Test Type:** UI  

**Pre-conditions:**
- User has valid credentials
- Browser has no existing session

**Test Steps:**
1. Navigate to application
2. Complete Microsoft SSO login flow
3. When "Stay signed in?" prompt appears, click "Yes"
4. Verify successful login

**Expected Results:**
- User logged in successfully
- Session persists after browser closure
- User remains logged in on browser restart (within token validity period)

**Validations:**
- ✅ **UI:** Dashboard accessible after browser restart without re-login
- ✅ **API:** Token remains valid, API calls succeed without re-authentication
- ❌ **Database:** N/A - No specific DB validation for this scenario

---

### TC_LOGIN_POS_003: Login After Session Timeout
**Priority:** High  
**Test Type:** UI, API  

**Pre-conditions:**
- User was previously logged in
- Session has expired (token expired)

**Test Steps:**
1. Wait for session to expire (or manually expire token)
2. Try to access application
3. Verify redirect to login page
4. Complete login flow with valid credentials

**Expected Results:**
- User redirected to Microsoft SSO login
- Login completes successfully
- New session established
- User can access application normally

**Validations:**
- ✅ **UI:** Seamless redirect to login when session expires
- ✅ **API:** New JWT token issued after re-login (different token from expired one)
- ✅ **Database:** New login session record created in Sessions table

---

### TC_LOGIN_POS_004: Login with Different User Roles (Admin)
**Priority:** High  
**Test Type:** UI, API, Database  

**Pre-conditions:**
- User has ADMIN role assigned in system

**Test Steps:**
1. Complete login with Admin user credentials
2. Verify dashboard loads
3. Check user role displayed in profile menu

**Expected Results:**
- Login successful
- Profile menu shows "ADMIN" role
- Admin-specific features/menus visible

**Validations:**
- ✅ **UI:** "ADMIN" role displayed in profile dropdown menu
- ✅ **API:** GET /api/v1/get_user_context/ returns roles: ["ADMIN"] or role: "ADMIN"
- ✅ **Database:** User record has admin role assigned (Users.Role = 'ADMIN')

---

### TC_LOGIN_POS_005: Login with Different User Roles (Regular User)
**Priority:** High  
**Test Type:** UI, API, Database  

**Pre-conditions:**
- User has regular USER role (non-admin)

**Test Steps:**
1. Complete login with regular user credentials
2. Verify dashboard loads
3. Check user role in profile menu

**Expected Results:**
- Login successful
- Profile menu shows "USER" role
- Admin features not visible/accessible

**Validations:**
- ✅ **UI:** "USER" role displayed, no admin menus visible
- ✅ **API:** GET /api/v1/get_user_context/ returns roles: ["USER"] or role: "USER"
- ✅ **Database:** User record has standard user role (Users.Role = 'USER')

---

### TC_LOGIN_POS_006: Brand/Workspace Selection After Login
**Priority:** Medium  
**Test Type:** UI, API  

**Pre-conditions:**
- User has access to multiple brands/workspaces
- User successfully logged in

**Test Steps:**
1. Complete login
2. Open profile menu
3. Click on brand selector
4. Select different brand (e.g., "Test", "brand1")
5. Verify application context switches

**Expected Results:**
- Brand selector shows all available brands
- Clicking brand switches workspace
- Dashboard updates with selected brand data

**Validations:**
- ✅ **UI:** Brand selector displays available brands, dashboard refreshes with selected brand data
- ✅ **API:** Subsequent API calls (e.g., /sankey_chart/, /cohorts/) use selected brand_id parameter
- ✅ **Database:** User's last_selected_brand updated in Users table

---

### TC_LOGIN_POS_007: First-Time Login (New User)
**Priority:** Medium  
**Test Type:** UI, Database  

**Pre-conditions:**
- User account created in Azure AD
- User has never logged into Trinity HCP app before

**Test Steps:**
1. Complete Microsoft SSO login with new user
2. Verify account setup/welcome screen (if applicable)
3. Access dashboard

**Expected Results:**
- Login successful
- User profile created in application database
- Default settings applied
- User can access application

**Validations:**
- ✅ **UI:** Successful redirect to dashboard after first login
- ✅ **API:** GET /api/v1/get_user_context/ returns newly created user context
- ✅ **Database:** New user record created in Users table with default settings (created_date = current timestamp)

---

### TC_LOGIN_POS_008: Logout and Re-login
**Priority:** High  
**Test Type:** UI, API  

**Pre-conditions:**
- User is currently logged in

**Test Steps:**
1. Click Profile button
2. Click "Logout" button
3. Verify redirect to login/Microsoft page
4. Log back in with same credentials

**Expected Results:**
- Logout successful, session cleared
- User redirected to login page
- Re-login successful without errors

**Validations:**
- ✅ **UI:** Clean logout (redirect to login page), successful re-login
- ✅ **API:** Previous session token invalidated (old token returns 401)
- ✅ **Database:** Logout timestamp recorded in Sessions table (logout_time field)

---

## 2. NEGATIVE SCENARIOS (12 Test Cases)

### TC_LOGIN_NEG_001: Login with Invalid Email Address
**Priority:** Critical  
**Test Type:** UI  

**Pre-conditions:**
- Application is accessible

**Test Steps:**
1. Navigate to application
2. Enter invalid/non-existent email (e.g., "invalid@notexist.com")
3. Click "Next"
4. Observe error message

**Expected Results:**
- Error message displayed: "This username may be incorrect..."
- Login does not proceed
- User remains on email entry page

**Validations:**
- ✅ **UI:** Microsoft SSO error message displayed (e.g., "This username may be incorrect...")
- ❌ **API:** N/A - Authentication fails at Microsoft level, app never receives request
- ❌ **Database:** N/A - Authentication fails before reaching application

---

### TC_LOGIN_NEG_002: Login with Incorrect Password
**Priority:** Critical  
**Test Type:** UI  

**Pre-conditions:**
- User has valid email

**Test Steps:**
1. Navigate to application
2. Enter valid email address
3. Click "Next"
4. Enter incorrect password
5. Click "Sign in"

**Expected Results:**
- Error message: "Your account or password is incorrect..."
- Login fails
- User remains on password entry page
- No access to application granted

**Validations:**
- ✅ **UI:** Microsoft SSO error message displayed (e.g., "Your account or password is incorrect...")
- ❌ **API:** N/A - Authentication fails at Microsoft level, no token issued
- ❌ **Database:** N/A - Failed login handled by Microsoft, not logged in application DB

---

### TC_LOGIN_NEG_003: Login with Empty Email Field
**Priority:** High  
**Test Type:** UI  

**Pre-conditions:**
- Application is accessible

**Test Steps:**
1. Navigate to application
2. Leave email field empty
3. Click "Next" button

**Expected Results:**
- Error message: "Enter a valid email address..."
- Next button may be disabled or show validation error
- Cannot proceed to password entry

**Validations:**
- ✅ **UI:** Client-side validation error displayed ("Enter a valid email address...")
- ❌ **API:** N/A - Client-side validation, no server request made
- ❌ **Database:** N/A - Validation happens before any server interaction

---

### TC_LOGIN_NEG_004: Login with Empty Password Field
**Priority:** High  
**Test Type:** UI  

**Pre-conditions:**
- Valid email entered

**Test Steps:**
1. Enter valid email
2. Click "Next"
3. Leave password field empty
4. Click "Sign in"

**Expected Results:**
- Error message: "Please enter the password..."
- Sign in button may be disabled
- Cannot complete login

**Validations:**
- ✅ **UI:** Client-side validation error displayed ("Please enter the password...")
- ❌ **API:** N/A - Client-side validation, no server request made
- ❌ **Database:** N/A - Validation happens before any server interaction

---

### TC_LOGIN_NEG_005: Login with Expired Password
**Priority:** Medium  
**Test Type:** Manual Only  
**⚠️ NOT AUTOMATABLE** - Requires Azure AD password policy configuration

**Pre-conditions:**
- User's password has expired (per Azure AD policy)

**Test Steps:**
1. Enter valid email
2. Enter expired password
3. Attempt login

**Expected Results:**
- User prompted to reset/change password
- Cannot access application until password updated
- Redirect to Microsoft password reset flow

**Validations:**
- **UI:** Password reset prompt displayed
- **API:** No access token granted

**Note:** This test requires a dedicated test account with expired password set in Azure AD, which is not practical for automation.

---

### TC_LOGIN_NEG_006: Login with Disabled/Deactivated Account
**Priority:** High  
**Test Type:** Manual Only  
**⚠️ NOT AUTOMATABLE** - Requires disabled test account in Azure AD

**Pre-conditions:**
- User account exists but is disabled in Azure AD or application database

**Test Steps:**
1. Attempt login with disabled account credentials
2. Observe error/access denial

**Expected Results:**
- Error message indicating account is disabled
- Access denied
- User cannot log in

**Validations:**
- **UI:** Account disabled error message
- **API:** 403 Forbidden or similar error
- **Database:** User IsActive = 0 or account_status = 'disabled'

**Note:** Requires maintaining a permanently disabled test account, which is not practical for automated testing.

---
Manual Only  
**⚠️ NOT AUTOMATABLE** - Requires network manipulation

**Pre-conditions:**
- Network connection is lost/unavailable

**Test Steps:**
1. Disconnect network
2. Attempt to navigate to application
3. Observe error

**Expected Results:**
- Browser shows "No internet connection" or similar error
- Cannot reach login page
- Graceful error handling

**Validations:**
- **UI:** Clear network error message

**Note:** Can be tested manually, but automating network disconnection is complex and unreliable in CI/CD environments.

**Validations:**
- **UI:** Clear network error message

---
Manual Only  
**⚠️ NOT APPLICABLE** - Microsoft SSO handles authentication

**Pre-conditions:**
- Application is accessible

**Test Steps:**
1. Enter SQL injection payload in email field (e.g., "admin'--", "' OR '1'='1")
2. Attempt to proceed

**Expected Results:**
- Input sanitized/rejected by Microsoft SSO
- No SQL injection successful
- Error or validation message shown

**Validations:**
- **UI:** Input rejected or sanitized
- **Security:** SQL injection prevented by Microsoft

**Note:** Since authentication is handled entirely by Microsoft Azure AD SSO (not the application's database), SQL injection on login is not applicable. Microsoft handles input validation.
- **UI:** Input rejected or sanitized
- **Database:** No malicious queries executed
- **Security:** SQL injection prevented
Manual Only  
**⚠️ NOT APPLICABLE** - Microsoft SSO handles authentication

**Pre-conditions:**
- Application is accessible

**Test Steps:**
1. Enter XSS payload in email field (e.g., "<script>alert('XSS')</script>")
2. Attempt login

**Expected Results:**
- Script not executed
- Input sanitized by Microsoft SSO
- No XSS vulnerability exploited

**Validations:**
- **UI:** Script tags escaped/removed
- **Security:** XSS attack prevented

**Note:** Since login is handled by Microsoft Azure AD, XSS testing on the login form is not applicable. Microsoft's security handles input sanitization.
- No XSS vulnerability exploited

**Validations:**
- **UI:** Script tags escaped/removed
- **Security:** XSS attack prevented

---

### TC_LOGIN_NEG_010: Login with Unauthorized User (No App Access)
**Priority:** High  
**Test Type:** UI, API  

**Pre-conditions:**
- User has valid Microsoft account
- User does NOT have permissions to access Trinity HCP app

**Test Steps:**
1. Complete Microsoft SSO login with unauthorized user
2. Observe access denial

**Expected Results:**
- Microsoft authentication succeeds
- Application denies access with "Access Denied" or "Unauthorized" message
- User redirected back or shown error page

**Validations:**
- ✅ **UI:** Access denied message displayed ("Unauthorized" or "You don't have access...")
- ✅ **API:** GET /api/v1/get_user_context/ returns 403 Forbidden or 401 Unauthorized
- ✅ **Database:** User not found in application Users table (SELECT returns 0 rows)

---

### TC_LOGIN_NEG_011: Login with Special Characters in Email
**Priority:** Low  
**Test Type:** UI  

**Pre-conditions:**
- Application is accessible

**Test Steps:**
1. Enter email with special characters (e.g., "user+test@domain.com", "user@sub-domain.com")
2. Attempt login

**Expected Results:**
- Valid special characters accepted (as per email RFC standards)
- Invalid special characters rejected with validation error

**Validations:**
- ✅ **UI:** Email validation accepts valid special characters, rejects invalid ones
- ❌ **API:** N/A - Microsoft SSO handles email validation
- ❌ **Database:** N/A - Validation happens at Microsoft level
Manual Only  
**⚠️ NOT AUTOMATABLE** - Risk of locking test accounts

**Pre-conditions:**
- User account exists

**Test Steps:**
1. Attempt login with wrong password 5+ times consecutively
2. Observe account lockout behavior

**Expected Results:**
- After threshold (e.g., 5 attempts), account temporarily locked
- Error message: "Account locked due to too many failed attempts"
- User must wait or reset password to unlock

**Validations:**
- **UI:** Account lockout message displayed
- **Database:** Failed login attempts counter incremented
- **Security:** Account lockout policy enforced (Azure AD policy)

**Note:** Automated testing could permanently lock test accounts. This should be tested manually with a dedicated throwaway account or in a separate test environment.

**Validations:**
- **UI:** Account lockout message displayed
- **Database:** Failed login attempts counter incremented
- **Security:** Account lockout policy enforced

---

## 3. EDGE CASES (7 Test Cases)

### TC_LOGIN_EDGE_001: Login with Very Long Email Address (256+ characters)
**Priority:** Low  
**Test Type:** UI  

**Pre-conditions:**
- Application is accessible

**Test Steps:**
1. Enter email address exceeding 256 characters
2. Attempt to proceed

**Expected Results:**
- Field validation limits input or shows error
- Email rejected if exceeds maximum length
- No application crash

**Validations:**
- ✅ **UI:** Field length validation enforced (input truncated or error shown)
- ❌ **API:** N/A - Client-side validation only
- ❌ **Database:** N/A - Validation happens before server interaction

---

### TC_LOGIN_EDGE_002: Login with Browser Back Button After Successful Login
**Priority:** Medium  
**Test Type:** UI  

**Pre-conditions:**
- User successfully logged in

**Test Steps:**
1. Complete login successfully
2. Click browser back button
3. Observe behavior

**Expected Results:**
- User remains logged in (not redirected to login again)
- Dashboard stays accessible
- No session corruption

**Validations:**
- ✅ **UI:** No unwanted redirect to login page, user remains on dashboard
- ✅ **API:** Session token still valid, API calls continue to work
- ❌ **Database:** N/A - No specific DB validation needed

---

### TC_LOGIN_EDGE_003: Login with Multiple Browser Tabs
**Priority:** Medium  
**Test Type:** UI  

**Pre-conditions:**
- Application accessible

**Test Steps:**
1. Open application in multiple tabs
2. Login in one tab
3. Check other tabs' behavior

**Expected Results:**
- Login in one tab logs in all tabs
- Session synchronized across tabs
- No conflicts or duplicate sessions

**Validations:**
- ✅ **UI:** All tabs show logged-in state, profile button visible in all tabs
- ✅ **API:** Single session token shared across tabs (same JWT in localStorage)
- ❌ **Database:** N/A - Single session entry for all tabs

---

### TC_LOGIN_EDGE_004: Login During Server Maintenance/Downtime
**Priority:** Medium  
**Test Type:** UI, API  

**Pre-conditions:**
- Application backend is down/maintenance mode

**Test Steps:**
1. Attempt to access application during downtime
2. Observe error handling

**Expected Results:**
- User-friendly error message displayed
- "Service temporarily unavailable" or similar
- No raw error stack traces shown

**Validations:**
- ✅ **UI:** User-friendly error page displayed ("Service temporarily unavailable...")
- ✅ **API:** HTTP status code 503 Service Unavailable or connection timeout
- ❌ **Database:** N/A - Database is down, cannot validate

---

### TC_LOGIN_EDGE_005: Login with Concurrent Sessions from Different Devices
**Priority:** Medium  
**Test Type:** UI, Database  

**Pre-conditions:**
- User has valid credentials

**Test Steps:**
1. Login from Device A (e.g., Desktop)
2. Login from Device B (e.g., Mobile) with same credentials
3. Verify both sessions work or one is terminated

**Expected Results:**
- Application policy followed (allow concurrent or terminate old session)
- If allowed: Both devices stay logged in
- If not: Device A session terminated when Device B logs in

**Validations:**
- ✅ **UI:** Both devices maintain logged-in state or one session terminated (based on policy)
- ✅ **API:** Separate tokens for each device or shared token (based on implementation)
- ✅ **Database:** Active sessions tracked in Sessions table (device_info, login_time per session)

---

### TC_LOGIN_EDGE_006: Login with Token Refresh During Active Session
**Priority:** Medium  
**Test Type:** API  

**Pre-conditions:**
- User is logged in
- JWT token near expiration

**Test Steps:**
1. User logged in and actively using application
2. Wait for token to approach expiration
3. Continue using application (trigger API calls)

**Expected Results:**
- Token automatically refreshed in background
- No interruption to user experience
- User not logged out unexpectedly

**Validations:**
- ✅ **UI:** Seamless continuation without re-login, no interruption to user
- ✅ **API:** New JWT token issued before old one expires (refresh token mechanism)
- ❌ **Database:** N/A - Token refresh handled in-memory, not typically logged

---

### TC_LOGIN_EDGE_007: Login with Different Browsers (Cross-Browser Testing)
**Priority:** Medium  
**Test Type:** UI  

**Pre-conditions:**
- Application accessible
- Multiple browsers available (Chrome, Edge, Firefox)

**Test Steps:**
1. Test login flow in Chrome
2. Test login flow in Edge
3. Test login flow in Firefox
4. Verify consistent behavior

**Expected Results:**
- Login works identically across all supported browsers
- No browser-specific issues
- UI renders correctly in all browsers

**Validations:**
- ✅ **UI:** Consistent login experience across Chrome, Edge, Firefox (element rendering, flow)
- ❌ **API:** N/A - API behavior is browser-agnostic
- ❌ **Database:** N/A - This is purely a UI compatibility test

---

## 4. SECURITY & PERFORMANCE (5 Test Cases)

### TC_LOGIN_SEC_001: Verify Password is Not Visible in Network Logs
**Priority:** Critical (Security)  
**Test Type:** Security  

**Pre-conditions:**
- User attempting login

**Test Steps:**
1. Open browser developer tools (Network tab)
2. Enter email and password
3. Submit login
4. Inspect network requests

**Expected Results:**
- Password not visible in plain text in any network request
- HTTPS encryption used
- No sensitive data exposed in URLs or logs

**Validations:**
- ✅ **UI:** Password field type="password" (dots displayed, not plain text)
- ✅ **API:** HTTPS used for all authentication requests (check protocol in network logs)
- ❌ **Database:** N/A - Password never stored in plain text (Azure AD handles)

---

### TC_LOGIN_SEC_002: Verify JWT Token Security
**Priority:** Critical (Security)  
**Test Type:** API, Security  

**Pre-conditions:**
- User successfully logged in

**Test Steps:**
1. Complete login
2. Capture JWT token from API response
3. Decode token (using jwt.io or similar)
4. Verify token claims and expiration

**Expected Results:**
- Token contains proper claims (user_id, roles, exp, iat)
- Token has reasonable expiration time
- Token signed with secure algorithm (RS256 or HS256)

**Validations:**
- ✅ **UI:** Token not exposed in UI/console logs
- ✅ **API:** JWT token structure valid (Header.Payload.Signature), contains required claims (user_id, roles, exp, iat), signed with secure algorithm (RS256/HS256)
- ❌ **Database:** N/A - Token validation is API-level only

---

### TC_LOGIN_SEC_003: Verify Session Timeout Enforcement
**Priority:** High (Security)  
**Test Type:** UI, API  

**Pre-conditions:**
- User logged in

**Test Steps:**
1. Login successfully
2. Remain inactive for configured timeout period (e.g., 30 minutes)
3. Attempt to use application

**Expected Results:**
- User automatically logged out after timeout
- Redirect to login page
- Session invalidated

**Validations:**
- ✅ **UI:** User automatically redirected to login page after inactivity timeout
- ✅ **API:** Expired token rejected with 401 Unauthorized when used for API calls
- ✅ **Database:** Session marked as expired in Sessions table (session_status = 'expired')

---

### TC_LOGIN_PERF_001: Login Page Load Time
**Priority:** Medium (Performance)  
**Test Type:** Performance  

**Pre-conditions:**
- Application accessible

**Test Steps:**
1. Navigate to application URL
2. Measure time to fully load login page

**Expected Results:**
- Login page loads within 3 seconds
- No performance bottlenecks

**Validations:**
- ✅ **UI:** Login page fully loads within 3 seconds (measure with browser performance API)
- ❌ **API:** N/A - This is a page load performance test, not API
- ❌ **Database:** N/A - No database interaction during initial page load

---

### TC_LOGIN_PERF_002: Authentication Response Time
**Priority:** Medium (Performance)  
**Test Type:** API, Performance  

**Pre-conditions:**
- User submitting valid credentials

**Test Steps:**
1. Enter valid credentials
2. Submit login
3. Measure time from submission to dashboard load

**Expected Results:**
- Complete authentication within 5 seconds
- API response time < 2000ms

**Validations:**
- **API:** /get_user_context response time < 2000ms
- **Performance:** T Automatable | Manual Only |
|----------|-------|-------------|-------------|
| **Positive Test Cases** | 8 | 8 | 0 |
| **Negative Test Cases** | 12 | 6 | 6 |
| **Edge Cases** | 7 | 7 | 0 |
| **Security & Performance** | 5 | 5 | 0 |
| **TOTAL TEST CASES** | **32** | **26** | **6** |

**Automation Breakdown:**
- ✅ **Automatable Test Cases:** 26 (81%)
- ⚠️ **Manual Only Test Cases:** 6 (19%)
  - TC_LOGIN_NEG_005: Expired Password
  - TC_LOGIN_NEG_006: Disabled Account
  - TC_LOGIN_NEG_007: No Network Connection
  - TC_LOGIN_NEG_008: SQL Injection (Not Applicable - Microsoft SSO)
  - TC_LOGIN_NEG_009: XSS Attack (Not Applicable - Microsoft SSO)
  - TC_LOGIN_NEG_012: Account Lockout

**Validation Types (Automatable Tests Only):**
- UI Validation: 24 test cases
- API Validation: 15 test cases
- Database Validation: 8 test cases
- Security Validation: 3 **32** |

**Validation Types:**
- UI Validation: 30 test cases
- API Validation: 18 test cases
- Database Validation: 10 test cases
- Security Validation: 5 test cases
- Performance Validation: 2 test cases

---

## Test Data Requirements

1. **Valid Test Users:**
   - Admin user credentials
   - Regular user credentials
   - User with multiple brand access
   - New user (first-time login)

2. **Invalid Test Data:**
   - Non-existent email addresses
   - Wrong passwords
   - Disabled account credentials
   - Unauthorized user credentials

3. **Environment:**
   - Database connection for validation
   - API access for token verification
   - Multiple browsers for cross-browser testing
   - Network throttling tools for performance testing

---

## Priority Breakdown

- **Critical:** 10 test cases
- **High:** 8 test cases
- **Medium:** 12 test cases
- **Low:** 2 test cases

---

**Review Required:** Please review these test cases and let me know if you want to:
1. Add more scenarios
2. Modify existing test cases
3. Proceed with implementation
