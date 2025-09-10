"""
AI Tools Framework: openai_api.py
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

openai_api.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# interfaces/openai_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
import json
import uuid
from datetime import datetime

from core.registry import registry
from core.base import ToolResultType
from config.settings import settings
import logging

import tools

logger = logging.getLogger(__name__)

# OpenAI-compatible data models
class FunctionParameter(BaseModel):
    type: str
    description: str
    enum: Optional[List[str]] = None
    default: Optional[Any] = None

class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class ToolDefinition(BaseModel):
    type: str = "function"
    function: FunctionDefinition

class ToolCall(BaseModel):
    id: str
    type: str = "function"
    function: Dict[str, Any]

class ToolCallResult(BaseModel):
    tool_call_id: str
    role: str = "tool"
    content: str

class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    tools: Optional[List[ToolDefinition]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Optional[Dict[str, int]] = None

class OpenAIToolAPI:
    """OpenAI-compatible API for tool execution"""
    
    def __init__(self):
        self.app = FastAPI(
            title="AI Tools OpenAI API",
            description="OpenAI-compatible API for tool execution with LM Studio",
            version="1.0.0"
        )
        self._setup_middleware()
        self._setup_routes()
    
    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/v1/tools")
        async def list_tools():
            """List available tools in OpenAI function format"""
            tools = []
            
            for tool_def in registry.list_tools():
                function_def = FunctionDefinition(
                    name=tool_def.name,
                    description=tool_def.description,
                    parameters=self._convert_to_openai_schema(tool_def.parameters)
                )
                
                tools.append(ToolDefinition(function=function_def))
            
            return {"tools": tools}
        
        @self.app.post("/v1/chat/completions")
        async def chat_completions(request: ChatCompletionRequest):
            """
            Handle chat completions with tool calls
            This endpoint processes tool calls and returns results
            """
            
            # Find the last message with tool calls
            tool_calls_message = None
            for msg in reversed(request.messages):
                if msg.tool_calls:
                    tool_calls_message = msg
                    break
            
            if not tool_calls_message:
                raise HTTPException(status_code=400, detail="No tool calls found in messages")
            
            # Process each tool call
            tool_results = []
            
            for tool_call in tool_calls_message.tool_calls:
                try:
                    # Extract function name and arguments
                    func_name = tool_call.function.get("name")
                    func_args = tool_call.function.get("arguments", {})
                    
                    # Parse arguments if they're a string
                    if isinstance(func_args, str):
                        func_args = json.loads(func_args)
                    
                    logger.info(f"Executing tool: {func_name} with args: {func_args}")
                    
                    # Get and execute the tool
                    tool = registry.get_tool(func_name)
                    result = await tool.execute(**func_args)
                    
                    # Format result
                    if result.success:
                        content = self._format_tool_result(result)
                    else:
                        content = f"Error: {result.error_message}"
                    
                    tool_results.append(ToolCallResult(
                        tool_call_id=tool_call.id,
                        content=content
                    ))
                    
                except Exception as e:
                    logger.error(f"Tool execution failed: {str(e)}")
                    tool_results.append(ToolCallResult(
                        tool_call_id=tool_call.id,
                        content=f"Tool execution failed: {str(e)}"
                    ))
            
            # Return response in OpenAI format
            return ChatCompletionResponse(
                id=f"chatcmpl-{uuid.uuid4().hex[:20]}",
                created=int(datetime.now().timestamp()),
                model=request.model,
                choices=[{
                    "index": 0,
                    "message": {
                        "role": "assistant", 
                        "content": None,
                        "tool_calls": [
                            {
                                "id": result.tool_call_id,
                                "type": "function",
                                "function": {
                                    "name": "tool_result",
                                    "arguments": json.dumps({"content": result.content})
                                }
                            } for result in tool_results
                        ]
                    },
                    "finish_reason": "tool_calls"
                }],
                usage={
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            )
        
        @self.app.post("/v1/tools/execute")
        async def execute_tool_direct(
            tool_name: str,
            arguments: Dict[str, Any]
        ):
            """
            Direct tool execution endpoint (non-OpenAI standard)
            Useful for testing and simple integrations
            """
            try:
                logger.info(f"Direct execution: {tool_name} with args: {arguments}")
                
                tool = registry.get_tool(tool_name)
                result = await tool.execute(**arguments)
                
                # Debug: Print the exact result structure
                print(f"DEBUG: result = {result}")
                print(f"DEBUG: result.result_type = {result.result_type}")
                print(f"DEBUG: type of result.result_type = {type(result.result_type)}")
                
                return {
                    "success": result.success,
                    "result_type": str(result.result_type),  # Force to string
                    "content": result.content,
                    "metadata": result.metadata,
                    "error_message": result.error_message
                }
                
            except Exception as e:
                print(f"DEBUG: Exception details: {e}")
                print(f"DEBUG: Exception type: {type(e)}")
                import traceback
                traceback.print_exc()
                logger.error(f"Direct tool execution failed: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "tools_available": len(registry.list_tools()),
                "timestamp": datetime.now().isoformat()
            }
    
    def _convert_to_openai_schema(self, parameters) -> Dict[str, Any]:
        """Convert tool parameters to OpenAI function schema"""
        properties = {}
        required = []
        
        for param in parameters:
            properties[param.name] = {
                "type": param.param_type,
                "description": param.description
            }
            
            if param.enum_values:
                properties[param.name]["enum"] = param.enum_values
            
            if param.default is not None:
                properties[param.name]["default"] = param.default
            
            if param.required:
                required.append(param.name)
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }
    
    def _format_tool_result(self, result) -> str:
        result_type = result.result_type if isinstance(result.result_type, str) else result.result_type.value
        if result_type == "json":
            return json.dumps(result.content, indent=2, ensure_ascii=False)
        elif result_type == "text":
            return str(result.content)
        else:
            return str(result.content)

