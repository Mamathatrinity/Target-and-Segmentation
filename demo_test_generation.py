"""
Demo: Test Gap Analyzer and Combinatorial Testing
Shows how to use the new autonomous test generation features.
"""
from framework.agent import (
    TestGapAnalyzer,
    CombinatorialTester,
    analyze_gaps,
    auto_generate_tests,
    create_combinatorial_suite
)


def demo_test_gap_analyzer():
    """Demo: Analyze coverage gaps and auto-generate tests."""
    print("\n" + "="*80)
    print("🔍 DEMO 1: TEST GAP ANALYZER")
    print("="*80)
    
    # Quick analysis
    print("\n--- Quick Gap Analysis ---")
    gaps = analyze_gaps("segments")
    
    print(f"\nFound {len(gaps)} missing tests")
    print("\nTop 5 gaps:")
    for gap in gaps[:5]:
        print(f"  - {gap['test_name']}")
        print(f"    Type: {gap['type']}, Priority: {gap['priority']}")
        print(f"    Validation: {', '.join(gap['validation_layers'])}")
    
    # Auto-generate missing tests
    print("\n--- Auto-Generate Tests ---")
    choice = input("\nGenerate missing tests? (y/n): ")
    if choice.lower() == 'y':
        result = auto_generate_tests("segments")
        print(f"\n✅ Generated {result['total_gaps']} tests")
        print(f"File: {result['output_file']}")


def demo_combinatorial_testing():
    """Demo: Combinatorial testing for exhaustive coverage."""
    print("\n" + "="*80)
    print("🧪 DEMO 2: COMBINATORIAL TESTING")
    print("="*80)
    
    tester = CombinatorialTester()
    
    # Define input space for "create segment" functionality
    print("\n--- Define Input Space ---")
    tester.define_input_space("create_segment", {
        "name": ["Valid Name", "", "A"*256, "Test<>!@#"],
        "status": ["active", "inactive"],
        "is_team": [True, False],
        "description": ["Test description", None]
    })
    
    print("Input space defined for 'create_segment':")
    print("  - name: 4 variations")
    print("  - status: 2 variations")
    print("  - is_team: 2 variations")
    print("  - description: 2 variations")
    print(f"  Total combinations: 4 × 2 × 2 × 2 = 32 test cases")
    
    # Generate pairwise (optimized)
    print("\n--- Pairwise Combinations (Optimized) ---")
    pairwise_cases = tester.generate_pairwise_combinations("create_segment")
    
    print(f"\nGenerated {len(pairwise_cases)} pairwise test cases")
    print("\nFirst 3 test cases:")
    for case in pairwise_cases[:3]:
        print(f"\n  {case['test_id']}:")
        print(f"    Inputs: {case['inputs']}")
        print(f"    Expected: {case['expected_result']}")
    
    # Generate full combinations
    print("\n--- Full Combinations (Exhaustive) ---")
    choice = input("\nGenerate ALL combinations? (32 tests) (y/n): ")
    if choice.lower() == 'y':
        full_cases = tester.generate_all_combinations("create_segment")
        print(f"\nGenerated {len(full_cases)} exhaustive test cases")
        
        passed = sum(1 for tc in full_cases if tc['expected_result'] == 'pass')
        failed = len(full_cases) - passed
        
        print(f"  Expected to pass: {passed}")
        print(f"  Expected to fail: {failed}")


def demo_boundary_testing():
    """Demo: Boundary value testing."""
    print("\n" + "="*80)
    print("📏 DEMO 3: BOUNDARY VALUE TESTING")
    print("="*80)
    
    tester = CombinatorialTester()
    
    # Define boundaries for segment name field
    print("\n--- Define Boundaries ---")
    boundaries = {
        "name": {"min": 1, "max": 255, "type": "string"},
        "user_count": {"min": 0, "max": 1000000, "type": "int"}
    }
    
    print("Boundaries defined:")
    print("  - name: 1-255 characters (string)")
    print("  - user_count: 0-1,000,000 (integer)")
    
    # Generate boundary tests
    print("\n--- Generate Boundary Tests ---")
    tester.define_input_space("segment_boundaries", boundaries)
    boundary_cases = tester.generate_boundary_tests("segment_boundaries", boundaries)
    
    print(f"\nGenerated {len(boundary_cases)} boundary test cases")
    print("\nBoundary test cases:")
    for case in boundary_cases:
        print(f"\n  {case['test_id']}:")
        print(f"    Input: {case['inputs']}")
        print(f"    Expected: {case['expected_result']}")
        print(f"    Type: {case['boundary_type']}")


def demo_advanced_usage():
    """Demo: Advanced usage - Custom analyzer."""
    print("\n" + "="*80)
    print("🚀 DEMO 4: ADVANCED USAGE")
    print("="*80)
    
    # Create custom analyzer
    analyzer = TestGapAnalyzer(test_base_path="tests/ui")
    
    # Analyze multiple apps
    print("\n--- Multi-App Analysis ---")
    for app in ["segments", "target_list", "universe_summary"]:
        gaps = analyzer.analyze_coverage_gaps(app)
        print(f"\n{app.title()}: {len(gaps)} missing tests")
    
    # Generate test code for specific gap
    print("\n--- Generate Specific Test ---")
    gaps = analyze_gaps("segments")
    if gaps:
        gap = gaps[0]  # First gap
        test_code = analyzer.generate_test_code(gap, "segments")
        
        print(f"\nGenerated code for: {gap['test_name']}")
        print("\n" + "-"*80)
        print(test_code)
        print("-"*80)


def main():
    """Run all demos."""
    print("\n" + "="*80)
    print("🤖 TEST GENERATION FRAMEWORK DEMO")
    print("Autonomous Test Discovery & Combinatorial Testing")
    print("="*80)
    
    demos = [
        ("Test Gap Analyzer", demo_test_gap_analyzer),
        ("Combinatorial Testing", demo_combinatorial_testing),
        ("Boundary Testing", demo_boundary_testing),
        ("Advanced Usage", demo_advanced_usage)
    ]
    
    print("\nAvailable demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  {len(demos)+1}. Run All")
    print(f"  0. Exit")
    
    choice = input("\nSelect demo (0-5): ")
    
    try:
        choice = int(choice)
        
        if choice == 0:
            print("\nExiting...")
            return
        elif choice == len(demos) + 1:
            # Run all
            for name, demo_func in demos:
                demo_func()
        elif 1 <= choice <= len(demos):
            # Run specific demo
            _, demo_func = demos[choice - 1]
            demo_func()
        else:
            print("\nInvalid choice!")
    except ValueError:
        print("\nInvalid input!")
    
    print("\n" + "="*80)
    print("✅ Demo Complete!")
    print("\nYou can now:")
    print("  1. Run: analyze_gaps('segments') - Find missing tests")
    print("  2. Run: auto_generate_tests('segments') - Create missing tests")
    print("  3. Use CombinatorialTester for exhaustive testing")
    print("="*80)


if __name__ == "__main__":
    main()
