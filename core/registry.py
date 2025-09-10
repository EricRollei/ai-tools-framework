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