#!/usr/bin/env python3
"""
AI Tools Framework: cleanup.py
Description: Project cleanup and maintenance utilities
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

cleanup.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

"""
Cleanup script for AI Tools Framework
Removes temporary files, test files, and development artifacts
"""

import os
import shutil
from pathlib import Path

def cleanup_ai_tools():
    """Remove unnecessary files from the AI Tools framework"""
    
    project_root = Path(__file__).parent
    
    # Files to remove (test files, temp files, development artifacts)
    files_to_remove = [
        # Inappropriate content files
        "artistic_nude_photos.md",
        "famous_nude_and_fashion_photographers.md", 
        "nf.py",
        
        # Old/backup files
        "README_OLD.md",
        "README_NEW.md",
        
        # Temporary log files
        # NOTE: ai_tools_stdio_mcp.log should be kept for LM Studio debugging
        
        # Development/test files that are no longer needed
        # NOTE: NEVER DELETE ai_tools_stdio_mcp.py - CRITICAL FOR LM STUDIO!
        # NOTE: NEVER DELETE claude_server.py - CRITICAL FOR CLAUDE DESKTOP!
        # NOTE: NEVER DELETE mcp_main.py - GENERAL PURPOSE MCP SERVER!
        "test_simple_http.py",    # Simple test file
        "test_email.py",          # Basic email test
        
        # Redundant documentation
        "AI_Tools_Demo.md",
        "EMAIL_SETUP.md", 
        "ENCODING_FIX.md",
        "EVERYTHING_INTEGRATION.md",
        "EXCEL_DATABASE_TOOLS.md",
        "HTTP_TOOLS.md",
        "REQUIREMENTS_SUMMARY.md",
        "WEB_SCRAPING_SOLUTIONS.md",
        "WORKSPACE_CLEAN.md",
        "BROWSER_TOOLS.md",
        
        # Redundant config files
        "claude_simple.json",
        "claude_system_python.json",
        "mcp_clean.json",
    ]
    
    # Directories to remove
    dirs_to_remove = [
        "photographers",  # Contains inappropriate images
        "documents",      # Empty directory
    ]
    
    print("🧹 AI Tools Framework Cleanup")
    print("=" * 40)
    
    # Remove files
    removed_files = 0
    for file_name in files_to_remove:
        file_path = project_root / file_name
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"✅ Removed file: {file_name}")
                removed_files += 1
            except Exception as e:
                print(f"❌ Failed to remove {file_name}: {e}")
        else:
            print(f"⏭️  File not found: {file_name}")
    
    # Remove directories
    removed_dirs = 0
    for dir_name in dirs_to_remove:
        dir_path = project_root / dir_name
        if dir_path.exists() and dir_path.is_dir():
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Removed directory: {dir_name}")
                removed_dirs += 1
            except Exception as e:
                print(f"❌ Failed to remove directory {dir_name}: {e}")
        else:
            print(f"⏭️  Directory not found: {dir_name}")
    
    # Clean __pycache__ directories
    pycache_cleaned = 0
    for pycache_dir in project_root.rglob("__pycache__"):
        if pycache_dir.is_dir():
            try:
                shutil.rmtree(pycache_dir)
                print(f"✅ Cleaned: {pycache_dir.relative_to(project_root)}")
                pycache_cleaned += 1
            except Exception as e:
                print(f"❌ Failed to clean {pycache_dir}: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Cleanup Summary:")
    print(f"   Files removed: {removed_files}")
    print(f"   Directories removed: {removed_dirs}")
    print(f"   __pycache__ cleaned: {pycache_cleaned}")
    
    # Show remaining important files
    print(f"\n📁 Important files kept:")
    important_files = [
        "README.md",
        "COMPLETE_DOCUMENTATION.md", 
        "QUICK_REFERENCE.md",
        "CLAUDE_DESKTOP_SETUP.md",
        "FRAMEWORK_OVERVIEW.md",
        "PRODUCTIVITY_TOOLS.md",
        "PROJECT_STRUCTURE.md",
        "CLAUDE_READY.md",
        "requirements.txt",
        ".env",
        "mcp_main.py",
        "claude_server.py",
        "claude_config.json",
        "updated_claude_config.json"
    ]
    
    for file_name in important_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"   ✅ {file_name}")
        else:
            print(f"   ❌ {file_name} - MISSING!")
    
    # Show remaining directories
    print(f"\n📂 Important directories kept:")
    important_dirs = ["core", "interfaces", "tools", "config", "examples", "venv"]
    for dir_name in important_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ - MISSING!")
    
    print(f"\n🎉 Cleanup completed! Framework is now clean and production-ready.")

if __name__ == "__main__":
    cleanup_ai_tools()
