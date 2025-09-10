"""
AI Tools Framework: registry.py
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

registry.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# core/registry.py  
from typing import Dict, List, Type
from .base import BaseTool, ToolDefinition
import logging

logger = logging.getLogger(__name__)

class ToolRegistry:
    """Central registry for all available tools"""
    
    def __init__(self):
        self._tools: Dict[str, Type[BaseTool]] = {}
        self._instances: Dict[str, BaseTool] = {}
        
    def register(self, tool_class: Type[BaseTool]) -> None:
        """Register a tool class"""
        # Create temporary instance to get definition
        temp_instance = tool_class()
        tool_name = temp_instance.definition.name
        
        self._tools[tool_name] = tool_class
        logger.info(f"Registered tool: {tool_name}")
        
    def get_tool(self, tool_name: str, config: Dict = None) -> BaseTool:
        """Get tool instance (cached)"""
        cache_key = f"{tool_name}_{hash(str(sorted((config or {}).items())))}"
        
        if cache_key not in self._instances:
            if tool_name not in self._tools:
                raise ValueError(f"Tool not found: {tool_name}")
                
            tool_class = self._tools[tool_name]
            self._instances[cache_key] = tool_class(config)
            
        return self._instances[cache_key]
    
    def list_tools(self) -> List[ToolDefinition]:
        """List all registered tools"""
        definitions = []
        for tool_class in self._tools.values():
            temp_instance = tool_class()
            definitions.append(temp_instance.definition)
        return definitions
    
    def get_tool_definition(self, tool_name: str) -> ToolDefinition:
        """Get definition for specific tool"""
        if tool_name not in self._tools:
            raise ValueError(f"Tool not found: {tool_name}")
            
        tool_class = self._tools[tool_name]
        temp_instance = tool_class()
        return temp_instance.definition

# Global registry instance
registry = ToolRegistry()