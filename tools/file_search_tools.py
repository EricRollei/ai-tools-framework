# tools/file_search_tools.py
"""
File search tools for the AI Tools framework
Includes native Windows search and Everything integration
"""

import os
import glob
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry
import re

class FileSearchTool(BaseTool):
    """Search for files on the local computer using various methods"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="search_files",
            description="Search for files on the local computer using filename patterns, content, or Everything search",
            category="file_system",
            parameters=[
                ToolParameter(
                    name="pattern",
                    description="Search pattern (filename, wildcard, or Everything syntax)",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="search_path",
                    description="Directory to search in (default: C:\\ for Everything, current directory for others)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="search_type",
                    description="Search method: 'everything' (fastest), 'glob' (pattern matching), 'content' (text in files)",
                    param_type="string",
                    required=False,
                    default="everything"
                ),
                ToolParameter(
                    name="max_results",
                    description="Maximum number of results to return",
                    param_type="number",
                    required=False,
                    default=50
                ),
                ToolParameter(
                    name="file_extensions",
                    description="Comma-separated list of file extensions to include (e.g., 'txt,pdf,docx')",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="include_content",
                    description="Whether to include file content preview in results",
                    param_type="boolean",
                    required=False,
                    default=False
                )
            ]
        )
    
    async def execute(self, pattern: str, search_path: Optional[str] = None, 
                     search_type: str = "everything", max_results: int = 50,
                     file_extensions: Optional[str] = None, include_content: bool = False) -> ToolResult:
        """Execute file search"""
        try:
            results = []
            
            if search_type == "everything":
                results = await self._search_with_everything(pattern, search_path, max_results, file_extensions)
            elif search_type == "glob":
                results = await self._search_with_glob(pattern, search_path, max_results, file_extensions)
            elif search_type == "content":
                results = await self._search_content(pattern, search_path, max_results, file_extensions)
            else:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Unknown search type: {search_type}. Use 'everything', 'glob', or 'content'.",
                    error_message=f"Unknown search type: {search_type}"
                )
            
            if include_content:
                results = await self._add_content_preview(results)
            
            # Format results
            if not results:
                content = f"No files found matching pattern '{pattern}'"
            else:
                content = self._format_results(results, pattern, search_type)
            
            return ToolResult(
                success=True,
                content=content,
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "search_files",
                    "pattern": pattern,
                    "search_type": search_type,
                    "results_count": len(results),
                    "search_path": search_path
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error searching files: {str(e)}",
                error_message=f"Error searching files: {str(e)}"
            )
    
    async def _search_with_everything(self, pattern: str, search_path: Optional[str], 
                                    max_results: int, file_extensions: Optional[str]) -> List[Dict]:
        """Search using Everything command line tool (es.exe)"""
        results = []
        
        # Check if Everything command line interface is available
        es_path = shutil.which("es.exe")
        if not es_path:
            # Try common Everything installation paths for es.exe
            common_paths = [
                r"C:\Program Files\ES-1.1.0.30.x64\es.exe",  # User's installation
                r"C:\Program Files\Everything\es.exe",
                r"C:\Program Files (x86)\Everything\es.exe",
                r"C:\Program Files\ES\es.exe",
                r"C:\Tools\Everything\es.exe",
                os.path.expanduser(r"~\AppData\Local\Everything\es.exe"),
                os.path.expanduser(r"~\AppData\Roaming\Everything\es.exe")
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    es_path = path
                    break
        
        if not es_path:
            # Fall back to glob search if es.exe not found
            return await self._search_with_glob(pattern, search_path, max_results, file_extensions)
        
        try:
            # Build Everything command line search
            cmd = [es_path]
            
            # Add result count limit
            cmd.extend(["-n", str(max_results)])
            
            # Build search pattern for Everything syntax
            search_terms = []
            
            # Add path filter if specified
            if search_path:
                # Everything uses path: syntax for path filtering
                search_terms.append(f'path:"{search_path}"')
            
            # Add the main search pattern
            search_terms.append(pattern)
            
            # Add file extension filter if specified
            if file_extensions:
                ext_terms = []
                for ext in file_extensions.split(","):
                    ext = ext.strip()
                    if not ext.startswith('.'):
                        ext = '.' + ext
                    ext_terms.append(f'ext:{ext}')
                
                # Combine with OR operator in Everything syntax
                if ext_terms:
                    search_terms.append(f'({" | ".join(ext_terms)})')
            
            # Combine all search terms
            search_query = " ".join(search_terms)
            cmd.append(search_query)
            
            # Execute Everything search
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and os.path.exists(line):
                        file_info = self._get_file_info(line)
                        results.append(file_info)
                        if len(results) >= max_results:
                            break
            else:
                # If Everything command failed, fall back to glob
                return await self._search_with_glob(pattern, search_path, max_results, file_extensions)
            
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError, Exception):
            # Fallback to glob search if Everything fails
            return await self._search_with_glob(pattern, search_path, max_results, file_extensions)
        
        return results
    
    async def _search_with_glob(self, pattern: str, search_path: Optional[str], 
                              max_results: int, file_extensions: Optional[str]) -> List[Dict]:
        """Search using Python glob patterns"""
        results = []
        
        if not search_path:
            search_path = os.getcwd()
        
        search_path = Path(search_path)
        
        try:
            # For simple patterns like "*", use directly; otherwise add wildcards
            if pattern == "*":
                search_patterns = ["**/*"]
            elif not any(char in pattern for char in ['*', '?', '[', ']']):
                # Simple text pattern - search in filename
                search_patterns = [f"**/*{pattern}*"]
            else:
                # Already a glob pattern
                search_patterns = [f"**/{pattern}"]
            
            # If file extensions specified, create patterns for each extension
            if file_extensions:
                ext_patterns = []
                for ext in file_extensions.split(","):
                    ext = ext.strip()
                    for base_pattern in search_patterns:
                        if base_pattern.endswith("*"):
                            ext_patterns.append(f"{base_pattern}.{ext}")
                        else:
                            ext_patterns.append(f"{base_pattern}*.{ext}")
                search_patterns = ext_patterns
            
            # Search with each pattern
            for search_pattern in search_patterns:
                try:
                    for file_path in search_path.glob(search_pattern):
                        if file_path.is_file():
                            file_info = self._get_file_info(str(file_path))
                            results.append(file_info)
                            if len(results) >= max_results:
                                break
                    if len(results) >= max_results:
                        break
                except (OSError, ValueError):
                    continue  # Skip invalid patterns
            
        except Exception as e:
            # If glob fails entirely, try simple os.walk
            return await self._search_with_walk(pattern, str(search_path), max_results, file_extensions)
        
        return results[:max_results]
    
    async def _search_with_walk(self, pattern: str, search_path: str, 
                              max_results: int, file_extensions: Optional[str]) -> List[Dict]:
        """Search using os.walk as fallback"""
        results = []
        pattern_lower = pattern.lower()
        
        extensions = None
        if file_extensions:
            extensions = [f".{ext.strip().lower()}" for ext in file_extensions.split(",")]
        
        try:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if len(results) >= max_results:
                        break
                    
                    file_lower = file.lower()
                    
                    # Check if filename matches pattern
                    if pattern_lower in file_lower:
                        # Check extension filter
                        if extensions:
                            file_ext = Path(file).suffix.lower()
                            if file_ext not in extensions:
                                continue
                        
                        file_path = os.path.join(root, file)
                        file_info = self._get_file_info(file_path)
                        results.append(file_info)
                
                if len(results) >= max_results:
                    break
                    
        except (PermissionError, OSError):
            pass  # Skip directories we can't access
        
        return results
    
    async def _search_content(self, pattern: str, search_path: Optional[str], 
                            max_results: int, file_extensions: Optional[str]) -> List[Dict]:
        """Search for pattern within file contents"""
        results = []
        
        if not search_path:
            search_path = os.getcwd()
        
        # Default to text file extensions if none specified
        if not file_extensions:
            file_extensions = "txt,py,js,html,css,json,xml,md,rst,log,ini,cfg,conf"
        
        extensions = [f".{ext.strip().lower()}" for ext in file_extensions.split(",")]
        pattern_regex = re.compile(re.escape(pattern), re.IGNORECASE)
        
        try:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if len(results) >= max_results:
                        break
                    
                    file_path = os.path.join(root, file)
                    file_ext = Path(file).suffix.lower()
                    
                    if file_ext in extensions:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if pattern_regex.search(content):
                                    file_info = self._get_file_info(file_path)
                                    file_info['content_match'] = True
                                    results.append(file_info)
                        except (PermissionError, OSError, UnicodeDecodeError):
                            continue
                
                if len(results) >= max_results:
                    break
                    
        except Exception:
            pass
        
        return results
    
    def _get_file_info(self, file_path: str) -> Dict:
        """Get file information"""
        try:
            stat = os.stat(file_path)
            path_obj = Path(file_path)
            
            return {
                'path': file_path,
                'name': path_obj.name,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'extension': path_obj.suffix,
                'directory': str(path_obj.parent)
            }
        except (OSError, PermissionError):
            return {
                'path': file_path,
                'name': Path(file_path).name,
                'size': 0,
                'modified': 0,
                'extension': Path(file_path).suffix,
                'directory': str(Path(file_path).parent)
            }
    
    async def _add_content_preview(self, results: List[Dict]) -> List[Dict]:
        """Add content preview to results"""
        for result in results:
            try:
                file_path = result['path']
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(500)  # First 500 characters
                    result['content_preview'] = content.strip()
            except (PermissionError, OSError, UnicodeDecodeError):
                result['content_preview'] = "[Unable to read file]"
        
        return results
    
    def _format_results(self, results: List[Dict], pattern: str, search_type: str) -> str:
        """Format search results for display"""
        if not results:
            return f"No files found matching '{pattern}'"
        
        output = [f"Found {len(results)} files matching '{pattern}' using {search_type} search:\n"]
        
        for i, result in enumerate(results, 1):
            path = result['path']
            name = result['name']
            size = result['size']
            
            # Format file size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.1f} MB"
            
            output.append(f"{i}. {name}")
            output.append(f"   Path: {path}")
            output.append(f"   Size: {size_str}")
            
            if 'content_match' in result:
                output.append(f"   Content match: Yes")
            
            if 'content_preview' in result:
                preview = result['content_preview'][:100]
                if len(result['content_preview']) > 100:
                    preview += "..."
                output.append(f"   Preview: {preview}")
            
            output.append("")
        
        return "\n".join(output)

# Register the tool
registry.register(FileSearchTool)
