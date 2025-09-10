# AI Tools Framework - Complete Documentation

## 🚀 Overview

The AI Tools Framework is a comprehensive productivity suite with **27 production-ready tools** that integrates seamlessly with both **Claude Desktop** and **LM Studio** via the Model Context Protocol (MCP). This framework provides AI assistants with powerful capabilities across file management, web research, data processing, team communication, and automation.

## 📊 Framework Statistics

- **Total Tools**: 27 production-ready tools
- **Tool Categories**: 6 major categories
- **Protocol**: MCP (Model Context Protocol) v1.13.1
- **Compatibility**: Claude Desktop, LM Studio
- **Python Version**: 3.11+
- **Architecture**: Async/await with comprehensive error handling

## 🛠️ Tool Categories & Capabilities

### 📁 **System & File Operations** (6 tools)
| Tool | Description | Key Features |
|------|-------------|--------------|
| `list_files` | Directory listing and navigation | Recursive listing, filtering, permissions |
| `read_file` | File content reading | Encoding detection, large file support |
| `write_file` | File creation and editing | Atomic writes, backup creation |
| `get_file_info` | File metadata and properties | Size, timestamps, permissions |
| `run_command` | System command execution | Safe execution, output capture |
| `search_files` | Ultra-fast Everything CLI integration | System-wide instant search, regex support |

### 🌐 **Network & Web Operations** (4 tools)
| Tool | Description | Key Features |
|------|-------------|--------------|
| `web_search` | Serper API web search | Real-time search, filtering, result ranking |
| `http_request` | HTTP/HTTPS requests | Anti-bot headers, session management |
| `download_file` | File downloads | Resume capability, progress tracking |
| `advanced_web_scraper` | Advanced web scraping | Academic site optimization, paywall bypass |

### 📊 **Data Processing & Analysis** (4 tools)
| Tool | Description | Key Features |
|------|-------------|--------------|
| `read_excel` / `write_excel` | Excel file operations | Professional formatting, auto-sizing |
| `sqlite_query` | Database operations | Full SQL support, transactions |
| `database_info` / `create_table` | Database management | Schema introspection, table creation |
| `clean_text` | Text processing | Cleaning, formatting, analysis |

### 📋 **Productivity Suite** (5 tools)
| Tool | Description | Key Features |
|------|-------------|--------------|
| `manage_calendar` | Calendar and event management | CRUD operations, scheduling, free time |
| `clipboard` | System clipboard operations | History management, cross-platform |
| `slack_message` | Slack team communication | Rich formatting, threading, files |
| `discord_webhook` | Discord server integration | Embeds, custom avatars, webhooks |
| `teams_webhook` | Microsoft Teams messaging | MessageCard format, facts, theming |

### 📧 **Communication & Documents** (4 tools)
| Tool | Description | Key Features |
|------|-------------|--------------|
| `send_email` | Email operations | Attachments, HTML/text, SMTP |
| `write_pdf` / `write_word` | Document creation | Professional formatting, templates |
| `write_markdown` / `write_csv` / `write_json` | Format conversion | Multi-format export, validation |
| `open_browser` / `open_search` | Browser automation | URL opening, search automation |

### 🎭 **Browser Automation** (4 tools)
| Tool | Description | Key Features |
|------|-------------|--------------|
| `mcp_playwright_browser_navigate` | Page navigation | URL handling, wait conditions |
| `mcp_playwright_browser_click` | Element interaction | Smart clicking, error handling |
| `mcp_playwright_browser_type` | Form input | Text entry, keyboard simulation |
| `mcp_playwright_browser_screenshot` | Page capture | Full page, element-specific screenshots |

---

## 🔧 Installation & Setup

### Prerequisites
- **Python 3.11+**
- **Node.js** (for sequential-thinking MCP server, optional)
- **Everything CLI** (for ultra-fast file search, optional but recommended)

### Environment Setup

#### 1. Clone and Setup
```bash
# Navigate to your ai-tools directory
cd A:\ai-tools

# Create and activate virtual environment (recommended)
python -m venv venv
venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Optional: Install clipboard support
pip install pyperclip
```

#### 2. Environment Variables
Create `.env` file with your API keys:
```bash
# Required for web search
SERPER_API_KEY=your-serper-api-key

# Email configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Team communication (optional)
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...

# Everything CLI path (auto-detected if not set)
EVERYTHING_CLI_PATH=C:\Program Files\ES-1.1.0.30.x64\es.exe
```

#### 3. Dependencies
```txt
# Core dependencies
mcp>=1.0.0
aiohttp>=3.12.15
pandas>=2.3.2
openpyxl>=3.1.5
requests>=2.32.3
python-dotenv>=1.0.1

# Optional enhancements
pyperclip>=1.9.0        # Clipboard operations
brotli>=1.1.0           # Web scraping compression
Pillow>=10.0.0          # Image processing
playwright>=1.40.0      # Browser automation
```

---

## 🎯 Integration Guides

## 🖥️ **Claude Desktop Integration**

### Configuration
1. **Locate Claude Desktop config file**:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Add AI Tools configuration**:
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "ai-tools": {
      "command": "A:/ai-tools/venv/Scripts/python.exe",
      "args": ["A:/ai-tools/claude_server.py"],
      "cwd": "A:/ai-tools",
      "env": {
        "PYTHONPATH": "A:/ai-tools",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1",
        "SERPER_API_KEY": "your-serper-api-key"
      }
    }
  }
}
```

3. **Restart Claude Desktop** completely

### Testing Claude Desktop Integration
```
Can you list all available tools?
Can you search for Python files in my system?
Can you create a calendar event for tomorrow at 2 PM?
Can you scrape content from https://example.com?
```

## 🔥 **LM Studio Integration**

### Configuration
1. **Open LM Studio**
2. **Go to Developer → MCP Servers**
3. **Add new server**:
```json
{
  "name": "ai-tools",
  "command": "python",
  "args": ["A:/ai-tools/mcp_main.py"],
  "cwd": "A:/ai-tools",
  "env": {
    "PYTHONPATH": "A:/ai-tools"
  }
}
```

4. **Start the server** and connect

### Testing LM Studio Integration
- Use the MCP tools panel in LM Studio
- Test with simple commands like file listing
- Verify all 27 tools are available

---

## 🔨 Adding New Tools

### Tool Development Process

#### 1. Create Tool Module
Create a new file in `tools/` directory:

```python
# tools/my_new_tool.py
from typing import Dict, Any
from core.base import BaseTool, ToolResult, ToolResultType, Parameter

class MyNewTool(BaseTool):
    """Description of what this tool does"""
    
    def __init__(self):
        super().__init__(
            name="my_new_tool",
            description="Detailed description of the tool's functionality",
            parameters=[
                Parameter(
                    name="input_param",
                    param_type="string",
                    description="Description of the parameter",
                    required=True
                ),
                Parameter(
                    name="optional_param",
                    param_type="number",
                    description="Optional parameter",
                    required=False,
                    default=10
                )
            ]
        )
    
    async def execute(self, input_param: str, optional_param: int = 10) -> ToolResult:
        """Execute the tool logic"""
        try:
            # Your tool logic here
            result = f"Processed {input_param} with {optional_param}"
            
            return ToolResult(
                success=True,
                content=result,
                result_type=ToolResultType.TEXT
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error_message=f"Tool execution failed: {str(e)}",
                result_type=ToolResultType.TEXT
            )
```

#### 2. Register the Tool
Add to `tools/__init__.py`:

```python
# Import your new tool
from .my_new_tool import MyNewTool

# Register with the registry
registry.register_tool(MyNewTool())
```

#### 3. Parameter Types
Supported parameter types:
- `"string"` - Text input
- `"number"` - Numeric input (int/float)
- `"boolean"` - True/false
- `"array"` - List of values
- `"object"` - Dictionary/JSON object

#### 4. Result Types
Available result types:
- `ToolResultType.TEXT` - Plain text response
- `ToolResultType.JSON` - JSON data response
- `ToolResultType.FILE` - File path response

#### 5. Error Handling
Always wrap tool logic in try/catch:
```python
try:
    # Tool logic
    return ToolResult(success=True, content=result)
except Exception as e:
    return ToolResult(
        success=False,
        error_message=f"Error: {str(e)}"
    )
```

### Advanced Tool Features

#### Async Operations
For I/O operations, use async/await:
```python
async def execute(self, url: str) -> ToolResult:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            return ToolResult(success=True, content=content)
```

#### Environment Variables
Access environment variables safely:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('MY_API_KEY')
if not api_key:
    return ToolResult(
        success=False,
        error_message="MY_API_KEY environment variable not set"
    )
```

#### File Operations
Use Path objects for cross-platform compatibility:
```python
from pathlib import Path

file_path = Path(file_path_param)
if not file_path.exists():
    return ToolResult(
        success=False,
        error_message=f"File not found: {file_path}"
    )
```

---

## 🧪 Testing & Validation

### Test Scripts
The framework includes comprehensive test scripts:

```bash
# Test Claude Desktop compatibility
python test_claude_compatibility.py

# Test MCP protocol
python test_mcp_protocol.py

# Diagnostic tool
python diagnose_claude.py

# Test individual tool categories
python examples/test_everything.py        # File search
python examples/test_web_scraping.py     # Web scraping
python examples/test_productivity_tools.py  # Productivity tools
```

### Manual Testing
1. **Server Startup**:
   ```bash
   # Test main server
   python mcp_main.py
   
   # Test Claude server
   python claude_server.py
   ```

2. **Tool Registration**:
   ```python
   from core.registry import registry
   print(f"Registered tools: {len(registry.list_tools())}")
   ```

3. **Individual Tool Testing**:
   ```python
   from tools.my_new_tool import MyNewTool
   tool = MyNewTool()
   result = await tool.execute("test_input")
   print(result.success, result.content)
   ```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. **Server Won't Start**
- Check Python version (3.11+ required)
- Verify virtual environment activation
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check environment variables in `.env` file

#### 2. **Tools Not Working**
- Verify API keys in `.env` file
- Check file permissions
- Test individual tools in isolation
- Review error logs in terminal

#### 3. **Claude Desktop Connection Issues**
- Verify config file location and syntax
- Use absolute paths with forward slashes
- Restart Claude Desktop completely
- Check Python executable path

#### 4. **LM Studio Integration Problems**
- Ensure MCP server is started in LM Studio
- Check server logs in LM Studio interface
- Verify working directory and paths
- Test with simple tools first

#### 5. **Everything CLI Search Not Working**
- Install Everything CLI: https://www.voidtools.com/
- Verify installation path in environment variables
- Test Everything CLI directly: `es.exe --help`

### Diagnostic Commands
```bash
# Check Python environment
python --version
python -c "import mcp; print('MCP available')"

# Test tool imports
python -c "import tools; print('Tools imported')"

# Check registry
python -c "from core.registry import registry; print(f'{len(registry.list_tools())} tools')"

# Test server creation
python -c "from interfaces.mcp_server import MCPToolServer; print('Server created')"
```

---

## 📈 Performance Optimization

### File Search Performance
- **Everything CLI**: Sub-second system-wide file search
- **Indexing**: Automatic background indexing of all drives
- **Regex Support**: Advanced pattern matching
- **Memory Efficient**: Minimal RAM usage

### Web Scraping Optimization
- **Anti-bot Protection**: Realistic browser headers
- **Rate Limiting**: Respectful request timing
- **Fallback Strategies**: Archive.today for paywalled content
- **Academic Site Support**: Specialized handling for research sites

### Database Performance
- **Connection Pooling**: Reuse database connections
- **Query Optimization**: Efficient SQL generation
- **Transaction Management**: Atomic operations
- **Schema Caching**: Reduce metadata queries

### Memory Management
- **Async Architecture**: Non-blocking I/O operations
- **Streaming**: Handle large files efficiently
- **Garbage Collection**: Proper resource cleanup
- **Connection Limits**: Prevent resource exhaustion

---

## 🔐 Security & Privacy

### API Key Management
- Store keys in `.env` file (never commit to version control)
- Use environment variable validation
- Implement key rotation strategies
- Monitor API usage and limits

### File System Security
- Path validation and sanitization
- Permission checking before operations
- Safe temporary file handling
- Prevent directory traversal attacks

### Network Security
- HTTPS enforcement for external requests
- Request timeout handling
- User-agent rotation for web scraping
- Rate limiting to prevent abuse

### Data Privacy
- No persistent storage of sensitive data
- Secure cleanup of temporary files
- Minimal data retention
- Transparent data handling practices

---

## 🚀 Advanced Usage Examples

### Workflow Automation
```python
# Example: Automated research workflow
# 1. Search for files
files = await search_files("research papers", file_type="pdf")

# 2. Web search for latest information
results = await web_search("machine learning 2024 papers")

# 3. Create calendar event for review
await manage_calendar("create", 
    title="Research Review", 
    start_datetime="2024-09-15 14:00"
)

# 4. Notify team
await slack_message("#research", "New papers found for review!")
```

### Data Processing Pipeline
```python
# Example: Excel to database pipeline
# 1. Read Excel data
data = await read_excel("sales_data.xlsx", sheet_name="Q3")

# 2. Process and clean
cleaned_data = await clean_text(data['description'])

# 3. Store in database
await create_table("sales", {
    "id": "INTEGER PRIMARY KEY",
    "amount": "REAL",
    "description": "TEXT"
})

# 4. Generate report
await write_pdf("Q3 Sales Report", processed_data)
```

### Team Communication Hub
```python
# Example: Multi-platform notification
message = "System maintenance scheduled for tonight"

# Notify via multiple channels
await slack_message("#general", message)
await discord_webhook(message, username="System Bot")
await teams_webhook("System Alert", message, color="FF0000")
await send_email("team@company.com", "Maintenance Alert", message)
```

---

## 📚 Resources & References

### Documentation Files
- `README.md` - Main project overview
- `FRAMEWORK_OVERVIEW.md` - Complete framework documentation
- `CLAUDE_DESKTOP_SETUP.md` - Claude Desktop integration guide
- `PRODUCTIVITY_TOOLS.md` - Productivity tools documentation
- `CLAUDE_READY.md` - Quick start guide

### Example Scripts
- `examples/test_everything.py` - File search examples
- `examples/test_web_scraping.py` - Web scraping examples
- `examples/test_productivity_tools.py` - Productivity examples

### Diagnostic Tools
- `test_claude_compatibility.py` - Claude Desktop compatibility test
- `diagnose_claude.py` - Comprehensive diagnostic tool
- `test_mcp_protocol.py` - MCP protocol testing

### Configuration Files
- `claude_config.json` - Claude Desktop configuration template
- `updated_claude_config.json` - Updated configuration
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template

---

## 🎯 Best Practices

### Development Guidelines
1. **Error Handling**: Always wrap operations in try/catch blocks
2. **Type Hints**: Use comprehensive type annotations
3. **Documentation**: Document all parameters and return values
4. **Testing**: Create test cases for new tools
5. **Logging**: Use structured logging for debugging

### Performance Guidelines
1. **Async Operations**: Use async/await for I/O operations
2. **Resource Management**: Properly close connections and files
3. **Memory Efficiency**: Stream large data instead of loading entirely
4. **Caching**: Cache frequently accessed data appropriately
5. **Rate Limiting**: Respect API limits and add delays

### Security Guidelines
1. **Input Validation**: Validate all user inputs
2. **Path Sanitization**: Check file paths for safety
3. **API Key Protection**: Never log or expose API keys
4. **Permission Checking**: Verify file/directory permissions
5. **Error Messages**: Don't leak sensitive information in errors

---

## 🏆 Conclusion

The AI Tools Framework provides a comprehensive, production-ready solution for AI-assisted productivity across multiple platforms. With 27 tools spanning file operations, web research, data processing, team communication, and automation, it represents a complete toolkit for modern workflows.

### Key Achievements
- ✅ **Universal Compatibility**: Works with both Claude Desktop and LM Studio
- ✅ **Production Ready**: Comprehensive error handling and testing
- ✅ **Extensible Architecture**: Easy to add new tools and capabilities
- ✅ **Performance Optimized**: Fast file search, efficient web scraping
- ✅ **Secure**: Proper API key management and input validation
- ✅ **Well Documented**: Complete setup and usage documentation

### Future Enhancements
- Additional AI model integrations
- Enhanced browser automation capabilities
- More data processing formats
- Extended team communication platforms
- Advanced workflow automation features

The framework is ready for production use and provides a solid foundation for AI-assisted productivity enhancement! 🚀
