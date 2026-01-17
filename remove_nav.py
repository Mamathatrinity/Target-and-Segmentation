fp = r'c:\Users\mv\Target_and_Segmentation_Automation\tests\ui\test_segments.py'
c = open(fp, 'r', encoding='utf-8').read()

# Remove navigation blocks - replace with page setup
nav_block = '''    with allure.step("Navigate to Segments page"):
        segments_page = SegmentsPage(page, Settings.APP_URL)
        segments_page.navigate_to_page()
        time.sleep(2)
        
'''

replacement = '''    page = segments_page_loaded
    segments_page = SegmentsPage(page, Settings.APP_URL)
    
'''

before_count = c.count(nav_block)
c = c.replace(nav_block, replacement)
after_count = c.count(nav_block)

open(fp, 'w', encoding='utf-8').write(c)
print(f'✅ Removed {before_count - after_count} navigation blocks')
print(f'Remaining: {after_count}')
