"""HELPER FUNCTIONS - Utility functions used across the application"""

import os
import json
from datetime import datetime

def allowed_file(filename, allowed_extensions):
    """Check if file type is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def format_date(date_obj, format='%d-%m-%Y'):
    """Format datetime object to string"""
    if isinstance(date_obj, datetime):
        return date_obj.strftime(format)
    return str(date_obj)

def get_time_ago(date_obj):
    """Get human-readable time difference"""
    if not date_obj:
        return "Unknown"
    
    diff = datetime.utcnow() - date_obj
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    
    hours = diff.seconds // 3600
    if hours > 0:
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    
    minutes = diff.seconds // 60
    if minutes > 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    
    return "Just now"

def parse_json(data):
    """Safely parse JSON string"""
    try:
        if isinstance(data, str):
            return json.loads(data)
        return data
    except (json.JSONDecodeError, TypeError):
        return {}

def truncate_text(text, length=100):
    """Truncate text to specified length"""
    if len(text) > length:
        return text[:length] + "..."
    return text

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
