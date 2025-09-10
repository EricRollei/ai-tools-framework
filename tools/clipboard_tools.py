"""
AI Tools Framework: clipboard_tools.py
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

clipboard_tools.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# tools/clipboard_tools.py
"""
Clipboard tools for copying and pasting text/data
"""

import json
from typing import Optional, Dict, Any
from pathlib import Path
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

# Try to import clipboard libraries
CLIPBOARD_AVAILABLE = False
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    pyperclip = None

class ClipboardTool(BaseTool):
    """Manage clipboard operations - copy and paste text"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.clipboard_history_file = Path("clipboard_history.json")
        self.max_history = 50
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="clipboard",
            description="Copy text to clipboard, paste from clipboard, and manage clipboard history",
            category="productivity",
            parameters=[
                ToolParameter(
                    name="action",
                    description="Action: 'copy', 'paste', 'history', 'clear_history'",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="text",
                    description="Text to copy to clipboard (required for 'copy' action)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="history_index",
                    description="Index from clipboard history to restore (0 = most recent)",
                    param_type="number",
                    required=False
                )
            ]
        )
    
    async def execute(self, action: str, text: Optional[str] = None, 
                     history_index: Optional[int] = None) -> ToolResult:
        """Execute clipboard operation"""
        try:
            if action == "copy":
                return await self._copy_to_clipboard(text)
            elif action == "paste":
                return await self._paste_from_clipboard()
            elif action == "history":
                return await self._show_clipboard_history()
            elif action == "clear_history":
                return await self._clear_clipboard_history()
            elif action == "restore":
                return await self._restore_from_history(history_index)
            else:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Unknown action: {action}. Use: copy, paste, history, clear_history, restore",
                    error_message=f"Unknown action: {action}"
                )
        
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Clipboard operation failed: {str(e)}",
                error_message=str(e)
            )
    
    def _load_history(self) -> list:
        """Load clipboard history from file"""
        if not self.clipboard_history_file.exists():
            return []
        
        try:
            with open(self.clipboard_history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_history(self, history: list) -> None:
        """Save clipboard history to file"""
        # Limit history size
        if len(history) > self.max_history:
            history = history[:self.max_history]
        
        with open(self.clipboard_history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def _add_to_history(self, text: str) -> None:
        """Add text to clipboard history"""
        if not text or len(text.strip()) == 0:
            return
        
        history = self._load_history()
        
        # Remove if already exists
        history = [item for item in history if item.get('text') != text]
        
        # Add to beginning
        import datetime
        history.insert(0, {
            'text': text,
            'timestamp': datetime.datetime.now().isoformat(),
            'length': len(text)
        })
        
        self._save_history(history)
    
    async def _copy_to_clipboard(self, text: str) -> ToolResult:
        """Copy text to clipboard"""
        if not text:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content="Text is required for copy operation",
                error_message="Missing text parameter"
            )
        
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(text)
                self._add_to_history(text)
                
                return ToolResult(
                    success=True,
                    result_type=ToolResultType.TEXT,
                    content=f"✅ Copied {len(text)} characters to clipboard",
                    metadata={
                        "action": "copy",
                        "length": len(text),
                        "preview": text[:100] + "..." if len(text) > 100 else text
                    }
                )
            except Exception as e:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Failed to copy to clipboard: {str(e)}",
                    error_message=str(e)
                )
        else:
            # Fallback: save to file
            self._add_to_history(text)
            with open("clipboard_fallback.txt", 'w', encoding='utf-8') as f:
                f.write(text)
            
            return ToolResult(
                success=True,
                result_type=ToolResultType.TEXT,
                content=f"⚠️ Pyperclip not available. Saved {len(text)} characters to clipboard_fallback.txt\n\nTo install clipboard support: pip install pyperclip",
                metadata={
                    "action": "copy_fallback",
                    "length": len(text),
                    "file": "clipboard_fallback.txt"
                }
            )
    
    async def _paste_from_clipboard(self) -> ToolResult:
        """Paste text from clipboard"""
        if CLIPBOARD_AVAILABLE:
            try:
                text = pyperclip.paste()
                
                if text:
                    return ToolResult(
                        success=True,
                        result_type=ToolResultType.TEXT,
                        content=f"📋 Clipboard content ({len(text)} characters):\n\n{text}",
                        metadata={
                            "action": "paste",
                            "length": len(text),
                            "content": text
                        }
                    )
                else:
                    return ToolResult(
                        success=True,
                        result_type=ToolResultType.TEXT,
                        content="📋 Clipboard is empty",
                        metadata={"action": "paste", "length": 0}
                    )
            except Exception as e:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Failed to paste from clipboard: {str(e)}",
                    error_message=str(e)
                )
        else:
            # Fallback: read from file
            try:
                with open("clipboard_fallback.txt", 'r', encoding='utf-8') as f:
                    text = f.read()
                
                return ToolResult(
                    success=True,
                    result_type=ToolResultType.TEXT,
                    content=f"📋 Fallback clipboard content ({len(text)} characters):\n\n{text}\n\nTo install clipboard support: pip install pyperclip",
                    metadata={
                        "action": "paste_fallback",
                        "length": len(text),
                        "content": text
                    }
                )
            except FileNotFoundError:
                return ToolResult(
                    success=True,
                    result_type=ToolResultType.TEXT,
                    content="📋 No fallback clipboard file found",
                    metadata={"action": "paste_fallback", "length": 0}
                )
    
    async def _show_clipboard_history(self) -> ToolResult:
        """Show clipboard history"""
        history = self._load_history()
        
        if not history:
            return ToolResult(
                success=True,
                result_type=ToolResultType.TEXT,
                content="📋 Clipboard history is empty",
                metadata={"action": "history", "count": 0}
            )
        
        lines = ["📋 Clipboard History:", ""]
        for i, item in enumerate(history[:20]):  # Show last 20 items
            timestamp = item.get('timestamp', 'Unknown time')
            text_length = item.get('length', len(item['text']))
            preview = item['text'][:80] + "..." if len(item['text']) > 80 else item['text']
            
            lines.append(f"{i}. [{timestamp[:16]}] ({text_length} chars)")
            lines.append(f"   {preview}")
            lines.append("")
        
        if len(history) > 20:
            lines.append(f"... and {len(history) - 20} more items")
        
        return ToolResult(
            success=True,
            result_type=ToolResultType.TEXT,
            content="\n".join(lines),
            metadata={"action": "history", "count": len(history)}
        )
    
    async def _clear_clipboard_history(self) -> ToolResult:
        """Clear clipboard history"""
        self._save_history([])
        
        return ToolResult(
            success=True,
            result_type=ToolResultType.TEXT,
            content="✅ Clipboard history cleared",
            metadata={"action": "clear_history"}
        )
    
    async def _restore_from_history(self, history_index: int) -> ToolResult:
        """Restore text from clipboard history"""
        if history_index is None:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content="History index is required for restore operation",
                error_message="Missing history_index parameter"
            )
        
        history = self._load_history()
        
        if not history:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content="Clipboard history is empty",
                error_message="Empty history"
            )
        
        if history_index < 0 or history_index >= len(history):
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Invalid history index: {history_index}. Valid range: 0-{len(history)-1}",
                error_message="Invalid history index"
            )
        
        text = history[history_index]['text']
        
        # Copy to clipboard
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(text)
            except:
                pass
        
        # Move to front of history
        item = history.pop(history_index)
        history.insert(0, item)
        self._save_history(history)
        
        return ToolResult(
            success=True,
            result_type=ToolResultType.TEXT,
            content=f"✅ Restored to clipboard ({len(text)} characters):\n\n{text[:200] + '...' if len(text) > 200 else text}",
            metadata={
                "action": "restore",
                "index": history_index,
                "length": len(text)
            }
        )

# Only register if we want clipboard functionality
# Note: pyperclip installation is optional
registry.register(ClipboardTool)
