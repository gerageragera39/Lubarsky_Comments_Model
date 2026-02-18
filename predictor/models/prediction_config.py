"""
Prediction Configuration Model
Contains data class for prediction configuration following SOLID principles.
"""

from dataclasses import dataclass


@dataclass
class PredictionConfig:
    """
    Represents the configuration for comment prediction.

    This class follows the Single Responsibility Principle by encapsulating
    all prediction-related configuration parameters.
    """
    model_path: str
    video_url: str
    output_file: str = "predict.csv"
    max_comments: int = 500
    batch_size: int = 32

    def validate(self) -> tuple[bool, str]:
        """
        Validate the configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.model_path:
            return False, "Model path is required"
        if not self.video_url:
            return False, "Video URL is required"
        if self.max_comments <= 0:
            return False, "Max comments must be positive"
        if self.batch_size <= 0:
            return False, "Batch size must be positive"
        return True, ""
