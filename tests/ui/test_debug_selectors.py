"""
DEBUG: Inspect actual HTML structure of Segments page
Run this to see what the real selectors should be
"""
import pytest
import time
from playwright.sync_api import Page
from framework.page_objects.segments_page import SegmentsPage
from config.settings import Settings


def test_debug_inspect_html(page: Page, settings: Settings):
    """
    DEBUG TEST: Inspect the actual HTML to find correct selectors
    """
    segments_page = SegmentsPage(page, settings.APP_URL)
    segments_page.navigate_to_page()
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    
    print("\n" + "="*80)
    print("PAGE STRUCTURE DEBUG")
    print("="*80)
    
    print(f"\nCurrent URL: {page.url}\n")
    
    # List all divs
    print("DIVS WITH CLASSES:")
    divs = page.locator('div').all()
    for i, div in enumerate(divs[:50]):
        classes = div.get_attribute('class') or ''
        if classes and len(classes) > 5:
            print(f"  {i}: {classes[:100]}")
    
    # List all elements that might be cards
    print("\n\nPOTENTIAL CARD CONTAINERS:")
    
    card_selectors = [
        '[role="article"]',
        '[class*="card"]',
        '[class*="Card"]',
        '[class*="segment"]',
        '[class*="Segment"]',
        'article',
        '.segment-card',
        'div[data-testid*="segment"]',
    ]
    
    for selector in card_selectors:
        count = page.locator(selector).count()
        if count > 0:
            print(f"✅ {selector:<40} -> {count} elements")
        else:
            print(f"❌ {selector:<40} -> 0 elements")
    
    # Get page body HTML (first 2000 chars)
    print("\n\nPAGE HTML STRUCTURE (first 3000 chars):")
    print("="*80)
    body_html = page.content()[:3000]
    print(body_html)
    print("...\n")
    
    # Save full HTML to file for inspection
    html_file = "page_debug.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(page.content())
    print(f"Full page HTML saved to: {html_file}\n")
