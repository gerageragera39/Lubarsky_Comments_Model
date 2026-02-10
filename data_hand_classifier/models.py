"""
Data models for the YouTube Comment Classifier
"""
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Sentiment(Enum):
    """Sentiment classification enum"""
    POSITIVE = 1
    NEUTRAL = 0
    NEGATIVE = -1


@dataclass
class Comment:
    """Represents a YouTube comment"""
    text: str
    sentiment: Optional[Sentiment] = None
    is_processed: bool = False
    action: Optional[str] = None  # 'classified', 'skipped', or None


@dataclass
class VideoInfo:
    """Represents YouTube video information"""
    url: str
    video_id: str


@dataclass
class SessionData:
    """Represents a classification session"""
    video_info: VideoInfo
    comments: list[Comment]
    
    def get_progress_stats(self) -> dict:
        """Get progress statistics for the session"""
        total = len(self.comments)
        processed = sum(1 for comment in self.comments if comment.is_processed)
        remaining = total - processed
        
        return {
            "total": total,
            "processed": processed,
            "remaining": remaining
        }