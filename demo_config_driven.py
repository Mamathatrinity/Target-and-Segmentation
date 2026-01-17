"""
Demo: Using API Contracts and UI Locators
Shows how configuration files make testing data-driven.
"""
from framework.adapters import get_config_loader


def demo_api_contracts():
    """Demo: API Contract Validation"""
    print("\n" + "="*80)
    print("DEMO: API Contract - Data-Driven API Validation")
    print("="*80)
    
    loader = get_config_loader()
    
    # Get contract for segments list endpoint
    contract = loader.get_api_contract('segments', 'list')
    
    print(f"\n✅ Loaded contract for: {contract['endpoint']}")
    print(f"   Method: {contract['method']}")
    print(f"   Expected Status: {contract['response']['status_code']}")
    print(f"   Required Parameters: {contract['parameters']['required']}")
    print(f"   Response Structure: {contract['response']['structure']}")
    
    print(f"\n   Required Fields:")
    for field in contract['response']['fields']:
        if field.get('required'):
            print(f"     • {field['name']} ({field['type']})")
    
    # Simulate response validation
    print(f"\n   Simulating Response Validation...")
    mock_response = {
        'status_code': 200,
        'data': {
            'segment_id': 'SEG_001',
            'segment_name': 'Test Segment',
            'status': 'active',
            'record_count': 1000,
            'created_by': 'user@test.com',
            'created_date': '2026-01-16T10:00:00Z',
            'brand_id': 'BR000001'
        }
    }
    
    validation = loader.validate_api_response('segments', 'get_by_id', mock_response)
    
    if validation['valid']:
        print(f"   ✅ Response is VALID")
    else:
        print(f"   ❌ Response has errors:")
        for error in validation['errors']:
            print(f"      • {error}")


def demo_ui_locators():
    """Demo: UI Locators from Config"""
    print("\n" + "="*80)
    print("DEMO: UI Locators - Separation of Concerns")
    print("="*80)
    
    loader = get_config_loader()
    
    # Get locators for segments page
    search_box = loader.get_locator('segments', 'list_page', 'search_box')
    create_btn = loader.get_locator('segments', 'list_page', 'create_button')
    
    print(f"\n✅ Loaded UI Locators:")
    print(f"   Search Box: {search_box}")
    print(f"   Create Button: {create_btn}")
    
    # Get dynamic locator
    segment_row = loader.get_locator('segments', 'list_page', 'segment_row', segment_id='SEG_001')
    print(f"   Segment Row (SEG_001): {segment_row}")
    
    # Get locator info
    info = loader.get_locator_info('segments', 'list_page', 'search_box')
    print(f"\n   Locator Info:")
    print(f"     Selector: {info['selector']}")
    print(f"     Type: {info['type']}")
    print(f"     Description: {info['description']}")
    
    print(f"\n   Benefits:")
    print(f"     ✅ Locators separate from test code")
    print(f"     ✅ Easy to update when UI changes")
    print(f"     ✅ Reusable across tests")
    print(f"     ✅ Self-documenting")


def demo_multi_app():
    """Demo: Multi-App Support"""
    print("\n" + "="*80)
    print("DEMO: Multi-App Configuration")
    print("="*80)
    
    loader = get_config_loader()
    
    # Show different apps
    print(f"\n✅ Configured Applications:")
    
    apps = ['segments', 'target_list', 'universe_summary']
    for app in apps:
        try:
            contract = loader.get_api_contract(app, 'list')
            print(f"   • {app.upper()}")
            print(f"     API: {contract['endpoint']}")
        except:
            contract = loader.api_contracts.get(app, {})
            if contract:
                print(f"   • {app.upper()}")
                print(f"     Endpoints: {', '.join(contract.keys())}")


def main():
    """Run all demos"""
    print("\n" + "="*80)
    print("🎯 Configuration-Driven Testing Demo")
    print("="*80)
    
    demo_api_contracts()
    demo_ui_locators()
    demo_multi_app()
    
    print("\n" + "="*80)
    print("✅ Demo Complete!")
    print("\nWhat This Gives You:")
    print("   📋 API contracts define expected structure")
    print("   🎯 UI locators separate from test code")
    print("   🔄 Change config, not code, when API/UI changes")
    print("   📊 Automatic validation against contracts")
    print("   🌐 Multi-app support built-in")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
