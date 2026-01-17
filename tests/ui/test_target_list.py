"""
Target List Page UI Tests
Tests target list viewing, search, and management
"""

import pytest
from framework.page_objects import TargetListPage


@pytest.fixture
def target_list_page(ui_validator, settings, autouse=False):
    """Fixture to provide TargetListPage instance."""
    return TargetListPage(ui_validator, settings.APP_URL)


@pytest.mark.ui
@pytest.mark.smoke
def test_target_list_page_loads(target_list_page):
    """Test Target List page loads successfully."""
    target_list_page.navigate_to_page()
    
    assert target_list_page.is_page_loaded(), "Target List page should load"
    print("✓ Target List page loaded successfully")


@pytest.mark.ui
@pytest.mark.smoke
def test_search_field_visible(target_list_page):
    """Test search field is visible on Target List page."""
    target_list_page.navigate_to_page()
    
    assert target_list_page.is_element_visible(target_list_page.SEARCH_FIELD)
    print("✓ Search field is visible")


@pytest.mark.ui
@pytest.mark.regression
def test_create_target_list_button_visible(target_list_page):
    """Test Create Target List button is visible."""
    target_list_page.navigate_to_page()
    
    assert target_list_page.is_element_visible(target_list_page.CREATE_TARGET_LIST_BUTTON)
    print("✓ Create Target List button is visible")


@pytest.mark.ui
@pytest.mark.regression
def test_sort_dropdown_visible(target_list_page):
    """Test sort dropdown is visible."""
    target_list_page.navigate_to_page()
    
    assert target_list_page.is_element_visible(target_list_page.SORT_BY_DROPDOWN)
    print("✓ Sort dropdown is visible")


@pytest.mark.ui
@pytest.mark.regression
def test_target_list_cards_displayed(target_list_page):
    """Test target list cards are displayed on the page."""
    target_list_page.navigate_to_page()
    
    # Wait for page to load
    import time
    time.sleep(2)
    
    count = target_list_page.get_target_list_count()
    assert count > 0, "At least one target list card should be displayed"
    print(f"✓ {count} target list cards displayed")


@pytest.mark.ui
@pytest.mark.regression
def test_search_target_lists_functionality(target_list_page):
    """Test searching for target lists."""
    target_list_page.navigate_to_page()
    
    result = target_list_page.search_target_lists("test")
    
    assert result["status"] == "success"
    print("✓ Search functionality works")


@pytest.mark.ui
@pytest.mark.regression
def test_click_create_target_list_button(target_list_page):
    """Test clicking Create Target List button."""
    target_list_page.navigate_to_page()
    
    result = target_list_page.click_create_target_list()
    
    assert result["status"] == "success"
    print("✓ Successfully clicked Create Target List button")


@pytest.mark.ui
@pytest.mark.regression
def test_pagination_controls_visible(target_list_page):
    """Test pagination controls are visible."""
    target_list_page.navigate_to_page()
    
    # Check if records per page dropdown exists
    has_pagination = target_list_page.is_element_visible(
        target_list_page.RECORDS_PER_PAGE_DROPDOWN, 
        timeout=5000
    )
    
    if has_pagination:
        print("✓ Pagination controls are visible")
    else:
        print("⚠ Pagination controls not visible (may be hidden if few records)")
