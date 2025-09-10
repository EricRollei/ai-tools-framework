# tools/file_management.py
"""
File management tools for the AI Tools framework
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

class FileListTool(BaseTool):
    """List files and directories in a specified path"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="list_files",
            description="List files and directories in a specified path",
            category="file_management",
            parameters=[
                ToolParameter(
                    name="path",
                    description="Directory path to list (use '.' for current directory)",
                    param_type="string",
                    required=True,
                    default="."
                ),
                ToolParameter(
                    name="show_hidden",
                    description="Whether to show hidden files (starting with .)",
                    param_type="boolean",
                    required=False,
                    default=False
                ),
                ToolParameter(
                    name="max_items",
                    description="Maximum number of items to return",
                    param_type="number",
                    required=False,
                    default=50
                )
            ]
        )
    
    async def execute(self, path: str = ".", show_hidden: bool = False, max_items: int = 50) -> ToolResult:
        """Execute file listing"""
        try:
            target_path = Path(path).resolve()
            
            if not target_path.exists():
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Path does not exist: {target_path}",
                    error_message=f"Path does not exist: {target_path}"
                )
            
            if not target_path.is_dir():
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Path is not a directory: {target_path}",
                    error_message=f"Path is not a directory: {target_path}"
                )
            
            items = []
            count = 0
            
            for item in sorted(target_path.iterdir()):
                if count >= max_items:
                    break
                
                if not show_hidden and item.name.startswith('.'):
                    continue
                
                item_info = {
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                    "modified": item.stat().st_mtime
                }
                
                items.append(item_info)
                count += 1
            
            result = {
                "path": str(target_path),
                "item_count": len(items),
                "items": items
            }
            
            return ToolResult(
                success=True,
                content=result,
                result_type=ToolResultType.JSON,
                metadata={"tool": "file_list", "path": str(target_path)}
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error listing files: {str(e)}",
                error_message=f"Error listing files: {str(e)}"
            )

class FileReadTool(BaseTool):
    """Read contents of a text file"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="read_file",
            description="Read the contents of a text file",
            category="file_management",
            parameters=[
                ToolParameter(
                    name="file_path",
                    description="Path to the file to read",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="encoding",
                    description="File encoding",
                    param_type="string",
                    required=False,
                    default="utf-8"
                ),
                ToolParameter(
                    name="max_size",
                    description="Maximum file size to read in bytes",
                    param_type="number",
                    required=False,
                    default=1048576  # 1MB
                )
            ]
        )
    
    async def execute(self, file_path: str, encoding: str = "utf-8", max_size: int = 1048576) -> ToolResult:
        """Execute file reading"""
        try:
            target_file = Path(file_path).resolve()
            
            if not target_file.exists():
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"File does not exist: {target_file}",
                    error_message=f"File does not exist: {target_file}"
                )
            
            if not target_file.is_file():
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Path is not a file: {target_file}",
                    error_message=f"Path is not a file: {target_file}"
                )
            
            file_size = target_file.stat().st_size
            if file_size > max_size:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"File too large ({file_size} bytes). Max size: {max_size} bytes",
                    error_message=f"File too large ({file_size} bytes). Max size: {max_size} bytes"
                )
            
            content = target_file.read_text(encoding=encoding)
            
            return ToolResult(
                success=True,
                content=content,
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "file_read",
                    "file_path": str(target_file),
                    "file_size": file_size,
                    "encoding": encoding
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error reading file: {str(e)}",
                error_message=f"Error reading file: {str(e)}"
            )

class FileWriteTool(BaseTool):
    """Write content to a file"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="write_file",
            description="Write content to a file",
            category="file_management",
            parameters=[
                ToolParameter(
                    name="file_path",
                    description="Path to the file to write",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="content",
                    description="Content to write to the file",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="encoding",
                    description="File encoding",
                    param_type="string",
                    required=False,
                    default="utf-8"
                ),
                ToolParameter(
                    name="create_dirs",
                    description="Create parent directories if they don't exist",
                    param_type="boolean",
                    required=False,
                    default=True
                )
            ]
        )
    
    async def execute(self, file_path: str, content: str, encoding: str = "utf-8", create_dirs: bool = True) -> ToolResult:
        """Execute file writing"""
        try:
            target_file = Path(file_path).resolve()
            
            if create_dirs:
                target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Clean the content to handle encoding issues
            cleaned_content = self._clean_content_for_encoding(content)
            
            # Try to write with specified encoding, fallback to safer options
            try:
                target_file.write_text(cleaned_content, encoding=encoding)
            except UnicodeEncodeError as e:
                # Fallback to utf-8 with error handling
                target_file.write_text(cleaned_content, encoding='utf-8', errors='ignore')
                
            return ToolResult(
                success=True,
                content=f"Successfully wrote {len(cleaned_content)} characters to {target_file}",
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "file_write",
                    "file_path": str(target_file),
                    "content_length": len(cleaned_content),
                    "encoding": encoding,
                    "original_length": len(content)
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error writing file: {str(e)}",
                error_message=f"Error writing file: {str(e)}"
            )
    
    def _clean_content_for_encoding(self, content: str) -> str:
        """Clean content to handle encoding issues"""
        import unicodedata
        
        # Replace common problematic characters
        replacements = {
            '\u2013': '-',  # en dash
            '\u2014': '-',  # em dash
            '\u2018': "'",  # left single quotation mark
            '\u2019': "'",  # right single quotation mark
            '\u201c': '"',  # left double quotation mark
            '\u201d': '"',  # right double quotation mark
            '\u2026': '...',  # horizontal ellipsis
            '\u00a0': ' ',  # non-breaking space
            '\u2022': '*',  # bullet
        }
        
        cleaned = content
        for char, replacement in replacements.items():
            cleaned = cleaned.replace(char, replacement)
        
        # Remove or replace any remaining problematic characters
        try:
            # Try to encode/decode to catch issues
            cleaned.encode('utf-8')
        except UnicodeEncodeError:
            # If there are still issues, normalize and filter
            cleaned = unicodedata.normalize('NFKD', cleaned)
            # Keep only characters that can be safely encoded
            cleaned = ''.join(char for char in cleaned if ord(char) < 65536 and char.isprintable() or char.isspace())
        
        return cleaned

class TextCleanTool(BaseTool):
    """Clean text content to remove problematic Unicode characters"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="clean_text",
            description="Clean text content to remove problematic Unicode characters that might cause encoding issues",
            category="file_management",
            parameters=[
                ToolParameter(
                    name="text",
                    description="Text content to clean",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="strict_ascii",
                    description="Whether to enforce strict ASCII characters only",
                    param_type="boolean",
                    required=False,
                    default=False
                )
            ]
        )
    
    async def execute(self, text: str, strict_ascii: bool = False) -> ToolResult:
        """Execute text cleaning"""
        try:
            import unicodedata
            
            # Replace common problematic characters
            replacements = {
                '\u2013': '-',  # en dash
                '\u2014': '-',  # em dash  
                '\u2018': "'",  # left single quotation mark
                '\u2019': "'",  # right single quotation mark
                '\u201c': '"',  # left double quotation mark
                '\u201d': '"',  # right double quotation mark
                '\u2026': '...',  # horizontal ellipsis
                '\u00a0': ' ',  # non-breaking space
                '\u2022': '*',  # bullet
                '\u2192': '->',  # right arrow
                '\u2190': '<-',  # left arrow
                '\u00b0': ' degrees',  # degree symbol
                '\u00b5': 'u',  # micro sign
                '\u03b2': 'beta',  # Greek beta (if strict ASCII)
                '\u03b1': 'alpha',  # Greek alpha (if strict ASCII)
                '\u03b3': 'gamma',  # Greek gamma (if strict ASCII)
            }
            
            cleaned = text
            
            # Apply replacements
            for char, replacement in replacements.items():
                if strict_ascii or char in ['\u2013', '\u2014', '\u2018', '\u2019', '\u201c', '\u201d', '\u2026', '\u00a0', '\u2022']:
                    cleaned = cleaned.replace(char, replacement)
            
            # If strict ASCII, remove non-ASCII characters
            if strict_ascii:
                cleaned = ''.join(char for char in cleaned if ord(char) < 128)
            else:
                # Normalize Unicode and remove surrogates
                cleaned = unicodedata.normalize('NFKD', cleaned)
                # Remove surrogate pairs and non-printable characters
                cleaned = ''.join(char for char in cleaned if 
                                not (0xD800 <= ord(char) <= 0xDFFF) and  # Remove surrogates
                                (char.isprintable() or char.isspace()))
            
            stats = {
                "original_length": len(text),
                "cleaned_length": len(cleaned),
                "characters_changed": len(text) - len(cleaned),
                "encoding_safe": True
            }
            
            # Test if the cleaned text can be safely encoded
            try:
                cleaned.encode('utf-8')
            except UnicodeEncodeError:
                stats["encoding_safe"] = False
            
            return ToolResult(
                success=True,
                content=cleaned,
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "clean_text",
                    "stats": stats,
                    "strict_ascii": strict_ascii
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error cleaning text: {str(e)}",
                error_message=f"Error cleaning text: {str(e)}"
            )

# Register all file management tools
registry.register(FileListTool)
registry.register(FileReadTool)
registry.register(FileWriteTool)
registry.register(TextCleanTool)
