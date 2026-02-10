"""
Training Controller
Manages the interaction between GUI components and the training service.
"""

import os
from typing import Optional

from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox

from ..models.training_config import TrainingConfig
from ..services.training_service import TrainingService
from ..utils.logging_utils import get_logger


class TrainingController:
    """
    Controller that manages the training workflow and UI interactions.
    
    This class follows the Single Responsibility Principle by coordinating
    the interaction between the GUI and the training service.
    """
    
    def __init__(self, view: QWidget):
        self.view = view
        self.training_service: Optional[TrainingService] = None
        self.logger = get_logger(self.__class__.__name__)

    def browse_csv_file(self):
        """Open file dialog to select a CSV file."""
        self.logger.debug("Opening CSV file browser dialog")
        path, _ = QFileDialog.getOpenFileName(
            self.view, "Выберите CSV-файл", "", "CSV files (*.csv);;All (*)"
        )
        if path:
            self.logger.info(f"Selected CSV file: {path}")
            return path
        self.logger.debug("No CSV file selected")
        return None

    def browse_output_directory(self):
        """Open directory dialog to select an output directory."""
        self.logger.debug("Opening output directory browser dialog")
        path = QFileDialog.getExistingDirectory(self.view, "Выберите папку")
        if path:
            self.logger.info(f"Selected output directory: {path}")
            return path
        self.logger.debug("No output directory selected")
        return None

    def create_training_config(self, 
                              csv_path: str,
                              text_col: str,
                              label_col: str,
                              model_name: str,
                              max_len: int,
                              lr: float,
                              batch_size: int,
                              epochs: int,
                              weight_decay: float,
                              warmup_steps: int,
                              patience: int,
                              output_dir: str,
                              freeze_mode: str,
                              unfreeze_layers: int) -> TrainingConfig:
        """Create a training configuration object."""
        self.logger.debug(f"Creating training config with parameters: "
                         f"csv_path={csv_path}, text_col={text_col}, label_col={label_col}, "
                         f"model_name={model_name}, max_len={max_len}, lr={lr}, "
                         f"batch_size={batch_size}, epochs={epochs}, weight_decay={weight_decay}, "
                         f"warmup_steps={warmup_steps}, patience={patience}, output_dir={output_dir}, "
                         f"freeze_mode={freeze_mode}, unfreeze_layers={unfreeze_layers}")
        
        config = TrainingConfig(
            csv_path=csv_path,
            text_col=text_col,
            label_col=label_col,
            model_name=model_name,
            max_len=max_len,
            lr=lr,
            batch_size=batch_size,
            epochs=epochs,
            weight_decay=weight_decay,
            warmup_steps=warmup_steps,
            patience=patience,
            output_dir=output_dir,
            freeze_mode=freeze_mode,
            unfreeze_layers=unfreeze_layers
        )
        
        self.logger.info("Training configuration created successfully")
        return config

    def validate_config(self, config: TrainingConfig) -> bool:
        """Validate the training configuration."""
        is_valid = config.validate()
        self.logger.debug(f"Configuration validation result: {is_valid}")
        return is_valid

    def start_training(self, config: TrainingConfig):
        """Start the training process with the given configuration."""
        self.logger.info("Attempting to start training")
        
        if not self.validate_config(config):
            self.logger.warning("Training configuration is invalid")
            QMessageBox.warning(self.view, "Ошибка", "Некорректные параметры обучения")
            return

        if not config.csv_path or not os.path.isfile(config.csv_path):
            self.logger.error(f"CSV file does not exist: {config.csv_path}")
            QMessageBox.warning(self.view, "Ошибка", f"CSV-файл не найден:\n{config.csv_path}")
            return

        self.logger.info("Starting training service")
        self.training_service = TrainingService(config)
        return self.training_service

    def stop_training(self):
        """Request to stop the current training process."""
        if self.training_service and self.training_service.isRunning():
            self.logger.info("Requesting training to stop")
            self.training_service.request_stop()
            return True
        self.logger.debug("No active training service to stop")
        return False

    def is_training_running(self) -> bool:
        """Check if training is currently running."""
        is_running = self.training_service is not None and self.training_service.isRunning()
        self.logger.debug(f"Training running status: {is_running}")
        return is_running