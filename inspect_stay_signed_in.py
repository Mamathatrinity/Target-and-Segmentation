"""
Inspect the 'Stay signed in?' prompt HTML to get correct selectors
"""
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def inspect_stay_signed_in():
    """Navigate to login and inspect the Stay signed in prompt."""
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    app_url = os.getenv("APP_URL", "https://tst-trinity-ng-app.azurewebsites.net")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to app
        print(f"[ACTION] Opening {app_url}...")
        page.goto(app_url, wait_until="networkidle")
        
        # Click Sign In
        print("[ACTION] Looking for Sign In button...")
        page.wait_for_load_state("networkidle", timeout=10000)
        
        try:
            sign_in_button = page.query_selector('button:has-text("Sign In")')
            if not sign_in_button:
                sign_in_button = page.query_selector('a:has-text("Sign In")')
            
            if sign_in_button:
                print("[OK] Found Sign In button, clicking...")
                sign_in_button.click()
            else:
                print("[ERROR] Sign In button not found")
                page.screenshot(path="screenshot_no_signin.png")
                return
        except Exception as e:
            print(f"[ERROR] Failed to click Sign In: {e}")
            return
        
        # Wait for Microsoft login page
        print("[ACTION] Waiting for Microsoft login page...")
        page.wait_for_url("**/login.microsoftonline.com/**", timeout=20000)
        
        # Enter email
        print(f"[ACTION] Entering email: {email}...")
        email_input = page.query_selector('input[type="email"]')
        if email_input:
            email_input.fill(email)
            email_input.press("Enter")
        
        # Wait for password field
        print("[ACTION] Waiting for password field...")
        page.wait_for_selector('input[type="password"]', timeout=10000)
        
        # Enter password
        print("[ACTION] Entering password...")
        password_input = page.query_selector('input[type="password"]')
        if password_input:
            password_input.fill(password)
            password_input.press("Enter")
        
        # Wait for Stay signed in prompt
        print("[ACTION] Waiting for 'Stay signed in?' prompt (10 second timeout)...")
        try:
            page.wait_for_selector('[role="alertdialog"]', timeout=10000)
            print("[OK] Stay signed in prompt appeared!")
            
            # Take screenshot of the entire page
            page.screenshot(path="screenshot_stay_signed_in_full.png")
            print("[OK] Full page screenshot saved")
            
            # Get HTML of the alert dialog
            alert_html = page.query_selector('[role="alertdialog"]').inner_html()
            print("\n[DEBUG] Alert dialog HTML:")
            print(alert_html)
            
            # Get all buttons
            buttons = page.query_selector_all('[role="alertdialog"] button')
            print(f"\n[DEBUG] Found {len(buttons)} buttons in alert dialog")
            for i, btn in enumerate(buttons):
                print(f"  Button {i}: {btn.text_content().strip()}")
                print(f"    Selector: button:has-text(\"{btn.text_content().strip()}\")")
                print(f"    innerHTML: {btn.inner_html()}")
            
            # Try various selectors
            print("\n[DEBUG] Testing selectors:")
            
            selectors_to_try = [
                'input[type="submit"][value="Yes"]',
                'button:has-text("Yes")',
                '[role="alertdialog"] button:has-text("Yes")',
                'text=Yes',
                '[role="button"]:has-text("Yes")',
            ]
            
            for selector in selectors_to_try:
                try:
                    element = page.query_selector(selector)
                    if element:
                        print(f"  ✓ FOUND: {selector}")
                        print(f"    Visible: {element.is_visible()}")
                        print(f"    Enabled: {element.is_enabled()}")
                    else:
                        print(f"  ✗ NOT FOUND: {selector}")
                except Exception as e:
                    print(f"  ✗ ERROR with {selector}: {e}")
            
        except Exception as e:
            print(f"[WARN] Stay signed in prompt did not appear (Microsoft might have skipped it): {e}")
            page.screenshot(path="screenshot_no_prompt.png")
        
        browser.close()

if __name__ == "__main__":
    inspect_stay_signed_in()
