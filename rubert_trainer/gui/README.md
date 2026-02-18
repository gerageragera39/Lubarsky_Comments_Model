# GUI Module

## Overview

The `gui` module implements the **View layer** of the MVC (Model-View-Controller) architecture. It provides all user interface components for the ruBERT Fine-Tuning Studio application, including the main window, custom widgets, and visual styling.

## Architecture

This module follows the **Single Responsibility Principle** and **Separation of Concerns** from SOLID design patterns. Each GUI component is responsible for a specific visual element, ensuring modularity and reusability.

## Files

### `__init__.py`

Package initialization file that exports GUI classes for external module access.

### `main_window.py`

**Purpose:** Defines the main application window and coordinates all GUI components.

**Key Components:**

#### `Signals` Class

PyQt6 signal container for thread-safe communication between the training service thread and the GUI main thread.

| Signal | Type | Description |
|--------|------|-------------|
| `log_signal` | `pyqtSignal(str)` | Transfers log messages from training thread to console |
| `progress_signal` | `pyqtSignal(int)` | Updates progress bar percentage |
| `finished_signal` | `pyqtSignal(bool, str)` | Signals training completion with success status and message |
| `metrics_signal` | `pyqtSignal(dict)` | Transfers training metrics for real-time visualization |

#### `MainWindow` Class

The primary application window containing all UI elements.

**UI Sections:**

1. **Header Section**
   - Application title and subtitle
   - Visual separator

2. **Dataset Configuration Group**
   - CSV file path input with browse button
   - Text column name input
   - Label column name input

3. **Model Configuration Group**
   - HuggingFace model name input (default: `ai-forever/ruBert-large`)
   - Maximum sequence length spinner (32-512)
   - Freezing strategy dropdown
   - Number of layers to unfreeze spinner

4. **Hyperparameters Group**
   - Learning rate (1e-7 to 1e-1)
   - Batch size (1-256)
   - Number of epochs (1-500)
   - Weight decay (0-1)
   - Warmup steps (0-10000)
   - Early stopping patience (1-100)
   - Output directory with browse button

5. **Metrics Dashboard**
   - Six metric cards displaying real-time training metrics:
     - `LOSS` - Current training/validation loss
     - `ACCURACY` - Current evaluation accuracy
     - `F1 MACRO` - Current F1 macro score
     - `EPOCH` - Current epoch number
     - `MAX ACC` - Best accuracy achieved during training
     - `F1@MAX ACC` - F1 score at the epoch with best accuracy

6. **Progress & Control Section**
   - Progress bar (gradient styled)
   - Start training button
   - Stop training button

7. **Console Output**
   - Read-only text area with monospace font
   - Color-coded log messages
   - Real-time training output display

8. **Status Bar**
   - Current application state indicator

**Styling:**

The application uses a GitHub-inspired dark theme defined in the `STYLESHEET` constant:
- Background: `#0d1117` (GitHub dark)
- Primary accent: `#58a6ff` (GitHub blue)
- Success: `#3fb950` (GitHub green)
- Error: `#f85149` (GitHub red)
- Text: `#c9d1d9` (GitHub text)

**Key Methods:**

| Method | Description |
|--------|-------------|
| `setup_ui()` | Initializes all UI components and layouts |
| `connect_signals()` | Connects training service signals to slot handlers |
| `_start_training()` | Initiates training workflow |
| `_stop_training()` | Requests training termination |
| `_on_log()` | Handles incoming log messages |
| `_on_progress()` | Updates progress bar |
| `_on_metrics()` | Updates metric cards with new values |
| `_on_finished()` | Handles training completion |
| `_console_append()` | Appends colored text to console |

### `metric_card.py`

**Purpose:** Provides a reusable metric display widget.

#### `MetricCard` Class

A styled card component for displaying a single training metric.

**Properties:**
- `title` - Metric name (displayed in uppercase, small font)
- `value` - Metric value (displayed in large, bold font)
- `color` - Custom color for the value text

**Methods:**
| Method | Description |
|--------|-------------|
| `set_value(text)` | Updates the displayed metric value |

**Visual Design:**
- Card background: `#0d1117`
- Border: `#30363d` with 8px border radius
- Padding: 16px horizontal, 12px vertical
- Minimum width: 140px

## Dependencies

- **PyQt6:** Qt6 bindings for Python (QtWidgets, QtCore, QtGui)
- **TrainingController:** Controller layer for business logic
- **TrainingConfig:** Configuration model
- **LoggerSetup:** Logging configuration

## Design Patterns

- **MVC Pattern:** Clear separation between View (GUI), Controller, and Model
- **Observer Pattern:** Signal-slot mechanism for event handling
- **Composite Pattern:** Complex UI built from reusable components
- **Strategy Pattern:** Different freeze strategies selectable via dropdown

## Thread Safety

All GUI updates occur on the main Qt thread. The `Signals` class provides thread-safe communication with the background `TrainingService` thread through PyQt6's signal-slot mechanism.

---

## TODO: Potential Improvements

- [ ] **TODO:** In `_on_metrics()` method, the logic for tracking `max_f1_for_max_acc_epoch` may have a race condition - `eval_accuracy` and `eval_f1_macro` can arrive in separate metric dictionaries, potentially causing the F1 value at max accuracy to be incorrectly captured. Consider storing the last seen values of both metrics and updating the max tracking atomically.

- [ ] **TODO:** The lambda function in `_start_training()` for connecting `metrics_signal` is redundant:
  ```python
  self.training_service.metrics_signal.connect(lambda m: self.signals.metrics_signal.emit(m))
  ```
  This could be simplified to direct connection for better performance.

- [ ] **TODO:** Console color detection in `_console_append()` uses string matching which could be error-prone. Consider using explicit color parameters or an enum for message types.

- [ ] **TODO:** The `Signals` class is defined inside `main_window.py` but could be extracted to a separate `signals.py` file for better organization and reusability across modules.

- [ ] **TODO:** No input sanitization for text fields (CSV path, column names, model name). Consider adding validation feedback directly in the UI before attempting to start training.
