"""
Utility functions for the YouTube Comment Classifier
"""
import re
import emoji


def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from URL"""
    patterns = [
        r"(?:v=|\/v\/|youtu\.be\/|\/embed\/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def clean_comment(text: str) -> str:
    """Clean and normalize a comment text"""
    text = emoji.replace_emoji(text, replace="")
    text = re.sub(r"[^\w\s.,!?;:'\"\-—–()@#$%&*/\\+={}\[\]<>^~`\n]", "", text, flags=re.UNICODE)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()