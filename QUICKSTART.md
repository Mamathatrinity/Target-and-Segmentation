# Quick Start Guide

## Setup (One-time)
```powershell
# 1. Install dependencies
pip install -r requirements.txt
playwright install

# 2. Configure environment
copy config\.env.example config\.env
# Edit config\.env with your settings

# 3. Verify setup
pytest --collect-only
```

## Run Tests
```powershell
# All tests
pytest -v

# Specific suite
pytest tests/api/ -v
pytest tests/ui/ -v  
pytest tests/database/ -v

# By marker
pytest -m smoke
pytest -m regression

# With HTML report
pytest --html=reports/report.html

# Parallel execution
pytest -n auto
```

## Use MCP Server (in VS Code)
Open Copilot Chat and use: @validation-server <tool_name>

Examples:
- @validation-server api_make_request with endpoint: "/api/targets"
- @validation-server db_execute_query with query: "SELECT * FROM users"
- @validation-server ui_validate_element_exists with selector: "#login"
