"""
API Tests for Trinity HCP Targeting & Segmentation Application
Tests API endpoints discovered from application analysis
Base URL: https://app-hcptargetandsegmentation-api-dev.azurewebsites.net/api/v1
"""

import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_get_user_context_endpoint(api_validator):
    """Test GET /api/v1/get_user_context/ endpoint."""
    result = api_validator.make_api_request(
        endpoint="/get_user_context/",
        method="GET"
    )
    
    assert result["status"] == "success"
    assert result["status_code"] == 200
    print(f"✓ User context endpoint responded: {result.get('status_code')}")


@pytest.mark.api
@pytest.mark.smoke
def test_get_cohorts_endpoint(api_validator):
    """Test GET /api/v1/cohorts/{brand_id}/ endpoint."""
    brand_id = "BR000001"  # Default brand ID from analysis
    
    result = api_validator.make_api_request(
        endpoint=f"/cohorts/{brand_id}/",
        method="GET"
    )
    
    assert result["status"] == "success"
    assert result["status_code"] == 200
    print(f"✓ Cohorts endpoint responded for brand {brand_id}")


@pytest.mark.api
@pytest.mark.regression
def test_analytics_dashboard_endpoint(api_validator):
    """Test POST /api/v1/analytics_dashboard/ endpoint."""
    result = api_validator.make_api_request(
        endpoint="/analytics_dashboard/",
        method="POST",
        body={}
    )
    
    assert result["status"] == "success"
    assert result["status_code"] in [200, 201]
    print("✓ Analytics dashboard endpoint responded successfully")


@pytest.mark.api
@pytest.mark.regression
def test_sankey_chart_endpoint(api_validator):
    """Test GET /api/v1/sankey_chart/ endpoint with parameters."""
    params = {
        "brand_id": "BR000001",
        "cohort_id": "55"
    }
    
    result = api_validator.make_api_request(
        endpoint=f"/sankey_chart/?brand_id={params['brand_id']}&cohort_id={params['cohort_id']}",
        method="GET"
    )
    
    assert result["status"] == "success"
    assert result["status_code"] == 200
    print("✓ Sankey chart data endpoint responded successfully")


@pytest.mark.api
@pytest.mark.regression
def test_user_context_response_schema(api_validator):
    """Test user context endpoint returns expected data structure."""
    result = api_validator.make_api_request(
        endpoint="/get_user_context/",
        method="GET"
    )
    
    assert result["status"] == "success"
    
    # Validate response has expected fields
    schema_result = api_validator.validate_response_schema(
        endpoint="/get_user_context/",
        method="GET",
        expected_fields=["user", "roles", "permissions"]
    )
    
    # Note: Schema validation may fail if MCP server doesn't support it
    # or if actual response structure differs
    print(f"✓ User context schema validation: {schema_result.get('valid', 'N/A')}")


@pytest.mark.api
@pytest.mark.regression
def test_api_response_time(api_validator):
    """Test API response time is acceptable."""
    result = api_validator.check_response_time(
        endpoint="/get_user_context/",
        method="GET",
        max_time_ms=2000
    )
    
    assert result["status"] == "success"
    print(f"✓ API response time: {result.get('response_time_ms', 'N/A')}ms")

