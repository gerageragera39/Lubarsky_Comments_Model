"""
Configuration module for the YouTube Comment Classifier
"""
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class Config:
    """Configuration class to hold all environment variables and constants"""
    
    API_KEY = os.getenv("API_KEY")
    DATASET_FILE = os.getenv("DATASET_FILE", "dataset.csv")
    MAX_COMMENTS = int(os.getenv("MAX_COMMENTS", "500"))
    SESSION_FILE = os.getenv("SESSION_FILE", "session.json")
    
    # Validate required environment variables
    @classmethod
    def validate(cls):
        """Validate that required environment variables are set"""
        if not cls.API_KEY:
            raise ValueError("API_KEY environment variable is required")