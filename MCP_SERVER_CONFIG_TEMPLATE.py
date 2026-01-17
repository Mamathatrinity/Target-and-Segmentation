# MCP Server Configuration - Centralized Credentials
# File: c:\Users\mv\mcp_servers\validation_mcp_server\mcp_config.py

"""
Centralized configuration for YOUR MCP validators
Store all credentials here - secure and reusable across all projects!
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from MCP server's .env file
MCP_DIR = Path(__file__).parent
load_dotenv(dotenv_path=MCP_DIR / '.env')


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DB_CONFIG = {
    "sqlserver": {
        "server": os.getenv("MCP_DB_SERVER", "your-server.database.windows.net"),
        "database": os.getenv("MCP_DB_NAME", "HCPTargetingSegmentation"),
        "username": os.getenv("MCP_DB_USER", "your_db_username"),
        "password": os.getenv("MCP_DB_PASSWORD", "your_db_password"),
        "driver": os.getenv("MCP_DB_DRIVER", "{ODBC Driver 17 for SQL Server}")
    }
}


# ============================================================================
# API CONFIGURATION
# ============================================================================

API_CONFIG = {
    "default_base_url": os.getenv(
        "MCP_API_BASE_URL", 
        "https://app-hcptargetandsegmentation-api-dev.azurewebsites.net/api/v1"
    ),
    "timeout": int(os.getenv("MCP_API_TIMEOUT", "30")),
    "retry_count": int(os.getenv("MCP_API_RETRY_COUNT", "3")),
    "retry_delay": int(os.getenv("MCP_API_RETRY_DELAY", "2"))
}


# ============================================================================
# UI CONFIGURATION
# ============================================================================

UI_CONFIG = {
    "default_timeout": int(os.getenv("MCP_UI_TIMEOUT", "30000")),  # milliseconds
    "headless": os.getenv("MCP_UI_HEADLESS", "false").lower() == "true",
    "screenshot_dir": os.getenv("MCP_UI_SCREENSHOT_DIR", "screenshots")
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_db_config(db_type="sqlserver"):
    """Get database configuration by type"""
    return DB_CONFIG.get(db_type, DB_CONFIG["sqlserver"])


def get_api_config():
    """Get API configuration"""
    return API_CONFIG


def get_ui_config():
    """Get UI configuration"""
    return UI_CONFIG
