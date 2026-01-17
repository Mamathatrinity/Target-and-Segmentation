"""
Test Executor - Executes tests based on planner's strategy
Handles test execution, captures results, manages failures.
"""
import pytest
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .memory import get_memory
from .self_healing import get_healing_engine
from .app_loader import get_app_loader
from .planner import get_planner


class TestExecutor:
    """
    Executes tests based on execution plan.
    Handles test running, result capture, and failure management.
    """
    
    def __init__(self):
        self.memory = get_memory()
        self.healer = get_healing_engine()
        self.loader = get_app_loader()
        self.planner = get_planner()
        
    def execute_plan(self, plan: Dict, auto_heal: bool = True) -> Dict:
        """
        Execute a test plan created by planner.
        
        Args:
            plan: Execution plan from TestPlanner
            auto_heal: Enable automatic healing on failures
            
        Returns:
            Execution results with pass/fail counts, duration, failures
        """
        print(f"\n{'='*80}")
        print(f"▶️  EXECUTING TEST PLAN: {plan['app']}")
        print(f"{'='*80}")
        
        # Set app context
        if not self.loader.set_current_app(plan['app']):
            return {"status": "error", "error": f"Unknown app: {plan['app']}"}
        
        app = self.loader.current_app
        
        # Execute tests in planned order
        results = {
            "app": plan['app'],
            "total_tests": plan['total_tests'],
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "healed": 0,
            "test_results": [],
            "start_time": str(datetime.now()),
            "end_time": None,
            "duration": 0
        }
        
        start_time = datetime.now()
        
        for test_info in plan['execution_order']:
            test_result = self._execute_single_test(
                test_info['test_name'], 
                app, 
                auto_heal
            )
            
            results['test_results'].append(test_result)
            
            # Update counts
            if test_result['status'] == 'passed':
                results['passed'] += 1
            elif test_result['status'] == 'failed':
                results['failed'] += 1
            elif test_result['status'] == 'error':
                results['errors'] += 1
            
            if test_result.get('healed'):
                results['healed'] += 1
        
        end_time = datetime.now()
        results['end_time'] = str(end_time)
        results['duration'] = (end_time - start_time).total_seconds()
        
        self._print_summary(results)
        return results
    
    def execute_single_test(self, app_name: str, test_id: str, auto_heal: bool = True) -> Dict:
        """
        Execute a single test.
        
        Args:
            app_name: Application name
            test_id: Test identifier (e.g., 'pos_003')
            auto_heal: Enable automatic healing
            
        Returns:
            Test result dict
        """
        print(f"\n{'='*80}")
        print(f"▶️  EXECUTING: {app_name.upper()} Test {test_id}")
        print(f"{'='*80}")
        
        # Set app context
        if not self.loader.set_current_app(app_name):
            return {"status": "error", "error": f"Unknown app: {app_name}"}
        
        app = self.loader.current_app
        test_name = f"{app.test_prefix}{test_id}"
        
        return self._execute_single_test(test_name, app, auto_heal)
    
    def _execute_single_test(self, test_name: str, app, auto_heal: bool) -> Dict:
        """Internal method to execute a single test."""
        
        # Check test history
        history = self.memory.get_test_history(test_name)
        if history:
            print(f"📊 Test History: {history['total_runs']} runs, "
                  f"{history['total_passes']} passes, {history['total_failures']} failures")
        
        # Build pytest command
        test_path = f"{app.module.replace('.', '/')}.py::{test_name}"
        pytest_args = [
            test_path,
            "-v",
            "--alluredir=allure-results",
            "--tb=short",
            "-s"  # Show print statements
        ]
        
        # Execute test
        start_time = datetime.now()
        exit_code = pytest.main(pytest_args)
        duration = (datetime.now() - start_time).total_seconds()
        
        # Build result
        result = {
            "test_name": test_name,
            "status": "passed" if exit_code == 0 else "failed",
            "duration": duration,
            "exit_code": exit_code,
            "healed": False,
            "timestamp": str(datetime.now())
        }
        
        # Handle failure
        if result['status'] == 'failed':
            print(f"\n❌ TEST FAILED in {duration:.2f}s")
            
            if auto_heal:
                print(f"\n🔧 Attempting auto-heal...")
                healed = self._attempt_heal(test_name, app.name)
                result['healed'] = healed
                
                if healed:
                    # Re-run test after healing
                    print(f"\n🔄 Re-running test after healing...")
                    rerun_start = datetime.now()
                    exit_code = pytest.main(pytest_args)
                    rerun_duration = (datetime.now() - rerun_start).total_seconds()
                    
                    if exit_code == 0:
                        result['status'] = 'passed'
                        result['duration'] += rerun_duration
                        print(f"\n✅ TEST PASSED AFTER HEALING in {rerun_duration:.2f}s")
                    else:
                        print(f"\n❌ Test still failing after healing")
        else:
            print(f"\n✅ TEST PASSED in {duration:.2f}s")
        
        # Record result
        self.memory.record_test_result(
            test_name=result['test_name'],
            passed=(result['status'] == 'passed'),
            duration=result['duration']
        )
        
        return result
    
    def _attempt_heal(self, test_name: str, app_name: str) -> bool:
        """
        Attempt to auto-heal a failing test.
        
        Returns:
            True if healing was successful, False otherwise
        """
        # In real implementation, would:
        # 1. Capture error details
        # 2. Detect pattern using self.healer
        # 3. Apply auto-fix if available
        # 4. Return success status
        
        # For now, simplified
        print(f"   Checking for known patterns...")
        
        # Check if we have a fix for this test
        bug_fixes = self.memory.memory_data.get("bug_fixes", [])
        for fix in bug_fixes:
            if test_name in fix.get("affected_tests", []):
                print(f"   ℹ️  Test was previously fixed: {fix['description']}")
                return False  # Already fixed, shouldn't fail
        
        print(f"   ⚠️  No auto-fix available for this test")
        return False
    
    def _print_summary(self, results: Dict):
        """Print execution summary."""
        print(f"\n{'='*80}")
        print(f"📊 EXECUTION SUMMARY")
        print(f"{'='*80}")
        print(f"App: {results['app']}")
        print(f"Total Tests: {results['total_tests']}")
        print(f"✅ Passed: {results['passed']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"⚠️  Errors: {results['errors']}")
        print(f"🔧 Healed: {results['healed']}")
        print(f"Duration: {results['duration']:.2f}s ({results['duration']/60:.1f} min)")
        
        pass_rate = (results['passed'] / results['total_tests'] * 100) if results['total_tests'] > 0 else 0
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if results['failed'] > 0:
            print(f"\nFailed Tests:")
            for test in results['test_results']:
                if test['status'] == 'failed':
                    healed_marker = " (healed attempted)" if test.get('healed') else ""
                    print(f"  ❌ {test['test_name']}{healed_marker}")
        
        print(f"{'='*80}\n")


_executor_instance = None

def get_executor() -> TestExecutor:
    """Get singleton executor instance."""
    global _executor_instance
    if _executor_instance is None:
        _executor_instance = TestExecutor()
    return _executor_instance
