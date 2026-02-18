"""
Prediction Service
Implements the core prediction logic following SOLID principles.
"""

import os
import csv
from typing import Optional, Callable
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from googleapiclient.discovery import build

from ..models.prediction_config import PredictionConfig
from ..models.prediction_result import PredictionResult, PredictionBatch
from ..utils.video_utils import extract_video_id
from ..utils.logging_utils import get_logger


class YouTubeCommentFetcher:
    """
    Fetches comments from YouTube videos.

    Single Responsibility: Handles only API communication for fetching comments.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.logger = get_logger(self.__class__.__name__)

    def fetch_comments(self, video_id: str, max_results: int = 500) -> list[str]:
        """
        Fetch comments from a YouTube video.

        Args:
            video_id: YouTube video ID
            max_results: Maximum number of comments to fetch

        Returns:
            List of comment texts
        """
        comments: list[str] = []
        next_page: Optional[str] = None

        while len(comments) < max_results:
            try:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(100, max_results - len(comments)),
                    pageToken=next_page,
                    textFormat="plainText",
                    order="relevance",
                )
                response = request.execute()

                for item in response["items"]:
                    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    comments.append(comment)

                next_page = response.get("nextPageToken")
                if not next_page:
                    break

            except Exception as e:
                self.logger.error(f"Error fetching comments: {e}")
                break

        self.logger.info(f"Fetched {len(comments)} comments for video {video_id}")
        return comments


class ModelPredictor:
    """
    Handles model loading and prediction.

    Single Responsibility: Handles only model inference operations.
    """

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.logger = get_logger(self.__class__.__name__)
        self._tokenizer: Optional[AutoTokenizer] = None
        self._model: Optional[AutoModelForSequenceClassification] = None
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger.info(f"Using device: {self._device}")

    @property
    def tokenizer(self) -> AutoTokenizer:
        """Lazy load tokenizer"""
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        return self._tokenizer

    @property
    def model(self) -> AutoModelForSequenceClassification:
        """Lazy load model"""
        if self._model is None:
            self._model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self._model.to(self._device)
            self._model.eval()
        return self._model

    def predict(self, texts: list[str], batch_size: int = 32) -> list[tuple[int, float]]:
        """
        Predict targets for a list of texts.

        Args:
            texts: List of texts to classify
            batch_size: Batch size for inference

        Returns:
            List of (target, confidence) tuples
        """
        results: list[tuple[int, float]] = []

        with torch.no_grad():
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                inputs = self.tokenizer(
                    batch_texts,
                    padding=True,
                    truncation=True,
                    max_length=512,
                    return_tensors="pt",
                )
                inputs = {k: v.to(self._device) for k, v in inputs.items()}

                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=-1)
                confidences, predictions = torch.max(probs, dim=-1)

                for pred, conf in zip(predictions.cpu().numpy(), confidences.cpu().numpy()):
                    results.append((int(pred), float(conf)))

        self.logger.info(f"Predicted {len(results)} texts")
        return results


class PredictionService:
    """
    Main prediction service coordinating comment fetching and model prediction.

    This class follows:
    - Single Responsibility: Coordinates prediction workflow
    - Dependency Inversion: Depends on abstractions (config objects)
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.logger = get_logger(self.__class__.__name__)
        self._comment_fetcher: Optional[YouTubeCommentFetcher] = None
        self._model_predictor: Optional[ModelPredictor] = None

    @property
    def comment_fetcher(self) -> YouTubeCommentFetcher:
        """Lazy load comment fetcher"""
        if self._comment_fetcher is None:
            self._comment_fetcher = YouTubeCommentFetcher(self.api_key)
        return self._comment_fetcher

    def predict(
        self,
        config: PredictionConfig,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> PredictionBatch:
        """
        Run prediction on comments from a YouTube video.

        Args:
            config: Prediction configuration
            progress_callback: Optional callback for progress updates (current, total)

        Returns:
            PredictionBatch with all results
        """
        self.logger.info(f"Starting prediction for video: {config.video_url}")

        # Extract video ID
        video_id = extract_video_id(config.video_url)
        if not video_id:
            raise ValueError(f"Invalid YouTube URL: {config.video_url}")

        # Fetch comments
        comments = self.comment_fetcher.fetch_comments(video_id, config.max_comments)
        if not comments:
            raise ValueError("No comments found for this video")

        if progress_callback:
            progress_callback(0, len(comments))

        # Load model and predict
        self._model_predictor = ModelPredictor(config.model_path)
        predictions = self._model_predictor.predict(comments, config.batch_size)

        # Create results
        results = [
            PredictionResult(comment=comment, target=target, confidence=confidence)
            for comment, (target, confidence) in zip(comments, predictions)
        ]

        batch = PredictionBatch(
            video_url=config.video_url,
            video_id=video_id,
            results=results,
            total_comments=len(comments),
        )

        if progress_callback:
            progress_callback(len(comments), len(comments))

        self.logger.info(f"Prediction completed: {len(results)} comments processed")
        return batch

    def save_results(self, batch: PredictionBatch, output_path: str):
        """
        Save prediction results to CSV file.

        Args:
            batch: Prediction batch to save
            output_path: Path to output CSV file
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        file_exists = path.exists()

        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["comment", "target", "confidence"])

            for result in batch.results:
                writer.writerow([result.comment, result.target, f"{result.confidence:.4f}"])

        self.logger.info(f"Results saved to {output_path}")

    def find_models(self, search_dir: str = ".") -> list[str]:
        """
        Find all trained model directories.

        Args:
            search_dir: Directory to search for models

        Returns:
            List of model directory paths
        """
        model_dirs: list[str] = []
        search_path = Path(search_dir)

        # Look for directories containing model files
        for pattern in ["**/config.json", "**/pytorch_model.bin", "**/model.safetensors"]:
            for file_path in search_path.glob(pattern):
                model_dir = str(file_path.parent)
                if model_dir not in model_dirs:
                    model_dirs.append(model_dir)

        return sorted(model_dirs)
