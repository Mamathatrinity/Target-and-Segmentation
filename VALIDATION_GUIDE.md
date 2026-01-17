# Comprehensive Validation Guide

## 🎯 Overview

The enhanced agent framework now provides **comprehensive API + UI + DB validation** with:
- ✅ **Detailed field-level validation** for each layer
- ✅ **Clear terminal output** with ✅/❌ icons and formatted sections
- ✅ **Rich Allure reports** with JSON responses, validation summaries, screenshots
- ✅ **Cross-layer validation** comparing API vs Database data

## 📊 Terminal Output Example

```
================================================================================
  API VALIDATION - GET /api/segments
================================================================================
  HTTP Status: 200 ✅
    Expected: 200, Actual: 200

  Field Validations:
    data_exists: ✅
      Expected: True
      Actual: True
      Type: equality
    page: ✅
      Expected: 1
      Actual: 1
      Type: equality
    per_page_limit: ✅
      Expected: True
      Actual: True
      Type: equality

  ✅ All validations passed!
================================================================================

================================================================================
  DATABASE VALIDATION - SELECT_BY_ID
================================================================================
  Query: SELECT * FROM segments WHERE id = %s
  Row Count: 1 ✅
    Expected: equality 1

  Field Validations:
    Record 0, id: ✅
      Expected: 123
      Actual: 123
    Record 0, name: ✅
      Expected: Test Segment
      Actual: Test Segment

  ✅ All validations passed!
================================================================================

================================================================================
  CROSS-LAYER VALIDATION - API vs Database
================================================================================
  id: ✅
    API:  123
    DB:   123
  name: ✅
    API:  Test Segment
    DB:   Test Segment
  description: ✅
    API:  Test Description
    DB:   Test Description

  ✅ All fields match across API and Database!
================================================================================
```

## 🚀 Usage Examples

### Example 1: API Validation with Field Checks

```python
from framework.adapters import APIAdapter

api_adapter = APIAdapter(api_validator, settings)

# Get segments with automatic validation
api_result, segments, total = api_adapter.get_segments(
    page=1, 
    per_page=10,
    validate=True  # Enables comprehensive validation
)

# Automatically validates:
# - HTTP status code (200)
# - Response structure (data, total fields)
# - Pagination parameters
# - Required fields in each segment
# - Prints to terminal + Allure report

# Get specific segment with expected field values
api_result, segment = api_adapter.get_segment_by_id(
    segment_id=123,
    validate=True,
    expected_fields={
        "name": "Test Segment",
        "description": "Test Description",
        "status": "active"
    }
)

# Automatically validates:
# - HTTP 200 status
# - ID matches
# - Required fields exist (name, description)
# - Field types are correct
# - Each expected field value matches
```

### Example 2: Database Validation with Field Checks

```python
from framework.adapters import DBAdapter

db_adapter = DBAdapter(mysql_connection)

# Get segment with field validation
db_result, segment = db_adapter.get_segment_by_id(
    segment_id=123,
    validate=True,
    expected_fields={
        "name": "Test Segment",
        "status": "active"
    }
)

# Automatically validates:
# - Query executed successfully
# - Exactly 1 record returned
# - ID matches
# - Required fields exist
# - Each expected field value matches
# - Prints to terminal + Allure report
```

### Example 3: UI Validation with Element Checks

```python
from framework.adapters import UIAdapter

ui_adapter = UIAdapter(page, SegmentsPage)

# Validate page with elements and content
ui_result = ui_adapter.validate_page(
    page_name="Segments List",
    element_checks=[
        {"name": "Page Title", "selector": "h1"},
        {"name": "Table", "selector": "table"},
        {"name": "Create Button", "selector": ".btn-create"}
    ],
    content_checks=[
        {"name": "Title", "selector": "h1", "expected": "Segments", "match_type": "contains"},
        {"name": "Count", "selector": ".count", "expected": "10", "match_type": "exact"}
    ]
)

# Automatically:
# - Checks all elements are visible
# - Validates text content
# - Takes screenshot
# - Prints to terminal + Allure report
```

### Example 4: Cross-Layer Validation

```python
# Compare API and Database data
cross_result = db_adapter.cross_validate_with_api(
    api_segment=api_segment,
    db_segment=db_segment,
    fields=["id", "name", "description", "status", "created_at"]
)

# Automatically:
# - Compares each field value
# - Shows API vs DB side-by-side
# - Highlights mismatches
# - Prints to terminal + Allure report

# Check if validation passed
if cross_result["overall_match"]:
    print("✅ Data consistent across layers!")
else:
    print(f"❌ Mismatches: {cross_result['errors']}")
```

## 📝 Complete Test Example

See `tests/examples/test_comprehensive_validation_example.py` for a full working example that demonstrates:
1. API validation with field checks
2. UI validation with element checks
3. Database validation with field checks
4. Cross-layer validation (API vs DB)

## 🎨 What You See in Terminal

### API Validation
- HTTP status code with ✅/❌
- Each field validation result
- Expected vs Actual values
- Validation type (equality, type, contains, etc.)
- Summary: All passed or list of errors

### Database Validation
- Query executed
- Row count validation
- Field-by-field validation per record
- Expected vs Actual values
- Summary: All passed or list of errors

### UI Validation
- Page loaded status
- Each element visibility check
- Content validation results
- Expected vs Actual text
- Summary: All passed or list of errors

### Cross-Layer Validation
- Field-by-field comparison
- API value vs DB value side-by-side
- Match status for each field
- Overall match status
- List of mismatches if any

## 📊 What You See in Allure Reports

### API Validation
- ✅ Validation summary with all checks
- 📄 Full JSON response
- 🔍 Field-by-field validation details

### Database Validation
- ✅ Validation summary with all checks
- 📄 Query details
- 📊 Sample of returned data (JSON)
- 🔍 Field-by-field validation details

### UI Validation
- ✅ Validation summary with all checks
- 📷 Screenshot of the page
- 🔍 Element and content check details

### Cross-Layer Validation
- ✅ Side-by-side comparison
- 🔄 Field matching results
- ❌ Detailed mismatch information

## 🔧 Validation Types Supported

### Field Validation Types
- `equality`: Exact match
- `type`: Type checking (int, str, etc.)
- `not_null`: Field is not None
- `contains`: String contains substring
- `greater_than`: Numeric comparison
- `less_than`: Numeric comparison
- `at_least`: Numeric >= comparison

### Match Types (UI Content)
- `exact`: Exact text match
- `contains`: Text contains expected string
- `not_empty`: Text is not empty

## 💡 Best Practices

1. **Enable validation by default** in tests:
   ```python
   api_result, data, count = api_adapter.get_segments(validate=True)
   ```

2. **Specify expected fields** for stricter validation:
   ```python
   db_result, segment = db_adapter.get_segment_by_id(
       segment_id=123,
       validate=True,
       expected_fields={"name": "Expected Name", "status": "active"}
   )
   ```

3. **Always use cross-layer validation** for critical data:
   ```python
   cross_result = db_adapter.cross_validate_with_api(
       api_segment, db_segment, 
       fields=["id", "name", "description"]
   )
   assert cross_result["overall_match"], "Data mismatch!"
   ```

4. **Check validation results** in code:
   ```python
   if api_result.errors:
       print(f"API validation failed: {api_result.errors}")
   ```

## 🎯 Benefits

✅ **Comprehensive** - All 3 layers validated (API, UI, DB)  
✅ **Detailed** - Field-level validation with clear output  
✅ **Terminal Visible** - See results immediately during test run  
✅ **Report Rich** - Allure shows full details with JSON/screenshots  
✅ **Easy to Use** - Single parameter `validate=True`  
✅ **Consistent** - Same validation pattern across all layers  
✅ **Cross-Validated** - Compare data across layers automatically  

---

**All validation results are shown in BOTH terminal output AND Allure reports!** 🎉
