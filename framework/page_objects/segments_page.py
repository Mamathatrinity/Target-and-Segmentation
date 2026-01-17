"""
Segments Page Object Model
Handles interactions with the Segments listing and management page
"""

from framework.page_objects.base_page import BasePage
from playwright.sync_api import Page
from framework.page_objects.retry_utils import retry_on_exception
import time


class SegmentsPage(BasePage):
    """Page object for Segments page."""
    
    # Page Elements - Using flexible selectors
    SEARCH_FIELD = 'input[placeholder*="Search"], input[aria-label*="Search"], [role="searchbox"]'
    CREATE_SEGMENT_BUTTON = 'button:has-text("Create Segment"), button:has-text("Create")'
    HCP_UNIVERSE_DROPDOWN = 'select, [role="combobox"]'
    SHOW_FILTER_DROPDOWN = 'select:has-text("My Segments"), [role="combobox"]:has-text("My Segments")'
    SORT_BY_DROPDOWN = 'select:has-text("Name"), [role="combobox"]:has-text("Name")'
    
    # Segment Card Elements
    SEGMENT_CARD = '.home__card'
    SEGMENT_NAME = 'h6'
    SEGMENT_DESCRIPTION = 'p'
    SEGMENT_HCP_COUNT = 'text=/\\d+\\.\\d+K HCPs|\\d+ HCPs/'
    
    # Pagination
    RECORDS_PER_PAGE_DROPDOWN = 'combobox[aria-label*="Records per page"]'
    PREVIOUS_PAGE_BUTTON = 'button[aria-label="Previous page"]'
    NEXT_PAGE_BUTTON = 'button[aria-label="Next page"]'
    PAGE_INFO = 'text=/\\d+–\\d+ of \\d+/'
    
    def __init__(self, page: Page, app_url: str):
        """
        Initialize Segments page.
        
        Args:
            page: Playwright Page instance
            app_url: Application base URL
        """
        super().__init__(page)
        self.page_url = f"{app_url}/segments"
    
    @retry_on_exception(max_retries=3, delay=1)
    def navigate_to_page(self) -> dict:
        """Navigate to Segments page."""
        return self.navigate_to(self.page_url)
    
    @retry_on_exception(max_retries=3, delay=1)
    def is_page_loaded(self) -> bool:
        """
        Check if Segments page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        # Wait for page to load
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
        except:
            pass
        
        # Check URL contains segments
        return "/segments" in self.page.url
    
    @retry_on_exception(max_retries=3, delay=1)
    def search_segments(self, search_text: str) -> dict:
        """
        Search for segments by name.
        
        Args:
            search_text: Text to search for
        
        Returns:
            dict: Result from typing action
        """
        # Use flexible search field selector
        return self.type_text(self.SEARCH_FIELD, search_text)
    
    @retry_on_exception(max_retries=3, delay=1)
    def clear_search(self) -> dict:
        """
        Clear the search field.
        
        Returns:
            dict: Result from clearing action
        """
        try:
            search_field = self.page.locator(self.SEARCH_FIELD).first
            search_field.clear()
            search_field.press("Enter")
            return {"status": "success", "message": "Search field cleared"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    @retry_on_exception(max_retries=3, delay=1)
    def select_hcp_universe(self, universe_name: str) -> dict:
        """
        Select an HCP universe from the dropdown.
        
        Args:
            universe_name: Name of the universe to select
        
        Returns:
            dict: Result from selection action
        """
        self.click_element(self.HCP_UNIVERSE_DROPDOWN)
        option_selector = f'text="{universe_name}"'
        return self.click_element(option_selector)
    
    @retry_on_exception(max_retries=3, delay=1)
    def select_show_filter(self, filter_option: str) -> dict:
        """
        Robustly select filter option (e.g., 'My Segments', 'Team Segments') from dropdown.
        Handles Material-UI dropdown/modal quirks.
        Args:
            filter_option: Filter option to select
        Returns:
            dict: Result from selection action
        """
        import time
        try:
            # 1. Click the dropdown to open it
            dropdown = self.page.locator(self.SHOW_FILTER_DROPDOWN).first
            dropdown.click(force=True)
            time.sleep(1)

            # 2. Wait for the dropdown options to be visible
            # Try multiple strategies for Material-UI
            option_clicked = False
            # Strategy 1: li:has-text
            try:
                option = self.page.locator(f'li:has-text("{filter_option}")').first
                if option.is_visible(timeout=2000):
                    option.click(force=True)
                    option_clicked = True
            except Exception:
                pass
            # Strategy 2: role=option
            if not option_clicked:
                try:
                    option = self.page.locator(f'[role="option"]:has-text("{filter_option}")').first
                    if option.is_visible(timeout=2000):
                        option.click(force=True)
                        option_clicked = True
                except Exception:
                    pass
            # Strategy 3: fallback text locator
            if not option_clicked:
                option = self.page.locator(f'text="{filter_option}"').first
                option.click(force=True)
                option_clicked = True

            time.sleep(1)
            # 3. Close dropdown if still open (press Escape)
            self.page.keyboard.press("Escape")
            time.sleep(0.5)
            return {"status": "success", "message": f"Selected filter: {filter_option}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    @retry_on_exception(max_retries=3, delay=1)
    def select_sort_by(self, sort_option: str) -> dict:
        """
        Select sort option (e.g., 'Name', 'Created Date').
        Clicking toggles between ASC/DESC/Default.
        
        Args:
            sort_option: Sort option to select
        
        Returns:
            dict: Result from selection action
        """
        try:
            # Find and click the sort dropdown
            sort_dropdown = self.page.locator(self.SORT_BY_DROPDOWN).first
            sort_dropdown.click()
            time.sleep(1)
            
            # Find and click the specific option from the dropdown menu
            # Try multiple selector strategies
            option_clicked = False
            
            # Strategy 1: Try exact text match in dropdown option
            try:
                option = self.page.locator(f'li:has-text("{sort_option}")').first
                if option.is_visible(timeout=2000):
                    option.click(force=True)
                    option_clicked = True
            except:
                pass
            
            # Strategy 2: Try role-based selection
            if not option_clicked:
                try:
                    option = self.page.locator(f'[role="option"]:has-text("{sort_option}")').first
                    if option.is_visible(timeout=2000):
                        option.click(force=True)
                        option_clicked = True
                except:
                    pass
            
            # Strategy 3: Simple text locator with force click
            if not option_clicked:
                option = self.page.locator(f'text="{sort_option}"').first
                option.click(force=True)
                option_clicked = True
            
            time.sleep(1)
            
            # Close dropdown if still open (press Escape)
            self.page.keyboard.press("Escape")
            time.sleep(0.5)
            
            return {"status": "success", "message": f"Selected sort: {sort_option}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    @retry_on_exception(max_retries=3, delay=1)
    def click_create_segment(self) -> dict:
        """Click Create Segment button and wait for create form to load."""
        result = self.click_element(self.CREATE_SEGMENT_BUTTON)
        # Wait for the Name input field to be visible (indicates form is ready)
        self.wait_for_element('input[placeholder*="Name"]', timeout=10000)
        return result
    
    @retry_on_exception(max_retries=3, delay=1)
    def get_segment_count(self) -> int:
        """
        Get the count of segment cards displayed.
        
        Returns:
            int: Number of segment cards
        """
        try:
            return self.page.locator(self.SEGMENT_CARD).count()
        except Exception:
            return 0
    
    @retry_on_exception(max_retries=3, delay=1)
    def click_segment_by_name(self, segment_name: str) -> dict:
        """
        Click on a segment card by its name.
        
        Args:
            segment_name: Name of the segment to click
        
        Returns:
            dict: Result from click action
        """
        segment_selector = f'h6:has-text("{segment_name}")'
        return self.click_element(segment_selector)
    
    @retry_on_exception(max_retries=3, delay=1)
    def is_segment_visible(self, segment_name: str) -> bool:
        """
        Check if a segment with given name is visible.
        
        Args:
            segment_name: Name of the segment
        
        Returns:
            bool: True if segment is visible
        """
        segment_selector = f'h6:has-text("{segment_name}")'
        return self.is_element_visible(segment_selector, timeout=5000)
    
    @retry_on_exception(max_retries=3, delay=1)
    def click_next_page(self) -> dict:
        """Click Next Page button in pagination."""
        return self.click_element(self.NEXT_PAGE_BUTTON)
    
    @retry_on_exception(max_retries=3, delay=1)
    def click_previous_page(self) -> dict:
        """Click Previous Page button in pagination."""
        return self.click_element(self.PREVIOUS_PAGE_BUTTON)
    
    @retry_on_exception(max_retries=3, delay=1)
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
