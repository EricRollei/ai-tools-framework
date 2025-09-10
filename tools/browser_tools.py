# tools/browser_tools.py
"""
Browser tools for opening URLs and web pages
"""

import webbrowser
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any, Optional
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

class OpenBrowserTool(BaseTool):
    """Open a URL in the default web browser"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="open_browser",
            description="Open a URL in the default web browser",
            category="web_browsing",
            parameters=[
                ToolParameter(
                    name="url",
                    description="The URL to open in the browser",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="new_tab",
                    description="Whether to open in a new tab (true) or new window (false)",
                    param_type="boolean",
                    required=False,
                    default=True
                ),
                ToolParameter(
                    name="browser",
                    description="Specific browser to use (auto, chrome, firefox, edge, safari)",
                    param_type="string",
                    required=False,
                    default="auto"
                )
            ]
        )
    
    async def execute(self, url: str, new_tab: bool = True, browser: str = "auto") -> ToolResult:
        """Open URL in browser"""
        try:
            # Validate URL format
            if not url.startswith(('http://', 'https://', 'ftp://', 'file://')):
                # Add https:// if no protocol specified
                if not url.startswith(('www.', 'localhost', '127.0.0.1')):
                    url = f"https://{url}"
                else:
                    url = f"https://{url}"
            
            # Determine browser to use
            browser_controller = None
            
            if browser.lower() == "auto":
                # Use default browser
                browser_controller = webbrowser.get()
            else:
                # Try to get specific browser
                try:
                    if browser.lower() == "chrome":
                        if platform.system() == "Windows":
                            browser_controller = webbrowser.get("windows-default")
                        elif platform.system() == "Darwin":  # macOS
                            browser_controller = webbrowser.get("macosx")
                        else:  # Linux
                            browser_controller = webbrowser.get("google-chrome")
                    elif browser.lower() == "firefox":
                        browser_controller = webbrowser.get("firefox")
                    elif browser.lower() == "edge":
                        if platform.system() == "Windows":
                            browser_controller = webbrowser.get("windows-default")
                        else:
                            browser_controller = webbrowser.get()
                    elif browser.lower() == "safari":
                        if platform.system() == "Darwin":
                            browser_controller = webbrowser.get("safari")
                        else:
                            browser_controller = webbrowser.get()
                    else:
                        browser_controller = webbrowser.get()
                except webbrowser.Error:
                    # Fall back to default browser
                    browser_controller = webbrowser.get()
            
            # Open URL
            if new_tab:
                success = webbrowser.open_new_tab(url)
            else:
                success = webbrowser.open_new(url)
            
            if success:
                action = "new tab" if new_tab else "new window"
                return ToolResult(
                    success=True,
                    content=f"Successfully opened {url} in {action}",
                    result_type=ToolResultType.TEXT,
                    metadata={
                        "tool": "open_browser",
                        "url": url,
                        "new_tab": new_tab,
                        "browser": browser,
                        "platform": platform.system()
                    }
                )
            else:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Failed to open URL: {url}",
                    error_message=f"Browser failed to open URL: {url}"
                )
                
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error opening browser: {str(e)}",
                error_message=f"Error opening browser: {str(e)}"
            )

class OpenSearchTool(BaseTool):
    """Open a search query in the default browser"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="open_search",
            description="Open a search query in the default browser using Google",
            category="web_browsing",
            parameters=[
                ToolParameter(
                    name="query",
                    description="The search query to open in the browser",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="search_engine",
                    description="Search engine to use (google, bing, duckduckgo, yahoo)",
                    param_type="string",
                    required=False,
                    default="google"
                ),
                ToolParameter(
                    name="new_tab",
                    description="Whether to open in a new tab",
                    param_type="boolean",
                    required=False,
                    default=True
                )
            ]
        )
    
    async def execute(self, query: str, search_engine: str = "google", new_tab: bool = True) -> ToolResult:
        """Open search query in browser"""
        try:
            # URL encode the query
            import urllib.parse
            encoded_query = urllib.parse.quote(query)
            
            # Build search URL based on search engine
            search_urls = {
                "google": f"https://www.google.com/search?q={encoded_query}",
                "bing": f"https://www.bing.com/search?q={encoded_query}",
                "duckduckgo": f"https://duckduckgo.com/?q={encoded_query}",
                "yahoo": f"https://search.yahoo.com/search?p={encoded_query}"
            }
            
            search_url = search_urls.get(search_engine.lower(), search_urls["google"])
            
            # Open URL
            if new_tab:
                success = webbrowser.open_new_tab(search_url)
            else:
                success = webbrowser.open_new(search_url)
            
            if success:
                action = "new tab" if new_tab else "new window"
                return ToolResult(
                    success=True,
                    content=f"Successfully opened search for '{query}' on {search_engine} in {action}",
                    result_type=ToolResultType.TEXT,
                    metadata={
                        "tool": "open_search",
                        "query": query,
                        "search_engine": search_engine,
                        "search_url": search_url,
                        "new_tab": new_tab
                    }
                )
            else:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Failed to open search for: {query}",
                    error_message=f"Browser failed to open search URL: {search_url}"
                )
                
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error opening search: {str(e)}",
                error_message=f"Error opening search: {str(e)}"
            )

# Register browser tools
registry.register(OpenBrowserTool)
registry.register(OpenSearchTool)
