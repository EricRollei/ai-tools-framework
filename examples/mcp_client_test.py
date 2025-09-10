"""
AI Tools Framework: mcp_client_test.py
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

mcp_client_test.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# examples/mcp_client_test.py
#!/usr/bin/env python3
"""
Test script for MCP client functionality
This simulates how Claude would interact with the MCP server
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.registry import registry
from tools import *  # This imports and registers all tools

async def test_mcp_interface():
    """Test MCP-style tool execution"""
    print("🔧 Testing MCP Interface...")
    
    # List available tools
    tools = registry.list_tools()
    print(f"📋 Available tools: {len(tools)}")
    
    for tool_def in tools:
        print(f"  • {tool_def.name}: {tool_def.description}")
    
    # Test tool execution
    print("\n🔍 Testing web search...")
    
    try:
        tool = registry.get_tool("web_search")
        result = await tool.execute(
            query="best Python web frameworks 2024",
            num_results=3
        )
        
        if result.success:
            print("✅ MCP tool execution successful!")
            print(f"📊 Result type: {result.result_type}")
            print(f"🏷️  Metadata: {json.dumps(result.metadata, indent=2)}")
        else:
            print(f"❌ Tool execution failed: {result.error_message}")
            
    except Exception as e:
        print(f"💥 MCP test error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_mcp_interface())
