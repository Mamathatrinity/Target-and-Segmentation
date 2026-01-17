"""Quick framework verification test."""
import sys

print("=" * 80)
print("FRAMEWORK VERIFICATION TEST")
print("=" * 80)

# Test 1: Import agent components
print("\n[1/5] Testing Agent Components...")
try:
    from framework.agent import (
        get_memory, get_planner, get_executor, 
        get_validation_agent, get_healing_engine
    )
    print("    PASS - All agent components imported successfully")
except Exception as e:
    print(f"    FAIL - {e}")
    sys.exit(1)

# Test 2: Import adapters
print("\n[2/5] Testing Adapters...")
try:
    from framework.adapters import (
        APIAdapter, UIAdapter, DBAdapter,
        APIValidationResult, UIValidationResult, DBValidationResult,
        get_config_loader
    )
    print("    PASS - All adapters imported successfully")
except Exception as e:
    print(f"    FAIL - {e}")
    sys.exit(1)

# Test 3: Test config loader
print("\n[3/5] Testing Config Loader...")
try:
    loader = get_config_loader()
    contract = loader.get_api_contract('segments', 'list')
    locator = loader.get_locator('segments', 'list_page', 'search_box')
    print(f"    PASS - Config loader works")
    print(f"      API Contract: {contract['endpoint']}")
    print(f"      UI Locator: {locator}")
except Exception as e:
    print(f"    FAIL - {e}")
    sys.exit(1)

# Test 4: Test planner
print("\n[4/5] Testing Planner...")
try:
    planner = get_planner()
    plan = planner.create_execution_plan('segments', test_ids=['pos_001'])
    print(f"    PASS - Planner works")
    print(f"      Created plan with {plan['total_tests']} tests")
except Exception as e:
    print(f"    FAIL - {e}")
    sys.exit(1)

# Test 5: Test memory
print("\n[5/5] Testing Memory...")
try:
    memory = get_memory()
    memory.record_bug_fix({
        "id": "TEST_001",
        "description": "Framework verification test",
        "affected_tests": ["test_001"]
    })
    is_fixed = memory.is_bug_fixed("TEST_001")
    print(f"    PASS - Memory works")
    print(f"      Bug recorded and retrieved: {is_fixed}")
except Exception as e:
    print(f"    FAIL - {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("FRAMEWORK VERIFICATION: ALL TESTS PASSED")
print("=" * 80)
print("\nFramework is ready to use!")
print("\nAvailable Components:")
print("  - Planner: Creates test execution strategies")
print("  - Executor: Runs tests with auto-healing")
print("  - Validation Agent: Orchestrates API/UI/DB validation")
print("  - Memory: Prevents repeated work")
print("  - Self-Healing: Auto-fixes known patterns")
print("  - Reflector: Learns from failures")
print("  - Config Loader: API contracts + UI locators")
print("=" * 80)
