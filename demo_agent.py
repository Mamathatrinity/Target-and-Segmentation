"""
Agent Framework Demo
Shows how to use all agent features.
"""
from framework.agent import (
    AutonomousRunner,
    get_memory,
    get_healing_engine,
    get_reflector
)


def demo_runner():
    """Demonstrate AutonomousRunner."""
    print("\n" + "="*80)
    print("🤖 AUTONOMOUS RUNNER DEMO")
    print("="*80)
    
    runner = AutonomousRunner()
    
    # List available apps
    print("\n1. List Apps:")
    runner.list_apps()
    
    # List features for an app
    print("\n2. List Features:")
    runner.list_features('segments')
    
    # Show stats
    print("\n3. Agent Statistics:")
    runner.stats()
    
    # Example: Run a test (commented out - requires fixtures)
    # result = runner.test('segments', 'pos_003')
    print("\n4. Example usage:")
    print("   runner.test('segments', 'pos_003')  # Run single test")
    print("   runner.test_suite('segments')       # Run all tests")


def demo_memory():
    """Demonstrate Memory System."""
    print("\n" + "="*80)
    print("💾 MEMORY SYSTEM DEMO")
    print("="*80)
    
    memory = get_memory()
    
    # Record a bug fix (example)
    print("\n1. Record Bug Fix:")
    memory.record_bug_fix({
        "id": "demo_bug_001",
        "description": "Fixed is_deleted column issue",
        "file": "tests/helpers/segments_db_helpers.py",
        "line": 206,
        "pattern": "db_001",
        "fix_action": "remove_column_from_query",
        "tests_affected": ["test_seg_pos_003", "test_seg_pos_008"]
    })
    print("   ✅ Bug fix recorded")
    
    # Get stats
    print("\n2. Memory Stats:")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Check if bug was fixed
    print("\n3. Check if bug fixed:")
    is_fixed = memory.is_bug_fixed("demo_bug_001")
    print(f"   demo_bug_001: {'✅ Fixed' if is_fixed else '❌ Not fixed'}")


def demo_self_healing():
    """Demonstrate Self-Healing Engine."""
    print("\n" + "="*80)
    print("🔧 SELF-HEALING ENGINE DEMO")
    print("="*80)
    
    healer = get_healing_engine()
    
    # Show fixable patterns
    print("\n1. Auto-Fixable Patterns:")
    patterns = healer.detector.get_fixable_patterns()
    for pattern in patterns:
        print(f"   - {pattern['name']}: {pattern['description']}")
    
    # Analyze a failure (example)
    print("\n2. Analyze Failure:")
    analysis = healer.analyze_failure(
        test_name="test_seg_pos_003",
        error="pymysql.err.OperationalError: Unknown column 'is_deleted'",
        traceback="File segments_db_helpers.py, line 206"
    )
    
    print(f"   Fixable: {'✅' if analysis['fixable'] else '❌'}")
    print(f"   Pattern: {analysis.get('pattern', {}).get('name', 'None')}")
    print(f"   Fix Action: {analysis.get('fix_action', 'None')}")
    print(f"   Confidence: {analysis['confidence'] * 100}%")
    
    # Get fix suggestions
    print("\n3. Fix Suggestions:")
    suggestions = healer.get_fix_suggestions(
        error="KeyError: slice(None, 10, None)",
        traceback="db_segments_page1[:10]"
    )
    for suggestion in suggestions:
        print(f"   - {suggestion}")


def demo_reflector():
    """Demonstrate Reflector (Learning)."""
    print("\n" + "="*80)
    print("🤔 REFLECTOR DEMO")
    print("="*80)
    
    reflector = get_reflector()
    
    # Reflect on a failure
    print("\n1. Reflect on Failure:")
    analysis = reflector.reflect_on_failure(
        test_name="test_seg_pos_007",
        error="KeyError: slice(None, 10, None)",
        traceback="File test_segments.py, line 1979, in test_seg_pos_007\n    for idx, seg in enumerate(db_segments_page1[:10], 1)"
    )
    
    # Get improvement suggestions
    print("\n2. Improvement Suggestions:")
    reflector.suggest_improvements()
    
    # Example session learning (mock data)
    print("\n3. Session Learning:")
    test_results = [
        {"status": "passed", "duration": 5.2},
        {"status": "passed", "duration": 4.8},
        {"status": "failed", "duration": 3.1}
    ]
    learnings = reflector.learn_from_session(test_results)
    
    print(f"\n   Session Stats:")
    stats = learnings["session_stats"]
    print(f"   Total: {stats['total_tests']}, Passed: {stats['passed']}, Failed: {stats['failed']}")
    print(f"   Pass Rate: {stats['pass_rate'] * 100:.1f}%")
    
    print(f"\n   Insights:")
    for insight in learnings["insights"]:
        print(f"   - {insight}")


def main():
    """Run all demos."""
    print("\n" + "="*80)
    print("🚀 AGENT FRAMEWORK - COMPLETE DEMO")
    print("="*80)
    print("\nThis demonstrates all ChatGPT features (except ONE test file)")
    
    demo_runner()
    demo_memory()
    demo_self_healing()
    demo_reflector()
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE")
    print("="*80)
    print("\nFramework is ready to use!")
    print("\nNext steps:")
    print("1. Run: python -m pytest tests/ui/test_segments.py -v")
    print("2. Review Allure reports")
    print("3. Start using adapters in tests (optional)")
    print("\nSee AGENT_FRAMEWORK_README.md for full documentation")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
