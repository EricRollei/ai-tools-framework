"""
AI Tools Framework: mcp_main.py
Description: General purpose MCP server for multiple platforms
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

mcp_main.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

﻿# mcp_main.py - Entry point for MCP server
#!/usr/bin/env python3
"""
MCP Server entry point for Claude Desktop integration
Run with: python mcp_main.py
"""

import asyncio
import sys
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 encoding for Claude Desktop
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Load environment variables early
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up logging for Claude Desktop
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# Import tools to trigger registration
try:
    import tools  # This triggers the tool registration in tools/__init__.py
    logger.info("Tools imported successfully")
except Exception as e:
    logger.error(f"Failed to import tools: {e}")
    sys.exit(1)

from interfaces.mcp_server import MCPToolServer

def main():
    """Synchronous entry point for console scripts"""
    try:
        logger.info("Starting AI Tools MCP Server for Claude Desktop...")
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
    
async def async_main():
    """Main entry point"""
    try:
        server = MCPToolServer()
        logger.info("MCP server instance created")
        await server.run()
    except Exception as e:
        logger.error(f"Async main error: {e}")
        raise

if __name__ == "__main__":
    main()
