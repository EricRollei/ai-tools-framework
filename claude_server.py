#!/usr/bin/env python3
"""
AI Tools Framework: claude_server.py
Description: Specialized MCP server optimized for Claude Desktop
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

claude_server.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

"""
Specialized MCP server launcher for Claude Desktop
This handles the stdio connection properly for Claude Desktop integration
"""

import sys
import os
import logging
from pathlib import Path

# Ensure proper encoding for Claude Desktop
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Configure logging to stderr (Claude Desktop requirement)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr,
    force=True
)

# Add project root to Python path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(project_root / '.env')

# Import and register tools
import tools

# We'll import the stdio server in main() to avoid early imports

def main():
    """Main entry point for Claude Desktop"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Initializing AI Tools MCP server for Claude Desktop...")
        
        # Use the custom stdio MCP server that handles initialization properly
        from ai_tools_stdio_mcp import AIToolsStdioMCP
        
        # Create server instance
        server = AIToolsStdioMCP()
        
        # Get tool count from registry
        from core.registry import registry
        tool_count = len(registry.list_tools())
        logger.info(f"Server created with {tool_count} tools registered")
        
        # Run the server (this is synchronous for stdio)
        server.run()
        
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Server shutdown requested")
        sys.exit(0)
    except Exception as e:
        logging.getLogger(__name__).error(f"Startup error: {e}")
        sys.exit(1)
