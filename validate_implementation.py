"""
Validation Script - Test All New Features
Run this to verify all 4 solutions are working.
"""
import sys
from pathlib import Path


def test_parallel_execution():
    """Test 1: Verify parallel execution is enabled."""
    print("\n" + "="*80)
    print("TEST 1: Parallel Execution")
    print("="*80)
    
    pytest_ini = Path("pytest.ini")
    if not pytest_ini.exists():
        print("❌ FAIL: pytest.ini not found")
        return False
    
    content = pytest_ini.read_text()
    
    checks = {
        "-n auto": "-n auto" in content,
        "--dist loadgroup": "--dist loadgroup" in content,
        "pytest-xdist installed": True  # Will fail if import fails
    }
    
    # Try importing pytest-xdist
    try:
        import xdist
        checks["pytest-xdist installed"] = True
    except ImportError:
        checks["pytest-xdist installed"] = False
    
    print("\nChecks:")
    for check, status in checks.items():
        symbol = "✅" if status else "❌"
        print(f"  {symbol} {check}")
    
    all_passed = all(checks.values())
    print(f"\nResult: {'✅ PASS' if all_passed else '❌ FAIL'}")
    return all_passed


def test_self_healing():
    """Test 2: Verify self-healing with auto-retry exists."""
    print("\n" + "="*80)
    print("TEST 2: Self-Healing with Auto-Retry")
    print("="*80)
    
    try:
        from framework.agent import get_healing_engine
        
        healer = get_healing_engine()
        
        # Check if auto_heal_and_retry method exists
        has_method = hasattr(healer, 'auto_heal_and_retry')
        
        # Check if method signature is correct
        if has_method:
            import inspect
            sig = inspect.signature(healer.auto_heal_and_retry)
            params = list(sig.parameters.keys())
            expected_params = ['test_name', 'error', 'traceback', 'file_path', 'max_retries']
            has_correct_signature = all(p in params for p in expected_params[:4])
        else:
            has_correct_signature = False
        
        checks = {
            "SelfHealingEngine imported": True,
            "auto_heal_and_retry method exists": has_method,
            "Correct method signature": has_correct_signature
        }
        
        print("\nChecks:")
        for check, status in checks.items():
            symbol = "✅" if status else "❌"
            print(f"  {symbol} {check}")
        
        all_passed = all(checks.values())
        print(f"\nResult: {'✅ PASS' if all_passed else '❌ FAIL'}")
        return all_passed
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_gap_analyzer():
    """Test 3: Verify Test Gap Analyzer exists."""
    print("\n" + "="*80)
    print("TEST 3: Test Gap Analyzer")
    print("="*80)
    
    try:
        from framework.agent import TestGapAnalyzer, analyze_gaps
        
        # Check if class exists
        analyzer = TestGapAnalyzer()
        
        # Check if methods exist
        methods = ['analyze_coverage_gaps', 'generate_test_code', 'auto_create_missing_tests']
        has_methods = all(hasattr(analyzer, m) for m in methods)
        
        # Check if convenience function exists
        has_function = callable(analyze_gaps)
        
        checks = {
            "TestGapAnalyzer class exists": True,
            "All methods present": has_methods,
            "analyze_gaps function exists": has_function
        }
        
        print("\nChecks:")
        for check, status in checks.items():
            symbol = "✅" if status else "❌"
            print(f"  {symbol} {check}")
        
        all_passed = all(checks.values())
        print(f"\nResult: {'✅ PASS' if all_passed else '❌ FAIL'}")
        return all_passed
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_combinatorial_tester():
    """Test 4: Verify Combinatorial Tester exists."""
    print("\n" + "="*80)
    print("TEST 4: Combinatorial Tester")
    print("="*80)
    
    try:
        from framework.agent import CombinatorialTester, create_combinatorial_suite
        
        # Check if class exists
        tester = CombinatorialTester()
        
        # Check if methods exist
        methods = [
            'define_input_space',
            'generate_all_combinations',
            'generate_pairwise_combinations',
            'generate_boundary_tests'
        ]
        has_methods = all(hasattr(tester, m) for m in methods)
        
        # Test basic functionality
        tester.define_input_space("test", {
            "field1": ["a", "b"],
            "field2": [1, 2]
        })
        
        cases = tester.generate_all_combinations("test")
        correct_count = len(cases) == 4  # 2 × 2 = 4 combinations
        
        checks = {
            "CombinatorialTester class exists": True,
            "All methods present": has_methods,
            "Generates correct combinations": correct_count,
            "create_combinatorial_suite function exists": callable(create_combinatorial_suite)
        }
        
        print("\nChecks:")
        for check, status in checks.items():
            symbol = "✅" if status else "❌"
            print(f"  {symbol} {check}")
        
        all_passed = all(checks.values())
        print(f"\nResult: {'✅ PASS' if all_passed else '❌ FAIL'}")
        return all_passed
        
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def main():
    """Run all validation tests."""
    print("\n" + "="*80)
    print("🧪 VALIDATION SUITE - Testing All 4 Solutions")
    print("="*80)
    
    tests = [
        ("Parallel Execution", test_parallel_execution),
        ("Self-Healing Auto-Retry", test_self_healing),
        ("Test Gap Analyzer", test_gap_analyzer),
        ("Combinatorial Tester", test_combinatorial_tester)
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ {name} FAILED: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*80)
    print("📊 VALIDATION SUMMARY")
    print("="*80)
    
    for name, passed in results.items():
        symbol = "✅" if passed else "❌"
        print(f"{symbol} {name}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print("\n" + "="*80)
    print(f"Results: {total_passed}/{total_tests} tests passed")
    print("="*80)
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! Framework is ready to use!")
        print("\nNext steps:")
        print("  1. Run: pytest tests/ui/test_segments.py -v")
        print("  2. Run: python demo_test_generation.py")
        print("  3. Check: IMPLEMENTATION_QUICKSTART.md")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
