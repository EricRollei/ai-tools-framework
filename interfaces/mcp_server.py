"""
AI Tools Framework: mcp_server.py
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

mcp_server.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# interfaces/mcp_server.py
import asyncio
import json
import sys
import traceback
from typing import Any, Dict, List
from pydantic import ValidationError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool as MCPTool,
    TextContent,
    CallToolResult,
    InitializeRequestParams,
    InitializeResult,
    ClientCapabilities,
    Implementation,
    InitializeRequest
)
from core.registry import registry
from core.base import ToolResultType
from config.settings import settings
import logging

# Set up logging for Claude Desktop compatibility
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)  # Claude Desktop reads stderr for logs
    ]
)
logger = logging.getLogger(__name__)

class MCPToolServer:
    """MCP Server implementation for tool execution"""
    
    def __init__(self):
        self.server = Server("ai-tools-mcp")
        self._setup_handlers()
        
    def _setup_handlers(self):
        """Set up MCP server handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> List[MCPTool]:
            """List all available tools"""
            try:
                tools = []
                
                for tool_def in registry.list_tools():
                    # Convert our tool definition to MCP format
                    mcp_tool = MCPTool(
                        name=tool_def.name,
                        description=tool_def.description,
                        inputSchema={
                            "type": "object",
                            "properties": self._convert_parameters_to_schema(tool_def.parameters),
                            "required": [p.name for p in tool_def.parameters if p.required]
                        }
                    )
                    tools.append(mcp_tool)
                    
                logger.info(f"Listed {len(tools)} tools for Claude Desktop")
                return tools
                
            except Exception as e:
                logger.error(f"Error listing tools: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return []
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Execute a tool with given arguments"""
            try:
                logger.info(f"Claude Desktop executing tool: {name} with args: {arguments}")
                
                # Get tool instance
                tool = registry.get_tool(name)
                if not tool:
                    error_msg = f"Tool '{name}' not found"
                    logger.error(error_msg)
                    return CallToolResult(
                        content=[TextContent(type="text", text=error_msg)],
                        isError=True
                    )
                
                # Execute the tool
                result = await tool.execute(**arguments)
                
                if result.success:
                    # Format successful result
                    content = self._format_tool_result(result)
                    logger.info(f"Tool '{name}' executed successfully")
                    return CallToolResult(content=[TextContent(type="text", text=content)])
                else:
                    # Handle error
                    error_content = f"Tool execution failed: {result.error_message}"
                    logger.error(f"Tool '{name}' failed: {result.error_message}")
                    return CallToolResult(
                        content=[TextContent(type="text", text=error_content)],
                        isError=True
                    )
                    
            except ValidationError as e:
                error_msg = f"Parameter validation failed for '{name}': {str(e)}"
                logger.error(error_msg)
                return CallToolResult(
                    content=[TextContent(type="text", text=error_msg)],
                    isError=True
                )
                
            except Exception as e:
                error_msg = f"Tool execution error for '{name}': {str(e)}"
                logger.error(error_msg)
                logger.error(f"Traceback: {traceback.format_exc()}")
                return CallToolResult(
                    content=[TextContent(type="text", text=error_msg)],
                    isError=True
                )
    
    def _convert_parameters_to_schema(self, parameters) -> Dict[str, Any]:
        """Convert tool parameters to JSON schema format"""
        properties = {}
        
        for param in parameters:
            prop = {
                "description": param.description
            }
            
            # Map parameter types to JSON schema types
            type_mapping = {
                "string": "string",
                "number": "number", 
                "boolean": "boolean",
                "array": "array",
                "object": "object"
            }
            
            prop["type"] = type_mapping.get(param.param_type, "string")
            
            # Add enum if specified
            if param.enum_values:
                prop["enum"] = param.enum_values
                
            # Add default if specified
            if param.default is not None:
                prop["default"] = param.default
                
            properties[param.name] = prop
            
        return properties
    
    def _format_tool_result(self, result) -> str:
        """Format tool result for MCP response"""
        if result.result_type == ToolResultType.JSON:
            # Pretty print JSON results
            return json.dumps(result.content, indent=2, ensure_ascii=False)
        elif result.result_type == ToolResultType.TEXT:
            return str(result.content)
        else:
            # For other types, convert to string representation
            return str(result.content)
    
    async def run(self):
        """Run the MCP server with enhanced error handling for Claude Desktop"""
        try:
            logger.info("Starting MCP server for Claude Desktop...")
            logger.info(f"Registered tools: {len(registry.list_tools())}")
            
            # Ensure stdio is properly configured
            sys.stdin.reconfigure(encoding='utf-8')
            sys.stdout.reconfigure(encoding='utf-8')
            
            async with stdio_server() as (read_stream, write_stream):
                logger.info("MCP server connected and ready")
                # Create proper initialization options for the server
                init_options = self.server.create_initialization_options()
                await self.server.run(
                    read_stream, 
                    write_stream,
                    initialization_options=init_options
                )
                
        except KeyboardInterrupt:
            logger.info("MCP server shutting down gracefully...")
        except Exception as e:
            logger.error(f"MCP server error: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise


