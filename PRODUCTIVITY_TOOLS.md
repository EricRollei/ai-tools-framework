# Productivity Tools Documentation

This document covers the new productivity tools: Calendar, Clipboard, and Communication (Slack/Discord/Teams).

## Calendar Tool 📅

### Features
- Create, update, delete events
- List events by date range
- Find free time slots
- Event scheduling and management
- Persistent storage in JSON format

### Usage Examples

#### Create Event
```json
{
  "tool": "manage_calendar",
  "action": "create",
  "title": "Team Meeting",
  "start_datetime": "2025-09-15 14:00",
  "end_datetime": "2025-09-15 15:30",
  "description": "Weekly team sync",
  "location": "Conference Room A"
}
```

#### List Events
```json
{
  "tool": "manage_calendar",
  "action": "list",
  "date_range": "this_week"
}
```

#### Find Free Time
```json
{
  "tool": "manage_calendar",
  "action": "find_free_time",
  "date_range": "today",
  "duration_hours": 2
}
```

#### Update Event
```json
{
  "tool": "manage_calendar",
  "action": "update",
  "event_id": "1224f44f",
  "title": "Updated Meeting Title",
  "start_datetime": "2025-09-15 15:00"
}
```

#### Delete Event
```json
{
  "tool": "manage_calendar",
  "action": "delete",
  "event_id": "1224f44f"
}
```

### Date Range Options
- `"today"` - Current day
- `"this_week"` - Current week (Monday to Sunday)
- `"this_month"` - Current month
- `"2025-09-15"` - Specific date

---

## Clipboard Tool 📋

### Features
- Copy text to system clipboard
- Paste from system clipboard
- Maintain clipboard history (50 items)
- Restore from history
- Fallback mode without pyperclip

### Usage Examples

#### Copy Text
```json
{
  "tool": "clipboard",
  "action": "copy",
  "text": "Important information to remember!"
}
```

#### Paste Text
```json
{
  "tool": "clipboard",
  "action": "paste"
}
```

#### View History
```json
{
  "tool": "clipboard",
  "action": "history"
}
```

#### Restore from History
```json
{
  "tool": "clipboard",
  "action": "restore",
  "history_index": 2
}
```

#### Clear History
```json
{
  "tool": "clipboard",
  "action": "clear_history"
}
```

### Installation
- **Recommended**: `pip install pyperclip` for full clipboard access
- **Fallback**: Works without pyperclip (saves to file)

---

## Communication Tools 💬

### Slack Tool 📱

#### Setup
1. Go to https://api.slack.com/apps
2. Create new app
3. OAuth & Permissions → Add `chat:write` scope
4. Install app to workspace
5. Copy Bot User OAuth Token
6. Add to `.env`: `SLACK_BOT_TOKEN=xoxb-your-token`

#### Usage Examples

##### Send Message
```json
{
  "tool": "slack_message",
  "channel": "#general",
  "text": "Hello from AI Tools! 🤖"
}
```

##### Send to User
```json
{
  "tool": "slack_message",
  "channel": "@username",
  "text": "Private message"
}
```

##### Thread Reply
```json
{
  "tool": "slack_message",
  "channel": "#general",
  "text": "Reply to thread",
  "thread_ts": "1234567890.123456"
}
```

##### Rich Message with Blocks
```json
{
  "tool": "slack_message",
  "channel": "#general",
  "text": "Fallback text",
  "blocks": "[{\"type\":\"section\",\"text\":{\"type\":\"mrkdwn\",\"text\":\"*Bold text* and _italics_\"}}]"
}
```

### Discord Tool 🎮

#### Setup
1. Go to Discord server
2. Edit channel → Integrations → Webhooks
3. Create webhook and copy URL
4. Add to `.env`: `DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...`

#### Usage Examples

##### Send Message
```json
{
  "tool": "discord_webhook",
  "content": "Hello Discord! 🚀",
  "username": "AI Assistant"
}
```

##### Rich Embed
```json
{
  "tool": "discord_webhook",
  "content": "Check out this embed!",
  "embeds": "[{\"title\":\"Alert\",\"description\":\"Something happened\",\"color\":16711680}]"
}
```

##### Custom Avatar
```json
{
  "tool": "discord_webhook",
  "content": "Message with custom avatar",
  "username": "Custom Bot",
  "avatar_url": "https://example.com/avatar.png"
}
```

### Microsoft Teams Tool 👔

#### Setup
1. Go to Teams channel
2. Click ... → Connectors
3. Add "Incoming Webhook"
4. Configure and copy URL
5. Add to `.env`: `TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...`

#### Usage Examples

##### Send Message
```json
{
  "tool": "teams_webhook",
  "title": "System Alert",
  "text": "Everything is running smoothly! ✅",
  "color": "00FF00"
}
```

##### Message with Facts
```json
{
  "tool": "teams_webhook",
  "title": "Status Report",
  "text": "Daily system status",
  "color": "0078D4",
  "facts": "{\"Uptime\":\"99.9%\",\"Errors\":\"0\",\"Last Check\":\"2025-09-15 14:30\"}"
}
```

---

## Environment Variables

Add these to your `.env` file to enable communication tools:

```bash
# Slack Integration
SLACK_BOT_TOKEN=xoxb-1234567890-1234567890123-abcdefghijklmnopqrstuvwx

# Discord Integration  
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz

# Microsoft Teams Integration
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/12345678-1234-1234-1234-123456789012@12345678-1234-1234-1234-123456789012/IncomingWebhook/abcdefghijklmnopqrstuvwxyz
```

---

## Advanced Usage

### Calendar + Communication Integration
```json
// Create meeting and notify team
{
  "tool": "manage_calendar", 
  "action": "create",
  "title": "Sprint Planning",
  "start_datetime": "2025-09-16 10:00",
  "end_datetime": "2025-09-16 12:00"
}

// Then notify
{
  "tool": "slack_message",
  "channel": "#dev-team",
  "text": "📅 Sprint Planning meeting scheduled for tomorrow 10 AM - 12 PM"
}
```

### Clipboard + Communication
```json
// Copy important info
{
  "tool": "clipboard",
  "action": "copy", 
  "text": "Server IP: 192.168.1.100, Login: admin, Port: 22"
}

// Share via Discord
{
  "tool": "discord_webhook",
  "content": "🔐 Server details copied to clipboard for team access"
}
```

### Free Time + Scheduling
```json
// Find free time
{
  "tool": "manage_calendar",
  "action": "find_free_time",
  "date_range": "this_week",
  "duration_hours": 1
}

// If free slots found, create meeting
{
  "tool": "manage_calendar",
  "action": "create",
  "title": "Code Review",
  "start_datetime": "2025-09-17 14:00",
  "end_datetime": "2025-09-17 15:00"
}
```

---

## Tool Capabilities Summary

| Tool | Features | Dependencies | Storage |
|------|----------|--------------|---------|
| **Calendar** | Events, scheduling, free time | None | `calendar_events.json` |
| **Clipboard** | Copy/paste, history | `pyperclip` (optional) | `clipboard_history.json` |
| **Slack** | Messages, threads, rich formatting | Slack Bot Token | None |
| **Discord** | Webhooks, embeds, custom avatars | Discord Webhook | None |
| **Teams** | Messages, facts, color themes | Teams Webhook | None |

Total new tools: **5 productivity tools** 🚀

These tools significantly enhance the AI framework's productivity capabilities for scheduling, data management, and team communication!
