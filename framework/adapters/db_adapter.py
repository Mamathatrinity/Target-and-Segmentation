"""
Database Validator Adapter
Clean interface to MCP database validation tools with comprehensive validation.
"""
from typing import Dict, Any, Optional, List, Tuple
import allure


class DBValidationResult:
    """Structured database validation result with detailed field checks."""
    
    def __init__(self, query_type: str):
        self.query_type = query_type
        self.query = ""
        self.row_count = 0
        self.data = []
        self.validations = {
            "query_executed": {"expected": True, "actual": False, "passed": False},
            "row_count": {"expected": None, "actual": None, "passed": False},
            "field_validations": {}
        }
        self.errors = []
        
    def validate_row_count(self, expected: int, actual: int, 
                          comparison: str = "equality") -> bool:
        """Validate row count."""
        if comparison == "equality":
            passed = expected == actual
        elif comparison == "greater_than":
            passed = actual > expected
        elif comparison == "less_than":
            passed = actual < expected
        elif comparison == "at_least":
            passed = actual >= expected
        else:
            passed = False
            
        self.validations["row_count"] = {
            "expected": expected,
            "actual": actual,
            "comparison": comparison,
            "passed": passed
        }
        
        if not passed:
            self.errors.append(f"Row count validation failed: expected {comparison} {expected}, got {actual}")
        
        return passed
    
    def validate_field(self, record_index: int, field_name: str, 
                      expected: Any, actual: Any,
                      validation_type: str = "equality") -> bool:
        """Validate field in a specific record."""
        if validation_type == "equality":
            passed = expected == actual
        elif validation_type == "not_null":
            passed = actual is not None
        elif validation_type == "type":
            passed = type(actual).__name__ == expected
        elif validation_type == "contains":
            passed = expected in str(actual)
        else:
            passed = False
        
        key = f"record_{record_index}_{field_name}"
        self.validations["field_validations"][key] = {
            "record_index": record_index,
            "field": field_name,
            "expected": expected,
            "actual": actual,
            "validation_type": validation_type,
            "passed": passed
        }
        
        if not passed:
            self.errors.append(
                f"Record {record_index}, field '{field_name}': expected {expected}, got {actual}"
            )
        
        return passed
    
    def print_summary(self):
        """Print detailed validation summary to terminal."""
        print("\n" + "="*80)
        print(f"  🗄️  DATABASE VALIDATION - {self.query_type}")
        print("="*80)
        
        # Query info
        print(f"  Query: {self.query[:100]}{'...' if len(self.query) > 100 else ''}")
        
        # Row count
        row_val = self.validations["row_count"]
        if row_val["expected"] is not None:
            icon = "✅" if row_val["passed"] else "❌"
            print(f"  Row Count: {row_val['actual']} {icon}")
            print(f"    Expected: {row_val.get('comparison', 'equality')} {row_val['expected']}")
        else:
            print(f"  Row Count: {self.row_count}")
        
        # Sample data from first record
        if self.data and len(self.data) > 0:
            print(f"\n  📊 Sample Data (First Record):")
            first_record = self.data[0]
            field_count = 0
            for key, value in first_record.items():
                if field_count >= 8:  # Limit to first 8 fields
                    break
                # Truncate long values
                str_value = str(value)
                if len(str_value) > 50:
                    str_value = str_value[:47] + "..."
                print(f"    {key}: {str_value}")
                field_count += 1
            if len(first_record) > 8:
                print(f"    ... and {len(first_record) - 8} more fields")
        
        # Field validations
        if self.validations["field_validations"]:
            passed_count = sum(1 for v in self.validations["field_validations"].values() if v["passed"])
            print(f"\n  🔍 Field Validations ({passed_count}/{len(self.validations['field_validations'])} passed):")
            for key, val in self.validations["field_validations"].items():
                icon = "✅" if val["passed"] else "❌"
                print(f"    Record {val['record_index']}, {val['field']}: {icon}")
                print(f"      Expected: {val['expected']}")
                print(f"      Actual: {val['actual']}")
        
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
        import json
        
        summary = "="*80 + "\n"
        summary += f"🗄️  DATABASE VALIDATION REPORT\n"
        summary += "="*80 + "\n\n"
        summary += f"Query Type: {self.query_type}\n"
        summary += f"Query: {self.query}\n"
        summary += f"Row Count: {self.row_count}\n\n"
        
        # Row count validation
        row_val = self.validations["row_count"]
        if row_val["expected"] is not None:
            icon = "✅" if row_val["passed"] else "❌"
            summary += f"Row Count Validation: {icon}\n"
            summary += f"  Expected: {row_val.get('comparison', 'equality')} {row_val['expected']}\n"
            summary += f"  Actual: {row_val['actual']}\n\n"
        
        # Sample data from first record
        if self.data and len(self.data) > 0:
            summary += "📊 Sample Data (First Record):\n"
            summary += "-"*80 + "\n"
            first_record = self.data[0]
            for key, value in first_record.items():
                str_value = str(value)
                if len(str_value) > 100:
                    str_value = str_value[:97] + "..."
                summary += f"  {key}: {str_value}\n"
            summary += "\n"
        
        # Field validations
        if self.validations["field_validations"]:
            passed_count = sum(1 for v in self.validations["field_validations"].values() if v["passed"])
            summary += f"Field Validations: {passed_count}/{len(self.validations['field_validations'])} passed\n"
            summary += "-"*80 + "\n"
            for key, val in self.validations["field_validations"].items():
                icon = "✅" if val["passed"] else "❌"
                summary += f"  Record {val['record_index']}, {val['field']}: {icon}\n"
                summary += f"    Expected: {val['expected']}\n"
                summary += f"    Actual: {val['actual']}\n"
            summary += "\n"
        
        # Errors
        if self.errors:
            summary += f"Errors ({len(self.errors)}):\n"
            for error in self.errors:
                summary += f"  ❌ {error}\n"
        else:
            summary += "✅ All validations passed!\n"
        
        summary += "\n" + "="*80
        
        allure.attach(
            summary,
            name="🗄️  Database Validation Summary",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # Also attach full query results as JSON
        if self.data:
            allure.attach(
                json.dumps(self.data[:10], indent=2, default=str),  # First 10 records
                name="Database Query Results (JSON)",
                attachment_type=allure.attachment_type.JSON
            )
        
        # Attach data sample
        if self.data:
            import json
            sample = self.data[:5]  # First 5 records
            allure.attach(
                json.dumps(sample, indent=2, default=str),
                name="Database Records Sample",
                attachment_type=allure.attachment_type.JSON
            )


class DBAdapter:
    """Adapter for database validation - wraps MCP mysql_connection."""
    
    def __init__(self, mysql_connection, db_helpers_module=None):
        """
        Initialize DB adapter.
        
        Args:
            mysql_connection: MCP MySQL connection fixture
            db_helpers_module: Module with DB helper functions
        """
        self.connection = mysql_connection
        self.helpers = db_helpers_module
        
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict]:
        """
        Execute SELECT query and return results.
        
        Returns list of dicts (rows).
        """
        if not self.connection:
            return []
        
        with allure.step(f"DB Query: {query[:100]}..."):
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            allure.attach(
                f"Query: {query}\nRows: {len(results)}",
                name="Database Query",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return results
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected rows."""
        if not self.connection:
            return 0
        
        cursor = self.connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        self.connection.commit()
        return cursor.rowcount
    
    def get_segments(self, page: int = 1, per_page: int = 10) -> Tuple[List[Dict], int]:
        """
        Get segments with pagination.
        
        Returns:
            (segments_list, total_count)
        """
        offset = (page - 1) * per_page
        
        # Get segments
        query = f"SELECT * FROM segments LIMIT {per_page} OFFSET {offset}"
        segments = self.execute_query(query)
        
        # Get total count
        count_query = "SELECT COUNT(*) as total FROM segments"
        count_result = self.execute_query(count_query)
        total = count_result[0]['total'] if count_result else 0
        
        return segments, total
    
    def get_segment_by_id(self, segment_id: int, 
                         validate: bool = True,
                         expected_fields: Optional[Dict] = None) -> Tuple[DBValidationResult, Optional[Dict]]:
        """
        Get single segment by ID with field-level validation.
        
        Args:
            segment_id: Segment ID
            validate: Perform comprehensive validation
            expected_fields: Dict of field_name: expected_value for validation
            
        Returns:
            (validation_result, segment_data)
        """
        result = DBValidationResult("SELECT_BY_ID")
        query = "SELECT * FROM segments WHERE id = %s"
        result.query = query
        
        results = self.execute_query(query, (segment_id,))
        result.row_count = len(results)
        result.data = results
        
        segment = results[0] if results else None
        
        if validate:
            # Validate query execution
            result.validations["query_executed"]["actual"] = True
            result.validations["query_executed"]["passed"] = True
            
            # Validate row count
            result.validate_row_count(1, len(results), "equality")
            
            if segment:
                # Validate ID matches
                result.validate_field(0, "id", segment_id, segment.get("id"), "equality")
                
                # Validate required fields exist
                result.validate_field(0, "name", True, segment.get("name") is not None, "equality")
                result.validate_field(0, "description", True, segment.get("description") is not None, "equality")
                
                # Validate expected field values if provided
                if expected_fields:
                    for field, expected_value in expected_fields.items():
                        actual_value = segment.get(field)
                        result.validate_field(0, field, expected_value, actual_value, "equality")
            
            # Print and attach
            result.print_summary()
            result.attach_to_allure()
        
        return result, segment
    
    def create_segment(self, segment_data: Dict) -> int:
        """
        Create segment in database.
        
        Returns: segment_id of created record
        """
        # Build INSERT query from segment_data
        columns = ', '.join(segment_data.keys())
        placeholders = ', '.join(['%s'] * len(segment_data))
        query = f"INSERT INTO segments ({columns}) VALUES ({placeholders})"
        
        cursor = self.connection.cursor()
        cursor.execute(query, tuple(segment_data.values()))
        self.connection.commit()
        
        return cursor.lastrowid
    
    def update_segment(self, segment_id: int, segment_data: Dict) -> int:
        """Update segment in database."""
        set_clause = ', '.join([f"{k} = %s" for k in segment_data.keys()])
        query = f"UPDATE segments SET {set_clause} WHERE id = %s"
        
        params = list(segment_data.values()) + [segment_id]
        return self.execute_update(query, tuple(params))
    
    def delete_segment(self, segment_id: int) -> int:
        """Delete segment from database."""
        query = "DELETE FROM segments WHERE id = %s"
        return self.execute_update(query, (segment_id,))
    
    def search_segments(self, query_text: str) -> List[Dict]:
        """Search segments by name or description."""
        query = """
            SELECT * FROM segments  with detailed terminal output.
        
        Args:
            api_segment: Segment data from API
            db_segment: Segment data from database
            fields: List of fields to compare
            
        Returns:
            Validation result with field-by-field comparison
        """
        validations = {
            "overall_match": True,
            "fields": {},
            "errors": []
        }
        
        print("\n" + "="*80)
        print("  CROSS-LAYER VALIDATION - API vs Database")
        print("="*80)
        
        for field in fields:
            api_value = api_segment.get(field)
            db_value = db_segment.get(field)
            matches = api_value == db_value
            
            validations["fields"][field] = {
                "api": api_value,
                "db": db_value,
                "match": matches
            }
            
            icon = "✅" if matches else "❌"
            print(f"  {field}: {icon}")
            print(f"    API:  {api_value}")
            print(f"    DB:   {db_value}")
            
            if not matches:
                validations["overall_match"] = False
                error_msg = f"Mismatch in '{field}': API={api_value}, DB={db_value}"
                validations["errors"].append(error_msg)
        
        if validations["overall_match"]:
            print(f"\n  ✅ All fields match across API and Database!")
        else:
            print(f"\n  ❌ Found {len(validations['errors'])} mismatches:")
            for error in validations["errors"]:
                print(f"    - {error}")
        
        print("="*80)
        
        # Allure attachment
        with allure.step("Cross-Layer Validation"):
            result_text = "API vs Database Comparison\n\n"
            for field, v in validations["fields"].items():
                icon = "✅" if v["match"] else "❌"
                result_text += f"{field}: {icon}\n"
                result_text += f"  API:  {v['api']}\n"
                result_text += f"  DB:   {v['db']}\n\n"
            
            if validations["errors"]:
                result_text += "Errors:\n"
                for error in validations["errors"]:
                    result_text += f"  - {error}\n"
            
            allure.attach(result_text, name="Cross-Layer Validation Details", attachment_type=allure.attachment_type.TEXT)
        return {
            "field": field,
            "expected": expected_value,
            "actual": actual_value,
            "passed": matches
        }
    
    def cross_validate_with_api(self, api_segment: Dict, db_segment: Dict, 
                                fields: List[str]) -> Dict:
        """
        Cross-validate API and DB data.
        
        Args:
            api_segment: Segment data from API
            db_segment: Segment data from database
            fields: List of fields to compare
            
        Returns:
            Validation result with field-by-field comparison
        """
        validations = {
            "overall_match": True,
            "fields": {}
        }
        
        for field in fields:
            api_value = api_segment.get(field)
            db_value = db_segment.get(field)
            matches = api_value == db_value
            
            validations["fields"][field] = {
                "api": api_value,
                "db": db_value,
                "match": matches
            }
            
            if not matches:
                validations["overall_match"] = False
        
        with allure.step("Cross-Layer Validation"):
            result_text = "\n".join([
                f"{field}: API={v['api']}, DB={v['db']}, Match={v['match']}"
                for field, v in validations["fields"].items()
            ])
            allure.attach(result_text, name="API vs DB Comparison", 
                         attachment_type=allure.attachment_type.TEXT)
        
        return validations
