# tools/database_tools.py
"""
Database tools for the AI Tools framework
Includes SQLite, MySQL, and PostgreSQL support
"""

import os
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
import json
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import pymysql
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

try:
    import psycopg2
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False

class SQLiteQueryTool(BaseTool):
    """Execute SQL queries on SQLite databases"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="sqlite_query",
            description="Execute SQL queries on SQLite database files - supports SELECT, INSERT, UPDATE, DELETE",
            category="database",
            parameters=[
                ToolParameter(
                    name="database_path",
                    description="Path to the SQLite database file",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="query",
                    description="SQL query to execute",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="output_format",
                    description="Output format for SELECT results",
                    param_type="string",
                    required=False,
                    default="json"
                ),
                ToolParameter(
                    name="max_rows",
                    description="Maximum number of rows to return for SELECT queries",
                    param_type="number",
                    required=False,
                    default=100
                ),
                ToolParameter(
                    name="create_if_missing",
                    description="Create database file if it doesn't exist",
                    param_type="boolean",
                    required=False,
                    default=False
                )
            ]
        )
    
    async def execute(self, database_path: str, query: str, output_format: str = "json",
                     max_rows: int = 100, create_if_missing: bool = False) -> ToolResult:
        """Execute SQLite query"""
        try:
            # Check if database exists
            if not os.path.exists(database_path) and not create_if_missing:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Database file not found: {database_path}. Use create_if_missing=true to create it.",
                    error_message="Database file not found"
                )
            
            # Create directory if needed
            if create_if_missing:
                Path(database_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Connect to database
            conn = sqlite3.connect(database_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            try:
                # Execute query
                cursor.execute(query)
                
                # Determine query type
                query_type = query.strip().upper().split()[0]
                
                if query_type == "SELECT":
                    # Fetch results for SELECT queries
                    if max_rows > 0:
                        rows = cursor.fetchmany(max_rows)
                    else:
                        rows = cursor.fetchall()
                    
                    # Convert to list of dictionaries
                    data = [dict(row) for row in rows]
                    
                    # Format output
                    if output_format.lower() == "json":
                        content = json.dumps(data, indent=2, default=str)
                    elif output_format.lower() == "csv" and PANDAS_AVAILABLE:
                        df = pd.DataFrame(data)
                        content = df.to_csv(index=False)
                    else:
                        # Simple table format
                        if data:
                            headers = list(data[0].keys())
                            content = "\t".join(headers) + "\n"
                            for row in data:
                                content += "\t".join(str(row[col]) for col in headers) + "\n"
                        else:
                            content = "No results returned"
                    
                    result_content = f"Query executed successfully on: {database_path}\n"
                    result_content += f"Query type: SELECT\n"
                    result_content += f"Rows returned: {len(data)}\n"
                    if data and len(data) == max_rows:
                        result_content += f"(Limited to {max_rows} rows)\n"
                    result_content += f"\nResults ({output_format} format):\n{content}"
                    
                else:
                    # For INSERT, UPDATE, DELETE, etc.
                    conn.commit()
                    rows_affected = cursor.rowcount
                    
                    result_content = f"Query executed successfully on: {database_path}\n"
                    result_content += f"Query type: {query_type}\n"
                    result_content += f"Rows affected: {rows_affected}"
                    
                    if query_type == "INSERT" and cursor.lastrowid:
                        result_content += f"\nLast inserted row ID: {cursor.lastrowid}"
                
                return ToolResult(
                    success=True,
                    content=result_content,
                    result_type=ToolResultType.TEXT,
                    metadata={
                        "tool": "sqlite_query",
                        "database_path": database_path,
                        "query_type": query_type,
                        "rows_affected": cursor.rowcount if query_type != "SELECT" else len(data) if query_type == "SELECT" else 0
                    }
                )
                
            finally:
                cursor.close()
                conn.close()
            
        except sqlite3.Error as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"SQLite error: {str(e)}",
                error_message=f"SQLite error: {str(e)}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Database query failed: {str(e)}",
                error_message=f"Database query failed: {str(e)}"
            )

class DatabaseInfoTool(BaseTool):
    """Get information about database structure and tables"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="database_info",
            description="Get information about database structure, tables, and schemas",
            category="database",
            parameters=[
                ToolParameter(
                    name="database_path",
                    description="Path to the SQLite database file",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="table_name",
                    description="Specific table to get info about (optional - if not provided, lists all tables)",
                    param_type="string",
                    required=False
                )
            ]
        )
    
    async def execute(self, database_path: str, table_name: Optional[str] = None) -> ToolResult:
        """Get database information"""
        try:
            if not os.path.exists(database_path):
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Database file not found: {database_path}",
                    error_message="Database file not found"
                )
            
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            
            try:
                if table_name:
                    # Get info about specific table
                    # Check if table exists
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                    if not cursor.fetchone():
                        return ToolResult(
                            success=False,
                            result_type=ToolResultType.ERROR,
                            content=f"Table '{table_name}' not found in database",
                            error_message="Table not found"
                        )
                    
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    
                    # Get sample data
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                    sample_rows = cursor.fetchall()
                    
                    result_content = f"Table Information: {table_name}\n"
                    result_content += f"Database: {database_path}\n"
                    result_content += f"Row count: {row_count:,}\n\n"
                    
                    result_content += "Columns:\n"
                    for col in columns:
                        cid, name, col_type, not_null, default_value, pk = col
                        result_content += f"  {name} ({col_type})"
                        if pk:
                            result_content += " [PRIMARY KEY]"
                        if not_null:
                            result_content += " [NOT NULL]"
                        if default_value is not None:
                            result_content += f" [DEFAULT: {default_value}]"
                        result_content += "\n"
                    
                    if sample_rows:
                        result_content += f"\nSample data (first {len(sample_rows)} rows):\n"
                        col_names = [col[1] for col in columns]
                        result_content += "\t".join(col_names) + "\n"
                        for row in sample_rows:
                            result_content += "\t".join(str(val) for val in row) + "\n"
                
                else:
                    # Get list of all tables
                    cursor.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') ORDER BY name")
                    objects = cursor.fetchall()
                    
                    result_content = f"Database Overview: {database_path}\n"
                    
                    if objects:
                        result_content += f"\nTables and Views ({len(objects)} total):\n"
                        for name, obj_type in objects:
                            # Get row count for tables
                            if obj_type == 'table':
                                try:
                                    cursor.execute(f"SELECT COUNT(*) FROM {name}")
                                    count = cursor.fetchone()[0]
                                    result_content += f"  📊 {name} (table) - {count:,} rows\n"
                                except:
                                    result_content += f"  📊 {name} (table)\n"
                            else:
                                result_content += f"  👁️ {name} (view)\n"
                    else:
                        result_content += "\nNo tables found in database."
                    
                    # Get database file size
                    file_size = os.path.getsize(database_path)
                    if file_size < 1024:
                        size_str = f"{file_size} bytes"
                    elif file_size < 1024 * 1024:
                        size_str = f"{file_size / 1024:.1f} KB"
                    else:
                        size_str = f"{file_size / (1024 * 1024):.1f} MB"
                    
                    result_content += f"\nDatabase file size: {size_str}"
                
                return ToolResult(
                    success=True,
                    content=result_content,
                    result_type=ToolResultType.TEXT,
                    metadata={
                        "tool": "database_info",
                        "database_path": database_path,
                        "table_name": table_name,
                        "file_size": os.path.getsize(database_path)
                    }
                )
                
            finally:
                cursor.close()
                conn.close()
            
        except sqlite3.Error as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"SQLite error: {str(e)}",
                error_message=f"SQLite error: {str(e)}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Database info failed: {str(e)}",
                error_message=f"Database info failed: {str(e)}"
            )

class CreateTableTool(BaseTool):
    """Create tables in SQLite databases"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="create_table",
            description="Create tables in SQLite databases with specified columns and data types",
            category="database",
            parameters=[
                ToolParameter(
                    name="database_path",
                    description="Path to the SQLite database file",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="table_name",
                    description="Name of the table to create",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="columns",
                    description="Table columns as JSON string - array of objects with 'name', 'type', and optional 'constraints'",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="create_database",
                    description="Create database file if it doesn't exist",
                    param_type="boolean",
                    required=False,
                    default=True
                ),
                ToolParameter(
                    name="drop_if_exists",
                    description="Drop table if it already exists",
                    param_type="boolean",
                    required=False,
                    default=False
                )
            ]
        )
    
    async def execute(self, database_path: str, table_name: str, columns: str,
                     create_database: bool = True, drop_if_exists: bool = False) -> ToolResult:
        """Create table in SQLite database"""
        try:
            # Parse columns specification
            try:
                column_specs = json.loads(columns)
            except json.JSONDecodeError:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="Invalid JSON format in columns parameter",
                    error_message="Invalid JSON format in columns"
                )
            
            if not isinstance(column_specs, list) or not column_specs:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="Columns must be a non-empty array of column specifications",
                    error_message="Invalid columns specification"
                )
            
            # Check if database exists
            if not os.path.exists(database_path) and not create_database:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Database file not found: {database_path}",
                    error_message="Database file not found"
                )
            
            # Create directory if needed
            if create_database:
                Path(database_path).parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            
            try:
                # Drop table if requested
                if drop_if_exists:
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                
                # Build CREATE TABLE statement
                column_definitions = []
                for col_spec in column_specs:
                    if not isinstance(col_spec, dict) or 'name' not in col_spec or 'type' not in col_spec:
                        return ToolResult(
                            success=False,
                            result_type=ToolResultType.ERROR,
                            content="Each column must have 'name' and 'type' properties",
                            error_message="Invalid column specification"
                        )
                    
                    col_def = f"{col_spec['name']} {col_spec['type']}"
                    
                    # Add constraints if specified
                    if 'constraints' in col_spec:
                        col_def += f" {col_spec['constraints']}"
                    
                    column_definitions.append(col_def)
                
                create_sql = f"CREATE TABLE {table_name} ({', '.join(column_definitions)})"
                
                # Execute CREATE TABLE
                cursor.execute(create_sql)
                conn.commit()
                
                result_content = f"Successfully created table: {table_name}\n"
                result_content += f"Database: {database_path}\n"
                result_content += f"Columns: {len(column_specs)}\n\n"
                result_content += "Table structure:\n"
                
                for col_spec in column_specs:
                    result_content += f"  {col_spec['name']} ({col_spec['type']})"
                    if 'constraints' in col_spec:
                        result_content += f" {col_spec['constraints']}"
                    result_content += "\n"
                
                result_content += f"\nSQL executed:\n{create_sql}"
                
                return ToolResult(
                    success=True,
                    content=result_content,
                    result_type=ToolResultType.TEXT,
                    metadata={
                        "tool": "create_table",
                        "database_path": database_path,
                        "table_name": table_name,
                        "columns_count": len(column_specs)
                    }
                )
                
            finally:
                cursor.close()
                conn.close()
            
        except sqlite3.Error as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"SQLite error: {str(e)}",
                error_message=f"SQLite error: {str(e)}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Create table failed: {str(e)}",
                error_message=f"Create table failed: {str(e)}"
            )

# Register SQLite tools (always available)
registry.register(SQLiteQueryTool)
registry.register(DatabaseInfoTool)
registry.register(CreateTableTool)
