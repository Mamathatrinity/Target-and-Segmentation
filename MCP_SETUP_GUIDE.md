# Setup Guide: Add DB Credentials to YOUR MCP Server

## ✅ What We Did
- Removed `db_connection_params` fixture from conftest.py
- Updated all 8 login tests to use MCP server credentials
- Created templates for YOUR MCP server configuration

---

## 🔧 Setup Steps (Do These in YOUR MCP Server)

### Step 1: Create Config File in YOUR MCP Server

**File:** `c:\Users\mv\mcp_servers\validation_mcp_server\mcp_config.py`

Copy the content from: [`MCP_SERVER_CONFIG_TEMPLATE.py`](MCP_SERVER_CONFIG_TEMPLATE.py)

Or run this command:
```powershell
Copy-Item "MCP_SERVER_CONFIG_TEMPLATE.py" "c:\Users\mv\mcp_servers\validation_mcp_server\mcp_config.py"
```

---

### Step 2: Create .env File in YOUR MCP Server

**File:** `c:\Users\mv\mcp_servers\validation_mcp_server\.env`

Copy the content from: [`MCP_SERVER_ENV_TEMPLATE.env`](MCP_SERVER_ENV_TEMPLATE.env)

Or run this command:
```powershell
Copy-Item "MCP_SERVER_ENV_TEMPLATE.env" "c:\Users\mv\mcp_servers\validation_mcp_server\.env"
```

Then **EDIT** the `.env` file with your actual credentials:
```env
MCP_DB_SERVER=your-actual-server.database.windows.net
MCP_DB_NAME=HCPTargetingSegmentation
MCP_DB_USER=your_db_username
MCP_DB_PASSWORD=your_db_password
```

---

### Step 3: Update YOUR db_validator.py

**File:** `c:\Users\mv\mcp_servers\validation_mcp_server\tools\db_validator.py`

Reference implementation: [`MCP_DB_VALIDATOR_UPDATE.py`](MCP_DB_VALIDATOR_UPDATE.py)

Add these changes to YOUR existing `db_validator.py`:

#### 3a. Add import at the top:
```python
from mcp_config import get_db_config
```

#### 3b. Update `__init__` method:
```python
def __init__(self):
    # Load default DB config from MCP server
    self.default_db_config = get_db_config("sqlserver")
    self.connection = None
    self.cursor = None
```

#### 3c. Update `connect_to_database` method:
```python
def connect_to_database(self, db_type="sqlserver", connection_params=None):
    """
    If connection_params not provided, uses MCP server defaults
    """
    try:
        # Use MCP defaults if no params provided
        if connection_params is None:
            connection_params = self.default_db_config
            print(f"[DB] Using MCP server default credentials for {db_type}")
        
        # YOUR existing connection logic here...
```

---

### Step 4: Install python-dotenv in YOUR MCP Server

If not already installed:
```powershell
cd c:\Users\mv\mcp_servers\validation_mcp_server
pip install python-dotenv
```

---

### Step 5: Test YOUR MCP Server Configuration

Run this to verify:
```powershell
cd c:\Users\mv\mcp_servers\validation_mcp_server
python
```

```python
>>> from mcp_config import get_db_config
>>> config = get_db_config("sqlserver")
>>> print(config)
{'server': '...', 'database': '...', 'username': '...', 'password': '***', 'driver': '...'}
>>>
>>> from tools.db_validator import DBValidator
>>> validator = DBValidator()
>>> result = validator.connect_to_database("sqlserver")
>>> print(result)
{'status': 'success'}
```

---

## ✅ What Changed in Your Test Project

### conftest.py
```python
@pytest.fixture(scope="session")
def db_validator():
    """
    Uses credentials from YOUR MCP server (secure & reusable!)
    """
    validator = DBValidator()
    # Credentials loaded from YOUR MCP server's config
    # No need to pass connection params - uses MCP defaults!
    yield validator
```

**Removed:**
- ❌ `db_connection_params` fixture (not needed anymore)

### test_login.py
**Before:**
```python
def test_pos_001(ui_validator, api_validator, db_validator, settings, db_connection_params):
    db_validator.connect_to_database("sqlserver", db_connection_params)
```

**After:**
```python
def test_pos_001(ui_validator, api_validator, db_validator, settings):
    db_validator.connect_to_database("sqlserver")  # Uses YOUR MCP defaults!
```

**Changed:**
- ✅ All 8 tests now use MCP server credentials
- ✅ No `db_connection_params` parameter
- ✅ Cleaner test signatures

---

## 🔒 Security Benefits

### Before (Credentials in Each Project)
```
Project 1/.env  → DB_SERVER, DB_PASSWORD  ❌ Duplicated
Project 2/.env  → DB_SERVER, DB_PASSWORD  ❌ Duplicated  
Project 3/.env  → DB_SERVER, DB_PASSWORD  ❌ Duplicated
```

### After (Credentials in MCP Server Only)
```
MCP Server/.env → DB credentials (ONE secure location) ✅
Project 1       → TEST_USER_EMAIL only
Project 2       → TEST_USER_EMAIL only
Project 3       → TEST_USER_EMAIL only
```

---

## 🚀 Benefits

1. **Security** - DB credentials in ONE central location
2. **Reusability** - All your projects use same MCP validators with built-in credentials
3. **Consistency** - Same DB connection logic across all automation projects
4. **No duplication** - Don't repeat credentials in every project's .env
5. **Easy updates** - Change credentials once in MCP, all projects updated
6. **Clean separation** - Test user credentials separate from infrastructure credentials

---

## 📁 Final Structure

### YOUR MCP Server
```
c:\Users\mv\mcp_servers\validation_mcp_server\
├── .env                       ← DB credentials (SECURE!)
├── mcp_config.py              ← Config loader
├── tools\
│   ├── api_validator.py       ← YOUR API validator
│   ├── db_validator.py        ← YOUR DB validator (updated)
│   └── ui_validator.py        ← YOUR UI validator
```

### Your Test Project
```
Target_and_Segmentation_Automation\
├── config\
│   ├── .env                   ← Only TEST_USER_EMAIL (no DB creds)
│   └── settings.py
├── tests\
│   ├── conftest.py            ← Uses MCP validators (no db_connection_params)
│   └── ui\
│       └── test_login.py      ← All tests simplified
```

---

## 🎯 Next Steps

1. **Copy config files to YOUR MCP server** (Steps 1-2 above)
2. **Update YOUR db_validator.py** (Step 3 above)
3. **Update MCP server .env** with actual credentials
4. **Update project .env** with TEST_USER_EMAIL only
5. **Run tests**: `pytest tests/ui/test_login.py -v -s`

All tests will now use YOUR MCP server's secure credentials automatically! 🔒✅
