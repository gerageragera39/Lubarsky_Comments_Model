"""
Configuration module for the YouTube Comment Classifier
"""
import os
import sys
from dotenv import load_dotenv


def get_resource_path(filename: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller build"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running in normal Python environment
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, filename)


# Load environment variables
load_dotenv()


class Config:
    """Configuration class to hold all environment variables and constants"""

    API_KEY = os.getenv("API_KEY")
    DATASET_FILE = get_resource_path("dataset.csv")
    MAX_COMMENTS = int(os.getenv("MAX_COMMENTS", "500"))
    SESSION_FILE = get_resource_path("session.json")

    # Validate required environment variables
    @classmethod
    def validate(cls):
        """Validate that required environment variables are set"""
        if not cls.API_KEY:
            raise ValueError("API_KEY environment variable is required")