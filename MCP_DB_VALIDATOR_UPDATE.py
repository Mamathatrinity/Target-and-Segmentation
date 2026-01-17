# Update YOUR db_validator.py
# File: c:\Users\mv\mcp_servers\validation_mcp_server\tools\db_validator.py

"""
INSTRUCTIONS: Add this to YOUR existing db_validator.py

1. Add import at the top:
   from mcp_config import get_db_config

2. Update __init__ method:
   Add: self.default_db_config = get_db_config("sqlserver")

3. Update connect_to_database method to use defaults if no params provided
"""

# ============================================================================
# EXAMPLE IMPLEMENTATION
# ============================================================================

from mcp_config import get_db_config
import pyodbc


class DBValidator:
    def __init__(self):
        # Load default DB config from MCP server
        self.default_db_config = get_db_config("sqlserver")
        self.connection = None
        self.cursor = None
    
    def connect_to_database(self, db_type="sqlserver", connection_params=None):
        """
        Connect to database
        If connection_params not provided, uses MCP server defaults
        
        Args:
            db_type: Type of database (default: "sqlserver")
            connection_params: Optional dict with connection details
                             If None, uses MCP server defaults
        
        Returns:
            dict: {"status": "success"} or {"status": "error", "error": "..."}
        """
        try:
            # Use MCP defaults if no params provided
            if connection_params is None:
                connection_params = self.default_db_config
                print(f"[DB] Using MCP server default credentials for {db_type}")
            
            # Build connection string
            if db_type == "sqlserver":
                conn_str = (
                    f"DRIVER={connection_params.get('driver', self.default_db_config['driver'])};"
                    f"SERVER={connection_params.get('server', connection_params.get('Server'))};"
                    f"DATABASE={connection_params.get('database', connection_params.get('Database'))};"
                    f"UID={connection_params.get('username', connection_params.get('User'))};"
                    f"PWD={connection_params.get('password', connection_params.get('Password'))}"
                )
                
                self.connection = pyodbc.connect(conn_str)
                self.cursor = self.connection.cursor()
                
                print(f"[DB] ✅ Connected to {connection_params.get('database', connection_params.get('Database'))}")
                return {"status": "success"}
            else:
                return {"status": "error", "error": f"Unsupported database type: {db_type}"}
                
        except Exception as e:
            error_msg = f"Database connection failed: {str(e)}"
            print(f"[DB] ❌ {error_msg}")
            return {"status": "error", "error": error_msg}
    
    def execute_query(self, query, fetch_results=False):
        """
        Execute SQL query
        
        Args:
            query: SQL query string
            fetch_results: If True, returns query results
        
        Returns:
            dict: {"status": "success", "results": [...], "row_count": N}
                 or {"status": "error", "error": "..."}
        """
        try:
            if not self.connection or not self.cursor:
                return {"status": "error", "error": "Not connected to database"}
            
            self.cursor.execute(query)
            
            if fetch_results:
                columns = [column[0] for column in self.cursor.description]
                results = []
                for row in self.cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                
                print(f"[DB] ✅ Query executed: {len(results)} row(s) returned")
                return {
                    "status": "success",
                    "results": results,
                    "row_count": len(results)
                }
            else:
                self.connection.commit()
                row_count = self.cursor.rowcount
                print(f"[DB] ✅ Query executed: {row_count} row(s) affected")
                return {
                    "status": "success",
                    "row_count": row_count
                }
                
        except Exception as e:
            error_msg = f"Query execution failed: {str(e)}"
            print(f"[DB] ❌ {error_msg}")
            return {"status": "error", "error": error_msg}
    
    def close_connection(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            print("[DB] ✅ Connection closed")
        except Exception as e:
            print(f"[DB] ⚠ Error closing connection: {str(e)}")
