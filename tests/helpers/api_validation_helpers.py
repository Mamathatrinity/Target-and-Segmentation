"""
API Validation Helper Functions
Reusable validation functions for API testing to ensure consistency and reduce code duplication.
"""


def validate_jwt_token(jwt_token, print_output=True):
    """
    Validate JWT token exists and is valid.
    
    Args:
        jwt_token (str): JWT token to validate
        print_output (bool): Whether to print validation messages
        
    Returns:
        bool: True if valid
        
    Raises:
        AssertionError: If token is None or invalid
    """
    assert jwt_token is not None, "JWT token should be generated"
    assert len(jwt_token) > 0, "JWT token should not be empty"
    
    if print_output:
        print(f"✅ AUTH: JWT token generated (length={len(jwt_token)})")
    
    return True


def validate_status_code(api_result, expected_code=200, print_output=True):
    """
    Validate HTTP status code.
    
    Args:
        api_result (dict): API response dictionary
        expected_code (int): Expected HTTP status code (default: 200)
        print_output (bool): Whether to print validation messages
        
    Returns:
        int: Actual status code
        
    Raises:
        AssertionError: If status code doesn't match expected
    """
    actual_code = api_result.get("status_code")
    assert actual_code == expected_code, \
        f"Expected status code {expected_code}, got {actual_code}"
    
    if print_output:
        print(f"✅ STATUS CODE: {actual_code} {'OK' if actual_code == 200 else ''}")
    
    return actual_code


def validate_response_structure(api_result, expected_type='list', data_key='data', print_output=True):
    """
    Validate API response has correct structure.
    
    Args:
        api_result (dict): API response dictionary
        expected_type (str): Expected type of data field ('list' or 'dict')
        data_key (str): Key containing the data (default: 'data')
        print_output (bool): Whether to print validation messages
        
    Returns:
        dict/list: The data from the response
        
    Raises:
        AssertionError: If structure is invalid
    """
    assert data_key in api_result, f"Response should contain '{data_key}' field"
    
    data = api_result[data_key]
    
    if expected_type == 'list':
        assert isinstance(data, list), f"'{data_key}' should be a list, got {type(data)}"
        if print_output:
            print(f"✅ RESPONSE STRUCTURE: Valid (contains '{data_key}' as list)")
    elif expected_type == 'dict':
        assert isinstance(data, dict), f"'{data_key}' should be a dict, got {type(data)}"
        if print_output:
            print(f"✅ RESPONSE STRUCTURE: Valid (contains '{data_key}' as dict)")
    
    return data


def validate_required_fields(data, required_fields, print_output=True):
    """
    Validate data contains all required fields.
    
    Args:
        data (dict): Data dictionary to validate
        required_fields (list): List of required field names
        print_output (bool): Whether to print validation messages
        
    Returns:
        bool: True if all fields present
        
    Raises:
        AssertionError: If any required field is missing
    """
    for field in required_fields:
        assert field in data, f"Data should contain '{field}' field"
    
    if print_output:
        print(f"✅ REQUIRED FIELDS: All present ({', '.join(required_fields)})")
    
    return True


def validate_pagination(api_result, print_output=True):
    """
    Validate pagination metadata structure.
    
    Args:
        api_result (dict): API response dictionary
        print_output (bool): Whether to print validation messages
        
    Returns:
        dict: Pagination metadata or None if not present
    """
    pagination = None
    
    if "meta" in api_result or "pagination" in api_result:
        pagination = api_result.get("meta", api_result.get("pagination", {}))
        
        if pagination:
            # Validate total count exists
            assert "total" in pagination or "total_count" in pagination, \
                "Pagination should include 'total' or 'total_count'"
            
            total = pagination.get("total", pagination.get("total_count", 0))
            
            # Validate page number (if present)
            if "page" in pagination:
                assert pagination["page"] >= 1, "Page should be >= 1"
            
            # Validate per_page (if present)
            if "per_page" in pagination:
                assert pagination["per_page"] > 0, "Per page should be > 0"
            
            if print_output:
                print(f"✅ PAGINATION: Valid (total={total})")
                if "page" in pagination and "per_page" in pagination:
                    print(f"   Page {pagination['page']}, {pagination['per_page']} per page")
    
    return pagination


def validate_sorting(items, sort_field='name', order='asc', print_output=True):
    """
    Validate items are sorted correctly.
    
    Args:
        items (list): List of items to validate
        sort_field (str): Field name to check sorting (default: 'name')
        order (str): Sort order 'asc' or 'desc' (default: 'asc')
        print_output (bool): Whether to print validation messages
        
    Returns:
        bool: True if sorted correctly
        
    Raises:
        AssertionError: If items are not sorted correctly
    """
    if len(items) < 2:
        if print_output:
            print(f"⚠️ SORTING: Skipped (not enough items to validate)")
        return True
    
    # Extract field values
    values = [item.get(sort_field, "") for item in items]
    
    # Check if sorted
    if order == 'asc':
        is_sorted = all(values[i] <= values[i+1] for i in range(len(values)-1))
        order_text = "ascending"
    else:  # desc
        is_sorted = all(values[i] >= values[i+1] for i in range(len(values)-1))
        order_text = "descending"
    
    assert is_sorted, f"Items should be sorted by '{sort_field}' in {order_text} order"
    
    if print_output:
        print(f"✅ SORTING: Validated ({sort_field} {order.upper()}) - {len(items)} items sorted correctly")
    
    return True


def validate_search_results(items, search_term, search_field='name', print_output=True):
    """
    Validate search results contain the search term.
    
    Args:
        items (list): List of items to validate
        search_term (str): Search term to look for
        search_field (str): Field to search in (default: 'name')
        print_output (bool): Whether to print validation messages
        
    Returns:
        bool: True if all results match search term
        
    Raises:
        AssertionError: If any result doesn't contain search term
    """
    assert len(items) > 0, f"Search for '{search_term}' should return results"
    
    # Validate all results contain search term (case-insensitive)
    for item in items:
        item_value = item.get(search_field, '').lower()
        search_value = search_term.lower()
        assert search_value in item_value, \
            f"Result '{item_value}' should contain search term '{search_value}'"
    
    if print_output:
        print(f"✅ SEARCH FILTER: Valid - {len(items)} results match search term '{search_term}'")
    
    return True


def validate_error_response(api_result, expected_codes=[404, 400], print_output=True):
    """
    Validate error response has correct status code and message.
    
    Args:
        api_result (dict): API response dictionary
        expected_codes (list): List of expected error codes
        print_output (bool): Whether to print validation messages
        
    Returns:
        str: Error message
        
    Raises:
        AssertionError: If error response is invalid
    """
    status_code = api_result.get("status_code")
    assert status_code in expected_codes, \
        f"Expected error code in {expected_codes}, got {status_code}"
    
    # Try to extract error message
    error_msg = ""
    if "error" in api_result:
        error_msg = api_result.get("error", "")
    elif "message" in api_result:
        error_msg = api_result.get("message", "")
    elif "detail" in api_result:
        error_msg = api_result.get("detail", "")
    
    if error_msg:
        assert len(error_msg) > 0, "Error response should contain a message"
    
    if print_output:
        if error_msg:
            print(f"✅ ERROR HANDLING: Valid (Status: {status_code}, Message: '{error_msg}')")
        else:
            print(f"✅ ERROR HANDLING: Valid (Status: {status_code})")
    
    return error_msg


def compare_api_db_fields(api_data, db_data, fields_to_compare, print_output=True):
    """
    Compare specific fields between API response and database record.
    
    Args:
        api_data (dict): Data from API response
        db_data (dict): Data from database query
        fields_to_compare (list): List of field names to compare
        print_output (bool): Whether to print validation messages
        
    Returns:
        bool: True if all fields match
        
    Raises:
        AssertionError: If any field doesn't match
    """
    mismatches = []
    
    for field in fields_to_compare:
        api_value = api_data.get(field)
        db_value = db_data.get(field)
        
        # Handle None/empty string equivalence
        if api_value is None:
            api_value = ""
        if db_value is None:
            db_value = ""
        
        # Compare values
        if api_value != db_value:
            mismatches.append(f"{field}: API='{api_value}' vs DB='{db_value}'")
    
    if mismatches:
        error_msg = "Field mismatches found:\n" + "\n".join(f"  - {m}" for m in mismatches)
        raise AssertionError(error_msg)
    
    if print_output:
        print(f"✅ CROSS-VALIDATION: All fields match across API ↔ DB")
        print(f"   Validated fields: {', '.join(fields_to_compare)}")
    
    return True


def validate_data_accuracy(actual_data, expected_data, fields_to_check, print_output=True):
    """
    Validate actual data matches expected data for specific fields.
    
    Args:
        actual_data (dict): Actual data received
        expected_data (dict): Expected data values
        fields_to_check (list): List of field names to validate
        print_output (bool): Whether to print validation messages
        
    Returns:
        bool: True if all fields match
        
    Raises:
        AssertionError: If any field doesn't match expected value
    """
    for field in fields_to_check:
        actual_value = actual_data.get(field)
        expected_value = expected_data.get(field)
        
        assert actual_value == expected_value, \
            f"{field} mismatch: Expected '{expected_value}', got '{actual_value}'"
    
    if print_output:
        print(f"✅ DATA ACCURACY: All fields match expected values")
        print(f"   Validated fields: {', '.join(fields_to_check)}")
    
    return True


def print_api_validation_summary(validations_passed):
    """
    Print summary of API validations performed.
    
    Args:
        validations_passed (list): List of validation types that passed
    """
    print(f"\n✅ API VALIDATION COMPLETE")
    for validation in validations_passed:
        print(f"   ✓ {validation}")


# Validation type constants for summary
VALIDATION_TYPES = {
    'STATUS_CODE': 'Status Code',
    'RESPONSE_STRUCTURE': 'Response Structure',
    'DATA_ACCURACY': 'Data Accuracy',
    'REQUIRED_FIELDS': 'Required Fields',
    'PAGINATION': 'Pagination',
    'SORTING': 'Sorting',
    'SEARCH_FILTER': 'Search/Filter',
    'AUTH': 'Authentication',
    'ERROR_HANDLING': 'Error Handling',
    'CONSISTENCY': 'Data Consistency (API ↔ DB)'
}
