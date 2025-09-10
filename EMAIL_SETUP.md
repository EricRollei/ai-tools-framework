# Email Setup Documentation 📧

## Overview
Comprehensive email functionality supporting SMTP sending, IMAP reading, and advanced features like attachments, HTML formatting, and bulk operations.

## Prerequisites

### Email Provider Configuration
Different email providers require specific settings:

#### Gmail Setup
1. **Enable 2-Factor Authentication**
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **SMTP Settings**:
   - Server: `smtp.gmail.com`
   - Port: `587` (TLS) or `465` (SSL)
   - Security: TLS/SSL required

#### Outlook/Hotmail Setup
1. **SMTP Settings**:
   - Server: `smtp-mail.outlook.com`
   - Port: `587`
   - Security: TLS required
2. **Authentication**: Use regular password (no app password needed)

#### Yahoo Mail Setup
1. **Generate App Password**:
   - Account Settings → Security → App passwords
2. **SMTP Settings**:
   - Server: `smtp.mail.yahoo.com`
   - Port: `587` or `465`
   - Security: TLS/SSL required

#### Custom/Corporate Email
- **SMTP Server**: Contact IT department
- **Port**: Usually 587, 465, or 25
- **Security**: TLS recommended
- **Authentication**: Domain credentials

## Environment Configuration

### Required Environment Variables
Add these to your `.env` file:

```env
# Email Configuration
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USE_TLS=true
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# IMAP Configuration (for reading emails)
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
EMAIL_IMAP_USE_SSL=true

# Optional: Default sender info
EMAIL_DEFAULT_FROM=your-email@gmail.com
EMAIL_DEFAULT_NAME=Your Name
```

### Gmail Example
```env
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USE_TLS=true
EMAIL_USERNAME=john.doe@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
EMAIL_IMAP_USE_SSL=true
```

### Outlook Example
```env
EMAIL_SMTP_SERVER=smtp-mail.outlook.com
EMAIL_SMTP_PORT=587
EMAIL_USE_TLS=true
EMAIL_USERNAME=john.doe@outlook.com
EMAIL_PASSWORD=your-outlook-password
EMAIL_IMAP_SERVER=outlook.office365.com
EMAIL_IMAP_PORT=993
EMAIL_IMAP_USE_SSL=true
```

## Available Tools

### 1. SendEmailTool
**Purpose**: Send emails with attachments and HTML formatting
**Function**: `send_email`

#### Parameters:
- `to` (string/array): Recipient email address(es)
- `subject` (string): Email subject line
- `body` (string): Email body content
- `cc` (string/array, optional): CC recipients
- `bcc` (string/array, optional): BCC recipients
- `html` (boolean, optional): Send as HTML (default: false)
- `attachments` (array, optional): File paths to attach

#### Examples:

**Simple text email:**
```json
{
  "to": "recipient@example.com",
  "subject": "Meeting Reminder",
  "body": "Don't forget about our meeting tomorrow at 2 PM."
}
```

**HTML email with formatting:**
```json
{
  "to": ["john@example.com", "jane@example.com"],
  "subject": "Weekly Report",
  "body": "<h1>Weekly Summary</h1><p>Here's what we accomplished:</p><ul><li>Task 1</li><li>Task 2</li></ul>",
  "html": true
}
```

**Email with attachments:**
```json
{
  "to": "client@company.com",
  "subject": "Project Deliverables",
  "body": "Please find the attached documents for review.",
  "attachments": ["report.pdf", "data.xlsx", "images/chart.png"]
}
```

**Email with CC and BCC:**
```json
{
  "to": "primary@example.com",
  "cc": ["manager@company.com"],
  "bcc": ["archive@company.com"],
  "subject": "Project Update",
  "body": "Here's the latest project status..."
}
```

### 2. ReadEmailTool
**Purpose**: Read and search emails from IMAP servers
**Function**: `read_email`

#### Parameters:
- `folder` (string, optional): Email folder to read (default: "INBOX")
- `limit` (number, optional): Number of emails to retrieve (default: 10)
- `search_criteria` (string, optional): Search criteria
- `mark_read` (boolean, optional): Mark emails as read (default: false)

#### Examples:

**Read latest emails:**
```json
{
  "limit": 5
}
```

**Search for specific emails:**
```json
{
  "search_criteria": "FROM john@example.com",
  "limit": 20
}
```

**Read from specific folder:**
```json
{
  "folder": "Sent",
  "limit": 10
}
```

## Advanced Usage

### 1. Bulk Email Sending
```python
# Send personalized emails to multiple recipients
recipients = [
    {"email": "john@example.com", "name": "John"},
    {"email": "jane@example.com", "name": "Jane"}
]

for recipient in recipients:
    await send_email(
        to=recipient["email"],
        subject=f"Hello {recipient['name']}",
        body=f"Dear {recipient['name']},\n\nThis is a personalized message...",
        html=False
    )
```

### 2. Email Templates
```python
# HTML email template
html_template = """
<html>
<body>
    <h2 style="color: #2E75B6;">Weekly Newsletter</h2>
    <p>Dear Subscriber,</p>
    <div style="background-color: #f5f5f5; padding: 20px; margin: 20px 0;">
        <h3>This Week's Highlights</h3>
        <ul>
            <li>Feature Update: New dashboard</li>
            <li>Blog Post: Best practices guide</li>
            <li>Event: Webinar on Thursday</li>
        </ul>
    </div>
    <p>Best regards,<br>The Team</p>
</body>
</html>
"""

await send_email(
    to="subscribers@example.com",
    subject="Weekly Newsletter",
    body=html_template,
    html=True
)
```

### 3. Email Automation Workflow
```python
# Check for new emails and respond
new_emails = await read_email(
    search_criteria="UNSEEN FROM support@",
    limit=50
)

for email in new_emails:
    if "urgent" in email["subject"].lower():
        await send_email(
            to=email["from"],
            subject=f"Re: {email['subject']}",
            body="Thank you for your message. We've received your urgent request and will respond within 2 hours."
        )
```

## IMAP Search Criteria

### Basic Searches
- `FROM john@example.com` - Emails from specific sender
- `TO jane@example.com` - Emails to specific recipient
- `SUBJECT "meeting"` - Emails with subject containing "meeting"
- `BODY "project"` - Emails with body containing "project"

### Date Searches
- `SINCE 01-Jan-2024` - Emails since specific date
- `BEFORE 31-Dec-2023` - Emails before specific date
- `ON 15-Mar-2024` - Emails on specific date

### Status Searches
- `UNSEEN` - Unread emails
- `SEEN` - Read emails
- `FLAGGED` - Flagged emails
- `UNFLAGGED` - Unflagged emails

### Combined Searches
- `FROM john@example.com UNSEEN` - Unread emails from John
- `SUBJECT "report" SINCE 01-Jan-2024` - Reports since January
- `TO manager@company.com FLAGGED` - Flagged emails to manager

## Email Security

### Authentication Best Practices
1. **Use App Passwords** - Never use main account passwords
2. **Enable 2FA** - Two-factor authentication required
3. **Secure Storage** - Store credentials in environment variables
4. **Regular Rotation** - Update passwords periodically

### Secure Configuration
```env
# Use app-specific passwords
EMAIL_PASSWORD=generated-app-password-here

# Enable encryption
EMAIL_USE_TLS=true
EMAIL_IMAP_USE_SSL=true

# Secure ports
EMAIL_SMTP_PORT=587
EMAIL_IMAP_PORT=993
```

## Error Handling

### Common SMTP Errors

#### Authentication Failed
**Error**: `535 Authentication failed`
**Solutions**:
1. Verify username/password
2. Check if app password is required
3. Enable "less secure apps" (not recommended)
4. Verify 2FA is properly configured

#### Connection Refused
**Error**: `Connection refused`
**Solutions**:
1. Check SMTP server address
2. Verify port number
3. Check firewall settings
4. Ensure TLS/SSL settings match

#### Rate Limiting
**Error**: `Too many connections`
**Solutions**:
1. Add delays between emails
2. Use connection pooling
3. Check provider limits
4. Consider bulk email service

### Common IMAP Errors

#### Authentication Failed
**Error**: `LOGIN failed`
**Solutions**:
1. Verify IMAP is enabled
2. Check credentials
3. Use app password
4. Verify server settings

#### Folder Not Found
**Error**: `Folder does not exist`
**Solutions**:
1. List available folders first
2. Use correct folder names
3. Check folder permissions
4. Try "INBOX" default

## Testing Email Configuration

### Test Script
```python
async def test_email_setup():
    try:
        # Test sending
        await send_email(
            to="your-email@example.com",
            subject="Test Email",
            body="This is a test email to verify configuration."
        )
        print("✅ Send email test passed")
        
        # Test reading
        emails = await read_email(limit=1)
        print(f"✅ Read email test passed - found {len(emails)} emails")
        
    except Exception as e:
        print(f"❌ Email test failed: {e}")
```

### Debug Mode
Enable verbose logging to diagnose issues:
```env
EMAIL_DEBUG=true
EMAIL_LOG_LEVEL=DEBUG
```

## Performance Optimization

### Sending Optimization
1. **Connection reuse** - Keep SMTP connections alive
2. **Batch processing** - Group emails efficiently
3. **Async operations** - Send emails concurrently
4. **Error handling** - Retry failed sends

### Reading Optimization
1. **Folder caching** - Cache folder structures
2. **Partial fetching** - Fetch headers first
3. **Search indexing** - Use server-side search
4. **Connection management** - Reuse IMAP connections

## Integration Examples

### 1. Notification System
```python
# Send alerts based on system events
async def send_alert(event_type, message):
    await send_email(
        to="admin@company.com",
        subject=f"System Alert: {event_type}",
        body=f"Alert Details:\n{message}\n\nTime: {datetime.now()}",
        html=False
    )
```

### 2. Report Distribution
```python
# Generate and email reports
async def send_weekly_report():
    # Generate report
    report_data = generate_report()
    
    # Create Excel file
    await write_excel("weekly_report.xlsx", report_data)
    
    # Email report
    await send_email(
        to=["manager@company.com", "team@company.com"],
        subject="Weekly Performance Report",
        body="Please find attached the weekly performance report.",
        attachments=["weekly_report.xlsx"]
    )
```

### 3. Customer Support Automation
```python
# Auto-respond to support emails
support_emails = await read_email(
    search_criteria="TO support@company.com UNSEEN",
    limit=100
)

for email in support_emails:
    await send_email(
        to=email["from"],
        subject=f"Re: {email['subject']}",
        body="Thank you for contacting support. We've received your message and will respond within 24 hours."
    )
```
