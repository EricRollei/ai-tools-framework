#!/usr/bin/env python3
"""
Specialized MCP server launcher for Claude Desktop
This handles the stdio connection properly for Claude Desktop integration
"""

import sys
import os
import asyncio
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

# Import MCP server
from interfaces.mcp_server import MCPToolServer

async def main():
    """Main entry point for Claude Desktop"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Initializing AI Tools MCP server for Claude Desktop...")
        
        # Create server instance
        server = MCPToolServer()
        
        # Get tool count from registry instead of server internals
        from core.registry import registry
        tool_count = len(registry.list_tools())
        logger.info(f"Server created with {tool_count} tools registered")
        
        # Run the server (this will handle stdio properly)
        await server.run()
        
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Server shutdown requested")
        sys.exit(0)
    except Exception as e:
        logging.getLogger(__name__).error(f"Startup error: {e}")
        sys.exit(1)
