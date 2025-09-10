"""
AI Tools Framework: email_tools.py
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

email_tools.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# tools/email_tools.py
"""
Email tools for the AI Tools framework
Requires email configuration via environment variables
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict, Any
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry
import os

class SendEmailTool(BaseTool):
    """Send an email via SMTP"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="send_email",
            description="Send an email via SMTP server (requires email configuration in .env)",
            category="communication",
            parameters=[
                ToolParameter(
                    name="to_email",
                    description="Recipient email address",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="subject",
                    description="Email subject",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="body",
                    description="Email body content",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="from_email",
                    description="Sender email address (if not set, uses SMTP_FROM_EMAIL env var)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="smtp_server",
                    description="SMTP server hostname (if not set, uses SMTP_SERVER env var)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="smtp_port",
                    description="SMTP server port - use 465 for SSL/TLS, 587 for STARTTLS (if not set, uses SMTP_PORT env var or 587)",
                    param_type="number",
                    required=False,
                    default=587
                ),
                ToolParameter(
                    name="is_html",
                    description="Whether the body content is HTML",
                    param_type="boolean",
                    required=False,
                    default=False
                )
            ]
        )
    
    async def execute(self, to_email: str, subject: str, body: str, 
                     from_email: Optional[str] = None, smtp_server: Optional[str] = None,
                     smtp_port: Optional[int] = None, is_html: bool = False) -> ToolResult:
        """Execute email sending"""
        try:
            # Get configuration from environment or parameters
            from_email = from_email or os.getenv('SMTP_FROM_EMAIL')
            smtp_server = smtp_server or os.getenv('SMTP_SERVER')
            # Handle port from env var or parameter or default
            if smtp_port is None:
                smtp_port = int(os.getenv('SMTP_PORT', 587))
            smtp_username = os.getenv('SMTP_USERNAME')
            smtp_password = os.getenv('SMTP_PASSWORD')
            
            if not from_email:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="From email not specified. Set SMTP_FROM_EMAIL environment variable or provide from_email parameter.",
                    error_message="From email not specified. Set SMTP_FROM_EMAIL environment variable or provide from_email parameter."
                )
            
            if not smtp_server:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="SMTP server not specified. Set SMTP_SERVER environment variable or provide smtp_server parameter.",
                    error_message="SMTP server not specified. Set SMTP_SERVER environment variable or provide smtp_server parameter."
                )
            
            if not smtp_username or not smtp_password:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="SMTP credentials not found. Set SMTP_USERNAME and SMTP_PASSWORD environment variables.",
                    error_message="SMTP credentials not found. Set SMTP_USERNAME and SMTP_PASSWORD environment variables."
                )
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            body_type = 'html' if is_html else 'plain'
            msg.attach(MIMEText(body, body_type))
            
            # Send email - handle SSL/TLS vs STARTTLS based on port
            if smtp_port == 465:
                # Use SSL/TLS (direct encryption)
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                # Use STARTTLS (upgrade unencrypted connection)
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            
            server.login(smtp_username, smtp_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
            
            return ToolResult(
                success=True,
                content=f"Email sent successfully to {to_email}",
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "send_email",
                    "to_email": to_email,
                    "subject": subject,
                    "from_email": from_email,
                    "smtp_server": smtp_server
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error sending email: {str(e)}",
                error_message=f"Error sending email: {str(e)}"
            )

class CheckEmailTool(BaseTool):
    """Check for new emails via IMAP"""
    
    def __init__(self):
        super().__init__(
            name="check_email",
            description="Check for new emails via IMAP",
            parameters=[
                ToolParameter(
                    name="max_emails",
                    description="Maximum number of recent emails to retrieve",
                    param_type="number",
                    required=False,
                    default=5
                ),
                ToolParameter(
                    name="imap_server",
                    description="IMAP server hostname (if not set, uses IMAP_SERVER env var)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="imap_port",
                    description="IMAP server port (if not set, uses IMAP_PORT env var or 993)",
                    param_type="number",
                    required=False,
                    default=993
                ),
                ToolParameter(
                    name="folder",
                    description="Email folder to check",
                    param_type="string",
                    required=False,
                    default="INBOX"
                )
            ]
        )
    
    async def execute(self, max_emails: int = 5, imap_server: Optional[str] = None,
                     imap_port: int = 993, folder: str = "INBOX") -> ToolResult:
        """Execute email checking"""
        try:
            # Get configuration from environment
            imap_server = imap_server or os.getenv('IMAP_SERVER')
            imap_username = os.getenv('IMAP_USERNAME') or os.getenv('SMTP_USERNAME')
            imap_password = os.getenv('IMAP_PASSWORD') or os.getenv('SMTP_PASSWORD')
            
            if not imap_server:
                return ToolResult(
                    success=False,
                    error_message="IMAP server not specified. Set IMAP_SERVER environment variable or provide imap_server parameter."
                )
            
            if not imap_username or not imap_password:
                return ToolResult(
                    success=False,
                    error_message="IMAP credentials not found. Set IMAP_USERNAME/IMAP_PASSWORD or SMTP_USERNAME/SMTP_PASSWORD environment variables."
                )
            
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(imap_server, imap_port)
            mail.login(imap_username, imap_password)
            mail.select(folder)
            
            # Search for emails
            typ, data = mail.search(None, 'ALL')
            mail_ids = data[0].split()
            
            # Get recent emails
            recent_emails = []
            for mail_id in mail_ids[-max_emails:]:
                typ, data = mail.fetch(mail_id, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                
                email_info = {
                    "id": mail_id.decode(),
                    "subject": msg.get('Subject', 'No Subject'),
                    "from": msg.get('From', 'Unknown'),
                    "date": msg.get('Date', 'Unknown'),
                    "to": msg.get('To', 'Unknown')
                }
                
                # Get body (simple text extraction)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            break
                else:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                
                email_info["body_preview"] = body[:200] + "..." if len(body) > 200 else body
                recent_emails.append(email_info)
            
            mail.logout()
            
            result = {
                "folder": folder,
                "total_emails": len(mail_ids),
                "retrieved_count": len(recent_emails),
                "emails": recent_emails
            }
            
            return ToolResult(
                success=True,
                content=result,
                result_type=ToolResultType.JSON,
                metadata={
                    "tool": "check_email",
                    "folder": folder,
                    "imap_server": imap_server
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error_message=f"Error checking email: {str(e)}"
            )

# Register email tools
registry.register(SendEmailTool)
# registry.register(CheckEmailTool)  # TODO: Update CheckEmailTool to new framework structure
