"""
Validation Agent - Orchestrates comprehensive validation
Coordinates API, UI, and Database validation across all layers.
"""
from typing import Dict, List, Optional, Any
from datetime import datetime

from framework.adapters import APIAdapter, UIAdapter, DBAdapter
from framework.adapters import APIValidationResult, UIValidationResult, DBValidationResult
from .memory import get_memory


class ValidationAgent:
    """
    Central validation orchestrator.
    Coordinates multi-layer validation (API, UI, DB) and cross-validation.
    """
    
    def __init__(self):
        self.memory = get_memory()
        self.api = None
        self.ui = None
        self.db = None
        
    def initialize(self, api_validator=None, ui_page=None, db_validator=None):
        """
        Initialize validation adapters.
        
        Args:
            api_validator: MCP API validator fixture
            ui_page: Playwright page object
            db_validator: MCP DB validator fixture
        """
        if api_validator:
            self.api = APIAdapter(api_validator)
        if ui_page:
            self.ui = UIAdapter(ui_page)
        if db_validator:
            self.db = DBAdapter(db_validator)
    
    def validate_all_layers(self, segment_id: str, expected_data: Dict) -> Dict:
        """
        Validate segment across all layers: API, UI, and Database.
        
        Args:
            segment_id: Segment ID to validate
            expected_data: Expected field values
            
        Returns:
            Comprehensive validation results from all layers
        """
        print(f"\n{'='*80}")
        print(f"🔍 VALIDATION AGENT: Multi-Layer Validation")
        print(f"{'='*80}")
        print(f"Segment ID: {segment_id}")
        print(f"Validating: API → UI → Database → Cross-Validation")
        
        results = {
            "segment_id": segment_id,
            "timestamp": str(datetime.now()),
            "layers": {},
            "cross_validation": {},
            "overall_status": "unknown"
        }
        
        # Layer 1: API Validation
        if self.api:
            print(f"\n📡 Layer 1: API Validation")
            api_result = self.api.get_segment_by_id(
                segment_id, 
                validate=True,
                expected_fields=expected_data
            )
            results['layers']['api'] = {
                "status": "passed" if api_result.success else "failed",
                "validations": api_result.validations,
                "errors": api_result.errors,
                "data": api_result.data
            }
        
        # Layer 2: UI Validation
        if self.ui:
            print(f"\n🖥️  Layer 2: UI Validation")
            ui_result = self.ui.validate_page(
                element_checks=[
                    {"name": "Segment Name", "selector": f"[data-segment-id='{segment_id}']"}
                ],
                content_checks=[
                    {
                        "name": "Segment Name Text",
                        "selector": f"[data-segment-id='{segment_id}'] .segment-name",
                        "expected": expected_data.get("segment_name", ""),
                        "match_type": "contains"
                    }
                ]
            )
            results['layers']['ui'] = {
                "status": "passed" if ui_result.success else "failed",
                "validations": ui_result.validations,
                "errors": ui_result.errors
            }
        
        # Layer 3: Database Validation
        if self.db:
            print(f"\n💾 Layer 3: Database Validation")
            db_result = self.db.get_segment_by_id(
                segment_id,
                validate=True,
                expected_fields=expected_data
            )
            results['layers']['database'] = {
                "status": "passed" if db_result.success else "failed",
                "validations": db_result.validations,
                "errors": db_result.errors,
                "data": db_result.data
            }
        
        # Cross-Layer Validation: API vs Database
        if self.api and self.db:
            print(f"\n🔄 Cross-Layer Validation: API vs Database")
            cross_result = self.db.cross_validate_with_api(
                segment_id=segment_id,
                api_adapter=self.api
            )
            results['cross_validation'] = {
                "api_vs_db": {
                    "status": "passed" if cross_result.success else "failed",
                    "validations": cross_result.validations,
                    "errors": cross_result.errors
                }
            }
        
        # Determine overall status
        all_passed = all(
            layer.get("status") == "passed" 
            for layer in results['layers'].values()
        )
        cross_passed = all(
            validation.get("status") == "passed"
            for validation in results.get('cross_validation', {}).values()
        )
        
        results['overall_status'] = "passed" if (all_passed and cross_passed) else "failed"
        
        self._print_summary(results)
        self._record_validation(results)
        
        return results
    
    def validate_api_only(self, segment_id: str, expected_data: Optional[Dict] = None) -> APIValidationResult:
        """
        Validate API layer only.
        
        Args:
            segment_id: Segment ID
            expected_data: Expected field values
            
        Returns:
            API validation result
        """
        print(f"\n📡 API-Only Validation: Segment {segment_id}")
        
        if not self.api:
            raise ValueError("API adapter not initialized")
        
        result = self.api.get_segment_by_id(
            segment_id,
            validate=True,
            expected_fields=expected_data
        )
        
        return result
    
    def validate_database_only(self, segment_id: str, expected_data: Optional[Dict] = None) -> DBValidationResult:
        """
        Validate Database layer only.
        
        Args:
            segment_id: Segment ID
            expected_data: Expected field values
            
        Returns:
            Database validation result
        """
        print(f"\n💾 Database-Only Validation: Segment {segment_id}")
        
        if not self.db:
            raise ValueError("DB adapter not initialized")
        
        result = self.db.get_segment_by_id(
            segment_id,
            validate=True,
            expected_fields=expected_data
        )
        
        return result
    
    def validate_ui_only(self, element_checks: List[Dict], content_checks: List[Dict] = None) -> UIValidationResult:
        """
        Validate UI layer only.
        
        Args:
            element_checks: List of elements to check visibility
            content_checks: List of content validations
            
        Returns:
            UI validation result
        """
        print(f"\n🖥️  UI-Only Validation")
        
        if not self.ui:
            raise ValueError("UI adapter not initialized")
        
        result = self.ui.validate_page(
            element_checks=element_checks,
            content_checks=content_checks or []
        )
        
        return result
    
    def cross_validate_api_db(self, segment_id: str) -> DBValidationResult:
        """
        Cross-validate API and Database data.
        
        Args:
            segment_id: Segment ID
            
        Returns:
            Cross-validation result
        """
        print(f"\n🔄 Cross-Validation: API vs Database")
        
        if not self.api or not self.db:
            raise ValueError("Both API and DB adapters must be initialized")
        
        result = self.db.cross_validate_with_api(
            segment_id=segment_id,
            api_adapter=self.api
        )
        
        return result
    
    def validate_field(self, layer: str, field_name: str, actual_value: Any, 
                      expected_value: Any = None, validation_type: str = "equality") -> Dict:
        """
        Validate a single field in any layer.
        
        Args:
            layer: 'api', 'ui', or 'database'
            field_name: Field to validate
            actual_value: Actual value from layer
            expected_value: Expected value (if applicable)
            validation_type: Type of validation
            
        Returns:
            Validation result
        """
        result = {
            "layer": layer,
            "field": field_name,
            "validation_type": validation_type,
            "actual": actual_value,
            "expected": expected_value,
            "passed": False,
            "error": None
        }
        
        try:
            if validation_type == "equality":
                result['passed'] = actual_value == expected_value
                if not result['passed']:
                    result['error'] = f"Expected {expected_value}, got {actual_value}"
            
            elif validation_type == "not_null":
                result['passed'] = actual_value is not None and actual_value != ""
                if not result['passed']:
                    result['error'] = "Value is null or empty"
            
            elif validation_type == "type":
                result['passed'] = isinstance(actual_value, expected_value)
                if not result['passed']:
                    result['error'] = f"Expected type {expected_value}, got {type(actual_value)}"
            
            elif validation_type == "contains":
                result['passed'] = expected_value in str(actual_value)
                if not result['passed']:
                    result['error'] = f"'{expected_value}' not found in '{actual_value}'"
            
        except Exception as e:
            result['passed'] = False
            result['error'] = str(e)
        
        return result
    
    def _print_summary(self, results: Dict):
        """Print validation summary."""
        print(f"\n{'='*80}")
        print(f"📊 VALIDATION SUMMARY")
        print(f"{'='*80}")
        print(f"Overall Status: {'✅ PASSED' if results['overall_status'] == 'passed' else '❌ FAILED'}")
        print(f"Segment ID: {results['segment_id']}")
        
        print(f"\nLayer Results:")
        for layer_name, layer_data in results.get('layers', {}).items():
            status_icon = "✅" if layer_data['status'] == 'passed' else "❌"
            print(f"  {status_icon} {layer_name.upper()}: {layer_data['status']}")
            if layer_data.get('errors'):
                for error in layer_data['errors']:
                    print(f"     ❌ {error}")
        
        if results.get('cross_validation'):
            print(f"\nCross-Validation Results:")
            for cv_name, cv_data in results['cross_validation'].items():
                status_icon = "✅" if cv_data['status'] == 'passed' else "❌"
                print(f"  {status_icon} {cv_name.replace('_', ' ').upper()}: {cv_data['status']}")
        
        print(f"{'='*80}\n")
    
    def _record_validation(self, results: Dict):
        """Record validation results in memory."""
        validation_record = {
            "segment_id": results['segment_id'],
            "timestamp": results['timestamp'],
            "overall_status": results['overall_status'],
            "layers_validated": list(results.get('layers', {}).keys()),
            "cross_validations": list(results.get('cross_validation', {}).keys())
        }
        
        # Store in memory
        if 'validations' not in self.memory.memory_data:
            self.memory.memory_data['validations'] = []
        
        self.memory.memory_data['validations'].append(validation_record)
        self.memory.save()


_validation_agent_instance = None

def get_validation_agent() -> ValidationAgent:
    """Get singleton validation agent instance."""
    global _validation_agent_instance
    if _validation_agent_instance is None:
        _validation_agent_instance = ValidationAgent()
    return _validation_agent_instance
