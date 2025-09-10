# tools/communication_tools.py
"""
Communication tools for Slack, Discord, and other messaging platforms
"""

import json
import aiohttp
from typing import Optional, Dict, Any, List
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry
import os

class SlackTool(BaseTool):
    """Send messages and interact with Slack"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="slack_message",
            description="Send messages to Slack channels or users (requires SLACK_BOT_TOKEN in .env)",
            category="communication",
            parameters=[
                ToolParameter(
                    name="channel",
                    description="Slack channel (e.g., '#general') or user (e.g., '@username') or channel ID",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="text",
                    description="Message text to send",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="thread_ts",
                    description="Timestamp of parent message to reply in thread",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="blocks",
                    description="Rich message blocks (JSON string) for advanced formatting",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="username",
                    description="Override bot username",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="icon_emoji",
                    description="Override bot icon with emoji (e.g., ':robot_face:')",
                    param_type="string",
                    required=False
                )
            ]
        )
    
    async def execute(self, channel: str, text: str, thread_ts: Optional[str] = None,
                     blocks: Optional[str] = None, username: Optional[str] = None,
                     icon_emoji: Optional[str] = None) -> ToolResult:
        """Send message to Slack"""
        try:
            token = os.getenv('SLACK_BOT_TOKEN')
            if not token:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="Slack bot token not found. Set SLACK_BOT_TOKEN in .env file.\n\nTo get a token:\n1. Go to https://api.slack.com/apps\n2. Create a new app\n3. Go to OAuth & Permissions\n4. Add 'chat:write' scope\n5. Install app to workspace",
                    error_message="Missing SLACK_BOT_TOKEN"
                )
            
            # Prepare message payload
            payload = {
                'channel': channel,
                'text': text
            }
            
            if thread_ts:
                payload['thread_ts'] = thread_ts
            
            if blocks:
                try:
                    payload['blocks'] = json.loads(blocks)
                except json.JSONDecodeError:
                    return ToolResult(
                        success=False,
                        result_type=ToolResultType.ERROR,
                        content="Invalid JSON format in blocks parameter",
                        error_message="Invalid JSON in blocks"
                    )
            
            if username:
                payload['username'] = username
            
            if icon_emoji:
                payload['icon_emoji'] = icon_emoji
            
            # Send message
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://slack.com/api/chat.postMessage',
                    headers=headers,
                    json=payload
                ) as response:
                    
                    result = await response.json()
                    
                    if result.get('ok'):
                        return ToolResult(
                            success=True,
                            result_type=ToolResultType.TEXT,
                            content=f"✅ Message sent to {channel}\n\nMessage: {text}",
                            metadata={
                                "channel": channel,
                                "timestamp": result.get('ts'),
                                "message": text
                            }
                        )
                    else:
                        error_msg = result.get('error', 'Unknown error')
                        return ToolResult(
                            success=False,
                            result_type=ToolResultType.ERROR,
                            content=f"Failed to send Slack message: {error_msg}",
                            error_message=error_msg
                        )
        
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Slack message failed: {str(e)}",
                error_message=str(e)
            )

class DiscordTool(BaseTool):
    """Send messages to Discord via webhooks"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="discord_webhook",
            description="Send messages to Discord via webhook (requires DISCORD_WEBHOOK_URL in .env)",
            category="communication",
            parameters=[
                ToolParameter(
                    name="content",
                    description="Message content to send",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="username",
                    description="Override webhook username",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="avatar_url",
                    description="Override webhook avatar URL",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="embeds",
                    description="Rich embeds (JSON string) for advanced formatting",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="tts",
                    description="Send as text-to-speech message",
                    param_type="boolean",
                    required=False,
                    default=False
                )
            ]
        )
    
    async def execute(self, content: str, username: Optional[str] = None,
                     avatar_url: Optional[str] = None, embeds: Optional[str] = None,
                     tts: bool = False) -> ToolResult:
        """Send message to Discord via webhook"""
        try:
            webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
            if not webhook_url:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="Discord webhook URL not found. Set DISCORD_WEBHOOK_URL in .env file.\n\nTo get a webhook URL:\n1. Go to your Discord server\n2. Edit channel -> Integrations -> Webhooks\n3. Create webhook and copy URL",
                    error_message="Missing DISCORD_WEBHOOK_URL"
                )
            
            # Prepare payload
            payload = {
                'content': content,
                'tts': tts
            }
            
            if username:
                payload['username'] = username
            
            if avatar_url:
                payload['avatar_url'] = avatar_url
            
            if embeds:
                try:
                    payload['embeds'] = json.loads(embeds)
                except json.JSONDecodeError:
                    return ToolResult(
                        success=False,
                        result_type=ToolResultType.ERROR,
                        content="Invalid JSON format in embeds parameter",
                        error_message="Invalid JSON in embeds"
                    )
            
            # Send message
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    
                    if response.status == 204:  # Discord webhook success
                        return ToolResult(
                            success=True,
                            result_type=ToolResultType.TEXT,
                            content=f"✅ Message sent to Discord\n\nMessage: {content}",
                            metadata={
                                "content": content,
                                "status": response.status
                            }
                        )
                    else:
                        error_text = await response.text()
                        return ToolResult(
                            success=False,
                            result_type=ToolResultType.ERROR,
                            content=f"Failed to send Discord message: HTTP {response.status}\n{error_text}",
                            error_message=f"HTTP {response.status}"
                        )
        
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Discord message failed: {str(e)}",
                error_message=str(e)
            )

class TeamsWebhookTool(BaseTool):
    """Send messages to Microsoft Teams via webhook"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="teams_webhook",
            description="Send messages to Microsoft Teams via webhook (requires TEAMS_WEBHOOK_URL in .env)",
            category="communication",
            parameters=[
                ToolParameter(
                    name="title",
                    description="Message title",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="text",
                    description="Message text content",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="color",
                    description="Theme color (hex code like 'FF5733')",
                    param_type="string",
                    required=False,
                    default="0078D4"
                ),
                ToolParameter(
                    name="facts",
                    description="Additional facts (JSON string with name/value pairs)",
                    param_type="string",
                    required=False
                )
            ]
        )
    
    async def execute(self, title: str, text: str, color: str = "0078D4",
                     facts: Optional[str] = None) -> ToolResult:
        """Send message to Microsoft Teams"""
        try:
            webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
            if not webhook_url:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="Teams webhook URL not found. Set TEAMS_WEBHOOK_URL in .env file.\n\nTo get a webhook URL:\n1. Go to your Teams channel\n2. Click ... -> Connectors\n3. Add 'Incoming Webhook'\n4. Configure and copy URL",
                    error_message="Missing TEAMS_WEBHOOK_URL"
                )
            
            # Prepare payload
            payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": color,
                "title": title,
                "text": text
            }
            
            if facts:
                try:
                    facts_data = json.loads(facts)
                    payload["sections"] = [{
                        "facts": [{"name": k, "value": v} for k, v in facts_data.items()]
                    }]
                except json.JSONDecodeError:
                    return ToolResult(
                        success=False,
                        result_type=ToolResultType.ERROR,
                        content="Invalid JSON format in facts parameter",
                        error_message="Invalid JSON in facts"
                    )
            
            # Send message
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    
                    if response.status == 200:
                        return ToolResult(
                            success=True,
                            result_type=ToolResultType.TEXT,
                            content=f"✅ Message sent to Teams\n\nTitle: {title}\nMessage: {text}",
                            metadata={
                                "title": title,
                                "text": text,
                                "status": response.status
                            }
                        )
                    else:
                        error_text = await response.text()
                        return ToolResult(
                            success=False,
                            result_type=ToolResultType.ERROR,
                            content=f"Failed to send Teams message: HTTP {response.status}\n{error_text}",
                            error_message=f"HTTP {response.status}"
                        )
        
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Teams message failed: {str(e)}",
                error_message=str(e)
            )

# Register the tools
registry.register(SlackTool)
registry.register(DiscordTool)
registry.register(TeamsWebhookTool)
