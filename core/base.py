"""
AI Tools Framework: base.py
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

base.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# core/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ToolResultType(str, Enum):
    """Types of tool results"""
    TEXT = "text"
    JSON = "json"
    IMAGE = "image"
    FILE = "file"
    ERROR = "error"

class ToolResult(BaseModel):
    """Standardized tool result format"""
    success: bool
    result_type: ToolResultType
    content: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None

    class Config:
        use_enum_values = True

class ToolParameter(BaseModel):
    """Tool parameter definition"""
    name: str
    param_type: str  # "string", "number", "boolean", "array", "object"
    description: str
    required: bool = True
    default: Any = None
    enum_values: Optional[List[Any]] = None

class ToolDefinition(BaseModel):
    """Tool metadata and schema"""
    name: str
    description: str
    parameters: List[ToolParameter]
    category: str = "general"
    version: str = "1.0.0"

class BaseTool(ABC):
    """Abstract base class for all tools"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @property
    @abstractmethod
    def definition(self) -> ToolDefinition:
        """Return tool definition for registration"""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters"""
        pass
    
    def validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean parameters against tool definition"""
        validated = {}

        for param_def in self.definition.parameters:
            value = params.get(param_def.name)

            # Check required parameters
            if param_def.required and value is None:
                if param_def.default is not None:
                    value = param_def.default
                else:
                    raise ValueError(f"Missing required parameter: {param_def.name}")

            # Type validation (basic)
            if value is not None:
                validated[param_def.name] = value

        return validated