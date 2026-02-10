"""
Controller for the comment classifier GUI
"""
from typing import Callable, Optional
from .models import Comment, Sentiment
from .session_manager import SessionManager
from .dataset_manager import DatasetManager


class ClassifierController:
    """Controller managing the business logic for comment classification"""
    
    def __init__(self, dataset_manager: DatasetManager, session_manager: SessionManager):
        self.dataset_manager = dataset_manager
        self.session_manager = session_manager
        
        # Current session state
        self.comments: list[Comment] = []
        self.current_index: int = 0
        
        # Navigation state
        self.can_go_back = False
        self.went_back_from: Optional[int] = None
    
    def start_new_session(self, comments: list[str]):
        """Start a new classification session with the given comments"""
        self.comments = [Comment(text=comment) for comment in comments]
        self.current_index = 0
        self.can_go_back = False
        self.went_back_from = None
    
    def resume_session(self):
        """Resume an existing session"""
        self.comments = self.session_manager.get_comments()
        self.current_index = self.session_manager.get_first_unprocessed_index()
        self.can_go_back = False
        self.went_back_from = None
    
    def classify_current_comment(self, sentiment: Sentiment):
        """Classify the current comment with the given sentiment"""
        if 0 <= self.current_index < len(self.comments):
            comment = self.comments[self.current_index]
            comment.sentiment = sentiment
            comment.is_processed = True
            comment.action = "classified"
            
            # Save to dataset
            self.dataset_manager.save_comment(comment.text, sentiment)
            
            # Mark as done in session
            self.session_manager.mark_processed(self.current_index, "classified")
            
            # Update navigation state
            self.can_go_back = True
            self.went_back_from = None
            
            # Move to next comment
            self.current_index += 1
    
    def skip_current_comment(self):
        """Skip the current comment"""
        if 0 <= self.current_index < len(self.comments):
            comment = self.comments[self.current_index]
            comment.action = "skipped"
            comment.is_processed = True
            
            # Mark as skipped in session
            self.session_manager.mark_processed(self.current_index, "skipped")
            
            # Update navigation state
            self.can_go_back = True
            self.went_back_from = None
            
            # Move to next comment
            self.current_index += 1
    
    def go_back(self):
        """Go back to the previous comment to reclassify it"""
        # Only allow going back once after classifying/skipping
        if not self.can_go_back or self.went_back_from is not None:
            return False
        
        # Check if we can go back
        if self.current_index > 0:
            prev_index = self.current_index - 1
            prev_comment = self.comments[prev_index]
            
            # Reset the previous comment's state
            prev_comment.is_processed = False
            prev_comment.action = None
            prev_comment.sentiment = None
            
            # Mark as undone in session
            self.session_manager.mark_unprocessed(prev_index)
            
            # Update navigation state
            self.current_index = prev_index
            self.can_go_back = False
            self.went_back_from = prev_index
            
            return True
        return False
    
    def get_current_comment(self) -> Optional[Comment]:
        """Get the current comment being processed"""
        if 0 <= self.current_index < len(self.comments):
            return self.comments[self.current_index]
        return None
    
    def has_more_comments(self) -> bool:
        """Check if there are more comments to process"""
        return self.current_index < len(self.comments)
    
    def get_progress(self) -> tuple[int, int]:
        """Get current progress (current index, total)"""
        return self.current_index, len(self.comments)
    
    def save_and_exit(self):
        """Save the current session and exit"""
        # The session is already saved after each action, so just return
        pass