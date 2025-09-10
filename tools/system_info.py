"""
AI Tools Framework: system_info.py
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

system_info.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# tools/system_info.py
"""
System information tools for the AI Tools framework
"""

import platform
import psutil
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from core.base import BaseTool, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

class SystemInfoTool(BaseTool):
    """Get comprehensive system information"""
    
    def __init__(self):
        super().__init__(
            name="system_info",
            description="Get comprehensive system information including OS, hardware, and network details",
            parameters=[
                ToolParameter(
                    name="include_processes",
                    description="Include running process information",
                    param_type="boolean",
                    required=False,
                    default=False
                ),
                ToolParameter(
                    name="include_network",
                    description="Include network interface information",
                    param_type="boolean",
                    required=False,
                    default=True
                )
            ]
        )
    
    async def execute(self, include_processes: bool = False, include_network: bool = True) -> ToolResult:
        """Execute system information gathering"""
        try:
            system_info = {}
            
            # Basic system information
            system_info["system"] = {
                "platform": platform.platform(),
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "hostname": socket.gethostname(),
                "uptime": datetime.now() - datetime.fromtimestamp(psutil.boot_time())
            }
            
            # CPU information
            system_info["cpu"] = {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "current_frequency": psutil.cpu_freq().current if psutil.cpu_freq() else "Unknown",
                "usage_percent": psutil.cpu_percent(interval=1)
            }
            
            # Memory information
            memory = psutil.virtual_memory()
            system_info["memory"] = {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "usage_percent": memory.percent
            }
            
            # Disk information
            disk_info = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "filesystem": partition.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "usage_percent": round((usage.used / usage.total) * 100, 2)
                    })
                except PermissionError:
                    continue
            system_info["disks"] = disk_info
            
            # Network information
            if include_network:
                network_info = []
                for interface, addresses in psutil.net_if_addrs().items():
                    interface_info = {"interface": interface, "addresses": []}
                    for addr in addresses:
                        interface_info["addresses"].append({
                            "family": str(addr.family),
                            "address": addr.address,
                            "netmask": getattr(addr, 'netmask', None),
                            "broadcast": getattr(addr, 'broadcast', None)
                        })
                    network_info.append(interface_info)
                system_info["network"] = network_info
            
            # Process information (if requested)
            if include_processes:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        processes.append(proc.info)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                # Sort by CPU usage and take top 10
                processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
                system_info["top_processes"] = processes[:10]
            
            return ToolResult(
                success=True,
                content=system_info,
                result_type=ToolResultType.JSON,
                metadata={
                    "tool": "system_info",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error_message=f"Error gathering system information: {str(e)}"
            )

class RunCommandTool(BaseTool):
    """Execute a system command safely"""
    
    def __init__(self):
        super().__init__(
            name="run_command",
            description="Execute a system command (use with caution)",
            parameters=[
                ToolParameter(
                    name="command",
                    description="Command to execute",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="timeout",
                    description="Command timeout in seconds",
                    param_type="number",
                    required=False,
                    default=30
                ),
                ToolParameter(
                    name="working_directory",
                    description="Working directory for command execution",
                    param_type="string",
                    required=False
                )
            ]
        )
    
    async def execute(self, command: str, timeout: int = 30, working_directory: str = None) -> ToolResult:
        """Execute system command"""
        try:
            # Security check - block potentially dangerous commands
            dangerous_patterns = ['rm -rf', 'del /s', 'format', 'fdisk', 'mkfs', 'dd if=']
            if any(pattern in command.lower() for pattern in dangerous_patterns):
                return ToolResult(
                    success=False,
                    error_message="Command blocked for security reasons"
                )
            
            # Set working directory
            cwd = Path(working_directory).resolve() if working_directory else None
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd
            )
            
            command_result = {
                "command": command,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "working_directory": str(cwd) if cwd else str(Path.cwd())
            }
            
            return ToolResult(
                success=result.returncode == 0,
                content=command_result,
                result_type=ToolResultType.JSON,
                metadata={
                    "tool": "run_command",
                    "command": command,
                    "return_code": result.returncode
                }
            )
            
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                error_message=f"Command timed out after {timeout} seconds"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error_message=f"Error executing command: {str(e)}"
            )

# Register system tools
registry.register(SystemInfoTool)
registry.register(RunCommandTool)
