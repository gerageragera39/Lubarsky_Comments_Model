"""
Training Configuration Models
Contains data classes for training configurations following SOLID principles.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TrainingConfig:
    """
    Represents the configuration for model training.
    
    This class follows the Single Responsibility Principle by encapsulating
    all training-related configuration parameters.
    """
    csv_path: str
    text_col: str
    label_col: str
    model_name: str
    max_len: int
    lr: float
    batch_size: int
    epochs: int
    weight_decay: float
    warmup_steps: int
    patience: int
    output_dir: str
    freeze_mode: str
    unfreeze_layers: int
    
    def validate(self) -> bool:
        """
        Validates the configuration parameters.
        
        :return: True if configuration is valid, False otherwise
        """
        if not self.csv_path or not self.text_col or not self.label_col:
            return False
        if self.max_len < 32 or self.max_len > 512:
            return False
        if self.lr <= 0 or self.lr >= 1:
            return False
        if self.batch_size <= 0 or self.batch_size > 256:
            return False
        if self.epochs <= 0 or self.epochs > 500:
            return False
        if self.patience <= 0 or self.patience > 100:
            return False
        if self.unfreeze_layers <= 0 or self.unfreeze_layers > 24:
            return False
        return True


@dataclass
class TrainingMetrics:
    """
    Represents training metrics collected during training.
    
    This class follows the Single Responsibility Principle by encapsulating
    all training metrics data.
    """
    loss: Optional[float] = None
    eval_loss: Optional[float] = None
    accuracy: Optional[float] = None
    eval_accuracy: Optional[float] = None
    f1_macro: Optional[float] = None
    eval_f1_macro: Optional[float] = None
    epoch: Optional[int] = None
    global_step: Optional[int] = None