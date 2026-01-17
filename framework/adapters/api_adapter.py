"""
API Validator Adapter
Clean interface to MCP API validation tools with comprehensive validation.
"""
from typing import Dict, Any, Optional, List, Tuple
import allure


class APIValidationResult:
    """Structured API validation result with detailed field checks."""
    
    def __init__(self, endpoint: str, method: str = "GET"):
        self.endpoint = endpoint
        self.method = method
        self.status_code = 0
        self.response_data = {}
        self.validations = {
            "status_code": {"expected": None, "actual": None, "passed": False},
            "response_structure": {"expected": None, "actual": None, "passed": False},
            "field_validations": {}
        }
        self.errors = []
        
    def validate_status(self, expected: int, actual: int) -> bool:
        """Validate HTTP status code."""
        passed = expected == actual
        self.validations["status_code"] = {
            "expected": expected,
            "actual": actual,
            "passed": passed
        }
        if not passed:
            self.errors.append(f"Status code mismatch: expected {expected}, got {actual}")
        return passed
    
    def validate_field(self, field_name: str, expected: Any, actual: Any, 
                      validation_type: str = "equality") -> bool:
        """Validate individual field."""
        if validation_type == "equality":
            passed = expected == actual
        elif validation_type == "type":
            passed = type(actual).__name__ == expected
        elif validation_type == "not_null":
            passed = actual is not None
        elif validation_type == "contains":
            passed = expected in str(actual)
        else:
            passed = False
            
        self.validations["field_validations"][field_name] = {
            "expected": expected,
            "actual": actual,
            "validation_type": validation_type,
            "passed": passed
        }
        
        if not passed:
            self.errors.append(f"Field '{field_name}' validation failed: expected {expected}, got {actual}")
        
        return passed
    
    def print_summary(self):
        """Print detailed validation summary to terminal."""
        print("\n" + "="*80)
        print(f"  📡 API VALIDATION - {self.method} {self.endpoint}")
        print("="*80)
        
        # Status code
        status_val = self.validations["status_code"]
        status_icon = "✅" if status_val["passed"] else "❌"
        print(f"  HTTP Status: {status_val['actual']} {status_icon}")
        if status_val["expected"]:
            print(f"    Expected: {status_val['expected']}, Actual: {status_val['actual']}")
        
        # Response data summary
        if self.response_data:
            print(f"\n  📊 Response Data:")
            if isinstance(self.response_data, dict):
                if 'data' in self.response_data:
                    data = self.response_data['data']
                    if isinstance(data, list):
                        print(f"    📄 Records: {len(data)}")
                    elif isinstance(data, dict):
                        print(f"    📝 Fields: {len(data)}")
                        for key in list(data.keys())[:5]:  # Show first 5 keys
                            value = str(data[key])[:50]  # Truncate long values
                            print(f"        {key}: {value}")
                if 'total' in self.response_data:
                    print(f"    🔢 Total: {self.response_data['total']}")
                if 'page' in self.response_data:
                    print(f"    📚 Page: {self.response_data['page']}")
        
        # Field validations
        if self.validations["field_validations"]:
            passed_count = sum(1 for v in self.validations["field_validations"].values() if v["passed"])
            print(f"\n  🔍 Field Validations ({passed_count}/{len(self.validations['field_validations'])} passed):")
            for field, val in self.validations["field_validations"].items():
                icon = "✅" if val["passed"] else "❌"
                print(f"    {field}: {icon}")
                if val["validation_type"] == "type":
                    print(f"      Type: {val['expected']} (actual: {type(val['actual']).__name__})")
                else:
                    print(f"      Expected: {val['expected']}")
                    print(f"      Actual: {val['actual']}")
                    print(f"      Type: {val['validation_type']}")
        
        # Errors
        if self.errors:
            print(f"\n  ❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"    - {error}")
        else:
            print(f"\n  ✅ All validations passed!")
        
        print("="*80)
    
    def attach_to_allure(self):
        """Attach validation results to Allure report."""
        # Main summary with detailed information
        summary = "="*80 + "\n"
        summary += f"📡 API VALIDATION REPORT\n"
        summary += "="*80 + "\n\n"
        summary += f"Endpoint: {self.method} {self.endpoint}\n"
        summary += f"Status Code: {self.validations['status_code']['actual']}\n\n"
        
        # Status validation
        status_val = self.validations["status_code"]
        if status_val["expected"]:
            icon = "✅" if status_val["passed"] else "❌"
            summary += f"Status Validation: {icon}\n"
            summary += f"  Expected: {status_val['expected']}\n"
            summary += f"  Actual: {status_val['actual']}\n\n"
        
        # Response data summary
        if self.response_data and isinstance(self.response_data, dict):
            summary += "Response Summary:\n"
            summary += "-"*80 + "\n"
            if 'data' in self.response_data:
                data = self.response_data['data']
                if isinstance(data, list):
                    summary += f"  📄 Records: {len(data)}\n"
                elif isinstance(data, dict):
                    summary += f"  📝 Fields: {len(data)}\n"
            if 'total' in self.response_data:
                summary += f"  🔢 Total: {self.response_data['total']}\n"
            if 'page' in self.response_data:
                summary += f"  📚 Page: {self.response_data['page']}\n"
            summary += "\n"
        
        # Field validations
        if self.validations["field_validations"]:
            passed_count = sum(1 for v in self.validations["field_validations"].values() if v["passed"])
            summary += f"🔍 Field Validations: {passed_count}/{len(self.validations['field_validations'])} passed\n"
            summary += "-"*80 + "\n"
            for field, val in self.validations["field_validations"].items():
                icon = "✅" if val["passed"] else "❌"
                summary += f"  {field}: {icon}\n"
                if val["validation_type"] == "type":
                    summary += f"    Type: {val['expected']} (actual: {type(val['actual']).__name__})\n"
                else:
                    summary += f"    Expected: {val['expected']}\n"
                    summary += f"    Actual: {val['actual']}\n"
            summary += "\n"
        
        # Errors
        if self.errors:
            summary += f"❌ Errors ({len(self.errors)}):\n"
            for error in self.errors:
                summary += f"  - {error}\n"
        else:
            summary += "✅ All validations passed!\n"
        
        summary += "\n" + "="*80
        
        allure.attach(
            summary,
            name="📡 API Validation Summary",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # Attach full response
        import json
        allure.attach(
            json.dumps(self.response_data, indent=2),
            name="API Response Data (JSON)",
            attachment_type=allure.attachment_type.JSON
        )


class APIAdapter:
    """Adapter for API validation - wraps MCP api_validator."""
    
    def __init__(self, api_validator, settings):
        """
        Initialize API adapter.
        
        Args:
            api_validator: MCP API validator fixture from conftest
            settings: App settings with brand_id and other config
        """
        self.validator = api_validator
        self.settings = settings
        self.brand_id = getattr(settings, 'BRAND_ID', 'BR000001')
        
    def call_api(self, endpoint: str, method: str = "GET", 
                 params: Optional[Dict] = None, 
                 data: Optional[Dict] = None,
                 add_brand_id: bool = True) -> Tuple[Dict, int]:
        """
        Make API call with automatic brand_id injection.
        
        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, PUT, DELETE)
            params: Query parameters
            data: Request body data
            add_brand_id: Auto-add brand_id to params
            
        Returns:
            (response_data, status_code)
        """
        params = params or {}
        
        # Auto-inject brand_id if needed
        if add_brand_id and "brand_id" not in params:
            params["brand_id"] = self.brand_id
        
        with allure.step(f"API {method} {endpoint}"):
            result = self.validator.make_api_request(
                endpoint=endpoint,
                method=method,
                params=params,
                data=data  # Changed from json_data to data
            )
            
            status_code = result.get("status_code", 0)
            response_data = result.get("response", {})
            
            # Attach to Allure
            allure.attach(
                f"Endpoint: {endpoint}\nMethod: {method}\nStatus: {status_code}",
                name="API Request",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return response_data, status_code
    
    def get_segments(self, page: int = 1, per_page: int = 10, 
                    filter_type: Optional[str] = None,
                    validate: bool = True) -> Tuple[APIValidationResult, List, int]:
        """
        Get segments with pagination and comprehensive validation.
        
        Args:
            page: Page number
            per_page: Items per page
            filter_type: Optional filter (my_segments, all_segments)
            validate: Perform comprehensive validation
            
        Returns:
            (validation_result, segments_list, total_count)
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        if filter_type:
            params["filter"] = filter_type
        
        # Create validation result
        result = APIValidationResult("/api/segments", "GET")
        
        response, status = self.call_api("/api/segments", params=params)
        result.status_code = status
        result.response_data = response
        
        # Extract segments from response
        segments = response.get("data", [])
        total = response.get("total", len(segments))
        
        if validate:
            # Validate status code
            result.validate_status(200, status)
            
            # Validate response structure
            result.validate_field("data_exists", True, "data" in response, "equality")
            result.validate_field("total_exists", True, "total" in response, "equality")
            
            # Validate pagination
            result.validate_field("page", page, response.get("page", page), "equality")
            result.validate_field("per_page_limit", True, len(segments) <= per_page, "equality")
            
            # Validate each segment has required fields
            if segments:
                first_segment = segments[0]
                result.validate_field("segment_has_id", True, "id" in first_segment, "equality")
                result.validate_field("segment_has_name", True, "name" in first_segment, "equality")
            
            # Print and attach results
            result.print_summary()
            result.attach_to_allure()
        
        return result, segments, total
    
    def get_segment_by_id(self, segment_id: int, 
                         validate: bool = True,
                         expected_fields: Optional[Dict] = None) -> Tuple[APIValidationResult, Optional[Dict]]:
        """
        Get single segment by ID with field-level validation.
        
        Args:
            segment_id: Segment ID
            validate: Perform comprehensive validation
            expected_fields: Dict of field_name: expected_value for validation
            
        Returns:
            (validation_result, segment_data)
        """
        result = APIValidationResult(f"/api/segments/{segment_id}", "GET")
        
        response, status = self.call_api(f"/api/segments/{segment_id}")
        result.status_code = status
        result.response_data = response
        
        segment = response.get("data") if status == 200 else None
        
        if validate:
            # Validate status
            result.validate_status(200, status)
            
            if segment:
                # Validate required fields exist
                result.validate_field("id", segment_id, segment.get("id"), "equality")
                result.validate_field("name_exists", True, "name" in segment, "equality")
                result.validate_field("description_exists", True, "description" in segment, "equality")
                
                # Validate field types
                result.validate_field("id_type", "int", segment.get("id"), "type")
                result.validate_field("name_type", "str", segment.get("name"), "type")
                
                # Validate expected field values if provided
                if expected_fields:
                    for field, expected_value in expected_fields.items():
                        actual_value = segment.get(field)
                        result.validate_field(field, expected_value, actual_value, "equality")
            
            # Print and attach
            result.print_summary()
            result.attach_to_allure()
        
        return result, segment
    
    def create_segment(self, segment_data: Dict) -> Tuple[Optional[Dict], int]:
        """
        Create new segment via API.
        
        Returns:
            (created_segment, status_code)
        """
        response, status = self.call_api(
            "/api/segments",
            method="POST",
            data=segment_data
        )
        
        if status in (200, 201):
            return response.get("data"), status
        return None, status
    
    def update_segment(self, segment_id: int, segment_data: Dict) -> Tuple[Optional[Dict], int]:
        """Update segment via API."""
        response, status = self.call_api(
            f"/api/segments/{segment_id}",
            method="PUT",
            data=segment_data
        )
        
        if status == 200:
            return response.get("data"), status
        return None, status
    
    def delete_segment(self, segment_id: int) -> Tuple[bool, int]:
        """Delete segment via API."""
        response, status = self.call_api(
            f"/api/segments/{segment_id}",
            method="DELETE"
        )
        
        return status == 200, status
    
    def search_segments(self, query: str, page: int = 1, per_page: int = 10) -> Tuple[List, int]:
        """Search segments by query."""
        params = {
            "q": query,
            "page": page,
            "per_page": per_page
        }
        
        response, status = self.call_api("/api/segments/search", params=params)
        segments = response.get("data", [])
        total = response.get("total", len(segments))
        
        return segments, total
    
    def validate_response(self, expected_status: int, actual_status: int,
                         field_checks: Optional[Dict] = None) -> Dict:
        """
        Validate API response with detailed checking.
        
        Args:
            expected_status: Expected HTTP status code
            actual_status: Actual status code received
            field_checks: Dict of field_name: expected_value for validation
            
        Returns:
            Validation result dict with pass/fail status
        """
        validations = {
            "status_code": expected_status == actual_status,
            "fields": {}
        }
        
        if field_checks:
            for field, expected in field_checks.items():
                validations["fields"][field] = {
                    "expected": expected,
                    "passed": False  # Will be updated by caller with actual value
                }
        
        return validations
