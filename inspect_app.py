"""
Simple App Inspector - List all form elements on Segments page
"""
from playwright.sync_api import sync_playwright
from config.settings import Settings
import time

settings = Settings()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print(f"\nOpening: {settings.APP_URL}/segments\n")
    page.goto(f"{settings.APP_URL}/segments")
    time.sleep(5)
    
    print("="*80)
    print("INPUT FIELDS")
    print("="*80)
    inputs = page.locator('input').all()
    for i, inp in enumerate(inputs):
        if inp.is_visible():
            print(f"{i}: type={inp.get_attribute('type')} | name={inp.get_attribute('name')} | placeholder={inp.get_attribute('placeholder')}")
    
    print("\n" + "="*80)
    print("TEXTAREAS")
    print("="*80)
    textareas = page.locator('textarea').all()
    for i, ta in enumerate(textareas):
        if ta.is_visible():
            print(f"{i}: name={ta.get_attribute('name')} | placeholder={ta.get_attribute('placeholder')}")
    
    print("\n" + "="*80)
    print("BUTTONS")
    print("="*80)
    buttons = page.locator('button').all()
    for i, btn in enumerate(buttons):
        if btn.is_visible():
            text = btn.text_content().strip()
            if text:
                print(f"{i}: {text[:60]}")
    
    print("\n" + "="*80)
    print("DATA-TESTID ELEMENTS")
    print("="*80)
    divs = page.locator('[data-testid]').all()
    for i, div in enumerate(divs[:10]):
        testid = div.get_attribute('data-testid')
        print(f"{i}: {testid}")
    
    print("\nDone. Keep browser open to inspect elements manually.")
    print("Right-click any element -> Inspect -> Copy selector\n")
    browser.close()
