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