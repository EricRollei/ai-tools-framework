# Claude Desktop Integration Guide

## Overview
This guide helps you integrate the AI Tools framework (27 tools) with Claude Desktop using the MCP (Model Context Protocol).

## Prerequisites

### 1. Python Environment
```bash
# Ensure Python 3.11+ is installed
python --version

# Navigate to ai-tools directory
cd a:\ai-tools

# Activate virtual environment
venv\Scripts\Activate.ps1

# Verify MCP installation
pip show mcp
```

### 2. Environment Setup
```bash
# Ensure .env file exists with your API keys
copy .env.example .env
notepad .env
```

Required environment variables:
```bash
SERPER_API_KEY=your-serper-api-key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token  # Optional
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...  # Optional
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...  # Optional
```

## Claude Desktop Configuration

### 1. Locate Claude Desktop Config
The configuration file is typically located at:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

### 2. Configuration Content
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ai-tools": {
      "command": "python",
      "args": ["a:/ai-tools/claude_server.py"],
      "cwd": "a:/ai-tools",
      "env": {
        "PYTHONPATH": "a:/ai-tools",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Important**: 
- Replace `a:/ai-tools` with your actual path to the ai-tools directory
- Use forward slashes (/) in paths, even on Windows
- Ensure the path is absolute, not relative

### 3. Alternative Configuration (if main doesn't work)
If the specialized server doesn't work, try the main server:

```json
{
  "mcpServers": {
    "ai-tools": {
      "command": "python",
      "args": ["a:/ai-tools/mcp_main.py"],
      "cwd": "a:/ai-tools",
      "env": {
        "PYTHONPATH": "a:/ai-tools",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

## Testing Before Claude Desktop

### 1. Compatibility Test
```bash
python test_claude_compatibility.py
```
This should show:
- ✅ Environment variables loaded
- ✅ Tools imported successfully  
- ✅ Registry loaded with 27 tools
- ✅ MCP server class imported
- ✅ All tested tool schemas valid
- ✅ Claude Desktop configuration valid

### 2. Manual Server Test
```bash
# Test server startup
python claude_server.py
```

Look for:
```
INFO - Initializing AI Tools MCP server for Claude Desktop...
INFO - Server created with 27 tools registered
INFO - Starting MCP server for Claude Desktop...
INFO - MCP server connected and ready
```

Press Ctrl+C to stop the test.

## Claude Desktop Integration Steps

### 1. Stop Claude Desktop
Completely quit Claude Desktop application.

### 2. Update Configuration
1. Open `claude_desktop_config.json` in a text editor
2. Add the ai-tools server configuration
3. Save the file

### 3. Restart Claude Desktop
1. Launch Claude Desktop
2. Look for MCP server connection messages in logs

### 4. Test Integration
Try these commands in Claude Desktop:

**Basic Test:**
```
Can you list the available tools?
```

**File Operations:**
```
Can you list the files in the current directory?
```

**Search Test:**
```
Can you search for Python files in the system?
```

**Calendar Test:**
```
Can you create a calendar event for tomorrow at 2 PM titled "Test Meeting"?
```

## Troubleshooting

### Issue: Server Starts but Stops Immediately

**Cause**: Usually a Python path or import issue.

**Solutions**:
1. **Check Python Installation**:
   ```bash
   which python  # Should point to your Python 3.11+ installation
   python -c "import mcp; print('MCP available')"
   ```

2. **Verify Virtual Environment**:
   ```bash
   # Make sure you're in the correct venv
   pip list | grep mcp
   ```

3. **Check File Paths**:
   ```bash
   # Ensure files exist
   ls a:/ai-tools/claude_server.py
   ls a:/ai-tools/mcp_main.py
   ```

4. **Test Imports**:
   ```bash
   cd a:\ai-tools
   python -c "import tools; print('Tools imported successfully')"
   ```

### Issue: "No MCP Servers Available"

**Cause**: Configuration file not found or malformed.

**Solutions**:
1. **Verify Config Location**:
   - Windows: Check `%APPDATA%\Claude\`
   - Ensure file is named exactly `claude_desktop_config.json`

2. **Validate JSON**:
   ```bash
   # Test JSON syntax
   python -c "import json; print(json.load(open('claude_config.json')))"
   ```

3. **Check Permissions**:
   - Ensure Claude Desktop can read the config file
   - Try running Claude Desktop as administrator (temporarily)

### Issue: Tools Not Working

**Cause**: Missing dependencies or environment variables.

**Solutions**:
1. **Check Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Environment Variables**:
   ```bash
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('SERPER_API_KEY' in os.environ)"
   ```

3. **Test Individual Tools**:
   ```bash
   python -c "from tools.serper_search import *; print('Serper tool loaded')"
   ```

## Success Indicators

When everything is working correctly, you should see:

### In Claude Desktop:
- MCP server connection indicator shows "Connected"
- Tools are available in the tool palette
- Commands execute without errors

### In Tool Responses:
- File operations return actual file listings
- Search functions return relevant results
- Calendar operations create/modify events
- Web scraping retrieves content

## Available Tool Categories

Once connected, you'll have access to:

1. **File Operations** (6 tools)
   - `list_files`, `read_file`, `write_file`, `get_file_info`, `run_command`, `file_search`

2. **Web & Network** (4 tools)  
   - `web_search`, `http_request`, `download_file`, `web_scraper`

3. **Data Processing** (4 tools)
   - `excel_operations`, `database_operations`, `text_processing`, `image_operations`

4. **Productivity Suite** (5 tools)
   - `manage_calendar`, `clipboard`, `slack_message`, `discord_webhook`, `teams_webhook`

5. **Information & Analysis** (4 tools)
   - `weather_info`, `crypto_tracker`, `news_fetcher`, `qr_operations`

6. **Communication & Media** (4 tools)
   - `email_operations`, `pdf_operations`, `audio_operations`, `compression_operations`

## Performance Notes

- **File Search**: Uses Everything CLI for ultra-fast system-wide search
- **Web Scraping**: Optimized for academic sites with anti-bot protection
- **Database**: SQLite operations with full SQL support
- **Excel**: Professional formatting and auto-sizing
- **Communication**: Webhook integration for team collaboration

## Support

If you encounter issues:

1. Run the compatibility test: `python test_claude_compatibility.py`
2. Check server logs in terminal when starting manually
3. Verify all paths are absolute and use forward slashes
4. Ensure Python virtual environment is activated
5. Confirm all required dependencies are installed

The AI Tools framework provides comprehensive functionality once properly integrated with Claude Desktop!
