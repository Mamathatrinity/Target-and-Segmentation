"""
Example: Comprehensive Validation with Agent Adapters
Shows API + UI + DB validation with field-level checks in terminal and Allure.
"""
import pytest
import allure
from framework.adapters import APIAdapter, UIAdapter, DBAdapter
from framework.page_objects.segments_page import SegmentsPage
from framework.page_objects.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.segments_positive
def test_comprehensive_validation_example(page, api_validator, mysql_connection, settings):
    """
    Example: Comprehensive API + UI + DB Validation
    Shows detailed field-level validation in terminal and Allure reports.
    """
    
    print("\n" + "="*80)
    print("🤖 COMPREHENSIVE VALIDATION EXAMPLE")
    print("="*80)
    
    # Setup
    login_page = LoginPage(page, settings.APP_URL)
    segments_page = SegmentsPage(page, settings.APP_URL)
    
    # Login
    if not login_page.is_logged_in():
        login_page.perform_login(settings.TEST_USER_EMAIL, settings.TEST_USER_PASSWORD)
    
    segments_page.navigate_to_page()
    
    # Create adapters
    api_adapter = APIAdapter(api_validator, settings)
    ui_adapter = UIAdapter(page, SegmentsPage)
    db_adapter = DBAdapter(mysql_connection)
    
    # ========================================================================
    # STEP 1: API VALIDATION with detailed field checks
    # ========================================================================
    with allure.step("API Validation - Get Segments"):
        print("\n" + "▶"*40)
        print("STEP 1: API VALIDATION")
        print("▶"*40)
        
        # Get segments with comprehensive validation
        api_result, api_segments, total_count = api_adapter.get_segments(
            page=1, 
            per_page=10,
            validate=True  # Enable comprehensive validation
        )
        
        # The validation automatically:
        # - Validates HTTP status code
        # - Validates response structure (data, total fields exist)
        # - Validates pagination (page, per_page correct)
        # - Validates each segment has required fields (id, name)
        # - Prints detailed output to terminal
        # - Attaches results to Allure report
        
        # Additional custom field validation
        if api_segments:
            first_segment = api_segments[0]
            segment_id = first_segment.get("id")
            
            print(f"\n  → Testing detailed validation for segment ID: {segment_id}")
    
    # ========================================================================
    # STEP 2: UI VALIDATION with element and content checks
    # ========================================================================
    with allure.step("UI Validation - Segments Page"):
        print("\n" + "▶"*40)
        print("STEP 2: UI VALIDATION")
        print("▶"*40)
        
        # Comprehensive page validation
        ui_result = ui_adapter.validate_page(
            page_name="Segments List",
            element_checks=[
                {"name": "Page Title", "selector": "h1"},
                {"name": "Segments Table", "selector": "table"},
                {"name": "Create Button", "selector": ".create-segment-btn"}
            ],
            content_checks=[
                {"name": "Title Text", "selector": "h1", "expected": "Segments", "match_type": "contains"}
            ]
        )
        
        # The validation automatically:
        # - Checks all specified elements are visible
        # - Validates text content matches expectations
        # - Prints detailed output to terminal
        # - Takes screenshot
        # - Attaches results to Allure report
    
    # ========================================================================
    # STEP 3: DATABASE VALIDATION with field-level checks
    # ========================================================================
    with allure.step("Database Validation - Query Segment"):
        print("\n" + "▶"*40)
        print("STEP 3: DATABASE VALIDATION")
        print("▶"*40)
        
        if api_segments:
            segment_id = api_segments[0].get("id")
            expected_name = api_segments[0].get("name")
            
            # Get from database with comprehensive validation
            db_result, db_segment = db_adapter.get_segment_by_id(
                segment_id=segment_id,
                validate=True,  # Enable comprehensive validation
                expected_fields={
                    "name": expected_name,
                    "id": segment_id
                }
            )
            
            # The validation automatically:
            # - Validates query executed successfully
            # - Validates row count (exactly 1 record)
            # - Validates ID matches
            # - Validates required fields exist (name, description)
            # - Validates expected field values match
            # - Prints detailed output to terminal
            # - Attaches results to Allure report
    
    # ========================================================================
    # STEP 4: CROSS-LAYER VALIDATION (API vs Database)
    # ========================================================================
    with allure.step("Cross-Layer Validation - API vs Database"):
        print("\n" + "▶"*40)
        print("STEP 4: CROSS-LAYER VALIDATION")
        print("▶"*40)
        
        if api_segments and db_segment:
            api_segment = api_segments[0]
            
            # Compare API and DB data field-by-field
            cross_validation = db_adapter.cross_validate_with_api(
                api_segment=api_segment,
                db_segment=db_segment,
                fields=["id", "name", "description", "created_at"]
            )
            
            # The validation automatically:
            # - Compares each field between API and DB
            # - Prints detailed comparison to terminal
            # - Shows mismatches with specific values
            # - Attaches detailed comparison to Allure report
            
            # Assert cross-validation passed
            assert cross_validation["overall_match"], \
                f"Cross-validation failed: {cross_validation['errors']}"
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("✅ COMPREHENSIVE VALIDATION COMPLETE")
    print("="*80)
    print("\nValidation Summary:")
    print(f"  API Validation:    {'✅ PASS' if not api_result.errors else '❌ FAIL'}")
    print(f"  UI Validation:     {'✅ PASS' if not ui_result.errors else '❌ FAIL'}")
    print(f"  DB Validation:     {'✅ PASS' if not db_result.errors else '❌ FAIL'}")
    print(f"  Cross-Layer:       {'✅ PASS' if cross_validation['overall_match'] else '❌ FAIL'}")
    print("="*80 + "\n")
    
    # All validations in terminal output AND Allure report
    # Terminal shows: ✅/❌ icons, detailed field comparisons, clear sections
    # Allure shows: JSON responses, validation summaries, screenshots, cross-layer comparisons
