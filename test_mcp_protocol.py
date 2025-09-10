#!/usr/bin/env python3
"""
Test MCP protocol communication for Claude Desktop debugging
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_mcp_protocol():
    """Test MCP protocol messages"""
    
    # Import after path setup
    from dotenv import load_dotenv
    load_dotenv()
    
    import tools
    from interfaces.mcp_server import MCPToolServer
    
    print("Creating MCP server instance...")
    server = MCPToolServer()
    
    print("Testing list_tools handler...")
    try:
        # Get the handler function
        list_tools_handler = None
        for handler in server.server._tool_list_handlers:
            list_tools_handler = handler
            break
        
        if list_tools_handler:
            tools_list = await list_tools_handler()
            print(f"✅ Successfully listed {len(tools_list)} tools")
            
            # Show first few tools
            for i, tool in enumerate(tools_list[:3]):
                print(f"  {i+1}. {tool.name}: {tool.description[:50]}...")
                
        else:
            print("❌ No list_tools handler found")
            
    except Exception as e:
        print(f"❌ Error testing list_tools: {e}")
        import traceback
        print(traceback.format_exc())
    
    print("\nTesting call_tool handler...")
    try:
        # Get the handler function
        call_tool_handler = None
        for handler in server.server._tool_call_handlers:
            call_tool_handler = handler
            break
        
        if call_tool_handler:
            # Test with a simple tool
            result = await call_tool_handler("list_files", {"directory_path": "."})
            print(f"✅ Successfully called list_files tool")
            print(f"   Result type: {type(result)}")
            print(f"   Content length: {len(result.content[0].text) if result.content else 0}")
        else:
            print("❌ No call_tool handler found")
            
    except Exception as e:
        print(f"❌ Error testing call_tool: {e}")
        import traceback
        print(traceback.format_exc())

def main():
    """Run the test"""
    print("🧪 Testing MCP Protocol Compatibility\n")
    asyncio.run(test_mcp_protocol())
    print("\n✅ MCP protocol test completed")

if __name__ == "__main__":
    main()
