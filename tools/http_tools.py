# tools/http_tools.py
"""
HTTP and download tools for the AI Tools framework
Includes HTTP requests and file downloading capabilities
"""

import os
import aiohttp
import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
from urllib.parse import urlparse, urljoin
import json
import time
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

class HTTPRequestTool(BaseTool):
    """Make HTTP requests (GET, POST, PUT, DELETE, etc.)"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="http_request",
            description="Make HTTP requests to APIs and websites with support for headers, authentication, and JSON/form data",
            category="network",
            parameters=[
                ToolParameter(
                    name="url",
                    description="The URL to make the request to",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="method",
                    description="HTTP method to use",
                    param_type="string",
                    required=False,
                    default="GET"
                ),
                ToolParameter(
                    name="headers",
                    description="HTTP headers as JSON string (e.g., '{\"Content-Type\": \"application/json\"}')",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="data",
                    description="Request body data (JSON string for JSON data, or form data)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="params",
                    description="URL query parameters as JSON string (e.g., '{\"key\": \"value\"}')",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="timeout",
                    description="Request timeout in seconds",
                    param_type="number",
                    required=False,
                    default=30
                ),
                ToolParameter(
                    name="follow_redirects",
                    description="Whether to follow HTTP redirects",
                    param_type="boolean",
                    required=False,
                    default=True
                ),
                ToolParameter(
                    name="verify_ssl",
                    description="Whether to verify SSL certificates",
                    param_type="boolean",
                    required=False,
                    default=True
                ),
                ToolParameter(
                    name="auth_bearer",
                    description="Bearer token for Authorization header",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="auth_basic_user",
                    description="Username for basic authentication",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="auth_basic_pass",
                    description="Password for basic authentication",
                    param_type="string",
                    required=False
                )
            ]
        )
    
    async def execute(self, url: str, method: str = "GET", headers: Optional[str] = None,
                     data: Optional[str] = None, params: Optional[str] = None,
                     timeout: int = 30, follow_redirects: bool = True, verify_ssl: bool = True,
                     auth_bearer: Optional[str] = None, auth_basic_user: Optional[str] = None,
                     auth_basic_pass: Optional[str] = None) -> ToolResult:
        """Execute HTTP request"""
        try:
            # Parse headers
            request_headers = {}
            if headers:
                try:
                    request_headers = json.loads(headers)
                except json.JSONDecodeError:
                    return ToolResult(
                        success=False,
                        result_type=ToolResultType.ERROR,
                        content="Invalid JSON format in headers",
                        error_message="Invalid JSON format in headers"
                    )
            
            # Parse query parameters
            query_params = {}
            if params:
                try:
                    query_params = json.loads(params)
                except json.JSONDecodeError:
                    return ToolResult(
                        success=False,
                        result_type=ToolResultType.ERROR,
                        content="Invalid JSON format in params",
                        error_message="Invalid JSON format in params"
                    )
            
            # Handle authentication
            auth = None
            if auth_bearer:
                request_headers['Authorization'] = f'Bearer {auth_bearer}'
            elif auth_basic_user and auth_basic_pass:
                auth = aiohttp.BasicAuth(auth_basic_user, auth_basic_pass)
            
            # Add common headers to avoid bot detection
            default_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Merge with user headers (user headers take precedence)
            final_headers = {**default_headers, **request_headers}
            
            # Merge with user headers (user headers take precedence)
            final_headers = {**default_headers, **request_headers}
            
            # Parse request data
            request_data = None
            if data:
                # Try to parse as JSON first
                try:
                    json_data = json.loads(data)
                    request_data = json_data
                    if 'Content-Type' not in final_headers:
                        final_headers['Content-Type'] = 'application/json'
                except json.JSONDecodeError:
                    # Treat as plain text/form data
                    request_data = data
            
            # Create connector with SSL settings
            connector = aiohttp.TCPConnector(verify_ssl=verify_ssl)
            
            # Make the request
            timeout_config = aiohttp.ClientTimeout(total=timeout)
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout_config
            ) as session:
                async with session.request(
                    method=method.upper(),
                    url=url,
                    headers=final_headers,
                    params=query_params,
                    json=request_data if isinstance(request_data, (dict, list)) else None,
                    data=request_data if isinstance(request_data, str) else None,
                    auth=auth,
                    allow_redirects=follow_redirects
                ) as response:
                    
                    # Get response details
                    status_code = response.status
                    response_headers = dict(response.headers)
                    
                    # Get response content
                    try:
                        # Try to parse as JSON first
                        response_data = await response.json()
                        content_type = "json"
                    except:
                        # Fall back to text
                        response_data = await response.text()
                        content_type = "text"
                    
                    # Format result
                    result_content = self._format_response(
                        url, method, status_code, response_headers, response_data, content_type
                    )
                    
                    is_success = 200 <= status_code < 400
                    error_msg = None if is_success else f"HTTP {status_code} error"
                    
                    return ToolResult(
                        success=is_success,
                        content=result_content,
                        result_type=ToolResultType.TEXT,
                        error_message=error_msg,
                        metadata={
                            "tool": "http_request",
                            "url": url,
                            "method": method,
                            "status_code": status_code,
                            "content_type": content_type,
                            "response_size": len(str(response_data))
                        }
                    )
            
        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Request timed out after {timeout} seconds",
                error_message=f"Request timed out after {timeout} seconds"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"HTTP request failed: {str(e)}",
                error_message=f"HTTP request failed: {str(e)}"
            )
    
    def _format_response(self, url: str, method: str, status_code: int, 
                        headers: Dict, data: Any, content_type: str) -> str:
        """Format the HTTP response for display"""
        lines = [
            f"HTTP {method} Request to: {url}",
            f"Status Code: {status_code}",
            "",
            "Response Headers:",
        ]
        
        # Add key headers
        important_headers = ['content-type', 'content-length', 'server', 'date']
        for header in important_headers:
            if header in headers:
                lines.append(f"  {header}: {headers[header]}")
        
        lines.append("")
        lines.append("Response Body:")
        
        if content_type == "json":
            # Pretty print JSON
            try:
                formatted_json = json.dumps(data, indent=2)
                if len(formatted_json) > 2000:
                    lines.append(formatted_json[:2000] + "... (truncated)")
                else:
                    lines.append(formatted_json)
            except:
                lines.append(str(data))
        else:
            # Handle text response
            text_data = str(data)
            if len(text_data) > 2000:
                lines.append(text_data[:2000] + "... (truncated)")
            else:
                lines.append(text_data)
        
        return "\n".join(lines)


class DownloadFileTool(BaseTool):
    """Download files from URLs with progress tracking"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="download_file",
            description="Download files from URLs to local filesystem with progress tracking and resume support",
            category="network",
            parameters=[
                ToolParameter(
                    name="url",
                    description="The URL of the file to download",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="local_path",
                    description="Local file path to save the download (if not specified, uses filename from URL)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="overwrite",
                    description="Whether to overwrite existing files",
                    param_type="boolean",
                    required=False,
                    default=False
                ),
                ToolParameter(
                    name="chunk_size",
                    description="Download chunk size in bytes",
                    param_type="number",
                    required=False,
                    default=8192
                ),
                ToolParameter(
                    name="timeout",
                    description="Download timeout in seconds",
                    param_type="number",
                    required=False,
                    default=300
                ),
                ToolParameter(
                    name="headers",
                    description="Additional HTTP headers as JSON string",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="verify_ssl",
                    description="Whether to verify SSL certificates",
                    param_type="boolean",
                    required=False,
                    default=True
                )
            ]
        )
    
    async def execute(self, url: str, local_path: Optional[str] = None,
                     overwrite: bool = False, chunk_size: int = 8192,
                     timeout: int = 300, headers: Optional[str] = None,
                     verify_ssl: bool = True) -> ToolResult:
        """Execute file download"""
        try:
            # Determine local file path
            if not local_path:
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename:
                    filename = "downloaded_file"
                local_path = filename
            
            # Convert to Path object and create directories if needed
            file_path = Path(local_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists and handle overwrite
            if file_path.exists() and not overwrite:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"File already exists: {local_path}. Use overwrite=true to replace it.",
                    error_message="File already exists"
                )
            
            # Parse headers
            request_headers = {}
            if headers:
                try:
                    request_headers = json.loads(headers)
                except json.JSONDecodeError:
                    return ToolResult(
                        success=False,
                        result_type=ToolResultType.ERROR,
                        content="Invalid JSON format in headers",
                        error_message="Invalid JSON format in headers"
                    )
            
            # Create connector with SSL settings
            connector = aiohttp.TCPConnector(verify_ssl=verify_ssl)
            timeout_config = aiohttp.ClientTimeout(total=timeout)
            
            start_time = time.time()
            downloaded_bytes = 0
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout_config
            ) as session:
                async with session.get(url, headers=request_headers) as response:
                    
                    if response.status != 200:
                        return ToolResult(
                            success=False,
                            result_type=ToolResultType.ERROR,
                            content=f"Failed to download file. HTTP {response.status}: {response.reason}",
                            error_message=f"HTTP {response.status}: {response.reason}"
                        )
                    
                    # Get file size if available
                    total_size = None
                    if 'content-length' in response.headers:
                        total_size = int(response.headers['content-length'])
                    
                    # Download the file
                    with open(file_path, 'wb') as file:
                        async for chunk in response.content.iter_chunked(chunk_size):
                            file.write(chunk)
                            downloaded_bytes += len(chunk)
            
            end_time = time.time()
            download_time = end_time - start_time
            
            # Calculate download speed
            speed_mbps = (downloaded_bytes / (1024 * 1024)) / download_time if download_time > 0 else 0
            
            # Format file size
            def format_bytes(bytes_val):
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if bytes_val < 1024:
                        return f"{bytes_val:.1f} {unit}"
                    bytes_val /= 1024
                return f"{bytes_val:.1f} TB"
            
            result_content = f"Successfully downloaded file from {url}\n"
            result_content += f"Saved to: {file_path.absolute()}\n"
            result_content += f"File size: {format_bytes(downloaded_bytes)}\n"
            result_content += f"Download time: {download_time:.2f} seconds\n"
            result_content += f"Average speed: {speed_mbps:.2f} MB/s"
            
            if total_size and total_size != downloaded_bytes:
                result_content += f"\nWarning: Expected {format_bytes(total_size)}, got {format_bytes(downloaded_bytes)}"
            
            return ToolResult(
                success=True,
                content=result_content,
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "download_file",
                    "url": url,
                    "local_path": str(file_path.absolute()),
                    "file_size": downloaded_bytes,
                    "download_time": download_time,
                    "speed_mbps": speed_mbps
                }
            )
            
        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Download timed out after {timeout} seconds",
                error_message=f"Download timed out after {timeout} seconds"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Download failed: {str(e)}",
                error_message=f"Download failed: {str(e)}"
            )


# Register the tools
registry.register(HTTPRequestTool)
registry.register(DownloadFileTool)
