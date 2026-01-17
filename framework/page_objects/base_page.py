"""
Base Page Object Model
Contains common methods used across all pages using standard Playwright
"""

from typing import Optional
from playwright.sync_api import Page, expect
import time


class BasePage:
    """Base class for all page objects using standard Playwright."""
    
    def __init__(self, page: Page):
        """
        Initialize base page with Playwright Page object.
        
        Args:
            page: Playwright Page instance from pytest fixture
        """
        self.page = page
        self.timeout = 30000  # 30 seconds default timeout
    
    def navigate_to(self, url: str):
        """Navigate to a specific URL."""
        print(f"[Navigation] Going to {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
    
    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.page.url
    
    def get_title(self) -> str:
        """Get the page title."""
        return self.page.title()
    
    def is_element_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if an element is visible.
        
        Args:
            selector: CSS selector or ARIA role selector
            timeout: Optional timeout in milliseconds
        
        Returns:
            bool: True if element is visible, False otherwise
        """
        timeout_ms = timeout if timeout else self.timeout
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
            return True
        except Exception:
            return False
    
    def click_element(self, selector: str, timeout: Optional[int] = None):
        """
        Click an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Optional timeout in milliseconds
        """
        timeout_ms = timeout if timeout else self.timeout
        self.page.click(selector, timeout=timeout_ms)
    
    def type_text(self, selector: str, text: str, timeout: Optional[int] = None):
        """
        Type text into an input field.
        
        Args:
            selector: CSS selector for the input field
            text: Text to type
            timeout: Optional timeout in milliseconds
        """
        timeout_ms = timeout if timeout else self.timeout
        self.page.fill(selector, text, timeout=timeout_ms)
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content of an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Optional timeout in milliseconds
        
        Returns:
            str: Text content of the element
        """
        timeout_ms = timeout if timeout else self.timeout
        element = self.page.wait_for_selector(selector, timeout=timeout_ms)
        return element.inner_text() if element else ""
    
    def wait_for_element(self, selector: str, timeout: Optional[int] = None):
        """
        Wait for an element to be visible.
        
        Args:
            selector: CSS selector
            timeout: Optional timeout in milliseconds
        """
        timeout_ms = timeout if timeout else self.timeout
        self.page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
    
    def take_screenshot(self, filename: str):
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Path/filename for the screenshot
        """
        self.page.screenshot(path=filename, full_page=True)
    
    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None):
        """
        Wait for URL to match pattern.
        
        Args:
            url_pattern: URL pattern to wait for
            timeout: Optional timeout in milliseconds
        """
        timeout_ms = timeout if timeout else self.timeout
        self.page.wait_for_url(url_pattern, timeout=timeout_ms)
    
    def press_key(self, selector: str, key: str):
        """
        Press a key on an element.
        
        Args:
            selector: CSS selector for the element
            key: Key to press (e.g., 'Enter', 'Escape')
        """
        self.page.press(selector, key)
    
    def hover(self, selector: str):
        """
        Hover over an element.
        
        Args:
            selector: CSS selector for the element
        """
        self.page.hover(selector)
    
    def select_option(self, selector: str, value: str):
        """
        Select an option from dropdown.
        
        Args:
            selector: CSS selector for the select element
            value: Value to select
        """
    
    def get_cookie(self, cookie_name: str) -> Optional[str]:
        """
        Get a specific cookie value.
        
        Args:
            cookie_name: Name of the cookie to retrieve
        
        Returns:
            str: Cookie value or None if not found
        """
        cookies = self.page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == cookie_name:
                return cookie['value']
        return None
    
    def get_all_cookies(self) -> list:
        """
        Get all cookies from the current browser context.
        
        Returns:
            list: List of cookie dictionaries
        """
        return self.page.context.cookies()
    
    def get_local_storage(self, key: str) -> Optional[str]:
        """
        Get a value from localStorage.
        
        Args:
            key: localStorage key name
        
        Returns:
            str: localStorage value or None if not found
        """
        try:
            value = self.page.evaluate(f"() => localStorage.getItem('{key}')")
            return value
        except Exception as e:
            print(f"[Warning] Could not read localStorage key '{key}': {e}")
            return None
    
    def get_session_storage(self, key: str) -> Optional[str]:
        """
        Get a value from sessionStorage.
        
        Args:
            key: sessionStorage key name
        
        Returns:
            str: sessionStorage value or None if not found
        """
        try:
            value = self.page.evaluate(f"() => sessionStorage.getItem('{key}')")
            return value
        except Exception as e:
            print(f"[Warning] Could not read sessionStorage key '{key}': {e}")
            return None
    
    def extract_auth_token(self) -> Optional[str]:
        """
        Extract authentication token from various sources (cookies, localStorage, sessionStorage).
        Tries common token storage locations including MSAL cache.
        
        Returns:
            str: Token value or None if not found
        """
        # Try common cookie names
        token_cookies = ['jwt', 'token', 'auth_token', 'access_token', 'session_token', 'Authorization']
        for cookie_name in token_cookies:
            token = self.get_cookie(cookie_name)
            if token:
                print(f"[Auth] ✓ Found token in cookie: {cookie_name}")
                return token
        
        # Try localStorage
        token_keys = ['jwt', 'token', 'auth_token', 'access_token', 'authToken', 'Authorization']
        for key in token_keys:
            token = self.get_local_storage(key)
            if token:
                print(f"[Auth] ✓ Found token in localStorage: {key}")
                return token
        
        # Try sessionStorage
        for key in token_keys:
            token = self.get_session_storage(key)
            if token:
                print(f"[Auth] ✓ Found token in sessionStorage: {key}")
                return token
        
        # Try to extract from MSAL cache in localStorage
        try:
            msal_cache_keys = self.page.evaluate("""
                () => {
                    const keys = [];
                    for (let i = 0; i < localStorage.length; i++) {
                        const key = localStorage.key(i);
                        if (key && (key.includes('msal') || key.includes('accesstoken') || key.includes('idtoken'))) {
                            keys.push(key);
                        }
                    }
                    return keys;
                }
            """)
            
            if msal_cache_keys:
                print(f"[Auth] Found MSAL cache keys: {msal_cache_keys}")
                # Try to extract token from MSAL cache
                # MSAL stores tokens with keys like: msal.2|...|accesstoken|...
                # The value is a JSON object with 'secret' field containing the actual token
                for key in msal_cache_keys:
                    # Look for accesstoken or idtoken in the key name
                    if 'accesstoken' in key.lower() or 'idtoken' in key.lower():
                        try:
                            cache_value = self.get_local_storage(key)
                            print(f"[Auth] DEBUG - Checking key: {key[:80]}...")
                            print(f"[Auth] DEBUG - Cache value type: {type(cache_value)}, length: {len(cache_value) if cache_value else 0}")
                            if cache_value:
                                print(f"[Auth] DEBUG - First 200 chars: {cache_value[:200]}")
                            if cache_value and isinstance(cache_value, str):
                                # Parse JSON if it's a cache object
                                import json
                                try:
                                    cache_obj = json.loads(cache_value)
                                    print(f"[Auth] DEBUG - Parsed JSON keys: {list(cache_obj.keys()) if isinstance(cache_obj, dict) else 'not a dict'}")
                                    # MSAL cache structure: {"secret": "token_value", "credentialType": "...", ...}
                                    if isinstance(cache_obj, dict) and 'secret' in cache_obj:
                                        print(f"[Auth] ✓ Found token in MSAL cache key: {key[:50]}...")
                                        return cache_obj['secret']
                                except json.JSONDecodeError as je:
                                    print(f"[Auth] DEBUG - JSON decode error: {je}")
                                    # Not JSON, might be plain text token
                                    if len(cache_value) > 50:  # Tokens are usually long
                                        print(f"[Auth] ✓ Found token in MSAL cache (plain text): {key[:50]}...")
                                        return cache_value
                        except Exception as e:
                            print(f"[Auth] Could not read MSAL cache key {key[:50]}: {e}")
                            continue
        except Exception as e:
            print(f"[Auth] Error reading MSAL cache: {e}")
        
        # Try to get all localStorage items for debugging
        try:
            all_storage = self.page.evaluate("""
                () => {
                    const items = {};
                    for (let i = 0; i < localStorage.length; i++) {
                        const key = localStorage.key(i);
                        if (key) {
                            const value = localStorage.getItem(key);
                            items[key] = value ? value.substring(0, 100) + '...' : null;
                        }
                    }
                    return items;
                }
            """)
            print(f"[Auth] DEBUG - All localStorage keys: {list(all_storage.keys())}")
        except Exception as e:
            print(f"[Auth] Could not list localStorage: {e}")
        
        print("[Auth] ✗ No authentication token found in cookies, localStorage, sessionStorage, or MSAL cache")
        print(f"[API] Available cookies: {[c['name'] for c in self.page.context.cookies()]}")
        print("[API] ✗ Could not extract JWT token from browser")
        return None
    
    def select(self, selector: str, value: str):
        """
        Select an option in a dropdown.
        
        Args:
            selector: Element selector
            value: Value to select
        """
        self.page.select_option(selector, value)
    
    def wait(self, milliseconds: int):
        """
        Wait for specified milliseconds.
        
        Args:
            milliseconds: Time to wait in milliseconds
        """
        time.sleep(milliseconds / 1000)
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Name for the screenshot file
        
        Returns:
            dict: Result from MCP server
        """
        return self.ui.take_screenshot(filename=filename)
