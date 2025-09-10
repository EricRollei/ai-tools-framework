# AI Tools Framework - Quick Reference

## 🚀 One-Minute Setup

### Claude Desktop
1. Add to `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "ai-tools": {
      "command": "A:/ai-tools/venv/Scripts/python.exe",
      "args": ["A:/ai-tools/claude_server.py"],
      "cwd": "A:/ai-tools",
      "env": {
        "PYTHONPATH": "A:/ai-tools",
        "SERPER_API_KEY": "your-key"
      }
    }
  }
}
```
2. Restart Claude Desktop
3. Test: "Can you list all available tools?"

### LM Studio  
1. Add MCP server in Developer settings:
```json
{
  "name": "ai-tools-stdio",
  "command": "A:/ai-tools/venv/Scripts/python.exe", 
  "args": ["A:/ai-tools/ai_tools_stdio_mcp.py"],
  "cwd": "A:/ai-tools",
  "env": {
    "PYTHONPATH": "A:/ai-tools",
    "SERPER_API_KEY": "your-serper-api-key"
  }
}
```
2. Start server and connect

## 🛠️ 27 Tools Quick Reference

### 📁 Files (6 tools)
| Tool | Usage | Example |
|------|-------|---------|
| `list_files` | Browse directories | List all Python files in current folder |
| `read_file` | Read file content | Show contents of config.json |
| `write_file` | Create/edit files | Create new README.md file |
| `search_files` | Find files fast | Search for "*.pdf" across entire system |
| `get_file_info` | File metadata | Get size and date of document.docx |
| `run_command` | Execute commands | Run "dir" or "ls" command |

### 🌐 Web (4 tools)
| Tool | Usage | Example |
|------|-------|---------|
| `web_search` | Search internet | Find "Python tutorials 2024" |
| `http_request` | API calls | GET request to REST API endpoint |
| `download_file` | Download files | Download PDF from URL |
| `advanced_web_scraper` | Scrape websites | Extract article text from news site |

### 📊 Data (4 tools)
| Tool | Usage | Example |
|------|-------|---------|
| `read_excel` | Read spreadsheets | Load sales data from Excel file |
| `write_excel` | Create spreadsheets | Generate report with charts |
| `sqlite_query` | Database operations | SELECT * FROM customers |
| `database_info` | DB schema info | Show all tables and columns |

### 📋 Productivity (5 tools)
| Tool | Usage | Example |
|------|-------|---------|
| `manage_calendar` | Events & scheduling | Create meeting for tomorrow 2 PM |
| `clipboard` | Copy/paste data | Copy text with history tracking |
| `slack_message` | Team communication | Send message to #general channel |
| `discord_webhook` | Discord integration | Post update to Discord server |
| `teams_webhook` | Teams integration | Send alert to Teams channel |

### 📧 Communication (8 tools)
| Tool | Usage | Example |
|------|-------|---------|
| `send_email` | Email operations | Send report with PDF attachment |
| `write_pdf` | Create PDFs | Generate formatted report |
| `write_word` | Create documents | Generate Word document |
| `write_markdown` | Create markdown | Generate README.md |
| `clean_text` | Text processing | Clean and format text data |
| `open_browser` | Browser automation | Open URL in default browser |

## ⚡ Power User Commands

### System Administration
```
Search for all log files larger than 10MB in the system
List all Python processes currently running
Find configuration files modified in the last 7 days
```

### Data Analysis
```
Read the Excel file sales_q3.xlsx and create a summary
Query the database for customers from New York
Generate a PDF report of monthly statistics
```

### Web Research
```
Search for "machine learning papers 2024" and summarize findings
Scrape the main content from https://example.com/article
Download all PDFs linked on the research page
```

### Team Coordination
```
Create a calendar event for "Sprint Planning" next Monday 10 AM
Send a Slack message to #dev-team about the deployment
Copy the server configuration to clipboard for sharing
```

### Automation Workflows
```
Search for Python files, read their imports, and create a dependency report
Download sales data, process in Excel, and email the summary
Monitor a website for changes and notify the team via Discord
```

## 🔧 Common Fixes

### Server Won't Start
```bash
# Check Python and dependencies
python --version  # Need 3.11+
pip install -r requirements.txt

# Test server manually
python claude_server.py
```

### Tools Not Working
```bash
# Check environment variables
cat .env  # or type .env on Windows

# Test tool imports
python -c "import tools; print('OK')"

# Run diagnostics
python diagnose_claude.py
```

### Path Issues
- Use forward slashes in config: `A:/ai-tools/`
- Use absolute paths, not relative
- Ensure Python executable path is correct

## 📝 Environment Variables
```bash
# Required
SERPER_API_KEY=your-serper-api-key

# Optional
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SLACK_BOT_TOKEN=xoxb-your-token
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...
```

## 🎯 Best Practices

### Tool Usage
- Start with simple commands to test connectivity
- Use specific file paths rather than relative paths
- Check tool responses for error messages
- Use clipboard tool to share data between operations

### Performance
- File search is ultra-fast with Everything CLI
- Web scraping respects rate limits
- Database operations use transactions
- Large files are processed in chunks

### Security
- API keys stored in .env file only
- File operations validate paths
- Web requests use realistic headers
- No sensitive data logged

## 📚 Key Files

### Servers
- `claude_server.py` - Optimized for Claude Desktop
- `mcp_main.py` - General MCP server for LM Studio

### Configuration
- `claude_config.json` - Claude Desktop config template
- `.env` - Environment variables (create from .env.example)
- `requirements.txt` - Python dependencies

### Documentation
- `COMPLETE_DOCUMENTATION.md` - Full documentation
- `CLAUDE_DESKTOP_SETUP.md` - Claude setup guide
- `FRAMEWORK_OVERVIEW.md` - Technical overview

### Testing
- `diagnose_claude.py` - Comprehensive diagnostics
- `test_claude_compatibility.py` - Compatibility test
- `examples/` - Usage examples

## 🚀 What Makes This Special

### Ultra-Fast Search
Everything CLI integration provides instant system-wide file search - faster than Windows built-in search by orders of magnitude.

### Academic Web Scraping
Specialized handling for research sites like ScienceDirect, PMC, arXiv with anti-bot protection and paywall bypass strategies.

### Professional Excel
Full Excel automation with formatting, charts, formulas, and auto-sizing - generate publication-ready spreadsheets.

### Team Integration
Native support for Slack, Discord, Teams with rich formatting, embeds, and webhook integration.

### Production Ready
Comprehensive error handling, async architecture, input validation, and security best practices throughout.

## 🎉 Success Stories

With this framework, AI assistants can:
- ✅ Find any file on your system in milliseconds
- ✅ Research and summarize academic papers automatically
- ✅ Generate professional Excel reports with charts
- ✅ Coordinate team schedules and send notifications
- ✅ Automate complex multi-step workflows
- ✅ Process data across multiple formats seamlessly
- ✅ Integrate with your existing tools and platforms

**27 tools. 2 platforms. Unlimited possibilities.** 🚀
