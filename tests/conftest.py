"""
Pytest Configuration and Fixtures
Uses YOUR custom MCP validators as Python modules
CI/CD Ready - Your validators work as regular Python imports (no MCP server needed!)
"""

import pytest
from config.settings import Settings
import os
import sys
import pymysql
import pymysql.cursors
import time
from playwright.sync_api import sync_playwright

# Import YOUR custom MCP validators as regular Python modules
sys.path.insert(0, r'c:\Users\mv\mcp_servers\validation_mcp_server')
from tools.api_validator import APIValidator
from tools.db_validator import DBValidator

# Import LoginPage for session-scoped login
from framework.page_objects.login_page import LoginPage


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def update_api_validator_token(api_validator, ui_page, settings):
    """
    Extract JWT token from browser (intercepted from network requests) and update API validator.
    
    Args:
        api_validator: APIValidator instance
        ui_page: Playwright Page object
        settings: Settings object with API configuration
    
    Returns:
        str: Extracted token or None
    """
    # First, try to get intercepted token from network requests
    if hasattr(ui_page, 'intercepted_token') and ui_page.intercepted_token["value"]:
        token = ui_page.intercepted_token["value"]
        print(f"[API] Using intercepted JWT token from network")
    else:
        # Fallback: Try to extract from browser storage
        from framework.page_objects.base_page import BasePage
        base_page = BasePage(ui_page)
        token = base_page.extract_auth_token()
    
    if token:
        # Update API validator headers with JWT token
        api_validator.headers['Authorization'] = f'Bearer {token}'
        print(f"[API] Updated API validator with JWT token (length: {len(token)})")
        return token
    else:
        print("[API] Could not extract JWT token from browser")
        return None


# ============================================================================
# CONFIGURATION
# ============================================================================

def pytest_addoption(parser):
    """Add custom command-line options for pytest."""
    # Note: pytest-playwright provides --browser-name, --headed, --slowmo, etc.
    # We use those native options instead of defining our own
    pass


# ============================================================================
# SETTINGS FIXTURE
# ============================================================================

@pytest.fixture(scope="session")
def settings():
    """Load application settings from environment."""
    return Settings()


# ============================================================================
# YOUR CUSTOM MCP VALIDATORS (Imported as Python Modules)
# ============================================================================

@pytest.fixture(scope="session")
def api_validator(settings):
    """
    YOUR custom API Validator - imported as Python module
    Works in CI/CD without MCP server running!
    Contains all your custom error handling, retry logic, logging
    """
    validator = APIValidator()
    validator.set_base_url(settings.API_BASE_URL)
    yield validator


@pytest.fixture(scope="session")
def db_validator():
    """
    YOUR custom Database Validator - imported as Python module
    Uses credentials from YOUR MCP server (secure & reusable!)
    Works in CI/CD without MCP server running!
    """
    validator = DBValidator()
    # Credentials loaded from YOUR MCP server's config
    # No need to pass connection params - uses MCP defaults!
    yield validator
    # Cleanup
    try:
        validator.close_connection()
    except:
        pass


@pytest.fixture(scope="session")
def mysql_connection():
    """
    Direct MySQL connection using pymysql (no ODBC driver needed!)
    Bypasses ODBC entirely for database validations
    """
    connection = None
    try:
        connection = pymysql.connect(
            host='mysql-customerengagement-dev.mysql.database.azure.com',
            port=3306,
            user='hcp_targetandsegment_user',
            password='yyug23@ER12fddT',
            database='mysql_hcp_targetandsegmentation_dev',
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=30
        )
        print("[DB] Connected to MySQL using pymysql (no ODBC needed!)")
        yield connection
    except Exception as e:
        print(f"[DB] MySQL connection failed: {str(e)}")
        yield None
    finally:
        if connection:
            try:
                connection.close()
            except:
                pass


@pytest.fixture(scope="session")
def playwright_instance():
    """Session-scoped playwright instance"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser_context(playwright_instance):
    """
    Session-scoped browser context
    Launches browser in INCOGNITO mode - fresh session every time
    Intercepts network requests to capture JWT tokens
    """
    browser_type = "chromium"
    print(f"\n[Browser] Selected: {browser_type} (INCOGNITO MODE)")
    
    # Store intercepted token
    intercepted_token = {"value": None}
    
    browser = getattr(playwright_instance, browser_type).launch(
        headless=False,
        slow_mo=100,
        args=["--no-sandbox", "--disable-gpu", "--incognito"]  # Incognito mode
    )
    
    # Create context (already in incognito mode from browser launch)
    context = browser.new_context()
    
    print("[Incognito] Mode enabled - fresh session with no stored cookies/cache")
    
    # Intercept network requests to capture JWT token from Authorization header
    def handle_request(route, request):
        auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            if len(token) > 50:  # JWT tokens are long
                if not intercepted_token["value"]:  # Only log first time
                    print(f"[Network] Intercepted JWT token from: {request.url[:80]}...")
                intercepted_token["value"] = token
        route.continue_()
    
    # Enable request interception
    context.route("**/*", handle_request)
    
    yield context, intercepted_token
    
    context.close()
    browser.close()
    print("\n[Browser] Closed after all tests completed")


@pytest.fixture(scope="session")
def page(browser_context):
    """
    Session-scoped page fixture
    ONE page for ALL tests - stays open during entire test session
    """
    context, intercepted_token = browser_context
    page = context.new_page()
    
    print("[Browser] Opened - will stay open for ALL tests")
    
    # Attach intercepted_token to page for easy access
    page.intercepted_token = intercepted_token
    
    yield page
    
    # Don't close page here - let browser_context teardown handle it


@pytest.fixture(scope="session", autouse=True)
def perform_login_once(page, settings):
    """
    Session-scoped login fixture - performs login ONCE for entire test session
    Incognito mode ensures fresh session with no old cookies
    """
    print("\n" + "="*80)
    print("SESSION SETUP: Performing login in INCOGNITO mode")
    print("="*80)
    
    login_page = LoginPage(page, settings.APP_URL)
    
    # Perform login - force fresh login to ensure actual authentication happens
    print("[SETUP] Logging in with valid credentials...")
    login_success = login_page.perform_login(
        email=settings.TEST_USER_EMAIL,
        password=settings.TEST_USER_PASSWORD,
        stay_signed_in=True,
        force_fresh_login=True  # Force actual login flow
    )
    
    assert login_success, "Session login must succeed"
    print(f"[OK] Logged in successfully - session active for ALL tests")
    print(f"    URL: {page.url}")
    
    # Wait for the app to make initial API calls after login
    # This gives the network interceptor a chance to capture the JWT token
    print("[SETUP] Waiting for app to load and make initial API calls...")
    page.wait_for_timeout(3000)  # Wait 3 seconds for app to load and make API requests
    
    # Check if token was intercepted
    if hasattr(page, 'intercepted_token') and page.intercepted_token["value"]:
        print(f"[OK] JWT token intercepted (length: {len(page.intercepted_token['value'])})")
    else:
        print("[WARN] No JWT token intercepted yet - will try to capture during test execution")
    print("="*80 + "\n")
    
    yield
    # No cleanup - browser session persists until end


@pytest.fixture(scope="session")
def segments_page_loaded(page):
    """
    Navigate to Segments page ONCE for entire test session
    All tests reuse the same loaded page - NO RELOADS!
    """
    from framework.page_objects.segments_page import SegmentsPage
    
    print("\n[SETUP] Navigating to Segments page (ONE TIME ONLY)...")
    segments_page = SegmentsPage(page, Settings.APP_URL)
    segments_page.navigate_to_page()
    time.sleep(2)  # Wait for initial load
    print("[OK] Segments page loaded - will be reused by ALL tests\n")
    
    yield page  # Return the page object for tests to use
    # No cleanup - page stays on segments for all tests


# ============================================================================
# SCREENSHOT ON FAILURE (Using YOUR ui_validator)
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot on test failure using YOUR ui_validator
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get ui_validator fixture if available
        if "ui_validator" in item.funcargs:
            ui_validator = item.funcargs["ui_validator"]
            
            # Create screenshots directory if it doesn't exist
            os.makedirs("reports/screenshots", exist_ok=True)
            
            # Generate screenshot filename
            screenshot_name = f"{item.nodeid.replace('::', '_').replace('/', '_')}.png"
            screenshot_path = os.path.join("reports/screenshots", screenshot_name)
            
            # Take screenshot using Playwright page directly
            try:
                if hasattr(ui_validator, 'page') and ui_validator.page:
                    ui_validator.page.screenshot(path=screenshot_path)
                    print(f"\n[SCREENSHOT] Saved to: {screenshot_path}")
                else:
                    print(f"\n[SCREENSHOT] Skipped - page not available")
            except Exception as e:
                print(f"\n[SCREENSHOT] Failed to capture: {str(e)}")


# ============================================================================
# TEST MARKERS
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "ui: UI tests using YOUR ui_validator")
    config.addinivalue_line("markers", "api: API tests using YOUR api_validator")
    config.addinivalue_line("markers", "database: Database tests using YOUR db_validator")
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "critical: Critical path tests")
    config.addinivalue_line("markers", "login_positive: Positive login scenarios")
    config.addinivalue_line("markers", "login_negative: Negative login scenarios")
    config.addinivalue_line("markers", "slow: Slow running tests")


# ============================================================================
# ALLURE REPORT AUTO-GENERATION
# ============================================================================

def pytest_sessionfinish(session, exitstatus):
    """
    Automatically generate and open Allure report after test session completes.
    Only runs when --alluredir option is used.
    """
    import subprocess
    import webbrowser
    import os
    
    # Check if alluredir option was provided
    allure_dir = session.config.getoption('--alluredir', default=None)
    
    if allure_dir:
        print("\n" + "="*80)
        print("  GENERATING ALLURE REPORT...")
        print("="*80)
        
        try:
            # Generate Allure report - let shell resolve the path
            result = subprocess.run(
                'allure generate allure-results --clean -o allure-report',
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("  [SUCCESS] Allure report generated successfully")
                print("  Report location: allure-report/index.html")
                print("="*80)
                
                # Open Allure report in browser
                print("\n  [INFO] Opening Allure report in browser...")
                try:
                    # Use allure open command to start server and open browser
                    subprocess.Popen(
                        'allure open allure-report',
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    print("  [SUCCESS] Allure report opened in browser")
                except Exception as e:
                    print(f"  [WARN] Could not auto-open browser: {e}")
                    print(f"  [INFO] Manually open: allure open allure-report")
            else:
                print(f"  [ERROR] Failed to generate Allure report: {result.stderr}")
        
        except Exception as e:
            print(f"  [ERROR] Error generating Allure report: {e}")
        
        print("="*80 + "\n")
