"""
Demo: ChatGPT Architecture Components
Shows planner, executor, and validation agent in action.
"""
from framework.agent import get_planner, get_executor, get_validation_agent


def demo_planner():
    """Demo: Test Planner creates execution strategy"""
    print("\n" + "="*80)
    print("DEMO 1: PLANNER - Creating Execution Strategy")
    print("="*80)
    
    planner = get_planner()
    
    # Create plan for segment tests
    plan = planner.create_execution_plan(
        app_name='segments',
        test_ids=['pos_001', 'pos_002', 'pos_003', 'pos_007', 'pos_010']
    )
    
    print(f"\n✅ Plan created with {plan['total_tests']} tests")
    print(f"   Estimated duration: {plan['estimated_duration']}s")
    print(f"   Risk level: {plan['risk_level']}")
    
    return plan


def demo_executor(plan):
    """Demo: Test Executor runs the plan"""
    print("\n" + "="*80)
    print("DEMO 2: EXECUTOR - Executing Test Plan")
    print("="*80)
    
    executor = get_executor()
    
    # Execute the plan
    # results = executor.execute_plan(plan, auto_heal=True)
    
    # For demo, execute single test
    result = executor.execute_single_test('segments', 'pos_001', auto_heal=True)
    
    print(f"\n✅ Execution complete")
    print(f"   Status: {result['status']}")
    print(f"   Duration: {result['duration']}s")
    
    return result


def demo_validation_agent():
    """Demo: Validation Agent (simulated - needs fixtures)"""
    print("\n" + "="*80)
    print("DEMO 3: VALIDATION AGENT - Multi-Layer Validation")
    print("="*80)
    
    agent = get_validation_agent()
    
    print("\nValidation Agent supports:")
    print("   ✅ API validation with field-level checks")
    print("   ✅ UI validation with element checks")
    print("   ✅ Database validation with field checks")
    print("   ✅ Cross-layer validation (API vs DB)")
    
    print("\nUsage example:")
    print("""
    agent.initialize(api_validator, page, db_validator)
    results = agent.validate_all_layers(
        segment_id="SEG_001",
        expected_data={"segment_name": "Test", "status": "active"}
    )
    """)
    
    print("\n✅ Validation agent ready for use in tests")


def main():
    """Run all demos"""
    print("\n" + "="*80)
    print("🤖 ChatGPT Architecture Demo")
    print("Demonstrating: Planner → Executor → Validation Agent")
    print("="*80)
    
    # Demo 1: Planner
    plan = demo_planner()
    
    # Demo 2: Executor
    # result = demo_executor(plan)
    print("\n(Skipping executor demo - would run actual tests)")
    
    # Demo 3: Validation Agent
    demo_validation_agent()
    
    print("\n" + "="*80)
    print("✅ Demo Complete!")
    print("\nAll ChatGPT components are now available:")
    print("   📋 Planner - framework/agent/planner.py")
    print("   ▶️  Executor - framework/agent/executor.py")
    print("   🔍 Validation Agent - framework/agent/validation_agent.py")
    print("   🧠 Memory - framework/agent/memory.py")
    print("   🔧 Self-Healing - framework/agent/self_healing.py")
    print("   💭 Reflector - framework/agent/reflector.py")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
