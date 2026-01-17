"""
Target List Page Object Model
Handles interactions with the Target List management page
"""

from framework.page_objects.base_page import BasePage
from playwright.sync_api import Page


class TargetListPage(BasePage):
    """Page object for Target List page."""
    
    # Page Elements
    SEARCH_FIELD = 'textbox[placeholder="Search target lists"]'
    SORT_BY_DROPDOWN = 'combobox:has-text("Name")'
    CREATE_TARGET_LIST_BUTTON = 'button:has-text("Create Target List")'
    
    # Target List Card Elements
    TARGET_CARD = '[role="article"]'
    TARGET_NAME = 'h6'
    TARGET_DESCRIPTION = 'p'
    TARGET_HCP_COUNT = 'text=/\\d+\\.\\d+K HCPs|\\d+ HCPs/'
    TARGET_DERIVED_SOURCE = 'text=/Derived:/'
    
    # Pagination
    RECORDS_PER_PAGE_DROPDOWN = 'combobox[aria-label*="Records per page"]'
    PREVIOUS_PAGE_BUTTON = 'button[aria-label="Previous page"]'
    NEXT_PAGE_BUTTON = 'button[aria-label="Next page"]'
    PAGE_INFO = 'text=/\\d+–\\d+ of \\d+/'
    
    def __init__(self, page: Page, app_url: str):
        """
        Initialize Target List page.
        
        Args:
            page: Playwright Page instance
            app_url: Application base URL
        """
        super().__init__(page)
        self.page_url = f"{app_url}/target-list"
    
    def navigate_to_page(self) -> dict:
        """Navigate to Target List page."""
        return self.navigate_to(self.page_url)
    
    def is_page_loaded(self) -> bool:
        """
        Check if Target List page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.SEARCH_FIELD, timeout=10000)
    
    def search_target_lists(self, search_text: str) -> dict:
        """
        Search for target lists by name.
        
        Args:
            search_text: Text to search for
        
        Returns:
            dict: Result from typing action
        """
        return self.type_text(self.SEARCH_FIELD, search_text)
    
    def select_sort_by(self, sort_option: str) -> dict:
        """
        Select sort option (e.g., 'Name', 'Created Date').
        
        Args:
            sort_option: Sort option to select
        
        Returns:
            dict: Result from selection action
        """
        self.click_element(self.SORT_BY_DROPDOWN)
        option_selector = f'text="{sort_option}"'
        return self.click_element(option_selector)
    
    def click_create_target_list(self) -> dict:
        """Click Create Target List button."""
        return self.click_element(self.CREATE_TARGET_LIST_BUTTON)
    
    def get_target_list_count(self) -> int:
        """
        Get the count of target list cards displayed.
        
        Returns:
            int: Number of target list cards
        """
        result = self.ui.count_elements(selector=self.TARGET_CARD)
        return result.get("count", 0)
    
    def click_target_list_by_name(self, target_name: str) -> dict:
        """
        Click on a target list card by its name.
        
        Args:
            target_name: Name of the target list to click
        
        Returns:
            dict: Result from click action
        """
        target_selector = f'h6:has-text("{target_name}")'
        return self.click_element(target_selector)
    
    def is_target_list_visible(self, target_name: str) -> bool:
        """
        Check if a target list with given name is visible.
        
        Args:
            target_name: Name of the target list
        
        Returns:
            bool: True if target list is visible
        """
        target_selector = f'h6:has-text("{target_name}")'
        return self.is_element_visible(target_selector, timeout=5000)
    
    def click_next_page(self) -> dict:
        """Click Next Page button in pagination."""
        return self.click_element(self.NEXT_PAGE_BUTTON)
    
    def click_previous_page(self) -> dict:
        """Click Previous Page button in pagination."""
        return self.click_element(self.PREVIOUS_PAGE_BUTTON)
    
    def select_records_per_page(self, count: int) -> dict:
        """
        Select number of records per page.
        
        Args:
            count: Number of records per page (e.g., 8, 16, 24)
        
        Returns:
            dict: Result from selection action
        """
        self.click_element(self.RECORDS_PER_PAGE_DROPDOWN)
        option_selector = f'text="{count}"'
        return self.click_element(option_selector)
