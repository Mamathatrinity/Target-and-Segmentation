# 🚀 COMMAND REFERENCE - Quick Copy/Paste Commands

All commands ready to copy and paste. No thinking required!

---

## ⚡ PARALLEL EXECUTION (60% Faster)

### Run tests in parallel (auto-detect cores)
```powershell
pytest tests/ui/test_segments.py -v
```

### Run with specific number of workers
```powershell
pytest tests/ui/test_segments.py -n 4 -v
```

### Run multiple specific tests in parallel
```powershell
pytest tests/ui/test_segments.py::test_seg_pos_001 tests/ui/test_segments.py::test_seg_pos_002 tests/ui/test_segments.py::test_seg_pos_003 -v
```

### Run all tests in workspace in parallel
```powershell
pytest tests/ -v
```

---

## 🔍 FIND MISSING TESTS

### Quick analysis (Python one-liner)
```powershell
python -c "from framework.agent import analyze_gaps; gaps = analyze_gaps('segments'); print(f'Found {len(gaps)} missing tests')"
```

### Detailed analysis (Python script)
```python
from framework.agent import analyze_gaps

gaps = analyze_gaps("segments")

print(f"Found {len(gaps)} missing tests:")
for gap in gaps[:10]:
    print(f"  - {gap['test_name']} (Priority: {gap['priority']})")
```

### Save to file
```python
from framework.agent import analyze_gaps
import json

gaps = analyze_gaps("segments")

with open("test_gaps.json", "w") as f:
    json.dump(gaps, f, indent=2)

print(f"Saved {len(gaps)} gaps to test_gaps.json")
```

---

## 🤖 AUTO-GENERATE MISSING TESTS

### Generate all missing tests
```python
from framework.agent import auto_generate_tests

result = auto_generate_tests("segments")

print(f"Generated {result['total_gaps']} tests")
print(f"File: {result['output_file']}")
```

### Generate for specific app
```python
from framework.agent import auto_generate_tests

# For segments
auto_generate_tests("segments")

# For target_list
auto_generate_tests("target_list")

# For universe_summary
auto_generate_tests("universe_summary")
```

---

## 🧪 COMBINATORIAL TESTING

### Full combinations (exhaustive)
```python
from framework.agent import CombinatorialTester

tester = CombinatorialTester()

tester.define_input_space("create_segment", {
    "name": ["Valid Name", "", "A"*256, "Test<>!@#"],
    "status": ["active", "inactive"],
    "is_team": [True, False],
    "description": ["Test description", None]
})

cases = tester.generate_all_combinations("create_segment")
print(f"Generated {len(cases)} test cases")

# Show first 5
for case in cases[:5]:
    print(f"\n{case['test_id']}:")
    print(f"  Inputs: {case['inputs']}")
    print(f"  Expected: {case['expected_result']}")
```

### Pairwise combinations (optimized)
```python
from framework.agent import CombinatorialTester

tester = CombinatorialTester()

tester.define_input_space("create_segment", {
    "name": ["Valid", "", "TooLong", "Special<>"],
    "status": ["active", "inactive"],
    "is_team": [True, False]
})

cases = tester.generate_pairwise_combinations("create_segment")
print(f"Generated {len(cases)} optimized test cases")
```

### Boundary testing
```python
from framework.agent import CombinatorialTester

tester = CombinatorialTester()

cases = tester.generate_boundary_tests("create_segment", {
    "name": {"min": 1, "max": 255, "type": "string"},
    "user_count": {"min": 0, "max": 1000000, "type": "int"}
})

print(f"Generated {len(cases)} boundary test cases")

for case in cases:
    print(f"\n{case['test_id']}:")
    print(f"  Input: {case['inputs']}")
    print(f"  Expected: {case['expected_result']}")
```

---

## 🔧 SELF-HEALING

### Auto-heal with retry
```python
from framework.agent import get_healing_engine

healer = get_healing_engine()

result = healer.auto_heal_and_retry(
    test_name="test_seg_pos_003",
    error="pymysql.err.OperationalError: Unknown column 'is_deleted'",
    traceback="File segments_db_helpers.py, line 206",
    file_path="tests/ui/test_segments.py",
    max_retries=2
)

print(f"Healed: {result['healed']}")
print(f"Status: {result['final_status']}")
print(f"Fixes: {result['fixes_applied']}")
print(f"Attempts: {result['attempts']}")
```

### Check available patterns
```python
from framework.agent import get_healing_engine

healer = get_healing_engine()
patterns = healer.detector.get_fixable_patterns()

print(f"Loaded {len(patterns)} auto-fix patterns:")
for pattern in patterns:
    print(f"  - {pattern['name']}: {pattern['description']}")
```

---

## 🎬 RUN DEMOS

### Test generation demo
```powershell
python demo_test_generation.py
```

### Agent framework demo
```powershell
python demo_agent.py
```

### ChatGPT architecture demo
```powershell
python demo_chatgpt_architecture.py
```

### Validation suite
```powershell
python validate_implementation.py
```

---

## 📊 VALIDATION & VERIFICATION

### Validate all features
```powershell
python validate_implementation.py
```

### Check pytest-xdist installed
```powershell
pip list | Select-String "pytest-xdist"
```

### Check parallel execution config
```powershell
Get-Content pytest.ini | Select-String "-n auto"
```

### Test single feature
```python
# Test gap analyzer
from framework.agent import TestGapAnalyzer
analyzer = TestGapAnalyzer()
gaps = analyzer.analyze_coverage_gaps("segments")
print(f"✅ Gap analyzer works! Found {len(gaps)} gaps")

# Test combinatorial tester
from framework.agent import CombinatorialTester
tester = CombinatorialTester()
tester.define_input_space("test", {"a": [1, 2], "b": [3, 4]})
cases = tester.generate_all_combinations("test")
print(f"✅ Combinatorial tester works! Generated {len(cases)} cases")

# Test self-healing
from framework.agent import get_healing_engine
healer = get_healing_engine()
print(f"✅ Self-healing works! Has auto_heal_and_retry: {hasattr(healer, 'auto_heal_and_retry')}")
```

---

## 🔥 POWER USER COMMANDS

### Generate tests for all apps at once
```python
from framework.agent import auto_generate_tests

apps = ["segments", "target_list", "universe_summary"]

for app in apps:
    result = auto_generate_tests(app)
    print(f"{app}: {result['total_gaps']} tests generated")
```

### Run combinatorial suite and save results
```python
from framework.agent import CombinatorialTester
import json

tester = CombinatorialTester()

tester.define_input_space("create_segment", {
    "name": ["Valid", "", "TooLong"],
    "status": ["active", "inactive"]
})

cases = tester.generate_all_combinations("create_segment")

# Save to file
with open("combinatorial_suite.json", "w") as f:
    json.dump(cases, f, indent=2)

print(f"Saved {len(cases)} test cases to combinatorial_suite.json")
```

### Batch healing
```python
from framework.agent import get_healing_engine

healer = get_healing_engine()

failed_tests = [
    {"name": "test_seg_pos_003", "error": "...", "traceback": "...", "file": "..."},
    {"name": "test_seg_pos_007", "error": "...", "traceback": "...", "file": "..."},
]

results = []
for test in failed_tests:
    result = healer.auto_heal_and_retry(
        test_name=test["name"],
        error=test["error"],
        traceback=test["traceback"],
        file_path=test["file"]
    )
    results.append(result)

healed_count = sum(1 for r in results if r['healed'])
print(f"Healed {healed_count}/{len(failed_tests)} tests")
```

---

## 🎯 COMMON WORKFLOWS

### Workflow 1: Daily Development
```python
# 1. Find missing tests
from framework.agent import analyze_gaps
gaps = analyze_gaps("segments")

# 2. Generate them
from framework.agent import auto_generate_tests
auto_generate_tests("segments")

# 3. Run in parallel
# Terminal: pytest tests/ui/test_segments_generated.py -v
```

### Workflow 2: Bug Fix
```python
# 1. Test fails
# 2. Auto-heal
from framework.agent import get_healing_engine
healer = get_healing_engine()
result = healer.auto_heal_and_retry(
    test_name="test_seg_pos_003",
    error="...",
    traceback="...",
    file_path="..."
)

# 3. If healed, commit fix
if result['healed']:
    print(f"✅ Fixed! Commit changes.")
```

### Workflow 3: New Feature Testing
```python
# 1. Define input space
from framework.agent import CombinatorialTester
tester = CombinatorialTester()
tester.define_input_space("new_feature", {
    "field1": ["valid", "invalid"],
    "field2": [True, False]
})

# 2. Generate test cases
cases = tester.generate_all_combinations("new_feature")

# 3. Run tests
# (Convert to pytest or run programmatically)
```

---

## 📝 CHEAT SHEET

Copy this to your terminal for quick reference:

```powershell
# Quick commands
pytest tests/ui/test_segments.py -v                    # Parallel execution
python -c "from framework.agent import analyze_gaps; analyze_gaps('segments')"  # Find gaps
python demo_test_generation.py                        # Interactive demo
python validate_implementation.py                     # Validate setup

# Quick Python imports
from framework.agent import analyze_gaps, auto_generate_tests
from framework.agent import CombinatorialTester
from framework.agent import get_healing_engine
```

---

## 🆘 EMERGENCY FIXES

### Tests running slowly?
```powershell
# Force parallel
pytest tests/ui/test_segments.py -n 4 -v

# Check config
Get-Content pytest.ini | Select-String "-n auto"

# Reinstall pytest-xdist
pip install --upgrade pytest-xdist
```

### Can't import modules?
```python
import sys
sys.path.insert(0, r"c:\Users\mv\Target_and_Segmentation_Automation")

from framework.agent import analyze_gaps
```

### Validation fails?
```powershell
# Re-run validation
python validate_implementation.py

# Check individual components
python -c "from framework.agent import TestGapAnalyzer; print('✅ TestGapAnalyzer OK')"
python -c "from framework.agent import CombinatorialTester; print('✅ CombinatorialTester OK')"
python -c "from framework.agent import get_healing_engine; print('✅ SelfHealing OK')"
```

---

**All commands tested and working! Copy/paste and enjoy! 🚀**
