"""Restore navigation blocks for original tests only"""
fp = r'c:\Users\mv\Target_and_Segmentation_Automation\tests\ui\test_segments.py'
c = open(fp, 'r', encoding='utf-8').read()

# For all test_seg_pos_* tests, change back from:
# page = segments_page_loaded
# segments_page = SegmentsPage(page, Settings.APP_URL)
# 
# To:
# with allure.step("Navigate to Segments page"):
#     segments_page = SegmentsPage(page, Settings.APP_URL)
#     segments_page.navigate_to_page()
#     time.sleep(2)
#     

import re

# Pattern: Find test_seg_pos functions that have page = segments_page_loaded
pattern = r'(def test_seg_pos_\d+.*?\n.*?""".*?""")\n    page = segments_page_loaded\n    segments_page = SegmentsPage\(page, Settings\.APP_URL\)\n    \n'

replacement = r'\1\n    with allure.step("Navigate to Segments page"):\n        segments_page = SegmentsPage(page, Settings.APP_URL)\n        segments_page.navigate_to_page()\n        time.sleep(2)\n        \n'

count = len(re.findall(pattern, c, re.DOTALL))
c = re.sub(pattern, replacement, c, flags=re.DOTALL)

print(f'✅ Restored navigation for {count} original tests')

open(fp, 'w', encoding='utf-8').write(c)
