import re

with open('tests/ui/test_segments.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Count steps per test
tests = {}
for i in range(1, 16):
    test_num = f'{i:03d}'
    
    # Test 001 has different name
    if i == 1:
        test_name = f'test_seg_pos_{test_num}_view_segments_list'
    else:
        test_name = f'test_seg_pos_{test_num}'
    
    # Find test boundaries
    test_start = content.find(f'def {test_name}(')
    if test_start == -1:
        continue
    
    # Find next function
    next_match = re.search(r'\ndef (test_|@pytest\.mark)', content[test_start+10:])
    test_end = test_start + 10 + next_match.start() if next_match else len(content)
    test_body = content[test_start:test_end]
    
    # Count Allure steps (including variations)
    ui_count = test_body.count('with allure.step("UI Validation')
    api_count = test_body.count('with allure.step("API Validation')
    db_count = test_body.count('with allure.step("Database Validation') + test_body.count('with allure.step("Database Validation')
    cross_count = test_body.count('with allure.step("Cross-Layer') # Will match "Cross-Layer Validation" or "Cross-Layer Data Validation"
    
    # Count attachments
    png_count = test_body.count('allure.attachment_type.PNG')
    json_count = test_body.count('allure.attachment_type.JSON')
    text_count = test_body.count('allure.attachment_type.TEXT')
    
    tests[test_num] = {
        'ui': ui_count, 'api': api_count, 'db': db_count, 'cross': cross_count,
        'png': png_count, 'json': json_count, 'text': text_count
    }

print('='*80)
print('ALLURE INTEGRATION VERIFICATION - ALL 15 TESTS')
print('='*80)
print(f"{'Test':<8} {'UI':<5} {'API':<5} {'DB':<5} {'Cross':<7} {'Attach':<12} {'Status':<10}")
print('-'*80)

complete_count = 0
for test_num in sorted(tests.keys()):
    t = tests[test_num]
    complete = all([t['ui'] >= 1, t['api'] >= 1, t['db'] >= 1, t['cross'] >= 1])
    status = '✅ COMPLETE' if complete else '❌ MISSING'
    if complete:
        complete_count += 1
    
    attach = f"P:{t['png']} J:{t['json']} T:{t['text']}"
    print(f"{test_num:<8} {t['ui']:<5} {t['api']:<5} {t['db']:<5} {t['cross']:<7} {attach:<12} {status}")

print('='*80)
print(f'SUMMARY: {complete_count}/15 tests have complete Allure integration (4 steps each)')
print('='*80)

if complete_count == 15:
    print('\n✅ SUCCESS: All 15 tests have complete Allure integration!')
else:
    print(f'\n❌ INCOMPLETE: {15 - complete_count} test(s) still need work')
