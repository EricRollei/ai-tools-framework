#!/usr/bin/env python3
"""
License Header Management for AI Tools Framework
Adds proper license headers and credit information to all Python files
"""

import os
import re
from pathlib import Path
from datetime import datetime

# License header template
LICENSE_HEADER = '''"""
AI Tools Framework: {filename}
Description: {description}
Author: Eric Hiss (GitHub: EricRollei)
Contact: [eric@historic.camera, eric@rollei.us]
Version: 1.0.0
Date: {creation_date}
License: Dual License (Non-Commercial and Commercial Use)
Copyright (c) 2025 Eric Hiss. All rights reserved.

Dual License:
1. Non-Commercial Use: This software is licensed under the terms of the
   Creative Commons Attribution-NonCommercial 4.0 International License.
   To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/
   
2. Commercial Use: For commercial use, a separate license is required.
   Please contact Eric Hiss at [eric@historic.camera, eric@rollei.us] for licensing options.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT.

Dependencies:
This code depends on several third-party libraries, each with its own license.
See LICENSE file for complete dependency information.

{filename} - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""'''

# File descriptions for different modules
FILE_DESCRIPTIONS = {
    # Core framework
    'core/base.py': 'Base classes and interfaces for all AI tools',
    'core/registry.py': 'Tool registration and management system',
    'core/__init__.py': 'Core framework initialization',
    
    # Tool implementations
    'tools/serper_search.py': 'Web search functionality using Serper API',
    'tools/file_management.py': 'File system operations and management',
    'tools/document_tools.py': 'Document creation and text processing',
    'tools/excel_tools.py': 'Excel spreadsheet operations with professional formatting',
    'tools/database_tools.py': 'SQLite database operations and schema management',
    'tools/http_tools.py': 'HTTP requests and file downloads with anti-bot protection',
    'tools/web_scraper_tools.py': 'Advanced web scraping with academic site optimization',
    'tools/email_tools.py': 'Email sending and receiving with SMTP/IMAP support',
    'tools/calendar_tools.py': 'Calendar and scheduling management',
    'tools/clipboard_tools.py': 'Clipboard operations and history management',
    'tools/communication_tools.py': 'Team communication tools (Slack, Discord, Teams)',
    'tools/browser_tools.py': 'Browser automation using Playwright',
    'tools/file_search_tools.py': 'Ultra-fast file search using Everything CLI',
    'tools/pdf_tools.py': 'PDF document creation and manipulation',
    'tools/word_tools.py': 'Microsoft Word document operations',
    'tools/system_info.py': 'System information and monitoring tools',
    'tools/__init__.py': 'Tool imports and registration setup',
    
    # Interfaces
    'interfaces/mcp_server.py': 'Model Context Protocol server implementation',
    'interfaces/openai_api.py': 'OpenAI-compatible API interface',
    'interfaces/__init__.py': 'Interface module initialization',
    
    # Configuration
    'config/settings.py': 'Application configuration and settings management',
    'config/__init__.py': 'Configuration module initialization',
    
    # Examples
    'examples/mcp_client_test.py': 'MCP client testing and demonstration',
    'examples/openai_client_test.py': 'OpenAI API client testing',
    'examples/test-tools.py': 'Tool functionality testing examples',
    'examples/__init__.py': 'Examples module initialization',
    
    # Main servers
    'mcp_main.py': 'General purpose MCP server for multiple platforms',
    'claude_server.py': 'Specialized MCP server optimized for Claude Desktop',
    'ai_tools_stdio_mcp.py': 'MCP server optimized for LM Studio stdio communication',
    
    # Testing and diagnostics
    'test_claude_compatibility.py': 'Claude Desktop integration testing',
    'test_everything.py': 'Everything CLI integration testing',
    'test_mcp_protocol.py': 'MCP protocol compliance testing',
    'test_productivity_tools.py': 'Productivity tools functionality testing',
    'test_web_scraping.py': 'Web scraping capabilities testing',
    'diagnose_claude.py': 'Claude Desktop integration diagnostics',
    
    # Utilities
    'cleanup.py': 'Project cleanup and maintenance utilities',
}

def get_creation_date():
    """Get current date for license header"""
    return datetime.now().strftime("%Y-%m-%d")

def extract_existing_docstring(content):
    """Extract existing docstring if present"""
    # Look for existing docstring pattern
    docstring_pattern = r'"""(.*?)"""'
    match = re.search(docstring_pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def has_license_header(content):
    """Check if file already has a license header"""
    return "AI Tools Framework:" in content and "Eric Hiss" in content and "Dual License" in content

def add_license_header(file_path):
    """Add license header to a Python file"""
    rel_path = os.path.relpath(file_path, '.')
    
    # Skip if already has license
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if has_license_header(content):
            print(f"✅ {rel_path} - Already has license header")
            return
    except Exception as e:
        print(f"❌ {rel_path} - Error reading file: {e}")
        return
    
    # Get description
    description = FILE_DESCRIPTIONS.get(rel_path, 'AI Tools Framework component')
    
    # Create license header
    filename = os.path.basename(file_path)
    header = LICENSE_HEADER.format(
        filename=filename,
        creation_date=get_creation_date(),
        description=description
    )
    
    # Split content into shebang, imports, and rest
    lines = content.split('\n')
    
    # Find where to insert header
    insert_pos = 0
    
    # Skip shebang if present
    if lines and lines[0].startswith('#!'):
        insert_pos = 1
    
    # Skip encoding declaration if present
    if len(lines) > insert_pos and 'coding:' in lines[insert_pos]:
        insert_pos += 1
    
    # Insert license header
    new_lines = lines[:insert_pos] + [header] + [''] + lines[insert_pos:]
    new_content = '\n'.join(new_lines)
    
    # Write back to file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ {rel_path} - Added license header")
    except Exception as e:
        print(f"❌ {rel_path} - Error writing file: {e}")

def process_directory(directory):
    """Process all Python files in a directory"""
    for root, dirs, files in os.walk(directory):
        # Skip virtual environment and cache directories
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                add_license_header(file_path)

def main():
    """Add license headers to all Python files in the project"""
    print("🔏 AI Tools Framework - License Header Management")
    print("=" * 50)
    
    # Process current directory
    process_directory('.')
    
    print("\n📄 License Information:")
    print("- License: Dual License (Non-Commercial CC BY-NC 4.0 / Commercial)")
    print("- Author: Eric Hiss")
    print("- Contact: eric@historic.camera, eric@rollei.us")
    print("- Copyright: 2025 Eric Hiss. All rights reserved.")
    print("- License file: LICENSE")
    
    print("\n✨ All Python files have been processed!")
    print("Next steps:")
    print("1. Review the added headers")
    print("2. Customize copyright holder if needed")
    print("3. Add any additional attribution")
    print("4. Commit changes before publishing")

if __name__ == "__main__":
    main()
