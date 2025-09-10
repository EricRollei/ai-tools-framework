# Encoding Fix Documentation 🔤

## Overview
Comprehensive UTF-8 encoding solutions for Windows environments, addressing common character encoding issues in Python applications, file I/O, and cross-platform compatibility.

## Common Encoding Issues

### Windows-Specific Problems
1. **Default CP1252 encoding** instead of UTF-8
2. **Console output corruption** with special characters
3. **File reading errors** with international text
4. **JSON parsing failures** with non-ASCII characters
5. **Database encoding mismatches**

### Symptoms
- **Garbled text**: `Ã¤Ã¶Ã¼` instead of `äöü`
- **UnicodeDecodeError**: `'charmap' codec can't decode byte`
- **UnicodeEncodeError**: `'ascii' codec can't encode character`
- **JSON errors**: Invalid JSON with Unicode characters
- **Console gibberish**: Squares or question marks

## Environment Configuration

### Python Environment Variables
Add these to your `.env` file or system environment:

```env
# Force UTF-8 encoding
PYTHONIOENCODING=utf-8
PYTHONUNBUFFERED=1

# Locale settings
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8

# Console encoding
PYTHONLEGACYWINDOWSFSENCODING=0
```

### Windows Console Configuration
```cmd
# Set console code page to UTF-8
chcp 65001

# PowerShell UTF-8 output
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### VS Code Configuration
Add to `settings.json`:
```json
{
  "files.encoding": "utf8",
  "files.autoGuessEncoding": true,
  "terminal.integrated.env.windows": {
    "PYTHONIOENCODING": "utf-8"
  }
}
```

## Python Code Fixes

### File I/O with Explicit Encoding
```python
# ❌ Wrong - Uses system default encoding
with open('file.txt', 'r') as f:
    content = f.read()

# ✅ Correct - Explicit UTF-8 encoding
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# ✅ Write with UTF-8
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("Hello 世界! 🌍")
```

### JSON Handling
```python
import json

# ❌ Wrong - May fail with Unicode
data = {"message": "Hello 世界!"}
with open('data.json', 'w') as f:
    json.dump(data, f)

# ✅ Correct - Explicit encoding and Unicode handling
data = {"message": "Hello 世界!"}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### HTTP Requests with Encoding
```python
import requests

# ❌ Wrong - May not handle encoding properly
response = requests.get('https://api.example.com/data')
text = response.text

# ✅ Correct - Explicit encoding handling
response = requests.get('https://api.example.com/data')
response.encoding = 'utf-8'
text = response.text

# ✅ Alternative - Use response.content with explicit decoding
response = requests.get('https://api.example.com/data')
text = response.content.decode('utf-8')
```

### CSV Files with International Characters
```python
import csv

# ❌ Wrong - May fail with Unicode
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# ✅ Correct - UTF-8 encoding
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# ✅ Writing CSV with Unicode
data = [['Name', 'City'], ['José', 'São Paulo'], ['李明', '北京']]
with open('international.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
```

## MCP Server Encoding Fixes

### Stdio Communication
```python
import sys
import json

# ✅ Force UTF-8 for stdio
if sys.platform == "win32":
    import codecs
    sys.stdin = codecs.getreader('utf-8')(sys.stdin.detach())
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# ✅ JSON serialization with UTF-8
def send_response(data):
    json_str = json.dumps(data, ensure_ascii=False)
    print(json_str, flush=True)
```

### Environment Setup for MCP
```python
import os
import locale

def setup_encoding():
    """Setup proper encoding for the application"""
    # Set environment variables
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    # Set locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, '')
        except locale.Error:
            pass  # Fallback to system default
    
    # Windows-specific fixes
    if sys.platform == "win32":
        # Set console code page
        try:
            import subprocess
            subprocess.run(['chcp', '65001'], shell=True, capture_output=True)
        except:
            pass
```

### Claude Desktop Integration
```python
# claude_server.py encoding fixes
import sys
import json
import asyncio
from typing import Any

async def main():
    # Ensure UTF-8 encoding for Windows
    if sys.platform == "win32":
        import codecs
        sys.stdin = codecs.getreader('utf-8')(sys.stdin.detach())
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    
    # Rest of MCP server code...
    
def write_message(message: dict) -> None:
    """Write message with proper UTF-8 encoding"""
    json_str = json.dumps(message, ensure_ascii=False, separators=(',', ':'))
    print(json_str, flush=True)
```

## Database Encoding

### SQLite UTF-8 Configuration
```python
import sqlite3

# ✅ SQLite with proper UTF-8 handling
conn = sqlite3.connect('database.db')
conn.execute("PRAGMA encoding = 'UTF-8'")

# Insert Unicode data
conn.execute(
    "INSERT INTO users (name, city) VALUES (?, ?)",
    ("José Silva", "São Paulo")
)
conn.commit()
```

### Connection String Examples
```python
# PostgreSQL
conn_string = "postgresql://user:pass@localhost/db?client_encoding=utf8"

# MySQL
conn_string = "mysql://user:pass@localhost/db?charset=utf8mb4"

# SQL Server
conn_string = "mssql://user:pass@localhost/db?charset=utf8"
```

## Web Scraping Encoding

### BeautifulSoup with Encoding Detection
```python
import requests
from bs4 import BeautifulSoup
import chardet

def scrape_with_encoding(url):
    response = requests.get(url)
    
    # Detect encoding
    detected = chardet.detect(response.content)
    encoding = detected['encoding']
    
    # Use detected encoding
    response.encoding = encoding
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding=encoding)
    return soup.get_text()
```

### aiohttp with Encoding
```python
import aiohttp

async def fetch_with_encoding(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Read as bytes first
            content = await response.read()
            
            # Get encoding from response or detect
            encoding = response.get_encoding()
            if not encoding:
                import chardet
                detected = chardet.detect(content)
                encoding = detected['encoding'] or 'utf-8'
            
            # Decode with proper encoding
            text = content.decode(encoding, errors='replace')
            return text
```

## Testing Encoding

### Test Script for Encoding Issues
```python
import sys
import json
import locale

def test_encoding():
    """Test various encoding scenarios"""
    print("🔍 Encoding Diagnostic Test")
    print("=" * 40)
    
    # System info
    print(f"Python version: {sys.version}")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"File system encoding: {sys.getfilesystemencoding()}")
    print(f"Locale: {locale.getpreferredencoding()}")
    
    # Environment variables
    print(f"PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING', 'Not set')}")
    print(f"LC_ALL: {os.environ.get('LC_ALL', 'Not set')}")
    
    # Test Unicode strings
    test_strings = [
        "Hello World",
        "Café français",
        "日本語テスト",
        "Тест на русском",
        "العربية اختبار",
        "🌍🚀📊💻",
    ]
    
    print("\n📝 Unicode String Tests:")
    for i, test_str in enumerate(test_strings, 1):
        try:
            print(f"{i}. {test_str}")
            
            # Test JSON serialization
            json_str = json.dumps({"text": test_str}, ensure_ascii=False)
            parsed = json.loads(json_str)
            assert parsed["text"] == test_str
            print(f"   ✅ JSON: OK")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test file operations
    print("\n📁 File Operation Tests:")
    test_file = "encoding_test.txt"
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Unicode test: 世界 🌍 Café")
        
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ File I/O: {content}")
        os.remove(test_file)
        
    except Exception as e:
        print(f"❌ File I/O Error: {e}")

if __name__ == "__main__":
    test_encoding()
```

## Troubleshooting Guide

### UnicodeDecodeError
**Error**: `'charmap' codec can't decode byte 0x81`
**Solution**:
```python
# Add explicit encoding
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

### UnicodeEncodeError  
**Error**: `'ascii' codec can't encode character`
**Solution**:
```python
# Set environment variable
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Or use explicit encoding
text.encode('utf-8')
```

### JSON Unicode Issues
**Error**: JSON with garbled characters
**Solution**:
```python
# Use ensure_ascii=False
json.dumps(data, ensure_ascii=False)

# Read JSON with UTF-8
with open('file.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### Console Output Problems
**Error**: Squares or question marks in console
**Solution**:
```cmd
# Set console code page
chcp 65001

# Set PowerShell encoding
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8
```

## Best Practices

### 1. Always Specify Encoding
```python
# ✅ Always explicit
open('file.txt', 'r', encoding='utf-8')
json.dumps(data, ensure_ascii=False)
response.encoding = 'utf-8'
```

### 2. Set Environment Early
```python
# At the start of your application
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
```

### 3. Handle Encoding Errors Gracefully
```python
try:
    text = content.decode('utf-8')
except UnicodeDecodeError:
    # Fallback with error handling
    text = content.decode('utf-8', errors='replace')
```

### 4. Test with International Data
```python
test_data = [
    "English text",
    "Français café",
    "日本語テスト",
    "Español niño",
    "🌍🚀📊"
]
```

### 5. Use UTF-8 BOM When Necessary
```python
# For Windows applications that need BOM
with open('file.txt', 'w', encoding='utf-8-sig') as f:
    f.write("Content with BOM")
```
