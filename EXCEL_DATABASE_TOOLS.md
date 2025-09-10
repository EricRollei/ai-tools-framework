# Excel & Database Tools Documentation 📊

## Overview
Comprehensive data processing tools for Excel spreadsheets and SQLite databases with professional formatting and advanced querying capabilities.

## Excel Tools

### 1. ReadExcelTool
**Purpose**: Read data from Excel files
**Function**: `read_excel`

#### Parameters:
- `file_path` (string): Path to Excel file
- `sheet_name` (string, optional): Sheet name (default: first sheet)
- `range_address` (string, optional): Cell range (e.g., "A1:D10")
- `headers` (boolean, optional): First row contains headers (default: true)

#### Features:
- ✅ **Multiple sheets** - Access any worksheet
- ✅ **Range selection** - Read specific cell ranges
- ✅ **Header detection** - Automatic column naming
- ✅ **Data type inference** - Numbers, dates, text
- ✅ **Formula evaluation** - Calculated values

#### Examples:

**Read entire sheet:**
```json
{
  "file_path": "sales_data.xlsx"
}
```

**Read specific sheet:**
```json
{
  "file_path": "report.xlsx",
  "sheet_name": "Q3 Results"
}
```

**Read cell range:**
```json
{
  "file_path": "data.xlsx",
  "sheet_name": "Summary",
  "range_address": "A1:F20"
}
```

### 2. WriteExcelTool
**Purpose**: Create and write Excel files with professional formatting
**Function**: `write_excel`

#### Parameters:
- `file_path` (string): Output file path
- `data` (array): Data to write (array of objects)
- `sheet_name` (string, optional): Sheet name (default: "Sheet1")
- `headers` (array, optional): Custom column headers
- `formatting` (object, optional): Styling options

#### Features:
- ✅ **Professional formatting** - Headers, borders, colors
- ✅ **Auto-sizing** - Optimal column widths
- ✅ **Data validation** - Type checking
- ✅ **Multiple sheets** - Create workbooks
- ✅ **Formulas** - Excel formula support

#### Examples:

**Simple data write:**
```json
{
  "file_path": "output.xlsx",
  "data": [
    {"Name": "John", "Age": 30, "City": "New York"},
    {"Name": "Jane", "Age": 25, "City": "Boston"}
  ]
}
```

**Advanced formatting:**
```json
{
  "file_path": "report.xlsx",
  "data": [
    {"Product": "Widget A", "Sales": 1000, "Profit": 200},
    {"Product": "Widget B", "Sales": 1500, "Profit": 300}
  ],
  "formatting": {
    "header_color": "#4472C4",
    "header_font_color": "#FFFFFF",
    "alternate_rows": true,
    "borders": true,
    "auto_filter": true
  }
}
```

## Database Tools

### 1. DatabaseQueryTool
**Purpose**: Execute SQL queries on SQLite databases
**Function**: `database_query`

#### Parameters:
- `database_path` (string): Path to SQLite database file
- `query` (string): SQL query to execute
- `parameters` (array, optional): Query parameters for prepared statements

#### Features:
- ✅ **Full SQL support** - SELECT, INSERT, UPDATE, DELETE
- ✅ **Prepared statements** - Safe parameter binding
- ✅ **Transaction support** - ACID compliance
- ✅ **Schema introspection** - Table/column information
- ✅ **Auto-create** - Creates database if doesn't exist

#### Examples:

**Select data:**
```json
{
  "database_path": "company.db",
  "query": "SELECT * FROM employees WHERE department = ?",
  "parameters": ["Sales"]
}
```

**Insert data:**
```json
{
  "database_path": "inventory.db",
  "query": "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
  "parameters": ["Widget C", 29.99, 100]
}
```

**Create table:**
```json
{
  "database_path": "new_db.db",
  "query": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE)"
}
```

### 2. DatabaseSchemaTool
**Purpose**: Inspect database structure and metadata
**Function**: `database_schema`

#### Parameters:
- `database_path` (string): Path to SQLite database file
- `table_name` (string, optional): Specific table to inspect

#### Features:
- ✅ **Table listing** - All tables in database
- ✅ **Column details** - Data types, constraints
- ✅ **Index information** - Performance indexes
- ✅ **Foreign keys** - Relationship mapping
- ✅ **Statistics** - Row counts, sizes

## Advanced Usage Patterns

### 1. Excel to Database Pipeline
```python
# 1. Read Excel data
excel_data = await read_excel("sales_data.xlsx", sheet_name="Q3")

# 2. Create database table
await database_query(
    database_path="sales.db",
    query="""CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        amount REAL,
        date TEXT
    )"""
)

# 3. Insert Excel data into database
for row in excel_data:
    await database_query(
        database_path="sales.db",
        query="INSERT INTO sales (product, amount, date) VALUES (?, ?, ?)",
        parameters=[row["Product"], row["Amount"], row["Date"]]
    )
```

### 2. Database to Excel Report
```python
# 1. Query database
results = await database_query(
    database_path="sales.db",
    query="""SELECT 
        product,
        SUM(amount) as total_sales,
        COUNT(*) as transaction_count
    FROM sales 
    GROUP BY product 
    ORDER BY total_sales DESC"""
)

# 2. Create formatted Excel report
await write_excel(
    file_path="sales_report.xlsx",
    data=results,
    formatting={
        "header_color": "#2E75B6",
        "header_font_color": "#FFFFFF",
        "borders": true,
        "auto_filter": true,
        "freeze_panes": "A2"
    }
)
```

### 3. Data Validation and Cleaning
```python
# Read data with validation
data = await read_excel("messy_data.xlsx")

# Clean and validate in database
await database_query(
    database_path="clean.db",
    query="""CREATE TABLE clean_data AS
    SELECT 
        TRIM(name) as name,
        CASE WHEN age > 0 AND age < 150 THEN age ELSE NULL END as age,
        LOWER(email) as email
    FROM raw_data
    WHERE email LIKE '%@%.%'"""
)
```

## Data Types and Formatting

### Excel Data Types:
- **Text**: String values
- **Number**: Integers and decimals
- **Date**: Date/datetime values
- **Boolean**: TRUE/FALSE values
- **Formula**: Excel formulas (=SUM(A1:A10))

### Database Data Types:
- **INTEGER**: Whole numbers
- **REAL**: Floating-point numbers
- **TEXT**: String values
- **BLOB**: Binary data
- **NULL**: Empty values

## Performance Tips

### Excel Performance:
1. **Read only needed ranges** instead of entire sheets
2. **Use appropriate data types** to reduce file size
3. **Limit formatting** for large datasets
4. **Consider CSV** for simple data exchange

### Database Performance:
1. **Create indexes** on frequently queried columns
2. **Use prepared statements** for repeated queries
3. **Batch inserts** in transactions
4. **Analyze query plans** for optimization

## Error Handling

### Common Excel Errors:
- **File not found**: Check file path
- **Sheet not found**: Verify sheet name
- **Invalid range**: Check cell range format
- **Permission denied**: Ensure file isn't open

### Common Database Errors:
- **Table doesn't exist**: Create table first
- **SQL syntax error**: Validate SQL query
- **Constraint violation**: Check unique/foreign key constraints
- **Database locked**: Close other connections

## Best Practices

### Excel Best Practices:
1. **Consistent headers** - Use clear, descriptive column names
2. **Data validation** - Validate data before writing
3. **Backup files** - Keep original files safe
4. **Version control** - Use meaningful filenames

### Database Best Practices:
1. **Normalize data** - Avoid data duplication
2. **Use transactions** - Ensure data consistency
3. **Regular backups** - Protect against data loss
4. **Monitor performance** - Optimize slow queries
