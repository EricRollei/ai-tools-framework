"""
AI Tools Framework: test-tools.py
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

test-tools.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# examples/test_tools.py
#!/usr/bin/env python3
"""
Test script to verify tool functionality
Run with: python examples/test_tools.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.serper_search import SerperSearchTool
from config.settings import settings

async def test_serper_search():
    """Test the Serper search tool"""
    print("🔍 Testing Serper Search Tool...")
    
    try:
        # Create tool instance
        tool = SerperSearchTool()
        
        # Test basic search
        result = await tool.execute(
            query="Python asyncio tutorial",
            num_results=5
        )
        
        if result.success:
            print("✅ Search successful!")
            print(f"📊 Found {result.metadata['num_results']} results")
            
            # Print first few results
            content = result.content
            for i, item in enumerate(content.get('organic', [])[:3]):
                print(f"\n{i+1}. {item['title']}")
                print(f"   🔗 {item['link']}")
                print(f"   📝 {item['snippet'][:100]}...")
            
            # Show knowledge graph if available
            if content.get('knowledge_graph'):
                kg = content['knowledge_graph']
                print(f"\n🧠 Knowledge Graph: {kg['title']}")
                print(f"   📖 {kg['description'][:100]}...")
        else:
            print(f"❌ Search failed: {result.error_message}")
            
    except Exception as e:
        print(f"💥 Test failed with error: {str(e)}")

async def test_multiple_searches():
    """Test multiple search types"""
    print("\n🔍 Testing Multiple Search Types...")
    
    tool = SerperSearchTool()
    
    searches = [
        ("news", "artificial intelligence breakthrough"),
        ("images", "python programming"),
        ("videos", "machine learning tutorial")
    ]
    
    for search_type, query in searches:
        try:
            result = await tool.execute(
                query=query,
                search_type=search_type,
                num_results=3
            )
            
            if result.success:
                count = len(result.content.get('organic', []))
                print(f"✅ {search_type.title()} search: {count} results for '{query}'")
            else:
                print(f"❌ {search_type.title()} search failed: {result.error_message}")
                
        except Exception as e:
            print(f"💥 {search_type.title()} search error: {str(e)}")

if __name__ == "__main__":
    if not settings.serper_api_key:
        print("❌ SERPER_API_KEY not found in environment variables!")
        print("Please set your API key in .env file or environment")
        sys.exit(1)
    
    asyncio.run(test_serper_search())
    asyncio.run(test_multiple_searches())
    print("\n🎉 All tests completed!")
