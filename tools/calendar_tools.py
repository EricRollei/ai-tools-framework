"""
AI Tools Framework: calendar_tools.py
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

calendar_tools.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# tools/calendar_tools.py
"""
Calendar tools for scheduling and event management
"""

import datetime
import json
import re
from typing import List, Optional, Dict, Any
from pathlib import Path
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

class CalendarTool(BaseTool):
    """Manage calendar events and scheduling"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.calendar_file = Path("calendar_events.json")
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="manage_calendar",
            description="Create, view, update, and delete calendar events",
            category="productivity",
            parameters=[
                ToolParameter(
                    name="action",
                    description="Action to perform: 'create', 'list', 'update', 'delete', 'find_free_time'",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="title",
                    description="Event title (required for create/update)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="start_datetime",
                    description="Start date and time (YYYY-MM-DD HH:MM format)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="end_datetime",
                    description="End date and time (YYYY-MM-DD HH:MM format)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="description",
                    description="Event description",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="location",
                    description="Event location",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="event_id",
                    description="Event ID (for update/delete operations)",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="date_range",
                    description="Date range for listing events (e.g., 'today', 'this_week', 'this_month', 'YYYY-MM-DD')",
                    param_type="string",
                    required=False,
                    default="this_week"
                ),
                ToolParameter(
                    name="duration_hours",
                    description="Duration in hours for find_free_time",
                    param_type="number",
                    required=False,
                    default=1
                )
            ]
        )
    
    async def execute(self, action: str, title: Optional[str] = None,
                     start_datetime: Optional[str] = None, end_datetime: Optional[str] = None,
                     description: Optional[str] = None, location: Optional[str] = None,
                     event_id: Optional[str] = None, date_range: str = "this_week",
                     duration_hours: float = 1) -> ToolResult:
        """Execute calendar operation"""
        try:
            if action == "create":
                return await self._create_event(title, start_datetime, end_datetime, description, location)
            elif action == "list":
                return await self._list_events(date_range)
            elif action == "update":
                return await self._update_event(event_id, title, start_datetime, end_datetime, description, location)
            elif action == "delete":
                return await self._delete_event(event_id)
            elif action == "find_free_time":
                return await self._find_free_time(date_range, duration_hours)
            else:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Unknown action: {action}. Use: create, list, update, delete, find_free_time",
                    error_message=f"Unknown action: {action}"
                )
        
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Calendar operation failed: {str(e)}",
                error_message=str(e)
            )
    
    def _load_events(self) -> List[Dict]:
        """Load events from file"""
        if not self.calendar_file.exists():
            return []
        
        try:
            with open(self.calendar_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_events(self, events: List[Dict]) -> None:
        """Save events to file"""
        with open(self.calendar_file, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, default=str)
    
    def _parse_datetime(self, dt_str: str) -> datetime.datetime:
        """Parse datetime string"""
        formats = [
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%m/%d/%Y %H:%M",
            "%m/%d/%Y"
        ]
        
        for fmt in formats:
            try:
                return datetime.datetime.strptime(dt_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse datetime: {dt_str}")
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    async def _create_event(self, title: str, start_datetime: str, end_datetime: str,
                           description: Optional[str], location: Optional[str]) -> ToolResult:
        """Create a new event"""
        if not title or not start_datetime:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content="Title and start_datetime are required for creating events",
                error_message="Missing required fields"
            )
        
        start_dt = self._parse_datetime(start_datetime)
        
        # If no end time provided, default to 1 hour duration
        if end_datetime:
            end_dt = self._parse_datetime(end_datetime)
        else:
            end_dt = start_dt + datetime.timedelta(hours=1)
        
        if end_dt <= start_dt:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content="End time must be after start time",
                error_message="Invalid time range"
            )
        
        event = {
            "id": self._generate_event_id(),
            "title": title,
            "start_datetime": start_dt.isoformat(),
            "end_datetime": end_dt.isoformat(),
            "description": description or "",
            "location": location or "",
            "created_at": datetime.datetime.now().isoformat()
        }
        
        events = self._load_events()
        events.append(event)
        self._save_events(events)
        
        return ToolResult(
            success=True,
            result_type=ToolResultType.TEXT,
            content=f"Event created successfully!\n\nEvent ID: {event['id']}\nTitle: {title}\nStart: {start_dt.strftime('%Y-%m-%d %H:%M')}\nEnd: {end_dt.strftime('%Y-%m-%d %H:%M')}" + 
                   (f"\nLocation: {location}" if location else "") +
                   (f"\nDescription: {description}" if description else ""),
            metadata={"event_id": event['id'], "action": "create"}
        )
    
    async def _list_events(self, date_range: str) -> ToolResult:
        """List events in date range"""
        events = self._load_events()
        now = datetime.datetime.now()
        
        # Parse date range
        if date_range == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + datetime.timedelta(days=1)
        elif date_range == "this_week":
            days_since_monday = now.weekday()
            start_date = (now - datetime.timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + datetime.timedelta(days=7)
        elif date_range == "this_month":
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                end_date = start_date.replace(year=now.year + 1, month=1)
            else:
                end_date = start_date.replace(month=now.month + 1)
        else:
            # Try to parse as specific date
            try:
                specific_date = self._parse_datetime(date_range)
                start_date = specific_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = start_date + datetime.timedelta(days=1)
            except ValueError:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content=f"Invalid date range: {date_range}. Use: today, this_week, this_month, or YYYY-MM-DD",
                    error_message="Invalid date range"
                )
        
        # Filter events in range
        filtered_events = []
        for event in events:
            event_start = datetime.datetime.fromisoformat(event['start_datetime'])
            if start_date <= event_start < end_date:
                filtered_events.append(event)
        
        # Sort by start time
        filtered_events.sort(key=lambda x: x['start_datetime'])
        
        if not filtered_events:
            return ToolResult(
                success=True,
                result_type=ToolResultType.TEXT,
                content=f"No events found for {date_range}",
                metadata={"count": 0, "date_range": date_range}
            )
        
        # Format output
        lines = [f"Events for {date_range}:", ""]
        for event in filtered_events:
            start_dt = datetime.datetime.fromisoformat(event['start_datetime'])
            end_dt = datetime.datetime.fromisoformat(event['end_datetime'])
            
            lines.append(f"📅 {event['title']} (ID: {event['id']})")
            lines.append(f"   📍 {start_dt.strftime('%Y-%m-%d %H:%M')} - {end_dt.strftime('%H:%M')}")
            if event.get('location'):
                lines.append(f"   🗺️  {event['location']}")
            if event.get('description'):
                lines.append(f"   📝 {event['description']}")
            lines.append("")
        
        return ToolResult(
            success=True,
            result_type=ToolResultType.TEXT,
            content="\n".join(lines),
            metadata={"count": len(filtered_events), "date_range": date_range}
        )
    
    async def _update_event(self, event_id: str, title: Optional[str], start_datetime: Optional[str],
                           end_datetime: Optional[str], description: Optional[str], location: Optional[str]) -> ToolResult:
        """Update an existing event"""
        if not event_id:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content="Event ID is required for updating events",
                error_message="Missing event ID"
            )
        
        events = self._load_events()
        event_found = False
        
        for event in events:
            if event['id'] == event_id:
                event_found = True
                
                # Update fields if provided
                if title:
                    event['title'] = title
                if start_datetime:
                    event['start_datetime'] = self._parse_datetime(start_datetime).isoformat()
                if end_datetime:
                    event['end_datetime'] = self._parse_datetime(end_datetime).isoformat()
                if description is not None:
                    event['description'] = description
                if location is not None:
                    event['location'] = location
                
                event['updated_at'] = datetime.datetime.now().isoformat()
                break
        
        if not event_found:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Event with ID {event_id} not found",
                error_message="Event not found"
            )
        
        self._save_events(events)
        
        return ToolResult(
            success=True,
            result_type=ToolResultType.TEXT,
            content=f"Event {event_id} updated successfully",
            metadata={"event_id": event_id, "action": "update"}
        )
    
    async def _delete_event(self, event_id: str) -> ToolResult:
        """Delete an event"""
        if not event_id:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content="Event ID is required for deleting events",
                error_message="Missing event ID"
            )
        
        events = self._load_events()
        original_count = len(events)
        events = [event for event in events if event['id'] != event_id]
        
        if len(events) == original_count:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Event with ID {event_id} not found",
                error_message="Event not found"
            )
        
        self._save_events(events)
        
        return ToolResult(
            success=True,
            result_type=ToolResultType.TEXT,
            content=f"Event {event_id} deleted successfully",
            metadata={"event_id": event_id, "action": "delete"}
        )
    
    async def _find_free_time(self, date_range: str, duration_hours: float) -> ToolResult:
        """Find free time slots"""
        events = self._load_events()
        now = datetime.datetime.now()
        
        # Parse date range (same logic as list_events)
        if date_range == "today":
            start_date = now.replace(hour=8, minute=0, second=0, microsecond=0)  # Start at 8 AM
            end_date = now.replace(hour=18, minute=0, second=0, microsecond=0)   # End at 6 PM
        elif date_range == "this_week":
            days_since_monday = now.weekday()
            start_date = (now - datetime.timedelta(days=days_since_monday)).replace(hour=8, minute=0, second=0, microsecond=0)
            end_date = start_date + datetime.timedelta(days=7)
        else:
            # Default to today
            start_date = now.replace(hour=8, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=18, minute=0, second=0, microsecond=0)
        
        # Get events in range
        busy_times = []
        for event in events:
            event_start = datetime.datetime.fromisoformat(event['start_datetime'])
            event_end = datetime.datetime.fromisoformat(event['end_datetime'])
            
            if event_start < end_date and event_end > start_date:
                busy_times.append((event_start, event_end))
        
        # Sort busy times
        busy_times.sort()
        
        # Find free slots
        free_slots = []
        current_time = max(start_date, now)
        
        for busy_start, busy_end in busy_times:
            if current_time + datetime.timedelta(hours=duration_hours) <= busy_start:
                free_slots.append((current_time, busy_start))
            current_time = max(current_time, busy_end)
        
        # Check for time after last event
        if current_time + datetime.timedelta(hours=duration_hours) <= end_date:
            free_slots.append((current_time, end_date))
        
        if not free_slots:
            return ToolResult(
                success=True,
                result_type=ToolResultType.TEXT,
                content=f"No free time slots of {duration_hours} hours found for {date_range}",
                metadata={"free_slots": 0, "duration_hours": duration_hours}
            )
        
        # Format output
        lines = [f"Free time slots ({duration_hours} hours) for {date_range}:", ""]
        for i, (slot_start, slot_end) in enumerate(free_slots, 1):
            lines.append(f"{i}. {slot_start.strftime('%Y-%m-%d %H:%M')} - {slot_end.strftime('%Y-%m-%d %H:%M')}")
        
        return ToolResult(
            success=True,
            result_type=ToolResultType.TEXT,
            content="\n".join(lines),
            metadata={"free_slots": len(free_slots), "duration_hours": duration_hours}
        )

# Register the tool
registry.register(CalendarTool)
