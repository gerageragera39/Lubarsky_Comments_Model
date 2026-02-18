"""
Prediction Controller
Manages the interaction between GUI components and the prediction service.
"""

import os
from typing import Optional, Callable
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QWidget

from ..models.prediction_config import PredictionConfig
from ..models.prediction_result import PredictionBatch
from ..services.prediction_service import PredictionService
from ..utils.logging_utils import get_logger
from ..utils.video_utils import validate_youtube_url


class PredictionWorker(QThread):
    """
    Background worker for running predictions.

    Single Responsibility: Handles prediction execution in a separate thread.
    """

    progress = pyqtSignal(int, int)  # current, total
    finished = pyqtSignal(object)  # PredictionBatch
    error = pyqtSignal(str)  # error message

    def __init__(self, service: PredictionService, config: PredictionConfig):
        super().__init__()
        self.service = service
        self.config = config

    def run(self):
        """Execute prediction in background"""
        try:
            batch = self.service.predict(
                self.config,
                progress_callback=lambda c, t: self.progress.emit(c, t),
            )
            self.service.save_results(batch, self.config.output_file)
            self.finished.emit(batch)
        except Exception as e:
            self.error.emit(str(e))


class PredictionController(QObject):
    """
    Controller that manages the prediction workflow and UI interactions.

    This class follows the Single Responsibility Principle by coordinating
    the interaction between the GUI and the prediction service.
    """

    # Signals for GUI updates
    prediction_started = pyqtSignal()
    prediction_progress = pyqtSignal(int, int)  # current, total
    prediction_finished = pyqtSignal(object)  # PredictionBatch
    prediction_error = pyqtSignal(str)  # error message
    models_loaded = pyqtSignal(list)  # list of model paths

    def __init__(self, view: QWidget, api_key: str):
        super().__init__()
        self.view = view
        self.api_key = api_key
        self.logger = get_logger(self.__class__.__name__)
        self._service: Optional[PredictionService] = None
        self._worker: Optional[PredictionWorker] = None

    @property
    def service(self) -> PredictionService:
        """Lazy load prediction service"""
        if self._service is None:
            self._service = PredictionService(self.api_key)
        return self._service

    def load_models(self, search_dir: str = "."):
        """
        Find and load available trained models.

        Args:
            search_dir: Directory to search for models
        """
        try:
            models = self.service.find_models(search_dir)
            self.models_loaded.emit(models)
            self.logger.info(f"Found {len(models)} model(s)")
        except Exception as e:
            self.logger.error(f"Error loading models: {e}")
            self.models_loaded.emit([])

    def validate_inputs(self, model_path: str, video_url: str) -> tuple[bool, str]:
        """
        Validate user inputs before starting prediction.

        Args:
            model_path: Path to the model directory
            video_url: YouTube video URL

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not model_path:
            return False, "Please select a model"

        if not Path(model_path).exists():
            return False, f"Model path does not exist: {model_path}"

        is_valid, error = validate_youtube_url(video_url)
        if not is_valid:
            return False, error

        return True, ""

    def start_prediction(
        self,
        model_path: str,
        video_url: str,
        output_file: str = "predict.csv",
        max_comments: int = 500,
    ):
        """
        Start prediction process.

        Args:
            model_path: Path to the model directory
            video_url: YouTube video URL
            output_file: Output CSV file path
            max_comments: Maximum number of comments to fetch
        """
        # Validate inputs
        is_valid, error = self.validate_inputs(model_path, video_url)
        if not is_valid:
            self.prediction_error.emit(error)
            return

        # Create config
        config = PredictionConfig(
            model_path=model_path,
            video_url=video_url,
            output_file=output_file,
            max_comments=max_comments,
        )

        # Validate config
        is_valid, error = config.validate()
        if not is_valid:
            self.prediction_error.emit(error)
            return

        self.logger.info(f"Starting prediction with config: {config}")

        # Create and start worker
        self._worker = PredictionWorker(self.service, config)
        self._worker.progress.connect(self.prediction_progress)
        self._worker.finished.connect(self._on_prediction_finished)
        self._worker.error.connect(self.prediction_error)

        self.prediction_started.emit()
        self._worker.start()

    def _on_prediction_finished(self, batch: PredictionBatch):
        """Handle prediction completion"""
        self.logger.info(f"Prediction finished: {batch.total_comments} comments")
        self.prediction_finished.emit(batch)
        self._worker = None

    def cancel_prediction(self):
        """Cancel ongoing prediction"""
        if self._worker and self._worker.isRunning():
            self._worker.terminate()
            self._worker.wait()
            self._worker = None
            self.logger.info("Prediction cancelled")

    def select_model_file(self, start_dir: str = ".") -> Optional[str]:
        """
        Open file dialog to select a model directory.

        Args:
            start_dir: Starting directory for the dialog

        Returns:
            Selected model path or None
        """
        path = QFileDialog.getExistingDirectory(
            self.view,
            "Select Model Directory",
            start_dir,
            QFileDialog.Option.ShowDirsOnly,
        )
        if path:
            self.logger.info(f"Selected model: {path}")
        return path

    def select_output_file(self, start_dir: str = ".", default_name: str = "predict.csv") -> Optional[str]:
        """
        Open file dialog to select output CSV file.

        Args:
            start_dir: Starting directory for the dialog
            default_name: Default file name

        Returns:
            Selected file path or None
        """
        path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Save Predictions",
            os.path.join(start_dir, default_name),
            "CSV Files (*.csv)",
        )
        if path:
            self.logger.info(f"Selected output file: {path}")
        return path

    def show_error(self, message: str):
        """Show error message box"""
        QMessageBox.critical(self.view, "Prediction Error", message)
        self.logger.error(message)

    def show_success(self, message: str):
        """Show success message box"""
        QMessageBox.information(self.view, "Prediction Complete", message)
        self.logger.info(message)
