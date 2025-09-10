#!/usr/bin/env python3
"""
AI Tools Framework: test_everything.py
Description: Everything CLI integration testing
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

test_everything.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

"""
Test script to verify Everything CLI integration
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.file_search_tools import FileSearchTool

async def test_everything_integration():
    """Test Everything CLI integration"""
    print("Testing Everything CLI integration...")
    
    # Create the file search tool
    search_tool = FileSearchTool()
    
    # Test 1: Search for Python files using Everything
    print("\n1. Testing Everything search for Python files:")
    try:
        result = await search_tool.execute(
            pattern="*.py",
            search_type="everything",
            max_results=5
        )
        print(f"Result: {result}")
        
        # Check if Everything was actually used
        if "using everything search" in str(result.content):
            print("✅ Everything CLI integration working!")
        else:
            print("⚠️ Everything CLI may not be working, but search completed")
            
    except Exception as e:
        print(f"❌ Error testing Everything: {e}")
    
    # Test 2: Search for files in current directory using glob
    print("\n2. Testing glob search for Python files in current directory:")
    try:
        result = await search_tool.execute(
            pattern="*.py",
            search_type="glob",
            search_path=os.getcwd(),
            max_results=5
        )
        print(f"Result: {result}")
        print("✅ Glob search working!")
        
    except Exception as e:
        print(f"❌ Error testing glob search: {e}")
    
    # Test 3: Test auto-detection (should prefer Everything if available)
    print("\n3. Testing auto-detection (should use Everything):")
    try:
        result = await search_tool.execute(
            pattern="*.txt",
            max_results=3
        )
        print(f"Result: {result}")
        
        if "using everything search" in str(result.content):
            print("✅ Auto-detection chose Everything CLI!")
        else:
            print("⚠️ Auto-detection used fallback method")
            
    except Exception as e:
        print(f"❌ Error testing auto-detection: {e}")

if __name__ == "__main__":
    asyncio.run(test_everything_integration())
