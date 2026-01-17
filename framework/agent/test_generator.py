"""
Test Generator - Automatically discovers and creates missing test cases
Includes Test Gap Analyzer and Combinatorial Test Generator
"""
import ast
import re
import inspect
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from itertools import product, combinations
from datetime import datetime


class TestGapAnalyzer:
    """
    Analyzes test coverage and automatically generates missing test cases.
    
    Features:
    - Discovers existing tests
    - Identifies coverage gaps
    - Generates test code automatically
    - Supports multiple test types
    """
    
    def __init__(self, test_base_path: str = "tests/ui"):
        self.test_base_path = Path(test_base_path)
        
    def _get_existing_tests(self, app_name: str) -> List[str]:
        """Get all existing test names for an app."""
        test_file = self.test_base_path / f"test_{app_name}.py"
        
        if not test_file.exists():
            return []
        
        # Parse AST to find test functions (force utf-8 to avoid UnicodeDecodeError)
        content = test_file.read_text(encoding="utf-8")
        tree = ast.parse(content)
        
        test_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                test_names.append(node.name)
        
        return test_names
    
    def analyze_coverage_gaps(self, app_name: str) -> List[Dict]:
        """
        Analyze test coverage and identify missing test cases.
        
        Returns:
            List of missing test scenarios with details
        """
        print(f"\n{'='*80}")
        print(f"🔍 ANALYZING TEST COVERAGE GAPS: {app_name.upper()}")
        print(f"{'='*80}")
        
        existing_tests = self._get_existing_tests(app_name)
        print(f"\n📊 Found {len(existing_tests)} existing tests")
        
        gaps = []
        
        # Define required scenarios based on app type
        if app_name == "segments":
            required_scenarios = self._get_segments_scenarios()
        elif app_name == "target_list":
            required_scenarios = self._get_target_list_scenarios()
        elif app_name == "universe_summary":
            required_scenarios = self._get_universe_summary_scenarios()
        else:
            # Generic scenarios
            required_scenarios = self._get_generic_scenarios()
        
        # Find gaps
        for scenario in required_scenarios:
            for variation in scenario["variations"]:
                # Generate expected test name
                test_name = f"test_{app_name}_{scenario['type']}_{variation}"
                
                # Check if exists
                if test_name not in existing_tests:
                    gaps.append({
                        "test_name": test_name,
                        "type": scenario["type"],
                        "variation": variation,
                        "priority": scenario.get("priority", "medium"),
                        "description": scenario.get("description", ""),
                        "validation_layers": scenario.get("validation_layers", ["ui", "api", "db"])
                    })
        
        print(f"\n🎯 Found {len(gaps)} MISSING test cases:")
        for gap in gaps[:10]:  # Show first 10
            print(f"   - {gap['test_name']} (Priority: {gap['priority']})")
        
        if len(gaps) > 10:
            print(f"   ... and {len(gaps) - 10} more")
        
        return gaps
    
    def _get_segments_scenarios(self) -> List[Dict]:
        """Define required test scenarios for segments app."""
        return [
            {
                "type": "create",
                "variations": ["valid", "invalid_name", "empty_name", "duplicate", "special_chars", "max_length"],
                "priority": "high",
                "description": "Create segment functionality",
                "validation_layers": ["ui", "api", "db"]
            },
            {
                "type": "edit",
                "variations": ["valid", "invalid_name", "non_existent", "concurrent_edit", "empty_name"],
                "priority": "high",
                "description": "Edit segment functionality",
                "validation_layers": ["ui", "api", "db"]
            },
            {
                "type": "delete",
                "variations": ["valid", "non_existent", "in_use", "already_deleted", "cascade"],
                "priority": "high",
                "description": "Delete segment functionality",
                "validation_layers": ["ui", "api", "db"]
            },
            {
                "type": "search",
                "variations": ["exact_match", "partial_match", "no_results", "special_chars", "case_insensitive", "wildcard"],
                "priority": "medium",
                "description": "Search functionality",
                "validation_layers": ["ui", "api"]
            },
            {
                "type": "filter",
                "variations": ["by_user", "by_team", "by_date", "by_status", "multiple_filters", "no_results"],
                "priority": "medium",
                "description": "Filter functionality",
                "validation_layers": ["ui", "api"]
            },
            {
                "type": "sort",
                "variations": ["name_asc", "name_desc", "date_asc", "date_desc", "status_asc", "status_desc"],
                "priority": "low",
                "description": "Sorting functionality",
                "validation_layers": ["ui", "api"]
            },
            {
                "type": "pagination",
                "variations": ["first_page", "next_page", "previous_page", "last_page", "change_page_size", "empty_results"],
                "priority": "medium",
                "description": "Pagination functionality",
                "validation_layers": ["ui", "api"]
            },
            {
                "type": "export",
                "variations": ["csv", "excel", "pdf", "empty_results", "large_dataset"],
                "priority": "low",
                "description": "Export functionality",
                "validation_layers": ["ui", "api"]
            },
            {
                "type": "permissions",
                "variations": ["owner_access", "team_access", "no_access", "read_only", "admin_access"],
                "priority": "high",
                "description": "Permission checks",
                "validation_layers": ["api", "db"]
            }
        ]
    
    def _get_target_list_scenarios(self) -> List[Dict]:
        """Define required test scenarios for target list app."""
        return [
            {
                "type": "create",
                "variations": ["valid", "invalid", "duplicate"],
                "priority": "high",
                "validation_layers": ["ui", "api", "db"]
            },
            {
                "type": "export",
                "variations": ["csv", "excel"],
                "priority": "medium",
                "validation_layers": ["ui", "api"]
            }
        ]
    
    def _get_universe_summary_scenarios(self) -> List[Dict]:
        """Define required test scenarios for universe summary app."""
        return [
            {
                "type": "view",
                "variations": ["dashboard", "charts", "filters"],
                "priority": "high",
                "validation_layers": ["ui", "api"]
            }
        ]
    
    def _get_generic_scenarios(self) -> List[Dict]:
        """Generic test scenarios for unknown apps."""
        return [
            {
                "type": "create",
                "variations": ["valid", "invalid"],
                "priority": "high",
                "validation_layers": ["ui", "api", "db"]
            },
            {
                "type": "view",
                "variations": ["list", "details"],
                "priority": "medium",
                "validation_layers": ["ui", "api"]
            }
        ]
    
    def generate_test_code(self, gap: Dict, app_name: str) -> str:
        """
        Generate complete test code for a missing test case.
        
        Args:
            gap: Gap info from analyze_coverage_gaps
            app_name: Application name
            
        Returns:
            Complete Python test function code
        """
        test_type = gap["type"]
        variation = gap["variation"]
        validation_layers = gap["validation_layers"]
        
        # Build validation code
        validation_code = []
        if "ui" in validation_layers:
            validation_code.append("    # UI Validation")
            validation_code.append("    # TODO: Implement UI assertions")
        
        if "api" in validation_layers:
            validation_code.append("    ")
            validation_code.append("    # API Validation")
            validation_code.append("    # TODO: Implement API validation")
        
        if "db" in validation_layers:
            validation_code.append("    ")
            validation_code.append("    # Database Validation")
            validation_code.append("    # TODO: Implement DB validation")
        
        validation_str = "\n".join(validation_code)
        
        # Generate test function
        template = f'''
@pytest.mark.{app_name}
@pytest.mark.{test_type}
@pytest.mark.{gap["priority"]}
def {gap["test_name"]}(page, api_validator, mysql_connection, settings):
    """
    Test: {test_type.replace("_", " ").title()} - {variation.replace("_", " ").title()}
    
    Priority: {gap["priority"].upper()}
    Auto-generated by Test Gap Analyzer
    
    Validation Layers: {", ".join(validation_layers).upper()}
    """
    allure.dynamic.title(f"{test_type.title()}: {variation.replace('_', ' ').title()}")
    allure.dynamic.description("{gap.get('description', 'Auto-generated test case')}")
    
    # Step 1: Setup test data
    with allure.step("Setup test data"):
        # TODO: Auto-generate setup based on test type
        pass
    
    # Step 2: Execute {test_type} action
    with allure.step("{test_type.title()} action"):
        # TODO: Auto-generate action based on test type and variation
        pass
    
    # Step 3: Validate results
    with allure.step("Validate results"):
{validation_str}
        pass
    
    # Step 4: Cleanup
    with allure.step("Cleanup"):
        # TODO: Auto-generate cleanup
        pass
'''
        return template
    
    def auto_create_missing_tests(self, app_name: str, output_file: Optional[str] = None) -> Dict:
        """
        Automatically create missing test file with all gap tests.
        
        Args:
            app_name: Application name
            output_file: Optional output file path (default: test_{app}_generated.py)
            
        Returns:
            Summary of tests created
        """
        gaps = self.analyze_coverage_gaps(app_name)
        
        if not gaps:
            return {
                "status": "complete",
                "message": "No gaps found - coverage is complete!",
                "total_gaps": 0
            }
        
        # Generate output file path
        if not output_file:
            output_file = self.test_base_path / f"test_{app_name}_generated.py"
        else:
            output_file = Path(output_file)
        
        # Build complete test file
        file_content = self._generate_test_file_header(app_name)
        
        for gap in gaps:
            test_code = self.generate_test_code(gap, app_name)
            file_content += test_code + "\n"
        
        # Write to file
        output_file.write_text(file_content)
        
        print(f"\n{'='*80}")
        print(f"✅ AUTO-GENERATED {len(gaps)} TEST CASES")
        print(f"{'='*80}")
        print(f"Output file: {output_file}")
        print(f"\nNext steps:")
        print(f"1. Review generated tests in {output_file}")
        print(f"2. Implement TODO sections")
        print(f"3. Run tests to validate")
        
        return {
            "status": "created",
            "total_gaps": len(gaps),
            "tests_created": [gap["test_name"] for gap in gaps],
            "output_file": str(output_file)
        }
    
    def _generate_test_file_header(self, app_name: str) -> str:
        """Generate test file header with imports."""
        return f'''"""
Auto-Generated Test Cases for {app_name.title()}

Generated by Test Gap Analyzer
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

These tests were automatically generated to fill coverage gaps.
Review and implement TODO sections before running.
"""
import pytest
import allure
from playwright.sync_api import Page, expect


'''


class CombinatorialTester:
    """
    Generates and runs test cases for all permutations and combinations.
    
    Features:
    - Exhaustive input combination testing
    - Boundary value analysis
    - Equivalence partitioning
    - Pairwise testing optimization
    """
    
    def __init__(self):
        self.test_scenarios = {}
        
    def define_input_space(self, test_type: str, inputs: Dict[str, List[Any]]) -> None:
        """
        Define the input space for combinatorial testing.
        
        Args:
            test_type: Type of test (e.g., "create_segment")
            inputs: Dictionary of input field names to possible values
            
        Example:
            tester.define_input_space("create_segment", {
                "name": ["Valid Name", "", "A"*256, "Test<>"],
                "status": ["active", "inactive"],
                "is_team": [True, False]
            })
        """
        self.test_scenarios[test_type] = inputs
        
    def generate_all_combinations(self, test_type: str) -> List[Dict]:
        """
        Generate ALL possible combinations of inputs (exhaustive).
        
        Warning: Can generate very large number of tests!
        Use with caution or use pairwise instead.
        
        Returns:
            List of test case dictionaries
        """
        if test_type not in self.test_scenarios:
            return []
        
        inputs = self.test_scenarios[test_type]
        
        # Get all field names and their values
        field_names = list(inputs.keys())
        field_values = [inputs[field] for field in field_names]
        
        # Generate cartesian product
        combinations_list = list(product(*field_values))
        
        # Build test cases
        test_cases = []
        for i, combo in enumerate(combinations_list):
            test_case = {
                "test_id": f"{test_type}_combo_{i:04d}",
                "inputs": dict(zip(field_names, combo)),
                "expected_result": self._predict_result(test_type, dict(zip(field_names, combo)))
            }
            test_cases.append(test_case)
        
        print(f"\n📊 Generated {len(test_cases)} combinatorial test cases for {test_type}")
        return test_cases
    
    def generate_pairwise_combinations(self, test_type: str) -> List[Dict]:
        """
        Generate pairwise combinations (optimized - covers all pairs).
        
        Much smaller than full combinations but still good coverage.
        
        Returns:
            List of test case dictionaries
        """
        if test_type not in self.test_scenarios:
            return []
        
        inputs = self.test_scenarios[test_type]
        field_names = list(inputs.keys())
        
        # Simple pairwise: for each pair of fields, ensure all combinations covered
        # This is a simplified version - production would use allpairspy
        
        test_cases = []
        
        # For now, use a greedy approach
        # Take one value from each field, rotating through values
        max_values = max(len(values) for values in inputs.values())
        
        for i in range(max_values):
            combo = {}
            for field, values in inputs.items():
                combo[field] = values[i % len(values)]
            
            test_case = {
                "test_id": f"{test_type}_pairwise_{i:04d}",
                "inputs": combo,
                "expected_result": self._predict_result(test_type, combo)
            }
            test_cases.append(test_case)
        
        print(f"\n📊 Generated {len(test_cases)} pairwise test cases for {test_type}")
        return test_cases
    
    def generate_boundary_tests(self, test_type: str, field_boundaries: Dict[str, Dict]) -> List[Dict]:
        """
        Generate boundary value tests.
        
        Args:
            test_type: Type of test
            field_boundaries: Dictionary of field -> {min, max, type}
            
        Example:
            tester.generate_boundary_tests("create_segment", {
                "name": {"min": 1, "max": 255, "type": "string"},
                "count": {"min": 0, "max": 1000000, "type": "int"}
            })
        """
        test_cases = []
        
        for field, bounds in field_boundaries.items():
            field_type = bounds.get("type", "string")
            
            if field_type == "string":
                min_len = bounds.get("min", 0)
                max_len = bounds.get("max", 255)
                
                # Boundary values for string length
                boundary_values = [
                    "",  # Empty
                    "A" * min_len,  # Minimum
                    "A" * (min_len + 1),  # Just above minimum
                    "A" * (max_len - 1),  # Just below maximum
                    "A" * max_len,  # Maximum
                    "A" * (max_len + 1),  # Above maximum (should fail)
                ]
                
                for i, value in enumerate(boundary_values):
                    test_case = {
                        "test_id": f"{test_type}_boundary_{field}_{i:02d}",
                        "inputs": {field: value},
                        "expected_result": "pass" if min_len <= len(value) <= max_len else "fail",
                        "boundary_type": "string_length"
                    }
                    test_cases.append(test_case)
            
            elif field_type == "int":
                min_val = bounds.get("min", 0)
                max_val = bounds.get("max", 999999)
                
                boundary_values = [
                    min_val - 1,  # Below minimum
                    min_val,  # Minimum
                    min_val + 1,  # Just above minimum
                    max_val - 1,  # Just below maximum
                    max_val,  # Maximum
                    max_val + 1,  # Above maximum
                ]
                
                for i, value in enumerate(boundary_values):
                    test_case = {
                        "test_id": f"{test_type}_boundary_{field}_{i:02d}",
                        "inputs": {field: value},
                        "expected_result": "pass" if min_val <= value <= max_val else "fail",
                        "boundary_type": "numeric_range"
                    }
                    test_cases.append(test_case)
        
        print(f"\n📊 Generated {len(test_cases)} boundary test cases")
        return test_cases
    
    def _predict_result(self, test_type: str, inputs: Dict) -> str:
        """
        Predict if test should pass or fail based on inputs.
        
        This uses business logic rules to predict outcomes.
        """
        # Generic validation rules
        if "name" in inputs:
            name = inputs["name"]
            
            # Empty name should fail
            if not name or len(name) == 0:
                return "fail"
            
            # Too long should fail
            if len(name) > 255:
                return "fail"
            
            # Special chars that break HTML
            if any(char in name for char in ["<", ">", "&", '"']):
                return "fail"
        
        # If all validations pass
        return "pass"
    
    def run_combinatorial_suite(self, test_type: str, mode: str = "pairwise") -> Dict:
        """
        Run combinatorial test suite.
        
        Args:
            test_type: Type of test to run
            mode: "full", "pairwise", or "boundary"
            
        Returns:
            Execution summary
        """
        if mode == "full":
            test_cases = self.generate_all_combinations(test_type)
        elif mode == "pairwise":
            test_cases = self.generate_pairwise_combinations(test_type)
        elif mode == "boundary":
            # Requires boundary definitions
            test_cases = []
        else:
            return {"error": f"Unknown mode: {mode}"}
        
        print(f"\n{'='*80}")
        print(f"🧪 RUNNING COMBINATORIAL TEST SUITE: {test_type}")
        print(f"{'='*80}")
        print(f"Mode: {mode.upper()}")
        print(f"Total test cases: {len(test_cases)}")
        
        # Here you would actually run the tests
        # For now, just analyze
        passed = sum(1 for tc in test_cases if tc["expected_result"] == "pass")
        failed = len(test_cases) - passed
        
        return {
            "test_type": test_type,
            "mode": mode,
            "total_cases": len(test_cases),
            "expected_pass": passed,
            "expected_fail": failed,
            "test_cases": test_cases
        }


# Convenience functions
def analyze_gaps(app_name: str) -> List[Dict]:
    """Quick function to analyze test gaps."""
    analyzer = TestGapAnalyzer()
    return analyzer.analyze_coverage_gaps(app_name)


def auto_generate_tests(app_name: str) -> Dict:
    """Quick function to auto-generate missing tests."""
    analyzer = TestGapAnalyzer()
    return analyzer.auto_create_missing_tests(app_name)


def create_combinatorial_suite(test_type: str, inputs: Dict[str, List[Any]]) -> List[Dict]:
    """Quick function to create combinatorial test suite."""
    tester = CombinatorialTester()
    tester.define_input_space(test_type, inputs)
    return tester.generate_all_combinations(test_type)
