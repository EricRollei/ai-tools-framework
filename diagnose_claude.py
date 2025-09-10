#!/usr/bin/env python3
"""
Claude Desktop MCP Diagnostic Tool
Helps identify and fix common integration issues
"""

import sys
import os
import json
import subprocess
from pathlib import Path
import platform

def check_python_environment():
    """Check Python installation and environment"""
    print("🐍 Python Environment Check")
    print("-" * 40)
    
    # Python version
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ required for MCP")
        return False
    else:
        print("✅ Python version compatible")
    
    # Python executable
    print(f"Python Executable: {sys.executable}")
    
    # Virtual environment check
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if in_venv:
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Not in virtual environment (recommended to use venv)")
    
    # Check MCP installation
    try:
        import mcp
        print(f"✅ MCP library version: {mcp.__version__}")
    except ImportError:
        print("❌ MCP library not installed")
        print("   Run: pip install mcp")
        return False
    
    return True

def check_project_structure():
    """Check project files and structure"""
    print("\n📁 Project Structure Check")
    print("-" * 40)
    
    project_root = Path(__file__).parent
    required_files = [
        "mcp_main.py",
        "claude_server.py", 
        "requirements.txt",
        "tools/__init__.py",
        "interfaces/mcp_server.py",
        "core/registry.py"
    ]
    
    all_good = True
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_good = False
    
    # Check .env file
    env_path = project_root / ".env"
    if env_path.exists():
        print("✅ .env file exists")
    else:
        print("⚠️  .env file not found (some tools may not work)")
    
    return all_good

def check_tool_imports():
    """Check that tools can be imported"""
    print("\n🔧 Tool Import Check")
    print("-" * 40)
    
    try:
        # Add project to path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
        
        # Import tools
        import tools
        print("✅ Tools module imported")
        
        # Check registry
        from core.registry import registry
        tool_count = len(registry.list_tools())
        print(f"✅ Registry loaded with {tool_count} tools")
        
        if tool_count < 20:
            print("⚠️  Expected ~27 tools, got fewer - some tools may have import issues")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def check_mcp_server():
    """Check MCP server can be created"""
    print("\n🖥️  MCP Server Check")
    print("-" * 40)
    
    try:
        from interfaces.mcp_server import MCPToolServer
        server = MCPToolServer()
        print("✅ MCP server instance created")
        
        # Try to get tools count (indirect way to test handlers)
        from core.registry import registry
        tools_count = len(registry.list_tools())
        print(f"✅ Server has access to {tools_count} tools")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP server creation failed: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def check_claude_config():
    """Check Claude Desktop configuration"""
    print("\n🔧 Claude Desktop Configuration Check")
    print("-" * 40)
    
    # Check if config file exists locally
    local_config = Path("claude_config.json")
    if local_config.exists():
        print("✅ Local claude_config.json found")
        
        try:
            with open(local_config, 'r') as f:
                config = json.load(f)
            print("✅ Configuration JSON is valid")
            
            # Check structure
            if "mcpServers" in config and "ai-tools" in config["mcpServers"]:
                server_config = config["mcpServers"]["ai-tools"]
                print("✅ ai-tools server configured")
                
                # Check paths
                if "args" in server_config and len(server_config["args"]) > 0:
                    script_path = Path(server_config["args"][0])
                    if script_path.exists():
                        print(f"✅ Server script exists: {script_path}")
                    else:
                        print(f"❌ Server script not found: {script_path}")
                        return False
                
                if "cwd" in server_config:
                    cwd_path = Path(server_config["cwd"])
                    if cwd_path.exists():
                        print(f"✅ Working directory exists: {cwd_path}")
                    else:
                        print(f"❌ Working directory not found: {cwd_path}")
                        return False
                
            else:
                print("❌ ai-tools server not properly configured")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return False
    else:
        print("⚠️  Local claude_config.json not found")
        print("   You'll need to manually add configuration to Claude Desktop")
    
    # Show Claude Desktop config location
    system = platform.system()
    if system == "Windows":
        config_path = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    elif system == "Darwin":  # macOS
        config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        config_path = Path.home() / ".config" / "claude" / "claude_desktop_config.json"
    
    print(f"\nClaude Desktop config should be at:")
    print(f"   {config_path}")
    
    if config_path.exists():
        print("✅ Claude Desktop config file exists")
    else:
        print("⚠️  Claude Desktop config file not found")
        print("   Create it manually or copy from claude_config.json")
    
    return True

def check_server_startup():
    """Test server startup"""
    print("\n🚀 Server Startup Test")
    print("-" * 40)
    
    try:
        script_path = Path(__file__).parent / "claude_server.py"
        if not script_path.exists():
            script_path = Path(__file__).parent / "mcp_main.py"
        
        print(f"Testing startup of: {script_path}")
        
        # Run server for 3 seconds to see if it starts without immediate crash
        import subprocess
        import time
        
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait briefly
        time.sleep(2)
        
        # Check if still running
        if process.poll() is None:
            print("✅ Server starts and runs (stopping test)")
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            stdout, stderr = process.communicate()
            print("❌ Server exited immediately")
            if stderr:
                print(f"   Error: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Startup test failed: {e}")
        return False

def generate_report():
    """Generate diagnostic report"""
    print("\n" + "="*60)
    print("🔍 CLAUDE DESKTOP MCP DIAGNOSTIC REPORT")
    print("="*60)
    
    checks = [
        ("Python Environment", check_python_environment),
        ("Project Structure", check_project_structure), 
        ("Tool Imports", check_tool_imports),
        ("MCP Server", check_mcp_server),
        ("Claude Config", check_claude_config),
        ("Server Startup", check_server_startup)
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"❌ {name} check failed with exception: {e}")
            results[name] = False
    
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your setup should work with Claude Desktop.")
        print("\nNext steps:")
        print("1. Copy claude_config.json content to Claude Desktop settings")
        print("2. Restart Claude Desktop")
        print("3. Test with: 'Can you list the available tools?'")
    else:
        print("\n⚠️  Some issues found. Please fix the failed checks above.")
        print("\nCommon fixes:")
        print("- Ensure virtual environment is activated")
        print("- Run: pip install -r requirements.txt")
        print("- Check file paths in configuration")
        print("- Verify .env file exists with required API keys")

if __name__ == "__main__":
    generate_report()
