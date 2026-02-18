# Controllers Module

## Overview

The `controllers` module implements the **Controller layer** of the MVC (Model-View-Controller) architecture. It serves as an intermediary between the GUI components (View) and the training service (Model), coordinating user interactions and business logic execution.

## Architecture

This module follows the **Single Responsibility Principle** from SOLID design patterns. Each controller is responsible for a specific domain of functionality, ensuring clean separation of concerns and maintainable code.

## Files

### `__init__.py`

Package initialization file that exports controller classes for external module access.

### `training_controller.py`

**Purpose:** Manages the training workflow and UI interactions for the ruBERT fine-tuning process.

**Key Responsibilities:**
- **File System Interactions:** Handles file and directory selection dialogs for CSV dataset and output path configuration
- **Configuration Management:** Creates and validates `TrainingConfig` objects from GUI input parameters
- **Training Lifecycle:** Initiates and controls the training process through the `TrainingService`
- **Input Validation:** Ensures all training parameters are valid before starting training

**Main Classes:**

#### `TrainingController`

| Method | Description |
|--------|-------------|
| `browse_csv_file()` | Opens file dialog for CSV dataset selection |
| `browse_output_directory()` | Opens directory dialog for output path selection |
| `create_training_config()` | Factory method creating `TrainingConfig` from GUI parameters |
| `validate_config()` | Validates training configuration parameters |
| `start_training()` | Initiates training process with validated configuration |
| `stop_training()` | Requests graceful termination of ongoing training |
| `is_training_running()` | Returns current training status |

**Integration Points:**
- **GUI (`../gui/main_window.py`):** Receives user input and triggers controller actions
- **Models (`../models/training_config.py`):** Creates configuration objects
- **Services (`../services/training_service.py`):** Manages training execution

**Usage Example:**
```python
controller = TrainingController(view_window)
config = controller.create_training_config(
    csv_path="dataset.csv",
    text_col="comment",
    label_col="target",
    model_name="ai-forever/ruBert-large",
    max_len=256,
    lr=2e-5,
    batch_size=8,
    epochs=50,
    weight_decay=0.01,
    warmup_steps=100,
    patience=20,
    output_dir="./output",
    freeze_mode="Head + Last N Layers",
    unfreeze_layers=3
)
if controller.validate_config(config):
    training_service = controller.start_training(config)
```

## Dependencies

- **PyQt6:** GUI framework for file dialogs and message boxes
- **TrainingConfig:** Configuration dataclass from models module
- **TrainingService:** Training execution service
- **Logging:** Application logging utilities

## Design Patterns

- **Controller Pattern:** Centralizes business logic and coordinates view-model interactions
- **Factory Method:** `create_training_config()` encapsulates object creation
- **Dependency Injection:** Controller receives view component via constructor

## Thread Safety

The controller operates on the main GUI thread. Long-running operations are delegated to `TrainingService` which executes in a separate thread via Qt's `QThread`.

---

## TODO: Potential Improvements

- [ ] **TODO:** Add file existence validation directly in `validate_config()` instead of separate check in `start_training()` - currently validation doesn't check if CSV file exists, which could lead to delayed error detection
- [ ] **TODO:** Consider implementing configuration persistence (save/load presets) for frequently used training parameters
- [ ] **TODO:** Add more granular validation error messages to help users identify specific invalid parameters
