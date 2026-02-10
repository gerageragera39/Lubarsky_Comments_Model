"""
API client for fetching YouTube comments
"""
from typing import List
from googleapiclient.discovery import build
from .utils import clean_comment


class YouTubeAPIClient:
    """Client for interacting with YouTube API to fetch comments"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)
    
    def fetch_comments(self, video_id: str, max_results: int = 500) -> List[str]:
        """Fetch comments from a YouTube video"""
        comments: List[str] = []
        next_page = None

        while len(comments) < max_results:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_results - len(comments)),
                pageToken=next_page,
                textFormat="plainText",
                order="relevance",
            )
            response = request.execute()
            for item in response.get("items", []):
                text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                cleaned_text = clean_comment(text)
                if cleaned_text:  # Only add non-empty comments
                    comments.append(cleaned_text)
            next_page = response.get("nextPageToken")
            if not next_page:
                break

        return comments