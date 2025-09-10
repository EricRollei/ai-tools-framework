#!/usr/bin/env python3
"""
AI Tools Framework: test_web_scraping.py
Description: Web scraping capabilities testing
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

test_web_scraping.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

"""
Test script for enhanced web scraping capabilities
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from tools.web_scraper_tools import AdvancedWebScraperTool
from tools.http_tools import HTTPRequestTool

async def test_academic_scraping():
    """Test enhanced scraping on academic sites"""
    print("Testing Enhanced Web Scraping for Academic Sites...")
    
    # Test URLs
    test_urls = [
        "https://www.sciencedirect.com/science/article/pii/S0047637424000952",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10451965/",
        "https://example.com"  # Simple test
    ]
    
    # Create tools
    scraper_tool = AdvancedWebScraperTool()
    http_tool = HTTPRequestTool()
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {url}")
        print('='*60)
        
        # Test 1: Enhanced HTTP Request
        print("\n1. Testing Enhanced HTTP Request Tool:")
        try:
            result = await http_tool.execute(
                url=url,
                method="GET"
            )
            
            if result.success:
                content_preview = result.content[:200] + "..." if len(result.content) > 200 else result.content
                print(f"✅ HTTP Success! Content length: {len(result.content)} chars")
                print(f"Preview: {content_preview}")
            else:
                print(f"❌ HTTP Failed: {result.error_message}")
                
        except Exception as e:
            print(f"❌ HTTP Exception: {e}")
        
        # Test 2: Advanced Web Scraper
        print("\n2. Testing Advanced Web Scraper Tool:")
        try:
            result = await scraper_tool.execute(
                url=url,
                extraction_mode="article",
                max_length=1000,  # Limit for testing
                bypass_paywall=True,
                delay_seconds=1
            )
            
            if result.success:
                print(f"✅ Scraper Success! Content length: {len(result.content)} chars")
                print(f"Metadata: {result.metadata}")
                content_preview = result.content[:300] + "..." if len(result.content) > 300 else result.content
                print(f"Preview: {content_preview}")
            else:
                print(f"❌ Scraper Failed: {result.error_message}")
                
        except Exception as e:
            print(f"❌ Scraper Exception: {e}")
        
        # Test 3: Title and Abstract extraction for academic papers
        if 'sciencedirect' in url or 'pmc.ncbi' in url:
            print("\n3. Testing Title & Abstract Extraction:")
            try:
                result = await scraper_tool.execute(
                    url=url,
                    extraction_mode="title_and_abstract",
                    max_length=2000,
                    delay_seconds=1
                )
                
                if result.success:
                    print(f"✅ Title/Abstract Success!")
                    print(f"Content:\n{result.content}")
                else:
                    print(f"❌ Title/Abstract Failed: {result.error_message}")
                    
            except Exception as e:
                print(f"❌ Title/Abstract Exception: {e}")
    
    print(f"\n{'='*60}")
    print("TESTING COMPLETE")
    print('='*60)

if __name__ == "__main__":
    asyncio.run(test_academic_scraping())
