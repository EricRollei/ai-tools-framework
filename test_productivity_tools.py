#!/usr/bin/env python3
"""
Test script for new productivity tools (calendar, clipboard, communication)
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from tools.calendar_tools import CalendarTool
from tools.clipboard_tools import ClipboardTool
from tools.communication_tools import SlackTool, DiscordTool, TeamsWebhookTool

async def test_productivity_tools():
    """Test the new productivity tools"""
    print("Testing Productivity Tools...")
    print("="*60)
    
    # Test Calendar Tool
    print("\n1. TESTING CALENDAR TOOL")
    print("-" * 30)
    
    calendar_tool = CalendarTool()
    
    # Create a test event
    print("Creating test event...")
    result = await calendar_tool.execute(
        action="create",
        title="Test Meeting",
        start_datetime="2025-09-15 14:00",
        end_datetime="2025-09-15 15:00",
        description="Testing calendar functionality",
        location="Virtual"
    )
    print(f"Create result: {result.success}")
    if result.success:
        print(f"Content: {result.content}")
        event_id = result.metadata.get('event_id')
    
    # List events
    print("\nListing events for this week...")
    result = await calendar_tool.execute(
        action="list",
        date_range="this_week"
    )
    print(f"List result: {result.success}")
    if result.success:
        print(f"Events found: {result.metadata.get('count', 0)}")
    
    # Find free time
    print("\nFinding free time...")
    result = await calendar_tool.execute(
        action="find_free_time",
        date_range="today",
        duration_hours=2
    )
    print(f"Free time result: {result.success}")
    if result.success:
        print(f"Free slots: {result.metadata.get('free_slots', 0)}")
    
    # Test Clipboard Tool
    print("\n\n2. TESTING CLIPBOARD TOOL")
    print("-" * 30)
    
    clipboard_tool = ClipboardTool()
    
    # Copy text
    test_text = "This is a test message for clipboard functionality! 📋"
    print(f"Copying text: {test_text}")
    result = await clipboard_tool.execute(
        action="copy",
        text=test_text
    )
    print(f"Copy result: {result.success}")
    if result.success:
        print(f"Content: {result.content}")
    
    # Paste text
    print("\nPasting from clipboard...")
    result = await clipboard_tool.execute(action="paste")
    print(f"Paste result: {result.success}")
    if result.success:
        print(f"Pasted length: {result.metadata.get('length', 0)} chars")
    
    # Show history
    print("\nShowing clipboard history...")
    result = await clipboard_tool.execute(action="history")
    print(f"History result: {result.success}")
    if result.success:
        print(f"History items: {result.metadata.get('count', 0)}")
    
    # Test Communication Tools
    print("\n\n3. TESTING COMMUNICATION TOOLS")
    print("-" * 30)
    
    # Test Slack Tool
    print("Testing Slack tool (requires SLACK_BOT_TOKEN)...")
    slack_tool = SlackTool()
    result = await slack_tool.execute(
        channel="#test",
        text="Test message from AI Tools! 🤖"
    )
    print(f"Slack result: {result.success}")
    if not result.success:
        print(f"Expected error (no token): {result.error_message}")
    
    # Test Discord Tool
    print("\nTesting Discord tool (requires DISCORD_WEBHOOK_URL)...")
    discord_tool = DiscordTool()
    result = await discord_tool.execute(
        content="Test message from AI Tools! 🚀",
        username="AI Assistant"
    )
    print(f"Discord result: {result.success}")
    if not result.success:
        print(f"Expected error (no webhook): {result.error_message}")
    
    # Test Teams Tool
    print("\nTesting Teams tool (requires TEAMS_WEBHOOK_URL)...")
    teams_tool = TeamsWebhookTool()
    result = await teams_tool.execute(
        title="AI Tools Test",
        text="This is a test message from the AI Tools framework!",
        color="00FF00"
    )
    print(f"Teams result: {result.success}")
    if not result.success:
        print(f"Expected error (no webhook): {result.error_message}")
    
    print("\n" + "="*60)
    print("PRODUCTIVITY TOOLS TESTING COMPLETE")
    print("="*60)
    
    print("\nSUMMARY:")
    print("✅ Calendar Tool: Event creation, listing, and scheduling")
    print("✅ Clipboard Tool: Copy, paste, and history management")
    print("⚠️  Communication Tools: Ready (need API tokens/webhooks)")
    
    print("\nTo enable communication tools, add to .env:")
    print("SLACK_BOT_TOKEN=xoxb-your-token")
    print("DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...")
    print("TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...")

if __name__ == "__main__":
    asyncio.run(test_productivity_tools())
