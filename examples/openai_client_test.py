"""
AI Tools Framework: openai_client_test.py
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

openai_client_test.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# examples/openai_client_test.py
#!/usr/bin/env python3
"""
Test script for OpenAI API client functionality
This simulates how LM Studio would interact with the API
"""

import httpx
import json
import asyncio

async def test_openai_api():
    """Test OpenAI-compatible API"""
    print("🌐 Testing OpenAI API Interface...")

    base_url = "http://localhost:8001"

    async with httpx.AsyncClient() as client:
        try:
            # Test health check
            health = await client.get(f"{base_url}/health")
            if health.status_code == 200:
                print("✅ API server is healthy")
                print(f"📊 {health.json()}")
            
            # Test list tools
            tools_response = await client.get(f"{base_url}/v1/tools")
            if tools_response.status_code == 200:
                tools = tools_response.json()['tools']
                print(f"\n📋 Available tools: {len(tools)}")
                for tool in tools:
                    print(f"  • {tool['function']['name']}: {tool['function']['description']}")
            
            # Test direct tool execution
            print("\n🔍 Testing direct tool execution...")
            direct_response = await client.post(
                f"{base_url}/v1/tools/execute",
                params={"tool_name": "web_search"},
                json={
                    "query": "FastAPI tutorial",
                    "num_results": 2
                }
            )
            
            if direct_response.status_code == 200:
                result = direct_response.json()
                print("✅ Direct execution successful!")
                print(f"📊 Success: {result['success']}")
                if result['success']:
                    content = result['content']
                    print(f"🔍 Found {len(content.get('organic', []))} results")
                
        except Exception as e:
            print(f"💥 API test error: {str(e)}")

if __name__ == "__main__":
    print("Note: Make sure the OpenAI API server is running with:")
    print("  python openai_main.py")
    print("Or: uvicorn openai_main:app --host localhost --port 8000")
    print()
    
    asyncio.run(test_openai_api())
