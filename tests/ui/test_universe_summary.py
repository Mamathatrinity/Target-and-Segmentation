"""
Universe Summary Page UI Tests
Tests dashboard, charts, navigation, and HCP universe selection
"""

import pytest
from framework.page_objects import LoginPage, UniverseSummaryPage


@pytest.fixture
def universe_page(ui_validator, settings, autouse=False):
    """Fixture to provide UniverseSummaryPage instance."""
    return UniverseSummaryPage(ui_validator, settings.APP_URL)


@pytest.mark.ui
@pytest.mark.smoke
def test_universe_summary_page_loads(universe_page):
    """Test Universe Summary page loads successfully."""
    universe_page.navigate_to_page()
    
    assert universe_page.is_page_loaded(), "Universe Summary page should load"
    print("✓ Universe Summary page loaded successfully")


@pytest.mark.ui
@pytest.mark.smoke
def test_hcp_universe_dropdown_visible(universe_page):
    """Test HCP Universe dropdown is visible."""
    universe_page.navigate_to_page()
    
    assert universe_page.is_element_visible(universe_page.HCP_UNIVERSE_DROPDOWN)
    print("✓ HCP Universe dropdown is visible")


@pytest.mark.ui
@pytest.mark.regression
def test_all_navigation_tabs_visible(universe_page):
    """Test all main navigation tabs are visible."""
    universe_page.navigate_to_page()
    
    assert universe_page.is_element_visible(universe_page.UNIVERSE_SUMMARY_TAB)
    assert universe_page.is_element_visible(universe_page.SEGMENTS_TAB)
    assert universe_page.is_element_visible(universe_page.TARGET_LIST_TAB)
    print("✓ All navigation tabs (Universe Summary, Segments, Target List) are visible")


@pytest.mark.ui
@pytest.mark.regression
def test_create_buttons_visible(universe_page):
    """Test Create Segment and Create Target List buttons are visible."""
    universe_page.navigate_to_page()
    
    assert universe_page.is_element_visible(universe_page.CREATE_SEGMENT_BUTTON)
    assert universe_page.is_element_visible(universe_page.CREATE_TARGET_LIST_BUTTON)
    print("✓ Create Segment and Create Target List buttons are visible")


@pytest.mark.ui
@pytest.mark.regression
def test_sub_tabs_visible(universe_page):
    """Test HCP Segmentation and HCP Overlap sub-tabs are visible."""
    universe_page.navigate_to_page()
    
    assert universe_page.is_element_visible(universe_page.HCP_SEGMENTATION_TAB)
    assert universe_page.is_element_visible(universe_page.HCP_OVERLAP_TAB)
    print("✓ HCP Segmentation and HCP Overlap sub-tabs are visible")


@pytest.mark.ui
@pytest.mark.regression
def test_sankey_chart_loads(universe_page):
    """Test Sankey chart visualization loads."""
    universe_page.navigate_to_page()
    
    assert universe_page.is_sankey_chart_visible(), "Sankey chart should be visible"
    print("✓ Sankey chart loaded successfully")


@pytest.mark.ui
@pytest.mark.regression
def test_all_insight_charts_load(universe_page):
    """Test all 4 insight charts load on the dashboard."""
    universe_page.navigate_to_page()
    
    # Wait for page to fully load
    import time
    time.sleep(2)
    
    assert universe_page.verify_all_charts_loaded(), "All insight charts should load"
    print("✓ All insight charts loaded (Specialty, Channel, Patient Makeup, Adopter Categories)")


@pytest.mark.ui
@pytest.mark.regression
def test_switch_to_hcp_overlap_tab(universe_page):
    """Test switching to HCP Overlap sub-tab."""
    universe_page.navigate_to_page()
    
    result = universe_page.switch_to_hcp_overlap_tab()
    
    assert result["status"] == "success"
    print("✓ Successfully switched to HCP Overlap tab")


@pytest.mark.ui
@pytest.mark.regression
def test_navigate_to_segments_from_universe(universe_page):
    """Test navigation to Segments tab from Universe Summary."""
    universe_page.navigate_to_page()
    
    result = universe_page.navigate_to_segments()
    
    assert result["status"] == "success"
    print("✓ Successfully navigated to Segments tab")


@pytest.mark.ui
@pytest.mark.regression
def test_navigate_to_target_list_from_universe(universe_page):
    """Test navigation to Target List tab from Universe Summary."""
    universe_page.navigate_to_page()
    
    result = universe_page.navigate_to_target_list()
    
    assert result["status"] == "success"
    print("✓ Successfully navigated to Target List tab")


@pytest.mark.ui
@pytest.mark.regression
def test_click_create_segment_button(universe_page):
    """Test clicking Create Segment button."""
    universe_page.navigate_to_page()
    
    result = universe_page.click_create_segment()
    
    assert result["status"] == "success"
    print("✓ Successfully clicked Create Segment button")


@pytest.mark.ui
@pytest.mark.regression
def test_profile_button_visible(universe_page):
    """Test Profile button is visible in header."""
    universe_page.navigate_to_page()
    
    assert universe_page.is_element_visible(universe_page.PROFILE_BUTTON)
    print("✓ Profile button is visible")
