#!/usr/bin/env python3
"""
AI Tools Framework: ai_tools_stdio_mcp.py
Description: MCP server optimized for LM Studio stdio communication
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

ai_tools_stdio_mcp.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

"""
AI Tools MCP server using simple stdio for LM Studio compatibility
Includes the web search functionality from your original framework
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import tools to trigger registration
import tools

from core.registry import registry

# Set up logging to file only
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_tools_stdio_mcp.log')
    ]
)
logger = logging.getLogger(__name__)

class AIToolsStdioMCP:
    """AI Tools MCP server using stdio for LM Studio"""
    
    def __init__(self):
        self.server_info = {
            "name": "ai-tools-stdio",
            "version": "1.0.0"
        }
        
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        logger.info(f"Initialize request received: {params}")  # Enhanced logging
        
        # Check what type params actually is  
        logger.info(f"Params type: {type(params)}")  # Debug the type
        
        # Log if capabilities exists and its type
        if 'capabilities' in params:
            logger.info(f"Capabilities found: {params['capabilities']}, type: {type(params['capabilities'])}")
        else:
            logger.info("No capabilities in params")
        
        return {
            "protocolVersion": "2025-06-18",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": self.server_info
        }
    
    def handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request"""
        logger.info("Tools list requested")
        
        tools = []
        
        # Get tools from registry
        for tool_def in registry.list_tools():
            # Convert our tool definition to MCP format
            mcp_tool = {
                "name": tool_def.name,
                "description": tool_def.description,
                "inputSchema": {
                    "type": "object",
                    "properties": self._convert_parameters_to_schema(tool_def.parameters),
                    "required": [p.name for p in tool_def.parameters if p.required]
                }
            }
            tools.append(mcp_tool)
        
        logger.info(f"Returning {len(tools)} tools")
        return {"tools": tools}
    
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
    
    def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Tool call: {tool_name} with args: {arguments}")
        
        try:
            # Validate tool exists
            if not tool_name:
                raise ValueError("Tool name is required")
            
            # Get tool instance
            tool = registry.get_tool(tool_name)
            
            # Execute the tool synchronously (convert async result)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(tool.execute(**arguments))
            finally:
                loop.close()
            
            # Ensure we have a valid result object
            if not hasattr(result, 'success'):
                raise ValueError("Tool returned invalid result object")
            
            if result.success:
                # Format successful result
                content = self._format_tool_result(result)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": content
                        }
                    ]
                }
            else:
                # Handle error - return as proper error response
                error_msg = getattr(result, 'error_message', 'Unknown error')
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error: {error_msg}"
                        }
                    ],
                    "isError": True
                }
                
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            logger.exception("Full traceback:")
            # Return error as content rather than raising
            return {
                "content": [
                    {
                        "type": "text", 
                        "text": f"Tool execution error: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    def _format_tool_result(self, result) -> str:
        """Format tool result for MCP response"""
        from core.base import ToolResultType
        
        if result.result_type == ToolResultType.JSON:
            # Pretty print JSON results
            return json.dumps(result.content, indent=2, ensure_ascii=False)
        elif result.result_type == ToolResultType.TEXT:
            return str(result.content)
        else:
            # For other types, convert to string representation
            return str(result.content)
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        logger.info(f"Handling request: {method} (ID: {request_id})")
        
        try:
            if method == "initialize":
                result = self.handle_initialize(params)
            elif method == "tools/list":
                result = self.handle_list_tools(params)
            elif method == "tools/call":
                result = self.handle_call_tool(params)
            else:
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Unknown method: {method}"
                        }
                    ],
                    "isError": True
                }
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            logger.exception("Full traceback:")
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
        
        return response
    
    def run(self):
        """Run the server synchronously"""
        logger.info("Starting AI Tools stdio MCP server...")
        logger.info("=== This is the CUSTOM stdio MCP server (ai_tools_stdio_mcp.py) ===")
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                logger.debug(f"Received: {line}")
                
                try:
                    request = json.loads(line)
                    response = self.handle_request(request)
                    
                    response_json = json.dumps(response)
                    logger.debug(f"Sending: {response_json}")
                    
                    print(response_json)
                    sys.stdout.flush()
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                    continue
                    
        except EOFError:
            logger.info("EOF received, shutting down")
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise

def main():
    """Main entry point"""
    server = AIToolsStdioMCP()
    server.run()

if __name__ == "__main__":
    logger.info("AI Tools stdio MCP server starting...")
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server interrupted")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.exception("Fatal error traceback:")
        sys.exit(1)
