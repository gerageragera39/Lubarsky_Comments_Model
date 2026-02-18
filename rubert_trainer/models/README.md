# Models Module

## Overview

The `models` module implements the **Model layer** of the MVC (Model-View-Controller) architecture. It defines the data structures and configuration objects used throughout the ruBERT Fine-Tuning Studio application.

## Architecture

This module follows the **Single Responsibility Principle** from SOLID design patterns. Each dataclass encapsulates a specific domain concept, ensuring clean data modeling and type safety.

## Files

### `__init__.py`

Package initialization file that exports model classes for external module access.

### `training_config.py`

**Purpose:** Defines data classes for training configuration and metrics storage.

**Key Classes:**

#### `TrainingConfig`

A dataclass that encapsulates all hyperparameters and settings required for model fine-tuning.

**Attributes:**

| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `csv_path` | `str` | Path to the training dataset CSV file | Must exist |
| `text_col` | `str` | Name of the column containing text data | Non-empty |
| `label_col` | `str` | Name of the column containing labels | Non-empty |
| `model_name` | `str` | HuggingFace model identifier | Valid HF model |
| `max_len` | `int` | Maximum token sequence length | 32-512 |
| `lr` | `float` | Learning rate for optimizer | 0 < lr < 1 |
| `batch_size` | `int` | Training batch size | 1-256 |
| `epochs` | `int` | Number of training epochs | 1-500 |
| `weight_decay` | `float` | L2 regularization strength | 0-1 |
| `warmup_steps` | `int` | Learning rate warmup steps | ≥ 0 |
| `patience` | `int` | Early stopping patience | 1-100 |
| `output_dir` | `str` | Directory for model checkpoints | Writable |
| `freeze_mode` | `str` | Parameter freezing strategy | See below |
| `unfreeze_layers` | `int` | Number of encoder layers to unfreeze | 1-24 |

**Freeze Modes:**

| Mode | Description |
|------|-------------|
| `"Только голова (classifier)"` | Freeze all parameters except classifier head |
| `"Голова + последние N слоёв"` | Freeze all except classifier + last N encoder layers |
| `"Без заморозки (full fine-tune)"` | All parameters are trainable |

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `validate()` | `bool` | Validates all configuration parameters against constraints |

**Validation Rules:**
```python
- csv_path, text_col, label_col: Must be non-empty
- max_len: 32 ≤ value ≤ 512
- lr: 0 < value < 1
- batch_size: 1 ≤ value ≤ 256
- epochs: 1 ≤ value ≤ 500
- patience: 1 ≤ value ≤ 100
- unfreeze_layers: 1 ≤ value ≤ 24
```

**Usage Example:**
```python
from models.training_config import TrainingConfig

config = TrainingConfig(
    csv_path="data/comments.csv",
    text_col="text",
    label_col="sentiment",
    model_name="ai-forever/ruBert-large",
    max_len=256,
    lr=2e-5,
    batch_size=8,
    epochs=50,
    weight_decay=0.01,
    warmup_steps=100,
    patience=20,
    output_dir="./models/output",
    freeze_mode="Голова + последние N слоёв",
    unfreeze_layers=3
)

if config.validate():
    print("Configuration is valid")
```

#### `TrainingMetrics`

A dataclass for storing training metrics collected during the training process.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `loss` | `float | None` | Current training loss |
| `eval_loss` | `float | None` | Current validation loss |
| `accuracy` | `float | None` | Current training accuracy |
| `eval_accuracy` | `float | None` | Current validation accuracy |
| `f1_macro` | `float | None` | Current training F1 macro score |
| `eval_f1_macro` | `float | None` | Current validation F1 macro score |
| `epoch` | `int | None` | Current epoch number |
| `global_step` | `int | None` | Current global training step |

**Usage:**
```python
from models.training_config import TrainingMetrics

metrics = TrainingMetrics(
    loss=0.523,
    eval_loss=0.489,
    eval_accuracy=0.847,
    eval_f1_macro=0.832,
    epoch=5,
    global_step=1250
)
```

## Dependencies

- **dataclasses:** Python standard library for dataclass decorators
- **typing:** Type hints for optional values

## Design Patterns

- **Data Class Pattern:** Immutable data containers with automatic method generation
- **Value Object Pattern:** Objects defined by their attributes rather than identity
- **Builder Pattern (implicit):** Configuration objects built incrementally before validation

## Integration Points

- **Controllers:** `TrainingController` creates `TrainingConfig` from GUI input
- **Services:** `TrainingService` consumes `TrainingConfig` and produces `TrainingMetrics`
- **GUI:** Metric cards display values from `TrainingMetrics`

## Data Flow

```
GUI Input → TrainingController → TrainingConfig → TrainingService
                                                    ↓
                                              TrainingMetrics
                                                    ↓
                                                 GUI Display
```

---

## TODO: Potential Improvements

- [ ] **TODO:** The `validate()` method does not check if `csv_path` actually exists on the filesystem. This validation is currently performed in `TrainingController.start_training()`, but moving it to the model would provide better encapsulation and earlier error detection.

- [ ] **TODO:** Consider adding a `__post_init__()` method to `TrainingConfig` for automatic validation upon object creation, ensuring that invalid configurations cannot be instantiated.

- [ ] **TODO:** The `freeze_mode` attribute uses Russian string literals which could cause issues in international environments. Consider using an Enum class:
  ```python
  from enum import Enum
  
  class FreezeMode(Enum):
      CLASSIFIER_ONLY = "classifier_only"
      CLASSIFIER_PLUS_N = "classifier_plus_n"
      FULL_FINETUNE = "full_finetune"
  ```

- [ ] **TODO:** Add field validators using a library like `pydantic` for more robust runtime validation and better error messages.

- [ ] **TODO:** The `TrainingMetrics` class could benefit from a method to compute derived metrics (e.g., improvement delta, best epoch tracking) rather than storing raw values only.
