"""
AI Tools Framework: __init__.py
Description: AI Tools Framework component
Author: Eric Hiss (GitHub: EricRollei)
Contact: [eric@historic.camera, eric@rollei.us]
Version: 1.0.0
Date: 2025-09-09
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

__init__.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# tools/__init__.py - Auto-import and register all tools

# Import all tools to trigger registration
from .serper_search import SerperSearchTool
from .file_management import FileListTool, FileReadTool, FileWriteTool, TextCleanTool
from .document_tools import MarkdownWriteTool, CSVWriteTool, JSONWriteTool
from .pdf_tools import *  # Only imports if reportlab available
from .word_tools import *  # Only imports if python-docx available
from .email_tools import SendEmailTool  # Email tools
from .browser_tools import OpenBrowserTool, OpenSearchTool  # Browser tools
from .file_search_tools import FileSearchTool  # File search tool
from .http_tools import HTTPRequestTool, DownloadFileTool  # HTTP and download tools
from .web_scraper_tools import AdvancedWebScraperTool  # Advanced web scraping
from .excel_tools import *  # Excel tools (only imports if pandas/openpyxl available)
from .database_tools import *  # Database tools (SQLite always available)
from .calendar_tools import CalendarTool  # Calendar management
from .clipboard_tools import ClipboardTool  # Clipboard operations
from .communication_tools import SlackTool, DiscordTool, TeamsWebhookTool  # Communication tools
# from .system_info import SystemInfoTool, RunCommandTool

# Note: Tools register themselves when imported via registry.register_tool() calls in each module

__all__ = [
    "SerperSearchTool",
    "FileListTool", 
    "FileReadTool", 
    "FileWriteTool",
    "TextCleanTool",
    "MarkdownWriteTool",
    "CSVWriteTool", 
    "JSONWriteTool",
    # PDF and Word tools are conditionally imported
    # "SendEmailTool", 
    # "CheckEmailTool",
    # "SystemInfoTool", 
    # "RunCommandTool"
]