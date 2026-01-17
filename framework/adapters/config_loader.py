"""
Configuration Loader for API Contracts and UI Locators
Loads YAML configuration files for data-driven testing.
"""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """Loads and manages API contracts and UI locators."""
    
    def __init__(self, config_dir: str = "framework/adapters"):
        self.config_dir = Path(config_dir)
        self._api_contracts = None
        self._ui_locators = None
    
    @property
    def api_contracts(self) -> Dict[str, Any]:
        """Load API contracts from YAML."""
        if self._api_contracts is None:
            contract_file = self.config_dir / "api_contract.yaml"
            with open(contract_file, 'r') as f:
                self._api_contracts = yaml.safe_load(f)
        return self._api_contracts
    
    @property
    def ui_locators(self) -> Dict[str, Any]:
        """Load UI locators from YAML."""
        if self._ui_locators is None:
            locators_file = self.config_dir / "ui_locators.yaml"
            with open(locators_file, 'r') as f:
                self._ui_locators = yaml.safe_load(f)
        return self._ui_locators
    
    def get_api_contract(self, app: str, operation: str) -> Dict[str, Any]:
        """
        Get API contract for specific app and operation.
        
        Args:
            app: Application name (segments, target_list, etc.)
            operation: API operation (list, get_by_id, create, etc.)
            
        Returns:
            API contract definition
        """
        contracts = self.api_contracts
        if app not in contracts:
            raise ValueError(f"No API contract found for app: {app}")
        
        if operation not in contracts[app]:
            raise ValueError(f"No API contract found for {app}.{operation}")
        
        return contracts[app][operation]
    
    def get_locator(self, app: str, page: str, element: str, **kwargs) -> str:
        """
        Get UI locator for specific element.
        
        Args:
            app: Application name (segments, target_list, etc.)
            page: Page name (list_page, create_page, etc.)
            element: Element name (search_box, create_button, etc.)
            **kwargs: Dynamic values for locator templates (e.g., segment_id)
            
        Returns:
            Locator selector string
        """
        locators = self.ui_locators
        
        if app not in locators:
            raise ValueError(f"No UI locators found for app: {app}")
        
        if page not in locators[app]:
            raise ValueError(f"No page '{page}' found for app: {app}")
        
        if element not in locators[app][page]:
            raise ValueError(f"No element '{element}' found for {app}.{page}")
        
        locator_info = locators[app][page][element]
        selector = locator_info['selector']
        
        # Handle dynamic locators (with placeholders)
        if locator_info.get('dynamic') and kwargs:
            selector = selector.format(**kwargs)
        
        return selector
    
    def get_locator_info(self, app: str, page: str, element: str) -> Dict[str, Any]:
        """
        Get full locator information (selector, type, description).
        
        Args:
            app: Application name
            page: Page name
            element: Element name
            
        Returns:
            Locator info dict with selector, type, description
        """
        locators = self.ui_locators
        return locators[app][page][element]
    
    def validate_api_response(self, app: str, operation: str, response: Dict) -> Dict[str, Any]:
        """
        Validate API response against contract.
        
        Args:
            app: Application name
            operation: API operation
            response: Actual API response
            
        Returns:
            Validation result with errors
        """
        contract = self.get_api_contract(app, operation)
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Validate status code
        expected_status = contract['response']['status_code']
        actual_status = response.get('status_code', 200)
        if actual_status != expected_status:
            result['valid'] = False
            result['errors'].append(
                f"Status code mismatch: expected {expected_status}, got {actual_status}"
            )
        
        # Validate required fields
        if 'fields' in contract['response']:
            response_data = response.get('data', response)
            
            for field_def in contract['response']['fields']:
                field_name = field_def['name']
                
                # Check required fields
                if field_def.get('required', False):
                    if field_name not in response_data:
                        result['valid'] = False
                        result['errors'].append(f"Missing required field: {field_name}")
                    else:
                        # Validate field type
                        expected_type = field_def.get('type')
                        actual_value = response_data[field_name]
                        
                        if not self._validate_type(actual_value, expected_type):
                            result['valid'] = False
                            result['errors'].append(
                                f"Field '{field_name}' type mismatch: "
                                f"expected {expected_type}, got {type(actual_value).__name__}"
                            )
                        
                        # Validate allowed values
                        if 'allowed_values' in field_def:
                            if actual_value not in field_def['allowed_values']:
                                result['valid'] = False
                                result['errors'].append(
                                    f"Field '{field_name}' has invalid value: {actual_value}. "
                                    f"Allowed: {field_def['allowed_values']}"
                                )
        
        return result
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate value type matches expected type."""
        type_map = {
            'string': str,
            'integer': int,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict
        }
        
        expected_python_type = type_map.get(expected_type)
        if expected_python_type is None:
            return True  # Unknown type, skip validation
        
        return isinstance(value, expected_python_type)


# Singleton instance
_config_loader = None

def get_config_loader() -> ConfigLoader:
    """Get singleton config loader instance."""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader
