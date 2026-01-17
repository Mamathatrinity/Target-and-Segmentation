"""
Profile Menu Page Object Model
Handles interactions with the user profile menu
"""

from framework.page_objects.base_page import BasePage
from playwright.sync_api import Page


class ProfileMenuPage(BasePage):
    """Page object for Profile Menu dropdown."""
    
    # Profile Button
    PROFILE_BUTTON = 'button[aria-label="Profile"]'
    
    # Profile Menu Elements
    USER_NAME = 'heading'  # First heading in menu will be user name
    USER_ROLE = 'paragraph:has-text("ADMIN")'
    USER_EMAIL = 'paragraph'  # Email will be in a paragraph
    
    # Brand Selector
    BRAND_SELECTOR_SECTION = 'text=Select Brand'
    
    # Logout Button
    LOGOUT_BUTTON = 'button[aria-label="Logout"]'
    LOGOUT_BUTTON_ALT = 'button:has-text("Logout")'
    
    def __init__(self, page: Page):
        """
        Initialize Profile Menu page.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
    
    def open_profile_menu(self) -> dict:
        """Open the profile menu dropdown."""
        return self.click_element(self.PROFILE_BUTTON)
    
    def is_menu_open(self) -> bool:
        """
        Check if profile menu is open.
        
        Returns:
            bool: True if menu is open
        """
        return self.is_element_visible(self.LOGOUT_BUTTON, timeout=3000)
    
    def get_user_name(self) -> str:
        """
        Get the displayed user name.
        
        Returns:
            str: User name text
        """
        result = self.get_text(self.USER_NAME)
        return result.get("text", "")
    
    def get_user_role(self) -> str:
        """
        Get the displayed user role.
        
        Returns:
            str: User role text
        """
        result = self.get_text(self.USER_ROLE)
        return result.get("text", "")
    
    def select_brand(self, brand_name: str) -> dict:
        """
        Select a brand from the brand selector.
        
        Args:
            brand_name: Name of the brand to select
        
        Returns:
            dict: Result from click action
        """
        brand_selector = f'text="{brand_name}"'
        return self.click_element(brand_selector)
    
    def click_logout(self) -> dict:
        """Click Logout button."""
        # Try primary selector first
        if self.is_element_visible(self.LOGOUT_BUTTON, timeout=2000):
            return self.click_element(self.LOGOUT_BUTTON)
        else:
            return self.click_element(self.LOGOUT_BUTTON_ALT)
    
    def perform_logout(self) -> bool:
        """
        Complete logout workflow.
        
        Returns:
            bool: True if logout successful
        """
        try:
            # Open profile menu
            self.open_profile_menu()
            
            # Wait for menu to open
            if not self.is_menu_open():
                return False
            
            # Click logout
            self.click_logout()
            
            return True
        except Exception as e:
            print(f"Error during logout: {str(e)}")
            return False
