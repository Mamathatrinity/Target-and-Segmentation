"""
Configuration settings for Test Automation Framework
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = Path(__file__).parent.parent
env_path = BASE_DIR / 'config' / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings and configuration."""
    
    # Application URLs
    APP_URL = os.getenv('APP_URL', 'https://localhost')
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://localhost/api')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
    
    # Database Configuration
    DB_TYPE = os.getenv('DB_TYPE', 'sqlserver')
    DB_SERVER = os.getenv('DB_SERVER', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'testdb')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_DRIVER = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')
    
    # API Authentication
    API_TOKEN = os.getenv('API_TOKEN', '')
    API_USERNAME = os.getenv('API_USERNAME', '')
    API_PASSWORD = os.getenv('API_PASSWORD', '')
    BRAND_ID = os.getenv('BRAND_ID', 'BR000001')  # Default brand ID for API calls
    
    # Test User Credentials (for UI login tests)
    TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL', '')
    TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD', '')
    
    # Additional Test Users (optional)
    REGULAR_USER_EMAIL = os.getenv('REGULAR_USER_EMAIL', '')
    REGULAR_USER_PASSWORD = os.getenv('REGULAR_USER_PASSWORD', '')
    NEW_USER_EMAIL = os.getenv('NEW_USER_EMAIL', '')
    NEW_USER_PASSWORD = os.getenv('NEW_USER_PASSWORD', '')
    
    # Browser Configuration
    HEADLESS_BROWSER = os.getenv('HEADLESS_BROWSER', 'true').lower() == 'true'
    BROWSER_TYPE = os.getenv('BROWSER_TYPE', 'chromium')
    VIEWPORT_WIDTH = int(os.getenv('VIEWPORT_WIDTH', '1920'))
    VIEWPORT_HEIGHT = int(os.getenv('VIEWPORT_HEIGHT', '1080'))
    
    # Test Configuration
    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '30'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    
    # Directories
    REPORT_DIR = BASE_DIR / os.getenv('REPORT_DIR', 'reports')
    SCREENSHOT_DIR = BASE_DIR / os.getenv('SCREENSHOT_DIR', 'screenshots')
    ALLURE_RESULTS_DIR = BASE_DIR / os.getenv('ALLURE_RESULTS_DIR', 'allure-results')
    
    # MCP Server Path
    MCP_SERVER_PATH = 'C:/Users/mv/mcp_servers/validation_mcp_server/server.py'
    
    @classmethod
    def get_db_connection_params(cls):
        """Get database connection parameters."""
        return {
            'server': cls.DB_SERVER,
            'database': cls.DB_NAME,
            'username': cls.DB_USER,
            'password': cls.DB_PASSWORD
        }
    
    @classmethod
    def get_viewport(cls):
        """Get browser viewport configuration."""
        return {
            'width': cls.VIEWPORT_WIDTH,
            'height': cls.VIEWPORT_HEIGHT
        }
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        cls.REPORT_DIR.mkdir(parents=True, exist_ok=True)
        cls.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        cls.ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# Initialize directories on import
Settings.ensure_directories()
