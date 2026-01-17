# 🧪 COMPLETE TESTING GUIDE

## Quick Status Check
Run this first to see overall status:
```powershell
python validate_implementation.py
```

---

## Test 1: Check if Tests Are Generated ✅
**Status:** 47 tests collected successfully

```powershell
# See all collected tests
python -m pytest tests/ui/test_segments_generated.py --collect-only -q

# Expected: Shows 47 test items with markers (high, create, search, etc.)
```

---

## Test 2: Run a Single Test
**Start here to test one test case**

```powershell
# Run just one test
python -m pytest tests/ui/test_segments_generated.py::test_segments_create_valid -v

# Or run by marker
python -m pytest tests/ui/test_segments_generated.py -m high -v --maxfail=1
```

**What to look for:**
- ✅ If test PASSES → Framework is working
- ❌ If test FAILS → Read error message to identify issue

---

## Test 3: Run All Tests by Category
**Run specific test types**

```powershell
# Only CREATE tests (6 tests)
python -m pytest tests/ui/test_segments_generated.py -m create -v

# Only SEARCH tests (6 tests)
python -m pytest tests/ui/test_segments_generated.py -m search -v

# Only DELETE tests (5 tests)
python -m pytest tests/ui/test_segments_generated.py -m delete -v

# Only HIGH priority tests
python -m pytest tests/ui/test_segments_generated.py -m high -v

# Only MEDIUM priority tests
python -m pytest tests/ui/test_segments_generated.py -m medium -v

# Only LOW priority tests
python -m pytest tests/ui/test_segments_generated.py -m low -v
```

---

## Test 4: Run All Generated Tests (Full Suite)
**Run the complete test suite**

```powershell
# Run all 47 tests with output
python -m pytest tests/ui/test_segments_generated.py -v

# Run all tests and stop on first failure
python -m pytest tests/ui/test_segments_generated.py -v --maxfail=1

# Run all tests and show last 50 lines of output
python -m pytest tests/ui/test_segments_generated.py -v --tb=short
```

---

## Test 5: Generate HTML Report
**Create visual test report**

```powershell
# Generate HTML report
python -m pytest tests/ui/test_segments_generated.py -v --html=reports/test_report.html --self-contained-html

# Then open the report
Start-Process "reports/test_report.html"
```

---

## Test 6: Test Infrastructure Components
**Test individual components**

```powershell
# Test page objects
python -c "
from framework.page_objects.segments_page import SegmentsPage
print('✅ SegmentsPage imports successfully')
print(f'✅ Has {len([m for m in dir(SegmentsPage) if not m.startswith(\"_\")])} methods')
"

# Test database helpers
python -c "
from tests.helpers.segments_db_helpers import *
print('✅ All database helpers import successfully')
"

# Test API validator
python -c "
from framework.validators.api_validator import APIValidator
print('✅ APIValidator imports successfully')
"
```

---

## Test 7: Validate Framework Files
**Check if all required files exist**

```powershell
# Check critical files
$files = @(
    'framework/page_objects/segments_page.py',
    'tests/helpers/segments_db_helpers.py',
    'tests/ui/test_segments_generated.py',
    'framework/agent/test_generator.py',
    'pytest.ini'
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ $file EXISTS"
    } else {
        Write-Host "❌ $file MISSING"
    }
}
```

---

## Test 8: Run Parallel Tests (if needed)
**Test parallel execution**

```powershell
# Run tests in parallel with 4 workers
python -m pytest tests/ui/test_segments_generated.py -v -n 4

# Or let pytest auto-detect CPU cores
python -m pytest tests/ui/test_segments_generated.py -v -n auto
```

---

## Common Issues & Fixes

### ❌ Issue: "test not found"
```
Solution: Run collection first
python -m pytest tests/ui/test_segments_generated.py --collect-only
```

### ❌ Issue: "ImportError: No module named X"
```
Solution: Check requirements and install missing packages
pip install -r requirements.txt
```

### ❌ Issue: "No browser found"
```
Solution: Install Playwright browsers
playwright install
```

### ❌ Issue: "Database connection failed"
```
Solution: Check database credentials in config/settings.py
Verify MySQL is running and accessible
```

---

## Expected Results

### ✅ If Everything Works:
```
======================== 47 passed in 42.31s ========================
```

### 🔍 If Tests Fail:
- Read the error message carefully
- Look for: ConnectionError, TimeoutError, AssertionError
- Check the database and application are running
- Review the test logs for specific failures

---

## Quick Testing Sequence

**Start here and work down:**

1. **Quick Check** (5 seconds)
   ```powershell
   python validate_implementation.py
   ```
   Expected: 3/4 tests pass (parallel execution is optional)

2. **Component Check** (10 seconds)
   ```powershell
   python -c "from framework.page_objects.segments_page import SegmentsPage; print('✅ OK')"
   ```
   Expected: ✅ OK

3. **Single Test** (30 seconds)
   ```powershell
   python -m pytest tests/ui/test_segments_generated.py::test_segments_create_valid -v
   ```
   Expected: PASSED or clear error message

4. **Category Tests** (5 minutes)
   ```powershell
   python -m pytest tests/ui/test_segments_generated.py -m high -v
   ```
   Expected: 6 HIGH priority tests pass

5. **Full Suite** (30+ minutes)
   ```powershell
   python -m pytest tests/ui/test_segments_generated.py -v
   ```
   Expected: 47 tests pass

---

## Monitoring Tests

### Watch for:
✅ **GREEN** = Test passed  
❌ **RED** = Test failed  
⚠️ **YELLOW** = Test skipped  
🔵 **BLUE** = Test running  

### Check logs at:
- `allure-results/` (Allure reports)
- `reports/` (HTML reports)
- Console output (direct feedback)

---

## Advanced Testing

### Run tests with detailed output
```powershell
python -m pytest tests/ui/test_segments_generated.py -vv --tb=long
```

### Run tests and show coverage
```powershell
python -m pytest tests/ui/test_segments_generated.py --cov=tests --cov-report=html
```

### Run tests with timeout (max 60s per test)
```powershell
python -m pytest tests/ui/test_segments_generated.py -v --timeout=60
```

### Run tests and retry on failure (2 retries)
```powershell
python -m pytest tests/ui/test_segments_generated.py -v --reruns 2
```

---

## Summary

| Test | Command | Time |
|------|---------|------|
| **Validation** | `python validate_implementation.py` | 5s |
| **Single Test** | `pytest tests/ui/test_segments_generated.py::test_segments_create_valid -v` | 30s |
| **Category** | `pytest tests/ui/test_segments_generated.py -m high -v` | 3m |
| **Full Suite** | `pytest tests/ui/test_segments_generated.py -v` | 30m |

✅ **Everything is working** if tests pass without errors!
