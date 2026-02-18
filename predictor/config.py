"""
Configuration module for the YouTube Comment Predictor
"""

import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class Config:
    """Configuration class to hold all environment variables and constants"""

    API_KEY = os.getenv("API_KEY")
    DEFAULT_OUTPUT_FILE = os.getenv("OUTPUT_FILE", "predict.csv")
    MAX_COMMENTS = int(os.getenv("MAX_COMMENTS", "500"))
    DEFAULT_BATCH_SIZE = int(os.getenv("BATCH_SIZE", "32"))
    LOG_DIR = os.getenv("LOG_DIR", "./logs")
    MODEL_SEARCH_DIR = os.getenv("MODEL_SEARCH_DIR", ".")

    # Validate required environment variables
    @classmethod
    def validate(cls):
        """Validate that required environment variables are set"""
        if not cls.API_KEY:
            raise ValueError("API_KEY environment variable is required")
        return True

    @classmethod
    def get_config_dict(cls) -> dict:
        """Get configuration as a dictionary"""
        return {
            "api_key": cls.API_KEY,
            "output_file": cls.DEFAULT_OUTPUT_FILE,
            "max_comments": cls.MAX_COMMENTS,
            "batch_size": cls.DEFAULT_BATCH_SIZE,
            "log_dir": cls.LOG_DIR,
            "model_search_dir": cls.MODEL_SEARCH_DIR,
        }
