#!/usr/bin/env python3
"""
AI Tools Framework: test_claude_compatibility.py
Description: Claude Desktop integration testing
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

test_claude_compatibility.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

"""
Test script to validate MCP server compatibility with Claude Desktop
"""

import sys
import json
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except Exception as e:
        print(f"❌ Failed to load environment: {e}")
        return False
    
    try:
        import tools
        print("✅ Tools imported successfully")
    except Exception as e:
        print(f"❌ Failed to import tools: {e}")
        return False
    
    try:
        from core.registry import registry
        tool_count = len(registry.list_tools())
        print(f"✅ Registry loaded with {tool_count} tools")
    except Exception as e:
        print(f"❌ Failed to load registry: {e}")
        return False
    
    try:
        from interfaces.mcp_server import MCPToolServer
        print("✅ MCP server class imported")
    except Exception as e:
        print(f"❌ Failed to import MCP server: {e}")
        return False
    
    return True

def test_tool_schemas():
    """Test that tool schemas are valid for MCP"""
    print("\nTesting tool schemas...")
    
    try:
        from core.registry import registry
        from interfaces.mcp_server import MCPToolServer
        
        server = MCPToolServer()
        
        # Test schema conversion
        tools = registry.list_tools()
        for tool_def in tools[:3]:  # Test first 3 tools
            try:
                schema = server._convert_parameters_to_schema(tool_def.parameters)
                print(f"✅ {tool_def.name}: Valid schema")
            except Exception as e:
                print(f"❌ {tool_def.name}: Schema error - {e}")
                return False
                
        print(f"✅ All tested tool schemas valid")
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False

def test_claude_config():
    """Test Claude Desktop configuration"""
    print("\nTesting Claude Desktop configuration...")
    
    config_path = Path("claude_config.json")
    if not config_path.exists():
        print("❌ claude_config.json not found")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if "mcpServers" not in config:
            print("❌ No mcpServers in config")
            return False
        
        if "ai-tools" not in config["mcpServers"]:
            print("❌ ai-tools server not configured")
            return False
        
        server_config = config["mcpServers"]["ai-tools"]
        
        # Check required fields
        required_fields = ["command", "args", "cwd"]
        for field in required_fields:
            if field not in server_config:
                print(f"❌ Missing required field: {field}")
                return False
        
        # Validate paths
        main_path = Path(server_config["args"][0])
        if not main_path.exists():
            print(f"❌ Main script not found: {main_path}")
            return False
        
        cwd_path = Path(server_config["cwd"])
        if not cwd_path.exists():
            print(f"❌ Working directory not found: {cwd_path}")
            return False
        
        print("✅ Claude Desktop configuration valid")
        return True
        
    except Exception as e:
        print(f"❌ Config validation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 AI Tools MCP Server - Claude Desktop Compatibility Test\n")
    
    all_passed = True
    
    # Run tests
    all_passed &= test_imports()
    all_passed &= test_tool_schemas()
    all_passed &= test_claude_config()
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed! Server should work with Claude Desktop.")
        print("\nNext steps:")
        print("1. Copy claude_config.json content to Claude Desktop settings")
        print("2. Restart Claude Desktop")
        print("3. Test with a simple command like 'list available tools'")
    else:
        print("❌ Some tests failed. Please fix issues before using with Claude Desktop.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
