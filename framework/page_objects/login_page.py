"""
Login Page Object Model

Handles Microsoft SSO authentication page interactions
"""


from framework.page_objects.base_page import BasePage
from playwright.sync_api import Page



class LoginPage(BasePage):
    """Page object for Microsoft SSO login page using standard Playwright."""
    
    # Trinity Landing Page Locators (FIRST page you see)
    TRINITY_SIGN_IN_BUTTON = 'button:has-text("Sign In")'  # Blue button on Trinity landing page
    TRINITY_SIGN_IN_BUTTON_ALT = 'a:has-text("Sign In")'
    
    # Microsoft SSO Login Page Locators (AFTER clicking Trinity Sign In)
    EMAIL_INPUT = 'input[type="email"]'
    PASSWORD_INPUT = 'input[type="password"]'
    NEXT_BUTTON = 'input[type="submit"]'
    SIGN_IN_BUTTON = 'input[type="submit"][value="Sign in"]'
    # Stay signed in selectors - buttons on the dialog
    STAY_SIGNED_IN_YES = 'button:has-text("Yes")'  # Blue Yes button
    STAY_SIGNED_IN_YES_ALT = 'button[type="submit"]:has-text("Yes")'  # Alternative button selector
    STAY_SIGNED_IN_NO = 'button:has-text("No")'  # Gray No button
    STAY_SIGNED_IN_NO_ALT = 'button[type="submit"]:has-text("No")'  # Alternative button selector
    ERROR_MESSAGE = '#errorText'
    
    def __init__(self, page: Page, app_url: str):
        """Initialize LoginPage with page and app URL."""
        super().__init__(page)
        self.app_url = app_url
    
    def click_trinity_sign_in(self):
        """Click the Sign In button on Trinity landing page to go to Microsoft SSO."""
        print("[ACTION] Waiting for Trinity landing page to load...")
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        print("[ACTION] Clicking 'Sign In' button on Trinity landing page...")
        try:
            # Wait for Sign In button to be visible
            self.wait_for_element(self.TRINITY_SIGN_IN_BUTTON, timeout=10000)
            self.click_element(self.TRINITY_SIGN_IN_BUTTON)
            print("[OK] Clicked Trinity 'Sign In' button")
        except Exception as e:
            print(f"[RETRY] Primary button not found, trying alternative selector...")
            self.wait_for_element(self.TRINITY_SIGN_IN_BUTTON_ALT, timeout=10000)
            self.click_element(self.TRINITY_SIGN_IN_BUTTON_ALT)
            print("[OK] Clicked Trinity 'Sign In' button (alternative)")
        
        # Wait for Microsoft login page to load
        self.page.wait_for_load_state("networkidle", timeout=15000)
        print("[OK] Microsoft SSO login page loaded")
    
    def enter_email(self, email: str):
        """Enter email address in Microsoft SSO login."""
        print(f"[ACTION] Entering email: {email}")
        self.wait_for_element(self.EMAIL_INPUT, timeout=15000)
        self.type_text(self.EMAIL_INPUT, email)
        print("[OK] Email entered")
    
    def click_next_after_email(self):
        """Click Next button after entering email."""
        print("[ACTION] Clicking 'Next' button...")
        self.click_element(self.NEXT_BUTTON)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        print("[OK] Clicked 'Next' button")
    
    def enter_password(self, password: str):
        """Enter password in Microsoft SSO login."""
        print(f"[ACTION] Entering password...")
        self.wait_for_element(self.PASSWORD_INPUT, timeout=15000)
        self.type_text(self.PASSWORD_INPUT, password)
        print("[OK] Password entered")
    
    def click_sign_in(self):
        """Click Sign In button after entering password."""
        print("[ACTION] Clicking 'Sign In' button...")
        self.click_element(self.SIGN_IN_BUTTON)
        # Don't wait here - let redirect happen naturally
        print("[OK] Clicked 'Sign In' button")
    
    def handle_stay_signed_in(self, stay_signed_in: bool = True):
        """Handle 'Stay signed in?' prompt - click input[value="Yes"] or input[value="No"]."""
        print(f"[ACTION] Handling 'Stay signed in?' prompt...")
        
        try:
            # Wait for the page to load after clicking Sign In
            self.page.wait_for_timeout(5000)
            
            if stay_signed_in:
                # Use exact selector for the Yes button: input[type="submit"][value="Yes"]
                print("[ACTION] Looking for input[type='submit'][value='Yes']")
                yes_button = self.page.locator("input[type='submit'][value='Yes']")
                yes_button.wait_for(state="visible", timeout=30000)
                yes_button.click()
                print("[OK] Clicked Yes button")
            else:
                print("[ACTION] Looking for input[type='submit'][value='No']")
                no_button = self.page.locator("input[type='submit'][value='No']")
                no_button.wait_for(state="visible", timeout=30000)
                no_button.click()
                print("[OK] Clicked No button")
                
        except Exception as e:
            print(f"[INFO] Stay signed in prompt did not appear: {type(e).__name__}")
    
    def get_error_message(self) -> str:
        """Get error message if login fails."""
        try:
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=3000):
                error_text = self.get_text(self.ERROR_MESSAGE)
                print(f"[ERROR] Login error message: {error_text}")
                return error_text
        except Exception:
            pass
        return ""
    
    def is_on_microsoft_login_page(self) -> bool:
        """Check if currently on Microsoft SSO login page."""
        return "login.microsoftonline.com" in self.page.url
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in by verifying URL is on app domain."""
        current_url = self.page.url
        # User is logged in if not on Microsoft login page and on the app domain
        return "login.microsoftonline.com" not in current_url and self.app_url.split("//")[1].split("/")[0] in current_url
    
    def is_login_successful(self, app_url: str) -> bool:
        """Check if login was successful by verifying redirect to app."""
        try:
            # Extract expected domain from app URL
            expected_domain = app_url.split("//")[1].split("/")[0]
            print(f"[INFO] Waiting for redirect to: {expected_domain}")
            
            # Wait for URL to change away from Microsoft login
            self.page.wait_for_url(lambda url: "login.microsoftonline.com" not in url, 
                                   timeout=60000)
            
            # Check if we're on the app domain
            current_url = self.page.url
            is_success = expected_domain in current_url
            
            if is_success:
                print(f"[OK] Login successful - redirected to: {current_url}")
            else:
                print(f"[WARN] Redirected but not to expected domain")
                print(f"[DEBUG] Current URL: {current_url}")
                print(f"[DEBUG] Expected domain: {expected_domain}")
            
            return is_success
        except Exception as e:
            current_url = self.page.url
            print(f"[ERROR] Login failed - timeout waiting for redirect")
            print(f"[DEBUG] Current URL: {current_url}")
            print(f"[DEBUG] Exception: {str(e)}")
            return False
    
    def perform_login(self, email: str, password: str, app_url: str = None, 
                     stay_signed_in: bool = False, force_fresh_login: bool = False) -> bool:
        """Perform complete Microsoft SSO login flow.
        
        Args:
            email: User email
            password: User password
            app_url: Optional app URL override (uses self.app_url if not provided)
            stay_signed_in: Whether to stay signed in
            force_fresh_login: Whether to force fresh login
        """
        target_url = app_url or self.app_url
        print("\n" + "="*80)
        print("[LOGIN] Starting Microsoft SSO login flow...")
        if force_fresh_login:
            print("[FORCE FRESH LOGIN] Ensuring clean session...")
        print("="*80)
        
        try:
            # Step 0: Navigate to app URL if not already there
            current_url = self.page.url
            if not current_url or target_url.split("//")[1].split("/")[0] not in current_url:
                print(f"[ACTION] Navigating to app: {target_url}")
                self.page.goto(target_url, wait_until="networkidle", timeout=30000)
                print("[OK] App loaded")
            else:
                print(f"[INFO] Already on app: {current_url}")
            
            # Step 1: Click Trinity Sign In button
            self.click_trinity_sign_in()
            
            # Step 2: Enter email
            self.enter_email(email)
            
            # Step 3: Click Next
            self.click_next_after_email()
            
            # Step 4: Enter password
            self.enter_password(password)
            
            # Step 5: Click Sign In
            self.click_sign_in()
            
            # Small delay to let the page process
            self.page.wait_for_timeout(1000)
            
            # Step 6: Handle "Stay signed in?" prompt
            self.handle_stay_signed_in(stay_signed_in)
            
            # Step 7: Verify login success
            is_success = self.is_login_successful(target_url)
            
            if is_success:
                print("="*80)
                print("[SUCCESS] Microsoft SSO login completed")
                print("="*80 + "\n")
            else:
                error_msg = self.get_error_message()
                if error_msg:
                    print(f"[ERROR] Login failed: {error_msg}")
                print("="*80)
                print("[FAILED] Microsoft SSO login did not complete successfully")
                print("="*80 + "\n")
            
            return is_success
            
        except Exception as e:
            print(f"[ERROR] Login failed with exception: {str(e)}")
            print("="*80)
            print("[FAILED] Microsoft SSO login encountered an error")
            print("="*80 + "\n")
            return False
