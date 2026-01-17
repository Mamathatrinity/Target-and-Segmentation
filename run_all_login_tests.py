"""
Run all login tests in sequential order:
1. Negative test cases
2. Edge test cases
3. Positive test cases
"""

import subprocess
import sys

def run_tests(test_pattern, description):
    """Run tests matching the pattern"""
    print("\n" + "="*100)
    print(f"RUNNING: {description}")
    print("="*100)
    
    cmd = [
        sys.executable,
        "-m", "pytest",
        "tests/ui/test_login_negative.py",
        "tests/ui/test_login.py",
        "-k", test_pattern,
        "-v",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd, cwd=r"C:\Users\mv\Target_and_Segmentation_Automation")
    return result.returncode

if __name__ == "__main__":
    print("\n" + "="*100)
    print("LOGIN TEST SUITE - SEQUENTIAL EXECUTION")
    print("="*100)
    
    # Run in order
    tests = [
        ("neg_", "NEGATIVE TEST CASES"),
        ("edge_", "EDGE TEST CASES"),
        ("pos_", "POSITIVE TEST CASES")
    ]
    
    results = {}
    for pattern, description in tests:
        exit_code = run_tests(pattern, description)
        results[description] = "PASSED" if exit_code == 0 else "FAILED"
    
    # Summary
    print("\n" + "="*100)
    print("TEST EXECUTION SUMMARY")
    print("="*100)
    for description, status in results.items():
        print(f"{description}: {status}")
    print("="*100)
