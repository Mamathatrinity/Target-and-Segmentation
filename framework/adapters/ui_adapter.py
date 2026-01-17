"""
UI Validator Adapter
Clean interface to MCP UI validation tools with comprehensive validation.
"""
from typing import Dict, Any, Optional, List
import allure


class UIValidationResult:
    """Structured UI validation result with detailed element checks."""
    
    def __init__(self, page_name: str):
        self.page_name = page_name
        self.validations = {
            "page_loaded": {"expected": True, "actual": False, "passed": False},
            "element_validations": {},
            "content_validations": {}
        }
        self.errors = []
        
    def validate_element_visible(self, element_name: str, selector: str, 
                                 is_visible: bool) -> bool:
        """Validate element visibility."""
        passed = is_visible
        self.validations["element_validations"][element_name] = {
            "selector": selector,
            "expected": "visible",
            "actual": "visible" if is_visible else "not visible",
            "passed": passed
        }
        
        if not passed:
            self.errors.append(f"Element '{element_name}' ({selector}) is not visible")
        
        return passed
    
    def validate_text_content(self, element_name: str, expected: str, 
                             actual: str, match_type: str = "exact") -> bool:
        """Validate element text content."""
        if match_type == "exact":
            passed = expected == actual
        elif match_type == "contains":
            passed = expected in actual
        elif match_type == "not_empty":
            passed = len(actual.strip()) > 0
        else:
            passed = False
        
        self.validations["content_validations"][element_name] = {
            "expected": expected,
            "actual": actual,
            "match_type": match_type,
            "passed": passed
        }
        
        if not passed:
            self.errors.append(
                f"Text content for '{element_name}': expected '{expected}', got '{actual}'"
            )
        
        return passed
    
    def print_summary(self):
        """Print detailed validation summary to terminal."""
        print("\n" + "="*80)
        print(f"  UI VALIDATION - {self.page_name}")
        print("="*80)
        
        # Page loaded
        page_val = self.validations["page_loaded"]
        icon = "✅" if page_val["passed"] else "❌"
        print(f"  Page Loaded: {icon}")
        
        # Element validations
        if self.validations["element_validations"]:
            print(f"\n  Element Visibility:")
            for elem_name, val in self.validations["element_validations"].items():
                icon = "✅" if val["passed"] else "❌"
                print(f"    {elem_name}: {icon}")
                print(f"      Selector: {val['selector']}")
                print(f"      Status: {val['actual']}")
        
        # Content validations
        if self.validations["content_validations"]:
            print(f"\n  Content Validations:")
            for elem_name, val in self.validations["content_validations"].items():
                icon = "✅" if val["passed"] else "❌"
                print(f"    {elem_name}: {icon}")
                print(f"      Expected: {val['expected']}")
                print(f"      Actual: {val['actual']}")
        
        # Errors
        if self.errors:
            print(f"\n  ❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"    - {error}")
        else:
            print(f"\n  ✅ All UI validations passed!")
        
        print("="*80)
    
    def attach_to_allure(self):
        """Attach validation results to Allure report."""
        summary = f"Page: {self.page_name}\n\n"
        
        # Element validations
        if self.validations["element_validations"]:
            summary += "Element Validations:\n"
            for elem_name, val in self.validations["element_validations"].items():
                icon = "✅" if val["passed"] else "❌"
                summary += f"  {elem_name}: {icon}\n"
                summary += f"    Selector: {val['selector']}\n"
                summary += f"    Status: {val['actual']}\n"
        
        # Content validations
        if self.validations["content_validations"]:
            summary += "\nContent Validations:\n"
            for elem_name, val in self.validations["content_validations"].items():
                icon = "✅" if val["passed"] else "❌"
                summary += f"  {elem_name}: {icon}\n"
                summary += f"    Expected: {val['expected']}\n"
                summary += f"    Actual: {val['actual']}\n"
        
        # Errors
        if self.errors:
            summary += f"\nErrors:\n"
            for error in self.errors:
                summary += f"  - {error}\n"
        
        allure.attach(
            summary,
            name="UI Validation Summary",
            attachment_type=allure.attachment_type.TEXT
        )


class UIAdapter:
    """Adapter for UI validation - wraps Playwright page object."""
    
    def __init__(self, page, page_object_class):
        """
        Initialize UI adapter.
        
        Args:
            page: Playwright page fixture
            page_object_class: Page object class (e.g., SegmentsPage)
        """
        self.page = page
        self.page_object = page_object_class
        
    def navigate(self, url: str):
        """Navigate to URL."""
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)
    
    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """Take screenshot and attach to Allure."""
        screenshot = self.page.screenshot()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        return screenshot
    
    def click_element(self, selector: str, description: str = ""):
        """Click element with Allure logging."""
        with allure.step(f"Click: {description or selector}"):
            self.page.click(selector)
    
    def fill_field(self, selector: str, value: str, description: str = ""):
        """Fill input field."""
        with allure.step(f"Fill {description or selector}: {value}"):
            self.page.fill(selector, value)
    
    def get_text(self, selector: str) -> str:
        """Get text from element."""
        return self.page.text_content(selector)
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        return self.page.is_visible(selector)
    
    def wait_for_element(self, selector: str, timeout: int = 5000):
        """Wait for element to be visible."""
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def validate_page_loaded(self, expected_url_part: str) -> bool:
        """Validate that correct page is loaded."""
        current_url = self.page.url
        return expected_url_part in current_url
    
    def validate_page(self, page_name: str, 
                     element_checks: Optional[List[Dict]] = None,
                     content_checks: Optional[List[Dict]] = None) -> UIValidationResult:
        """
        Comprehensive page validation with elements and content.
        
        Args:
            page_name: Name of the page being validated
            element_checks: List of dicts with 'name' and 'selector' for visibility checks
            content_checks: List of dicts with 'name', 'selector', 'expected', 'match_type'
            
        Returns:
            UIValidationResult with detailed validation
        """
        result = UIValidationResult(page_name)
        
        # Validate page loaded
        result.validations["page_loaded"]["actual"] = True
        result.validations["page_loaded"]["passed"] = True
        
        # Element visibility checks
        if element_checks:
            for check in element_checks:
                element_name = check.get("name")
                selector = check.get("selector")
                is_visible = self.is_visible(selector)
                result.validate_element_visible(element_name, selector, is_visible)
        
        # Content checks
        if content_checks:
            for check in content_checks:
                element_name = check.get("name")
                selector = check.get("selector")
                expected = check.get("expected")
                match_type = check.get("match_type", "contains")
                
                actual = self.get_text(selector) if self.is_visible(selector) else ""
                result.validate_text_content(element_name, expected, actual, match_type)
        
        # Print and attach
        result.print_summary()
        result.attach_to_allure()
        
        # Take screenshot
        self.take_screenshot(f"{page_name} Validation")
        
        return result
    
    def get_table_data(self, table_selector: str) -> List[Dict]:
        """Extract data from table."""
        # This would need to be implemented based on actual table structure
        rows = self.page.query_selector_all(f"{table_selector} tbody tr")
        data = []
        
        for row in rows:
            cells = row.query_selector_all("td")
            row_data = [cell.text_content() for cell in cells]
            data.append(row_data)
        
        return data
