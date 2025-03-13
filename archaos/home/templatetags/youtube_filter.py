from django import template
import re

register = template.Library()

@register.filter
def youtube_id(value):
    """
    Extracts the YouTube video ID from a URL.
    """
    # Define regex patterns for different YouTube URL formats
    patterns = [
        r'^https?://(?:www\.)?youtube\.com/watch\?v=([^&]+)',
        r'^https?://youtu\.be/([^?]+)',
    ]

    # Try to match each pattern
    for pattern in patterns:
        match = re.match(pattern, value)
        if match:
            return match.group(1)

    # If no patterns match, return the original value
    return value
