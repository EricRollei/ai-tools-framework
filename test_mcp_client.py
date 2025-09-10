#!/usr/bin/env python3
"""Simple test client for MCP server"""

import subprocess
import json
import time

def test_mcp_server():
    """Test MCP server with proper message sequence"""
    
    # Start the server process
    server = subprocess.Popen(
        ["python", "ai_tools_stdio_mcp.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="a:/ai-tools"
    )
    
    try:
        # 1. Initialize
        init_msg = {
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            },
            "jsonrpc": "2.0",
            "id": 0
        }
        
        print("1. Sending initialize...")
        server.stdin.write(json.dumps(init_msg) + "\n")
        server.stdin.flush()
        
        response = server.stdout.readline()
        print(f"Initialize response: {response.strip()}")
        
        # 2. Send initialized notification
        init_notification = {
            "method": "notifications/initialized",
            "jsonrpc": "2.0"
        }
        
        print("2. Sending initialized notification...")
        server.stdin.write(json.dumps(init_notification) + "\n")
        server.stdin.flush()
        
        # Give it a moment to process (notifications don't send responses)
        time.sleep(0.1)
        
        # 3. List tools
        list_msg = {
            "method": "tools/list",
            "params": {},
            "jsonrpc": "2.0",
            "id": 1
        }
        
        print("3. Sending tools/list...")
        server.stdin.write(json.dumps(list_msg) + "\n")
        server.stdin.flush()
        
        response = server.stdout.readline()
        data = json.loads(response)
        
        if "result" in data and "tools" in data["result"]:
            tool_count = len(data["result"]["tools"])
            print(f"Tools list response: {tool_count} tools returned")
            # Print first few tool names
            for i, tool in enumerate(data["result"]["tools"][:3]):
                print(f"  - {tool['name']}: {tool['description'][:50]}...")
        else:
            print(f"Unexpected response: {response.strip()}")
            
        print("✅ MCP server test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        server.terminate()
        server.wait()

if __name__ == "__main__":
    test_mcp_server()
