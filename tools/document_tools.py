# tools/document_tools.py
"""
Document creation tools for various formats
"""

import json
import csv
import io
from pathlib import Path
from typing import Dict, Any, List, Optional
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

class MarkdownWriteTool(BaseTool):
    """Create Markdown documents with proper formatting"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="write_markdown",
            description="Create a Markdown (.md) document with proper formatting",
            category="document_creation",
            parameters=[
                ToolParameter(
                    name="file_path",
                    description="Path to the markdown file to create",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="title",
                    description="Document title",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="content",
                    description="Main content (can include markdown syntax)",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="author",
                    description="Document author",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="add_toc",
                    description="Add table of contents",
                    param_type="boolean",
                    required=False,
                    default=False
                )
            ]
        )
    
    async def execute(self, file_path: str, title: str, content: str, 
                     author: Optional[str] = None, add_toc: bool = False) -> ToolResult:
        """Create markdown document"""
        try:
            target_file = Path(file_path)
            if not target_file.suffix:
                target_file = target_file.with_suffix('.md')
            
            # Build markdown content
            md_content = f"# {title}\n\n"
            
            if author:
                md_content += f"**Author:** {author}\n\n"
            
            if add_toc:
                # Extract headers for TOC (simple version)
                headers = []
                for line in content.split('\n'):
                    if line.startswith('#'):
                        level = len(line) - len(line.lstrip('#'))
                        header_text = line.lstrip('#').strip()
                        headers.append((level, header_text))
                
                if headers:
                    md_content += "## Table of Contents\n\n"
                    for level, header in headers:
                        indent = "  " * (level - 1)
                        anchor = header.lower().replace(' ', '-').replace('.', '').replace(',', '')
                        md_content += f"{indent}- [{header}](#{anchor})\n"
                    md_content += "\n"
            
            md_content += content
            
            # Ensure parent directory exists
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            target_file.write_text(md_content, encoding='utf-8')
            
            return ToolResult(
                success=True,
                content=f"Successfully created markdown file: {target_file}",
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "write_markdown",
                    "file_path": str(target_file),
                    "title": title,
                    "content_length": len(md_content),
                    "has_toc": add_toc
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error creating markdown file: {str(e)}",
                error_message=f"Error creating markdown file: {str(e)}"
            )

class CSVWriteTool(BaseTool):
    """Create CSV files from structured data"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="write_csv",
            description="Create a CSV file from structured data",
            category="document_creation",
            parameters=[
                ToolParameter(
                    name="file_path",
                    description="Path to the CSV file to create",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="headers",
                    description="Column headers (comma-separated)",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="data",
                    description="Data rows (JSON array of arrays or objects)",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="delimiter",
                    description="CSV delimiter character",
                    param_type="string",
                    required=False,
                    default=","
                )
            ]
        )
    
    async def execute(self, file_path: str, headers: str, data: str, delimiter: str = ",") -> ToolResult:
        """Create CSV file"""
        try:
            target_file = Path(file_path)
            if not target_file.suffix:
                target_file = target_file.with_suffix('.csv')
            
            # Parse headers
            header_list = [h.strip() for h in headers.split(',')]
            
            # Parse data
            try:
                data_parsed = json.loads(data)
            except json.JSONDecodeError:
                # Try to parse as simple rows
                data_parsed = []
                for line in data.strip().split('\n'):
                    row = [cell.strip() for cell in line.split(delimiter)]
                    data_parsed.append(row)
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output, delimiter=delimiter)
            
            # Write headers
            writer.writerow(header_list)
            
            # Write data
            for row in data_parsed:
                if isinstance(row, dict):
                    # Convert dict to list based on headers
                    row_data = [str(row.get(header, '')) for header in header_list]
                else:
                    # Assume it's already a list/array
                    row_data = [str(cell) for cell in row]
                writer.writerow(row_data)
            
            csv_content = output.getvalue()
            output.close()
            
            # Ensure parent directory exists
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            target_file.write_text(csv_content, encoding='utf-8')
            
            return ToolResult(
                success=True,
                content=f"Successfully created CSV file: {target_file}",
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "write_csv",
                    "file_path": str(target_file),
                    "rows": len(data_parsed),
                    "columns": len(header_list),
                    "delimiter": delimiter
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error creating CSV file: {str(e)}",
                error_message=f"Error creating CSV file: {str(e)}"
            )

class JSONWriteTool(BaseTool):
    """Create JSON files with proper formatting"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="write_json",
            description="Create a JSON file with proper formatting",
            category="document_creation",
            parameters=[
                ToolParameter(
                    name="file_path",
                    description="Path to the JSON file to create",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="data",
                    description="JSON data as string",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="pretty_print",
                    description="Format JSON with indentation",
                    param_type="boolean",
                    required=False,
                    default=True
                )
            ]
        )
    
    async def execute(self, file_path: str, data: str, pretty_print: bool = True) -> ToolResult:
        """Create JSON file"""
        try:
            target_file = Path(file_path)
            if not target_file.suffix:
                target_file = target_file.with_suffix('.json')
            
            # Parse and validate JSON
            try:
                json_data = json.loads(data)
            except json.JSONDecodeError as e:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Invalid JSON data: {str(e)}",
                    error_message=f"Invalid JSON data: {str(e)}"
                )
            
            # Format JSON
            if pretty_print:
                json_content = json.dumps(json_data, indent=2, ensure_ascii=False)
            else:
                json_content = json.dumps(json_data, ensure_ascii=False)
            
            # Ensure parent directory exists
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            target_file.write_text(json_content, encoding='utf-8')
            
            return ToolResult(
                success=True,
                content=f"Successfully created JSON file: {target_file}",
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "write_json",
                    "file_path": str(target_file),
                    "content_length": len(json_content),
                    "pretty_formatted": pretty_print
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error creating JSON file: {str(e)}",
                error_message=f"Error creating JSON file: {str(e)}"
            )

# Register document tools
registry.register(MarkdownWriteTool)
registry.register(CSVWriteTool) 
registry.register(JSONWriteTool)
