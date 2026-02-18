"""
Video Utilities
Helper functions for working with YouTube video URLs
"""

import re


def extract_video_id(url: str) -> str | None:
    """
    Extract YouTube video ID from URL.

    Supports various YouTube URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID

    Args:
        url: YouTube video URL

    Returns:
        Video ID if found, None otherwise
    """
    if not url:
        return None

    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([a-zA-Z0-9_-]{11})",
        r"([a-zA-Z0-9_-]{11})",  # Fallback: just the ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def validate_youtube_url(url: str) -> tuple[bool, str]:
    """
    Validate a YouTube URL.

    Args:
        url: URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url:
        return False, "URL is required"

    video_id = extract_video_id(url)
    if not video_id:
        return False, "Invalid YouTube URL format"

    return True, ""
