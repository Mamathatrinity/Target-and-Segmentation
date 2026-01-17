# Allure Integration Fix Plan for Tests 004-015

## Current Status
- Tests 001-003: ✅ Complete Allure integration
- Tests 005-007: ⚠️ Partial (missing Cross-Layer step)
- Test 004: ❌ Minimal (only API step)
- Tests 008-015: ❌ No integration

## Required Pattern (from test_001)
Each test MUST have these allure.step() blocks:

### 1. UI Validation Step
```python
with allure.step("UI Validation - [Test Specific Action]"):
    # UI actions
    screenshot = page.screenshot()
    allure.attach(screenshot, name="[Action] Screenshot", attachment_type=allure.attachment_type.PNG)
    
    ui_output = "="*80 + "\n"
    ui_output += "  UI VALIDATION\n"
    ui_output += "="*80 + "\n"
    ui_output += f"  [Key validation points]\n"
    ui_output += "="*80
    allure.attach(ui_output, name="UI Validation Summary", attachment_type=allure.attachment_type.TEXT)
```

### 2. API Validation Step
```python
with allure.step("API Validation - [API Action]"):
    import json
    # API request params
    api_params = { ... }
    allure.attach(json.dumps(api_params, indent=2), name="API Request Parameters", attachment_type=allure.attachment_type.JSON)
    
    # API call
    api_result, api_segments, api_count = call_segments_api(...)
    
    # Attach response
    allure.attach(json.dumps(api_result, indent=2), name="Full API Response", attachment_type=allure.attachment_type.JSON)
    
    # Validation summary
    api_summary = "="*80 + "\n"
    api_summary += "  API VALIDATION RESULTS\n"
    api_summary += "="*80 + "\n"
    api_summary += f"  Status Code: {api_result.get('status_code')}\n"
    api_summary += f"  [Key metrics]\n"
    api_summary += "="*80
    allure.attach(api_summary, name="API Validation Summary", attachment_type=allure.attachment_type.TEXT)
```

### 3. Database Validation Step
```python
with allure.step("Database Validation - [DB Query]"):
    db_output = "="*80 + "\n"
    db_output += "  DATABASE VALIDATION\n"
    db_output += "="*80 + "\n"
    
    if mysql_connection:
        # DB queries
        db_output += f"  Connection: Active\n"
        db_output += f"  Query: [SQL or function called]\n"
        db_output += f"  Results: [count/data]\n"
    else:
        db_output += "  Connection: Not available\n"
    
    db_output += "="*80
    allure.attach(db_output, name="Database Validation Summary", attachment_type=allure.attachment_type.TEXT)
```

### 4. Cross-Layer Validation Step
```python
with allure.step("Cross-Layer Validation - Compare UI/API/DB"):
    cross_layer = "="*80 + "\n"
    cross_layer += "  CROSS-LAYER VALIDATION\n"
    cross_layer += "="*80 + "\n"
    cross_layer += f"  UI Results:  [value]\n"
    cross_layer += f"  API Results: [value]\n"
    cross_layer += f"  DB Results:  [value]\n"
    cross_layer += f"  Consistency: [PASS/FAIL/WARN]\n"
    cross_layer += "="*80
    allure.attach(cross_layer, name="Cross-Layer Validation", attachment_type=allure.attachment_type.TEXT)
```

## Execution Plan

I will update ALL tests 004-015 with complete Allure integration using multi_replace_string_in_file in batches:

1. Batch 1: Tests 004, 005, 006, 007 (fix/complete Allure)
2. Batch 2: Tests 008, 009, 010, 011 (add full Allure)
3. Batch 3: Tests 012, 013, 014, 015 (add full Allure)

Each batch will ensure ALL 4 steps are present with proper attachments.
