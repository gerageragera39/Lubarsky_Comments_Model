# Controllers Module

## Overview

The `controllers` module implements the **Controller layer** of the MVC (Model-View-Controller) architecture. It serves as an intermediary between the GUI components (View) and the prediction service (Model), coordinating user interactions and business logic execution.

## Architecture

This module follows the **Single Responsibility Principle** from SOLID design patterns. Each controller is responsible for a specific domain of functionality, ensuring clean separation of concerns and maintainable code.

## Files

### `__init__.py`

Package initialization file that exports controller classes for external module access.

### `prediction_controller.py`

**Purpose:** Manages the prediction workflow and UI interactions for the comment prediction process.

**Key Responsibilities:**
- **File System Interactions:** Handles file and directory selection dialogs for model and output path configuration
- **Configuration Management:** Creates and validates `PredictionConfig` objects from GUI input parameters
- **Prediction Lifecycle:** Initiates and controls the prediction process through the `PredictionService`
- **Input Validation:** Ensures all prediction parameters are valid before starting prediction

**Main Classes:**

#### `PredictionWorker`

A `QThread` subclass that runs prediction in a background thread.

**Signals:**

| Signal | Type | Description |
|--------|------|-------------|
| `progress` | `pyqtSignal(int, int)` | Progress update (current, total) |
| `finished` | `pyqtSignal(object)` | Prediction completed with `PredictionBatch` |
| `error` | `pyqtSignal(str)` | Error occurred with error message |

**Methods:**

| Method | Description |
|--------|-------------|
| `run()` | Execute prediction in background thread |

#### `PredictionController`

Main controller coordinating GUI and service interaction.

**Signals:**

| Signal | Type | Description |
|--------|------|-------------|
| `prediction_started` | `pyqtSignal()` | Prediction process started |
| `prediction_progress` | `pyqtSignal(int, int)` | Progress update |
| `prediction_finished` | `pyqtSignal(object)` | Prediction completed |
| `prediction_error` | `pyqtSignal(str)` | Error occurred |
| `models_loaded` | `pyqtSignal(list)` | Models discovered |

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `view: QWidget`, `api_key: str` | - | Initialize controller |
| `load_models` | `search_dir: str` | - | Find and emit available models |
| `validate_inputs` | `model_path: str`, `video_url: str` | `tuple[bool, str]` | Validate user inputs |
| `start_prediction` | Various | - | Start prediction process |
| `cancel_prediction` | - | - | Cancel ongoing prediction |
| `select_model_file` | `start_dir: str` | `Optional[str]` | Open model selection dialog |
| `select_output_file` | `start_dir: str`, `default_name: str` | `Optional[str]` | Open save dialog |
| `show_error` | `message: str` | - | Show error message box |
| `show_success` | `message: str` | - | Show success message box |

## Usage Example

```python
from PyQt6.QtWidgets import QWidget
from predictor.controllers import PredictionController

# Create controller
view = QWidget()
controller = PredictionController(view, api_key="your_api_key")

# Connect signals
controller.models_loaded.connect(lambda models: print(f"Found {len(models)} models"))
controller.prediction_progress.connect(lambda c, t: print(f"{c}/{t}"))
controller.prediction_finished.connect(lambda batch: print(f"Done: {batch.total_comments}"))
controller.prediction_error.connect(lambda err: print(f"Error: {err}"))

# Load available models
controller.load_models(".")

# Start prediction
controller.start_prediction(
    model_path="./models/run_1",
    video_url="https://youtu.be/abc123",
    output_file="predict.csv",
    max_comments=500
)

# Cancel if needed
# controller.cancel_prediction()
```

## State Management

The controller maintains internal state for:
- Active prediction worker
- Service instance (lazy-loaded)
- Logger instance

## Error Handling

All errors are caught and emitted via the `prediction_error` signal. The controller also provides `show_error` and `show_success` methods for displaying messages to the user.
