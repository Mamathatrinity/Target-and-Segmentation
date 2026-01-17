"""
Create Segment Workflow UI Tests
Tests the complete segment creation flow
"""

import pytest
from framework.page_objects import CreateSegmentPage


@pytest.fixture
def create_segment_page(ui_validator, settings, autouse=False):
    """Fixture to provide CreateSegmentPage instance."""
    return CreateSegmentPage(ui_validator, settings.APP_URL)


@pytest.mark.ui
@pytest.mark.smoke
def test_create_segment_page_loads(create_segment_page):
    """Test Create Segment page loads successfully."""
    create_segment_page.navigate_to_page()
    
    assert create_segment_page.is_page_loaded(), "Create Segment page should load"
    print("✓ Create Segment page loaded successfully")


@pytest.mark.ui
@pytest.mark.regression
def test_page_title_visible(create_segment_page):
    """Test page title 'Build Segment' is visible."""
    create_segment_page.navigate_to_page()
    
    assert create_segment_page.is_element_visible(create_segment_page.PAGE_TITLE)
    print("✓ 'Build Segment' page title is visible")


@pytest.mark.ui
@pytest.mark.regression
def test_required_fields_visible(create_segment_page):
    """Test all required input fields are visible."""
    create_segment_page.navigate_to_page()
    
    assert create_segment_page.is_element_visible(create_segment_page.SEGMENT_NAME_INPUT)
    assert create_segment_page.is_element_visible(create_segment_page.HCP_UNIVERSE_HEADING)
    print("✓ Required fields (Segment Name, HCP Universe) are visible")


@pytest.mark.ui
@pytest.mark.regression
def test_optional_fields_visible(create_segment_page):
    """Test optional input fields are visible."""
    create_segment_page.navigate_to_page()
    
    assert create_segment_page.is_element_visible(create_segment_page.DESCRIPTION_INPUT)
    assert create_segment_page.is_element_visible(create_segment_page.TAGS_INPUT)
    print("✓ Optional fields (Description, Tags) are visible")


@pytest.mark.ui
@pytest.mark.regression
def test_team_segment_toggle_visible(create_segment_page):
    """Test Team Segment toggle is visible."""
    create_segment_page.navigate_to_page()
    
    assert create_segment_page.is_element_visible(create_segment_page.TEAM_SEGMENT_SWITCH)
    print("✓ Team Segment toggle is visible")


@pytest.mark.ui
@pytest.mark.regression
def test_navigation_buttons_visible(create_segment_page):
    """Test Back and Next buttons are visible."""
    create_segment_page.navigate_to_page()
    
    assert create_segment_page.is_element_visible(create_segment_page.BACK_BUTTON)
    assert create_segment_page.is_element_visible(create_segment_page.NEXT_BUTTON)
    print("✓ Back and Next buttons are visible")


@pytest.mark.ui
@pytest.mark.regression
def test_enter_segment_name(create_segment_page):
    """Test entering segment name."""
    create_segment_page.navigate_to_page()
    
    test_name = "Automation Test Segment"
    result = create_segment_page.enter_segment_name(test_name)
    
    assert result["status"] == "success"
    print(f"✓ Successfully entered segment name: {test_name}")


@pytest.mark.ui
@pytest.mark.regression
def test_enter_description(create_segment_page):
    """Test entering segment description."""
    create_segment_page.navigate_to_page()
    
    test_description = "This is an automated test segment description"
    result = create_segment_page.enter_description(test_description)
    
    assert result["status"] == "success"
    print("✓ Successfully entered segment description")


@pytest.mark.ui
@pytest.mark.regression
def test_fill_complete_segment_form(create_segment_page):
    """Test filling complete segment creation form."""
    create_segment_page.navigate_to_page()
    
    success = create_segment_page.fill_segment_details(
        name="Complete Test Segment",
        description="Full segment with all fields",
        tags=["Automation", "Testing"],
        team_segment=True
    )
    
    assert success == True
    print("✓ Successfully filled complete segment creation form")


@pytest.mark.ui
@pytest.mark.regression
def test_click_back_button(create_segment_page):
    """Test clicking Back button."""
    create_segment_page.navigate_to_page()
    
    result = create_segment_page.click_back()
    
    assert result["status"] == "success"
    print("✓ Successfully clicked Back button")
