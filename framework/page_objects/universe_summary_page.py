"""
Universe Summary Page Object Model
Handles interactions with the Universe Summary dashboard
"""

from framework.page_objects.base_page import BasePage
from playwright.sync_api import Page


class UniverseSummaryPage(BasePage):
    """Page object for Universe Summary page."""
    
    # Navigation Tab Locators
    UNIVERSE_SUMMARY_TAB = 'tab[aria-label="UNIVERSE SUMMARY"]'
    SEGMENTS_TAB = 'tab[aria-label="SEGMENTS"]'
    TARGET_LIST_TAB = 'tab[aria-label="TARGET LIST"]'
    
    # Header Elements
    NOTIFICATIONS_BUTTON = 'button[aria-label="Notifications"]'
    HELP_BUTTON = 'button[aria-label="Help"]'
    APPLICATIONS_BUTTON = 'button[aria-label="Applications"]'
    PROFILE_BUTTON = 'button[aria-label="Profile"]'
    
    # Universe Summary Page Elements
    HCP_UNIVERSE_DROPDOWN = 'combobox[aria-label="Select a HCP Universe"]'
    UNIVERSE_COUNT_TEXT = 'text=Entire Universe of HCPs'
    CREATE_SEGMENT_BUTTON = 'button:has-text("Create Segment")'
    CREATE_TARGET_LIST_BUTTON = 'button:has-text("Create Target List")'
    
    # Sub-tabs
    HCP_SEGMENTATION_TAB = 'tab:has-text("HCP Segmentation")'
    HCP_OVERLAP_TAB = 'tab:has-text("HCP Overlap")'
    
    # Sankey Chart
    SANKEY_CHART = 'svg'
    
    # Insight Charts
    SPECIALTY_CHART = 'text=Specialty Composition'
    CHANNEL_CHART = 'text=Channel Preference'
    PATIENT_MAKEUP_CHART = 'text=Patient Makeup Distribution'
    ADOPTER_CHART = 'text=Adopter Categories'
    
    def __init__(self, page: Page, app_url: str):
        """
        Initialize Universe Summary page.
        
        Args:
            page: Playwright Page instance
            app_url: Application base URL
        """
        super().__init__(page)
        self.page_url = f"{app_url}/universe-summary"
    
    def navigate_to_page(self) -> dict:
        """Navigate to Universe Summary page."""
        return self.navigate_to(self.page_url)
    
    def is_page_loaded(self) -> bool:
        """
        Check if Universe Summary page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.HCP_UNIVERSE_DROPDOWN, timeout=10000)
    
    def select_hcp_universe(self, universe_name: str) -> dict:
        """
        Select an HCP universe from the dropdown.
        
        Args:
            universe_name: Name of the universe to select
        
        Returns:
            dict: Result from click action
        """
        # Click the dropdown
        self.click_element(self.HCP_UNIVERSE_DROPDOWN)
        
        # Click the specific option
        option_selector = f'text="{universe_name}"'
        return self.click_element(option_selector)
    
    def click_create_segment(self) -> dict:
        """Click Create Segment button."""
        return self.click_element(self.CREATE_SEGMENT_BUTTON)
    
    def click_create_target_list(self) -> dict:
        """Click Create Target List button."""
        return self.click_element(self.CREATE_TARGET_LIST_BUTTON)
    
    def switch_to_hcp_segmentation_tab(self) -> dict:
        """Switch to HCP Segmentation sub-tab."""
        return self.click_element(self.HCP_SEGMENTATION_TAB)
    
    def switch_to_hcp_overlap_tab(self) -> dict:
        """Switch to HCP Overlap sub-tab."""
        return self.click_element(self.HCP_OVERLAP_TAB)
    
    def is_sankey_chart_visible(self) -> bool:
        """
        Check if Sankey chart is visible.
        
        Returns:
            bool: True if Sankey chart is visible
        """
        return self.is_element_visible(self.SANKEY_CHART, timeout=10000)
    
    def is_specialty_chart_visible(self) -> bool:
        """Check if Specialty Composition chart is visible."""
        return self.is_element_visible(self.SPECIALTY_CHART)
    
    def is_channel_chart_visible(self) -> bool:
        """Check if Channel Preference chart is visible."""
        return self.is_element_visible(self.CHANNEL_CHART)
    
    def is_patient_makeup_chart_visible(self) -> bool:
        """Check if Patient Makeup Distribution chart is visible."""
        return self.is_element_visible(self.PATIENT_MAKEUP_CHART)
    
    def is_adopter_chart_visible(self) -> bool:
        """Check if Adopter Categories chart is visible."""
        return self.is_element_visible(self.ADOPTER_CHART)
    
    def verify_all_charts_loaded(self) -> bool:
        """
        Verify all charts are loaded on the page.
        
        Returns:
            bool: True if all charts are visible
        """
        return (
            self.is_sankey_chart_visible() and
            self.is_specialty_chart_visible() and
            self.is_channel_chart_visible() and
            self.is_patient_makeup_chart_visible() and
            self.is_adopter_chart_visible()
        )
    
    def navigate_to_segments(self) -> dict:
        """Navigate to Segments tab."""
        return self.click_element(self.SEGMENTS_TAB)
    
    def navigate_to_target_list(self) -> dict:
        """Navigate to Target List tab."""
        return self.click_element(self.TARGET_LIST_TAB)
    
    def click_profile(self) -> dict:
        """Click Profile button to open profile menu."""
        return self.click_element(self.PROFILE_BUTTON)
