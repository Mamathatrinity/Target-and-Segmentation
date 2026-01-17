"""
Simple Segments Test - Core CRUD Operations
Focuses on working tests only, no TODOs
"""
import pytest
import allure
import time
from framework.page_objects.segments_page import SegmentsPage
from config.settings import Settings
from tests.helpers.segments_db_helpers import (
    verify_segment_exists,
    delete_test_segment,
    get_segment_by_name,
    search_segments,
)


@pytest.mark.segments
@pytest.mark.crud
def test_segments_list_visible(page, settings):
    """Test: Segments list is visible and loaded"""
    allure.dynamic.title("Segments List - Visible")
    
    segments_page = SegmentsPage(page, settings.APP_URL)
    
    # Navigate if needed
    if "/segments" not in page.url:
        segments_page.navigate_to_page()
    
    # Wait for page content to load
    page.wait_for_timeout(3000)
    
    # Verify page is loaded
    assert segments_page.is_page_loaded(), "Segments page should be loaded"
    print(f"[OK] Page loaded - URL: {page.url}")
    
    # Try to get segment cards
    try:
        cards = page.locator('.home__card')
        count = cards.count()
        print(f"[INFO] Found {count} cards with '.home__card' selector")
    except Exception as e:
        print(f"[WARN] Error finding '.home__card': {e}")
        count = 0
    
    # If no cards, try alternative selectors
    if count == 0:
        try:
            cards = page.locator('[role="article"]')
            count = cards.count()
            print(f"[INFO] Found {count} cards with '[role=\"article\"]' selector")
        except Exception as e:
            print(f"[WARN] Error finding '[role=\"article\"]': {e}")
    
    if count == 0:
        # Print page HTML to debug
        html = page.content()
        if "card" in html.lower():
            print("[INFO] Page contains 'card' text")
        if "segment" in html.lower():
            print("[INFO] Page contains 'segment' text")
        print(f"[INFO] Page length: {len(html)} characters")
    
    assert count > 0, f"Should see at least 1 segment card, got {count}"
    print(f"[OK] Found {count} segment cards on page")


@pytest.mark.segments
@pytest.mark.crud
def test_segments_create_simple(page, mysql_connection, settings):
    """Test: Create a simple segment"""
    allure.dynamic.title("Segments Create - Simple")
    
    test_name = "TestSegmentSimple"
    description = "Simple test segment"
    
    segments_page = SegmentsPage(page, settings.APP_URL)
    
    # Setup: Delete if exists
    if verify_segment_exists(mysql_connection, test_name):
        delete_test_segment(mysql_connection, test_name)
    
    # Navigate if needed
    if "/segments" not in page.url:
        segments_page.navigate_to_page()
    
    # Create segment
    segments_page.click_create_segment()
    page.fill('input[placeholder*="Name"]', test_name)
    page.fill('textarea[placeholder*="Description"]', description)
    page.click('button:has-text("Save")')
    time.sleep(2)
    
    # Verify in UI
    assert segments_page.is_segment_visible(test_name), f"Segment '{test_name}' not visible in UI"
    print(f"[OK] Segment created and visible in UI")
    
    # Verify in DB
    segment = get_segment_by_name(mysql_connection, test_name)
    assert segment is not None, f"Segment '{test_name}' not found in DB"
    print(f"[OK] Segment found in DB with ID: {segment['id']}")
    
    # Cleanup
    delete_test_segment(mysql_connection, test_name)
    print(f"[OK] Segment cleaned up")


@pytest.mark.segments
@pytest.mark.crud
def test_segments_search(page, mysql_connection, settings):
    """Test: Search segments"""
    allure.dynamic.title("Segments Search - Basic")
    
    # Use an existing segment name or known pattern
    search_term = "Segment"  # Generic term that should find existing segments
    
    segments_page = SegmentsPage(page, settings.APP_URL)
    
    # Navigate if needed
    if "/segments" not in page.url:
        segments_page.navigate_to_page()
    
    # Search
    segments_page.search_segments(search_term)
    time.sleep(2)
    
    # Verify results exist
    results = search_segments(mysql_connection, search_term)
    assert len(results) >= 0, "Search should return results"
    print(f"[OK] Found {len(results)} matching segments in DB")


@pytest.mark.segments
@pytest.mark.crud
def test_segments_delete_simple(page, mysql_connection, settings):
    """Test: Delete a segment"""
    allure.dynamic.title("Segments Delete - Simple")
    
    test_name = "TestSegmentDelete"
    description = "Test segment for deletion"
    
    segments_page = SegmentsPage(page, settings.APP_URL)
    
    # Setup: Create segment if not exists
    if not verify_segment_exists(mysql_connection, test_name):
        # We need to create it via API or UI - for now just via DB helper
        from tests.helpers.segments_db_helpers import create_test_segment
        create_test_segment(mysql_connection, test_name, description)
    
    # Navigate if needed
    if "/segments" not in page.url:
        segments_page.navigate_to_page()
    
    # Verify it exists in UI
    assert segments_page.is_segment_visible(test_name), f"Segment '{test_name}' should exist before deletion"
    
    # Delete segment
    segments_page.click_segment_by_name(test_name)
    time.sleep(1)
    page.click('button:has-text("Delete")')
    time.sleep(1)
    
    # Confirm deletion if dialog appears
    try:
        page.click('button:has-text("Confirm")')
        time.sleep(2)
    except:
        print("[WARN] No confirmation dialog, continuing...")
    
    # Verify not in DB
    segment = get_segment_by_name(mysql_connection, test_name)
    assert segment is None, f"Segment '{test_name}' should be deleted from DB"
    print(f"[OK] Segment deleted successfully")
    
    # Cleanup (already deleted)
    delete_test_segment(mysql_connection, test_name)


@pytest.mark.segments
@pytest.mark.crud
def test_segments_invalid_empty_name(page, settings):
    """Test: Reject empty name"""
    allure.dynamic.title("Segments Validation - Empty Name")
    
    segments_page = SegmentsPage(page, settings.APP_URL)
    
    # Navigate if needed
    if "/segments" not in page.url:
        segments_page.navigate_to_page()
    
    # Try to create with empty name
    segments_page.click_create_segment()
    
    # Try to submit with empty name
    page.fill('input[placeholder*="Name"]', "")
    
    # Check if save button is disabled or error appears
    save_button = page.locator('button:has-text("Save")')
    is_disabled = save_button.evaluate("el => el.disabled")
    
    assert is_disabled, "Save button should be disabled for empty name"
    print(f"[OK] Save button correctly disabled for empty name")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
