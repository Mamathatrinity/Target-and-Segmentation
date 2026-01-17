"""
Script to remove navigation from all test cases
Replace page fixture with segments_page_loaded
"""
import re

file_path = r'c:\Users\mv\Target_and_Segmentation_Automation\tests\ui\test_segments.py'

# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update all test signatures: page -> segments_page_loaded
patterns_to_replace = [
    (r'def test_seg_sort_(\d+_\w+)\(page,', r'def test_seg_sort_\1(segments_page_loaded,'),
    (r'def test_seg_my_sort_(\d+_\w+)\(page,', r'def test_seg_my_sort_\1(segments_page_loaded,'),
    (r'def test_seg_team_sort_(\d+_\w+)\(page,', r'def test_seg_team_sort_\1(segments_page_loaded,'),
]

for old, new in patterns_to_replace:
    before_count = len(re.findall(old, content))
    content = re.sub(old, new, content)
    after_count = len(re.findall(new, content))
    print(f'✅ Updated {before_count} matches for {old}')

# 2. Remove navigation blocks and add page setup
# Pattern: Navigate to Segments page block in sorting/filter tests
nav_blocks = [
    # Basic sorting tests
    (r'(def test_seg_sort_\d+_\w+\(segments_page_loaded.*?""".*?\n)    with allure\.step\("Navigate to Segments page"\):\n        segments_page = SegmentsPage\(page, Settings\.APP_URL\)\n        segments_page\.navigate_to_page\(\)\n        time\.sleep\(2\)\n        \n',
     r'\1    page = segments_page_loaded\n    segments_page = SegmentsPage(page, Settings.APP_URL)\n    \n'),
    
    # My Segments tests  
    (r'(def test_seg_my_sort_\d+_\w+\(segments_page_loaded.*?""".*?\n)    with allure\.step\("Navigate to Segments page"\):\n        segments_page = SegmentsPage\(page, Settings\.APP_URL\)\n        segments_page\.navigate_to_page\(\)\n        time\.sleep\(2\)\n        \n',
     r'\1    page = segments_page_loaded\n    segments_page = SegmentsPage(page, Settings.APP_URL)\n    \n'),
    
    # Team Segments tests
    (r'(def test_seg_team_sort_\d+_\w+\(segments_page_loaded.*?""".*?\n)    with allure\.step\("Navigate to Segments page"\):\n        segments_page = SegmentsPage\(page, Settings\.APP_URL\)\n        segments_page\.navigate_to_page\(\)\n        time\.sleep\(2\)\n        \n',
     r'\1    page = segments_page_loaded\n    segments_page = SegmentsPage(page, Settings.APP_URL)\n    \n'),
]

for pattern, replacement in nav_blocks:
    count = len(re.findall(pattern, content, re.DOTALL))
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    print(f'✅ Removed {count} navigation blocks')

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n✅ ALL TESTS UPDATED - No more page reloads!')
