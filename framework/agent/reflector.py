"""
LLM Reflector - Learning from Test Failures
Analyzes patterns, suggests improvements, and helps agent learn.
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from .memory import get_memory
from .self_healing import get_healing_engine


class TestFailureAnalyzer:
    """Analyzes test failures to extract insights."""
    
    def __init__(self):
        self.memory = get_memory()
        self.healer = get_healing_engine()
        
    def analyze_failure(self, test_name: str, error: str, 
                       traceback: str, test_code: Optional[str] = None) -> Dict:
        """
        Deep analysis of test failure.
        
        Returns insights about root cause, patterns, and suggestions.
        """
        analysis = {
            "test_name": test_name,
            "timestamp": str(datetime.now()),
            "error_type": self._classify_error(error),
            "pattern_match": None,
            "root_cause": None,
            "suggestions": [],
            "learnings": []
        }
        
        # Check for known patterns
        pattern = self.healer.detector.detect_pattern(error, traceback)
        if pattern:
            analysis["pattern_match"] = pattern["name"]
            analysis["root_cause"] = pattern["description"]
            analysis["suggestions"] = self._get_pattern_suggestions(pattern)
        else:
            # No known pattern - analyze raw error
            analysis["root_cause"] = self._infer_root_cause(error, traceback)
            analysis["suggestions"] = self._generate_suggestions(error, traceback)
            analysis["learnings"].append("New error pattern - consider adding to knowledge base")
        
        # Check test history for flakiness
        history = self.memory.get_test_history(test_name)
        if history and history["total_runs"] > 2:
            pass_rate = history["total_passes"] / history["total_runs"]
            if 0.3 < pass_rate < 0.7:
                analysis["learnings"].append(
                    f"Test is flaky: {pass_rate*100:.1f}% pass rate - investigate timing or data issues"
                )
        
        return analysis
    
    def _classify_error(self, error: str) -> str:
        """Classify error type."""
        error_lower = error.lower()
        
        if "timeout" in error_lower or "wait" in error_lower:
            return "timing"
        elif "assert" in error_lower:
            return "assertion"
        elif "keyerror" in error_lower or "attributeerror" in error_lower:
            return "data_structure"
        elif "connection" in error_lower or "network" in error_lower:
            return "network"
        elif "database" in error_lower or "sql" in error_lower:
            return "database"
        elif "400" in error or "404" in error or "500" in error:
            return "api"
        else:
            return "unknown"
    
    def _infer_root_cause(self, error: str, traceback: str) -> str:
        """Infer root cause from error message and traceback."""
        error_type = self._classify_error(error)
        
        if error_type == "data_structure":
            return "Data structure mismatch - check function return types"
        elif error_type == "database":
            return "Database schema or query issue"
        elif error_type == "api":
            return "API request error - check parameters and authentication"
        elif error_type == "timing":
            return "Timing or synchronization issue - may need longer waits"
        else:
            return f"Error type: {error_type} - requires investigation"
    
    def _get_pattern_suggestions(self, pattern: Dict) -> List[str]:
        """Get suggestions for a known pattern."""
        suggestions = [
            f"Known pattern: {pattern['name']}",
            f"Fix action: {pattern['fix_action']}"
        ]
        
        if pattern.get("auto_fix"):
            suggestions.append("✅ Auto-fix available - run with self-healing enabled")
        else:
            suggestions.append("⚠️ Manual fix required")
        
        return suggestions
    
    def _generate_suggestions(self, error: str, traceback: str) -> List[str]:
        """Generate suggestions for unknown errors."""
        error_type = self._classify_error(error)
        
        suggestions_map = {
            "data_structure": [
                "Verify function return types match expected structure",
                "Check if dict keys exist before accessing",
                "Add type hints for better IDE support"
            ],
            "database": [
                "Verify database schema matches code expectations",
                "Check for missing or renamed columns",
                "Ensure database connection is active"
            ],
            "api": [
                "Verify all required parameters are provided",
                "Check authentication token is valid",
                "Confirm API endpoint exists and is accessible"
            ],
            "timing": [
                "Increase wait timeouts",
                "Add explicit waits for elements",
                "Check for race conditions"
            ],
            "network": [
                "Verify network connectivity",
                "Check VPN connection if required",
                "Confirm service URLs are correct"
            ]
        }
        
        return suggestions_map.get(error_type, ["Investigate error manually"])


class ImprovementSuggester:
    """Suggests test and framework improvements."""
    
    def __init__(self):
        self.memory = get_memory()
        
    def suggest_improvements(self) -> Dict[str, List[str]]:
        """Generate improvement suggestions based on memory."""
        suggestions = {
            "test_reliability": [],
            "code_quality": [],
            "framework_enhancements": [],
            "best_practices": []
        }
        
        # Analyze flaky tests
        flaky = self.memory.get_flaky_tests()
        if flaky:
            suggestions["test_reliability"].append(
                f"Fix {len(flaky)} flaky tests: {', '.join(flaky[:3])}"
            )
        
        # Analyze fixed bugs for patterns
        stats = self.memory.get_stats()
        if stats["total_bugs_fixed"] > 5:
            suggestions["code_quality"].append(
                "Consider refactoring common bug patterns to prevent recurrence"
            )
        
        # Suggest framework enhancements
        if stats["total_patterns"] < 10:
            suggestions["framework_enhancements"].append(
                "Expand pattern knowledge base for better auto-healing coverage"
            )
        
        # Best practices
        suggestions["best_practices"].extend([
            "Run full test suite before committing",
            "Review Allure reports for detailed validation insights",
            "Keep MCP validators updated with latest API changes"
        ])
        
        return suggestions
    
    def analyze_test_coverage(self, app_name: str, test_results: List[Dict]) -> Dict:
        """Analyze test coverage and identify gaps."""
        coverage = {
            "total_tests": len(test_results),
            "passing_tests": sum(1 for t in test_results if t.get("status") == "passed"),
            "failing_tests": sum(1 for t in test_results if t.get("status") == "failed"),
            "gaps": []
        }
        
        pass_rate = coverage["passing_tests"] / coverage["total_tests"] if coverage["total_tests"] > 0 else 0
        
        if pass_rate < 0.8:
            coverage["gaps"].append("Pass rate below 80% - investigate failing tests")
        
        if pass_rate == 1.0 and coverage["total_tests"] < 10:
            coverage["gaps"].append("Limited test coverage - consider adding edge cases")
        
        return coverage


class Reflector:
    """Main reflector class - coordinates analysis and learning."""
    
    def __init__(self):
        self.analyzer = TestFailureAnalyzer()
        self.suggester = ImprovementSuggester()
        self.memory = get_memory()
        
    def reflect_on_failure(self, test_name: str, error: str, traceback: str) -> Dict:
        """
        Full reflection on test failure.
        
        Returns comprehensive analysis with suggestions and learnings.
        """
        print(f"\n🤔 Reflecting on failure: {test_name}")
        
        analysis = self.analyzer.analyze_failure(test_name, error, traceback)
        
        print(f"\n📋 Analysis:")
        print(f"  Error Type: {analysis['error_type']}")
        print(f"  Root Cause: {analysis['root_cause']}")
        
        if analysis.get("pattern_match"):
            print(f"  Pattern Match: ✅ {analysis['pattern_match']}")
        else:
            print(f"  Pattern Match: ❌ New error type")
        
        print(f"\n💡 Suggestions:")
        for suggestion in analysis["suggestions"]:
            print(f"  - {suggestion}")
        
        if analysis.get("learnings"):
            print(f"\n📚 Learnings:")
            for learning in analysis["learnings"]:
                print(f"  - {learning}")
        
        return analysis
    
    def suggest_improvements(self) -> Dict:
        """Get improvement suggestions."""
        print(f"\n✨ Improvement Suggestions:")
        
        suggestions = self.suggester.suggest_improvements()
        
        for category, items in suggestions.items():
            if items:
                print(f"\n  {category.replace('_', ' ').title()}:")
                for item in items:
                    print(f"    - {item}")
        
        return suggestions
    
    def learn_from_session(self, test_results: List[Dict]) -> Dict:
        """
        Learn from a test session.
        
        Args:
            test_results: List of test result dicts
            
        Returns:
            Session learnings and insights
        """
        total = len(test_results)
        passed = sum(1 for t in test_results if t.get("status") == "passed")
        failed = sum(1 for t in test_results if t.get("status") == "failed")
        
        learnings = {
            "session_stats": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": passed / total if total > 0 else 0
            },
            "insights": [],
            "action_items": []
        }
        
        # Generate insights
        if failed == 0:
            learnings["insights"].append("✅ All tests passing - excellent!")
        elif failed < total * 0.2:
            learnings["insights"].append("✅ Most tests passing - minor fixes needed")
        else:
            learnings["insights"].append("⚠️ Significant failures - requires investigation")
        
        # Action items
        if failed > 0:
            learnings["action_items"].append("Review failed tests and apply auto-heal")
        
        return learnings


# Global reflector instance
_reflector_instance = None

def get_reflector() -> Reflector:
    """Get global reflector instance (singleton)."""
    global _reflector_instance
    if _reflector_instance is None:
        _reflector_instance = Reflector()
    return _reflector_instance
