"""
Create Segment Page Object Model
Handles interactions with the Create Segment page
"""

from typing import Dict, Any
from framework.page_objects.base_page import BasePage


class CreateSegmentPage(BasePage):
    """Page object for Create Segment page."""
    
    # Page Elements
    BACK_BUTTON = 'button[aria-label="back"]'
    PAGE_TITLE = 'heading:has-text("Build Segment")'
    NEXT_BUTTON = 'button:has-text("Next")'
    
    # Input Fields
    SEGMENT_NAME_INPUT = 'textbox[aria-label="Segment Name *"]'
    DESCRIPTION_INPUT = 'textbox[aria-label="Description"]'
    TAGS_INPUT = 'combobox[aria-label="Tags"]'
    
    # HCP Universe Section
    HCP_UNIVERSE_HEADING = 'heading:has-text("Select HCP Universe *")'
    
    # Team Segment Toggle
    TEAM_SEGMENT_SWITCH = 'switch'
    TEAM_SEGMENT_LABEL = 'text=Team Segment'
    TEAM_SEGMENT_DESCRIPTION = 'text=Available to all team members'
    
    def __init__(self, page, app_url: str):
        """
        Initialize Create Segment page.
        
        Args:
            page: Playwright Page instance
            app_url: Application base URL
        """
        super().__init__(page)
        self.page_url = f"{app_url}/create-segment"
    
    def navigate_to_page(self) -> dict:
        """Navigate to Create Segment page."""
        return self.navigate_to(self.page_url)
    
    def is_page_loaded(self) -> bool:
        """
        Check if Create Segment page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.PAGE_TITLE, timeout=10000)
    
    def click_back(self) -> dict:
        """Click Back button to return to previous page."""
        return self.click_element(self.BACK_BUTTON)
    
    def enter_segment_name(self, name: str) -> dict:
        """
        Enter segment name.
        
        Args:
            name: Segment name to enter
        
        Returns:
            dict: Result from typing action
        """
        return self.type_text(self.SEGMENT_NAME_INPUT, name)
    
    def enter_description(self, description: str) -> dict:
        """
        Enter segment description.
        
        Args:
            description: Description text to enter
        
        Returns:
            dict: Result from typing action
        """
        return self.type_text(self.DESCRIPTION_INPUT, description)
    
    def add_tag(self, tag: str) -> dict:
        """
        Add a tag to the segment.
        
        Args:
            tag: Tag text to add
        
        Returns:
            dict: Result from selection action
        """
        # Click the tags dropdown
        self.click_element(self.TAGS_INPUT)
        
        # Type or select the tag
        return self.type_text(self.TAGS_INPUT, tag)
    
    def toggle_team_segment(self, enable: bool = True) -> dict:
        """
        Toggle the Team Segment switch.
        
        Args:
            enable: True to enable team segment, False to disable
        
        Returns:
            dict: Result from click action
        """
        # Check current state and toggle if needed
        return self.click_element(self.TEAM_SEGMENT_SWITCH)
    
    def click_next(self) -> dict:
        """Click Next button to proceed to next step."""
        return self.click_element(self.NEXT_BUTTON)
    
    def fill_segment_details(
        self, 
        name: str, 
        description: str = "", 
        tags: list = None, 
        team_segment: bool = False
    ) -> bool:
        """
        Fill all segment details on the first page.
        
        Args:
            name: Segment name (required)
            description: Segment description (optional)
            tags: List of tags to add (optional)
            team_segment: Whether to enable team segment (default: False)
        
        Returns:
            bool: True if all fields filled successfully
        """
        try:
            # Enter segment name
            self.enter_segment_name(name)
            
            # Enter description if provided
            if description:
                self.enter_description(description)
            
            # Add tags if provided
            if tags:
                for tag in tags:
                    self.add_tag(tag)
            
            # Toggle team segment if needed
            if team_segment:
                self.toggle_team_segment(True)
            
            return True
        except Exception as e:
            print(f"Error filling segment details: {str(e)}")
            return False
