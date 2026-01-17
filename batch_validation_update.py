"""
Batch update script to add API + DB validation to all remaining sorting tests
"""

# Simplified validation template for remaining tests
validation_template = '''
    with allure.step("📡 API Validation"):
        api_result = call_segments_api(api_validator, {api_params}, per_page=100)
        api_count = len(extract_api_segments(api_result))
        print(f"\\n📡 API: {{api_count}}")
        
    with allure.step("🗄️ DB Validation"):
        db_count = len({db_helper})
        print(f"\\n🗄️ DB: {{db_count}}")
        
    with allure.step("✅ Cross-Layer Validation"):
        match = print_validation_summary(ui_count, api_count, db_count, "{test_name}")
        assert match, f"Count mismatch! UI={{ui_count}}, API={{api_count}}, DB={{db_count}}"
'''

remaining_tests = {
    "test_seg_my_sort_003_date_asc": {"filter": "my", "sort": "created_at", "order": "asc"},
    "test_seg_my_sort_004_date_desc": {"filter": "my", "sort": "created_at", "order": "desc"},
    "test_seg_my_sort_005_creator_asc": {"filter": "my", "sort": "created_by", "order": "asc"},
    "test_seg_my_sort_006_creator_desc": {"filter": "my", "sort": "created_by", "order": "desc"},
    "test_seg_team_sort_001_name_asc": {"filter": "team", "sort": "name", "order": "asc"},
    "test_seg_team_sort_002_name_desc": {"filter": "team", "sort": "name", "order": "desc"},
    "test_seg_team_sort_003_date_asc": {"filter": "team", "sort": "created_at", "order": "asc"},
    "test_seg_team_sort_004_date_desc": {"filter": "team", "sort": "created_at", "order": "desc"},
    "test_seg_team_sort_005_creator_asc": {"filter": "team", "sort": "created_by", "order": "asc"},
    "test_seg_team_sort_006_creator_desc": {"filter": "team", "sort": "created_by", "order": "desc"},
}

print(f"✅ COMPLETED (16/26 tests have full validation):")
print("   - 5 Search tests")
print("   - 7 Basic sorting tests")  
print("   - 2 My Segments tests")
print("   - 2 My Segments + sort tests (partial)")
print()
print(f"⏳ REMAINING: {len(remaining_tests)} tests need API + DB validation")
for test in remaining_tests:
    print(f"   - {test}")
print()
print("I'll update these now using manual edits...")
