"""
Prediction Result Model
Contains data classes for prediction results following SOLID principles.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class TargetLabel(Enum):
    """Target label enum for classification results"""
    NEGATIVE = 0
    NEUTRAL = 1
    POSITIVE = 2

    @classmethod
    def from_int(cls, value: int) -> "TargetLabel":
        """Convert integer to TargetLabel"""
        mapping = {0: cls.NEGATIVE, 1: cls.NEUTRAL, 2: cls.POSITIVE}
        return mapping.get(value, cls.NEUTRAL)

    @property
    def display_name(self) -> str:
        """Get display name for the label"""
        names = {
            TargetLabel.NEGATIVE: "Negative",
            TargetLabel.NEUTRAL: "Neutral",
            TargetLabel.POSITIVE: "Positive"
        }
        return names.get(self, "Unknown")


@dataclass
class PredictionResult:
    """
    Represents a single prediction result.

    This class follows the Single Responsibility Principle by encapsulating
    all data related to a single comment prediction.
    """
    comment: str
    target: int
    confidence: Optional[float] = None

    @property
    def target_label(self) -> TargetLabel:
        """Get the target as a TargetLabel enum"""
        return TargetLabel.from_int(self.target)

    @property
    def target_display(self) -> str:
        """Get the display name for the target"""
        return self.target_label.display_name


@dataclass
class PredictionBatch:
    """
    Represents a batch of prediction results.

    This class encapsulates a collection of prediction results
    along with metadata about the prediction session.
    """
    video_url: str
    video_id: str
    results: list[PredictionResult]
    total_comments: int = 0

    @property
    def summary(self) -> dict[str, int]:
        """Get summary statistics of predictions"""
        summary = {label.display_name: 0 for label in TargetLabel}
        for result in self.results:
            summary[result.target_display] += 1
        return summary
