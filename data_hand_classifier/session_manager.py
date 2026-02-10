"""
Session manager for saving and restoring classification progress
"""
import os
import json
from typing import Dict, List
from .models import SessionData, Comment, VideoInfo


class SessionManager:
    """
    Manages session data for resuming classification progress
    """
    
    def __init__(self, path: str):
        self.path = path
    
    def has_active_session(self) -> bool:
        """Check if there's an active session that can be resumed"""
        if not os.path.exists(self.path):
            return False
        try:
            data = self._load()
            return any(not comment.is_processed for comment in data.comments)
        except Exception:
            return False
    
    def _load(self) -> SessionData:
        """Load session data from file"""
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Convert the loaded data to our models
        video_info = VideoInfo(
            url=data["video_url"],
            video_id=data["video_id"]
        )
        
        comments = []
        for comment_data in data["comments"]:
            comment = Comment(
                text=comment_data["text"],
                is_processed=comment_data["done"],
                action=comment_data.get("action")
            )
            comments.append(comment)
        
        return SessionData(
            video_info=video_info,
            comments=comments
        )
    
    def _save(self, session_data: SessionData):
        """Save session data to file"""
        # Convert our models to dictionary format
        data = {
            "video_url": session_data.video_info.url,
            "video_id": session_data.video_info.video_id,
            "comments": [
                {
                    "text": comment.text,
                    "done": comment.is_processed,
                    "action": comment.action
                }
                for comment in session_data.comments
            ]
        }
        
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_session(self, video_url: str, video_id: str, comments: List[str]):
        """Create a new session with the given video and comments"""
        session_data = SessionData(
            video_info=VideoInfo(url=video_url, video_id=video_id),
            comments=[Comment(text=comment) for comment in comments]
        )
        self._save(session_data)
    
    def get_session_info(self) -> Dict:
        """Get information about the current session"""
        data = self._load()
        stats = data.get_progress_stats()
        
        return {
            "video_url": data.video_info.url,
            "video_id": data.video_info.video_id,
            "total": stats["total"],
            "done": stats["processed"],
            "remaining": stats["remaining"],
        }
    
    def get_comments(self) -> List[Comment]:
        """Get all comments in the session"""
        data = self._load()
        return data.comments
    
    def get_first_unprocessed_index(self) -> int:
        """Get the index of the first unprocessed comment"""
        data = self._load()
        for i, comment in enumerate(data.comments):
            if not comment.is_processed:
                return i
        return len(data.comments)
    
    def mark_processed(self, index: int, action: str):
        """Mark a comment as processed with the given action"""
        data = self._load()
        if 0 <= index < len(data.comments):
            data.comments[index].is_processed = True
            data.comments[index].action = action
            self._save(data)
    
    def mark_unprocessed(self, index: int):
        """Mark a comment as unprocessed (for undo functionality)"""
        data = self._load()
        if 0 <= index < len(data.comments):
            data.comments[index].is_processed = False
            data.comments[index].action = None
            self._save(data)
    
    def get_action(self, index: int) -> str | None:
        """Get the action taken for a comment at the given index"""
        data = self._load()
        if 0 <= index < len(data.comments):
            return data.comments[index].action
        return None
    
    def delete_session(self):
        """Delete the session file"""
        if os.path.exists(self.path):
            os.remove(self.path)