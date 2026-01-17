"""
Test Planner - Plans test execution strategy
Analyzes dependencies, prioritizes tests, creates execution plan.
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from .memory import get_memory
from .app_loader import get_app_loader


class TestPlanner:
    """
    Plans test execution based on:
    - Test dependencies
    - Historical pass/fail rates
    - Data requirements
    - Priority levels
    """
    
    def __init__(self):
        self.memory = get_memory()
        self.loader = get_app_loader()
        
    def create_execution_plan(self, app_name: str, test_ids: Optional[List[str]] = None) -> Dict:
        """
        Create execution plan for tests.
        
        Args:
            app_name: Application to test (segments, target_list, etc.)
            test_ids: Specific tests to run, or None for all
            
        Returns:
            Execution plan with test order, dependencies, data needs
        """
        print(f"\n📋 Creating execution plan for {app_name}...")
        
        # Set app context
        if not self.loader.set_current_app(app_name):
            return {"status": "error", "error": f"Unknown app: {app_name}"}
        
        app = self.loader.current_app
        
        # Get all tests if not specified
        if not test_ids:
            test_ids = self._discover_all_tests(app)
        
        # Analyze each test
        test_analysis = []
        for test_id in test_ids:
            test_name = f"{app.test_prefix}{test_id}"
            analysis = self._analyze_test(test_name, app_name)
            test_analysis.append(analysis)
        
        # Determine execution order
        ordered_tests = self._prioritize_tests(test_analysis)
        
        # Identify data requirements
        data_requirements = self._identify_data_needs(ordered_tests, app)
        
        # Create final plan
        plan = {
            "app": app_name,
            "total_tests": len(ordered_tests),
            "execution_order": ordered_tests,
            "data_requirements": data_requirements,
            "estimated_duration": self._estimate_duration(ordered_tests),
            "risk_level": self._assess_risk(ordered_tests),
            "created_at": str(datetime.now())
        }
        
        self._print_plan(plan)
        return plan
    
    def _analyze_test(self, test_name: str, app_name: str) -> Dict:
        """Analyze individual test for planning."""
        history = self.memory.get_test_history(test_name)
        
        analysis = {
            "test_name": test_name,
            "app": app_name,
            "priority": "normal",
            "risk": "low",
            "dependencies": [],
            "data_needs": [],
            "estimated_duration": 30.0  # Default 30 seconds
        }
        
        if history:
            # Calculate pass rate
            pass_rate = history["total_passes"] / history["total_runs"] if history["total_runs"] > 0 else 0
            
            # Determine risk level
            if pass_rate < 0.5:
                analysis["risk"] = "high"
                analysis["priority"] = "high"
            elif 0.5 <= pass_rate < 0.8:
                analysis["risk"] = "medium"
            
            # Use average duration
            if history.get("avg_duration"):
                analysis["estimated_duration"] = history["avg_duration"]
            
            # Check if test is flaky
            if history["total_runs"] > 3 and 0.3 < pass_rate < 0.7:
                analysis["is_flaky"] = True
                analysis["priority"] = "high"  # Run flaky tests early
        
        # Identify dependencies from test name
        analysis["dependencies"] = self._identify_dependencies(test_name)
        
        # Identify data needs
        analysis["data_needs"] = self._identify_test_data_needs(test_name)
        
        return analysis
    
    def _identify_dependencies(self, test_name: str) -> List[str]:
        """Identify test dependencies."""
        dependencies = []
        
        # Tests that modify data should run after read tests
        if "create" in test_name.lower() or "add" in test_name.lower():
            dependencies.append("view_tests_first")
        
        if "delete" in test_name.lower():
            dependencies.append("create_tests_first")
        
        if "update" in test_name.lower() or "edit" in test_name.lower():
            dependencies.append("create_tests_first")
        
        return dependencies
    
    def _identify_test_data_needs(self, test_name: str) -> List[str]:
        """Identify what data the test needs."""
        data_needs = []
        
        # Parse from test name
        if "segment" in test_name.lower():
            data_needs.append("test_segment")
        
        if "filter" in test_name.lower():
            data_needs.append("multiple_segments")
        
        if "pagination" in test_name.lower():
            data_needs.append("multiple_segments")
        
        if "delete" in test_name.lower() or "update" in test_name.lower():
            data_needs.append("disposable_segment")
        
        return data_needs
    
    def _prioritize_tests(self, test_analysis: List[Dict]) -> List[Dict]:
        """
        Prioritize tests for execution.
        
        Priority order:
        1. High priority (failing/flaky tests) first
        2. View/read tests before create/modify tests
        3. Create tests before update/delete tests
        """
        def priority_score(test):
            score = 0
            
            # Priority level
            if test.get("priority") == "high":
                score += 1000
            elif test.get("priority") == "medium":
                score += 500
            
            # Test type
            if "view" in test["test_name"].lower() or "list" in test["test_name"].lower():
                score += 300  # Run read tests first
            elif "create" in test["test_name"].lower():
                score += 200
            elif "update" in test["test_name"].lower() or "edit" in test["test_name"].lower():
                score += 100
            elif "delete" in test["test_name"].lower():
                score += 50  # Run delete tests last
            
            return score
        
        return sorted(test_analysis, key=priority_score, reverse=True)
    
    def _identify_data_needs(self, ordered_tests: List[Dict], app) -> Dict:
        """Identify all data requirements for test suite."""
        data_needs = {
            "test_segments": 0,
            "disposable_segments": 0,
            "multiple_segments": False
        }
        
        for test in ordered_tests:
            if "test_segment" in test.get("data_needs", []):
                data_needs["test_segments"] += 1
            if "disposable_segment" in test.get("data_needs", []):
                data_needs["disposable_segments"] += 1
            if "multiple_segments" in test.get("data_needs", []):
                data_needs["multiple_segments"] = True
        
        return data_needs
    
    def _estimate_duration(self, ordered_tests: List[Dict]) -> float:
        """Estimate total execution time."""
        total = sum(test.get("estimated_duration", 30.0) for test in ordered_tests)
        return round(total, 2)
    
    def _assess_risk(self, ordered_tests: List[Dict]) -> str:
        """Assess overall risk level of test suite."""
        high_risk = sum(1 for t in ordered_tests if t.get("risk") == "high")
        medium_risk = sum(1 for t in ordered_tests if t.get("risk") == "medium")
        
        if high_risk > len(ordered_tests) * 0.3:
            return "high"
        elif medium_risk > len(ordered_tests) * 0.5:
            return "medium"
        else:
            return "low"
    
    def _discover_all_tests(self, app) -> List[str]:
        """Discover all tests for app (simplified)."""
        # In real implementation, would scan test files
        # For now, return common pattern
        return [f"pos_00{i}" for i in range(1, 16)]
    
    def _print_plan(self, plan: Dict):
        """Print execution plan summary."""
        print(f"\n{'='*80}")
        print(f"📋 EXECUTION PLAN")
        print(f"{'='*80}")
        print(f"App: {plan['app']}")
        print(f"Total Tests: {plan['total_tests']}")
        print(f"Estimated Duration: {plan['estimated_duration']}s ({plan['estimated_duration']/60:.1f} min)")
        print(f"Risk Level: {plan['risk_level'].upper()}")
        print(f"\nExecution Order:")
        for i, test in enumerate(plan['execution_order'][:5], 1):
            priority_icon = "🔴" if test.get("priority") == "high" else "🟡" if test.get("priority") == "medium" else "🟢"
            print(f"  {i}. {priority_icon} {test['test_name']} "
                  f"({test.get('estimated_duration', 30):.1f}s, risk: {test.get('risk', 'low')})")
        if len(plan['execution_order']) > 5:
            print(f"  ... and {len(plan['execution_order']) - 5} more tests")
        print(f"{'='*80}\n")


_planner_instance = None

def get_planner() -> TestPlanner:
    """Get singleton planner instance."""
    global _planner_instance
    if _planner_instance is None:
        _planner_instance = TestPlanner()
    return _planner_instance
