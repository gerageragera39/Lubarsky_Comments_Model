# Services Module

## Overview

The `services` module implements the **Service layer** of the application architecture. It contains the core business logic for model training, executing the fine-tuning process in a background thread while providing real-time feedback to the GUI.

## Architecture

This module follows multiple SOLID principles:
- **Single Responsibility Principle:** Each class handles a specific concern (stream redirection, callback handling, training execution)
- **Dependency Inversion Principle:** Services depend on abstractions (config objects) rather than concrete implementations
- **Interface Segregation:** Qt signals provide clean interfaces for cross-thread communication

## Files

### `__init__.py`

Package initialization file that exports service classes for external module access.

### `training_service.py`

**Purpose:** Implements the core training logic for ruBERT model fine-tuning.

**Key Classes:**

#### `StreamRedirector`

A custom stream wrapper that redirects Python's stdout/stderr to Qt signals for GUI display.

**Inheritance:** `io.StringIO`

**Purpose:** Captures console output from third-party libraries (transformers, sklearn) and redirects it to the GUI console.

**Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `signal` | `pyqtSignal` | Qt signal to emit captured text |
| `original` | `file-like` | Original stream to preserve (optional) |

**Methods:**
| Method | Description |
|--------|-------------|
| `write(text)` | Captures text, emits via signal, forwards to original stream |
| `flush()` | Flushes the original stream if present |

**Usage:**
```python
# Redirect stdout to Qt signal
sys.stdout = StreamRedirector(log_signal, original_stdout)
```

#### `GUITrainerCallback`

A HuggingFace `TrainerCallback` implementation that bridges the training loop with the GUI.

**Inheritance:** `TrainerCallback`

**Purpose:** Intercepts training events and emits them as Qt signals for real-time GUI updates.

**Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `signal_log` | `pyqtSignal(str)` | Signal for log messages |
| `signal_progress` | `pyqtSignal(int)` | Signal for progress updates |
| `signal_metrics` | `pyqtSignal(dict)` | Signal for metrics data |
| `_current_epoch` | `int` | Tracks current epoch number |

**Callback Methods:**

| Method | Trigger | Description |
|--------|---------|-------------|
| `on_epoch_begin()` | Start of each epoch | Logs epoch header with visual formatting |
| `on_log()` | Training log event | Emits training metrics (loss, learning rate) |
| `on_evaluate()` | Validation event | Emits validation metrics with formatted box |
| `on_step_end()` | Training step completion | Updates progress bar percentage |

**Output Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ▶  Эпоха 5 / 50
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  loss: 0.523456
  learning_rate: 0.000019

  ┌─────────── Validation ───────────┐
  │  eval_loss: 0.489123
  │  eval_accuracy: 0.847000
  │  eval_f1_macro: 0.832000
  └──────────────────────────────────┘
```

#### `TrainingService`

The main service class that orchestrates the entire training process.

**Inheritance:** `QThread`

**Purpose:** Executes model training in a background thread while maintaining GUI responsiveness.

**Signals:**

| Signal | Type | Description |
|--------|------|-------------|
| `log_signal` | `pyqtSignal(str)` | Training log messages |
| `progress_signal` | `pyqtSignal(int)` | Progress percentage (0-100) |
| `finished_signal` | `pyqtSignal(bool, str)` | Completion status and result path |
| `metrics_signal` | `pyqtSignal(object)` | Training metrics dictionary |

**Attributes:**
| Attribute | Type | Description |
|-----------|------|-------------|
| `config` | `TrainingConfig` | Training configuration |
| `_stop_requested` | `bool` | Graceful stop flag |
| `logger` | `logging.Logger` | Service logger |

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `request_stop()` | `None` | Sets stop flag for graceful termination |
| `run()` | `None` | Thread entry point, manages stream redirection |
| `_execute_training()` | `None` | Main training logic implementation |
| `_apply_freeze_strategy()` | `None` | Applies parameter freezing based on config |

**Training Pipeline:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Training Pipeline                        │
├─────────────────────────────────────────────────────────────┤
│  1. Load Dataset (pandas DataFrame from CSV)                │
│  2. Map Labels (-1,0,1 → 0,1,2)                             │
│  3. Stratified Split (80% train, 20% validation)            │
│  4. Convert to HuggingFace Datasets                         │
│  5. Load Tokenizer                                          │
│  6. Tokenize Datasets                                       │
│  7. Load Model (AutoModelForSequenceClassification)         │
│  8. Apply Freeze Strategy                                   │
│  9. Configure TrainingArguments                             │
│ 10. Initialize Trainer with Callbacks                       │
│ 11. Execute Training                                        │
│ 12. Save Best Model                                         │
└─────────────────────────────────────────────────────────────┘
```

**Freeze Strategies:**

| Mode | Implementation |
|------|----------------|
| `Только голова (classifier)` | Freeze all parameters, unfreeze classifier only |
| `Голова + последние N слоёв` | Freeze all, unfreeze classifier + last N encoder layers |
| `Без заморозки (full fine-tune)` | All parameters remain trainable |

**Label Mapping:**
```python
# Original labels → Model labels
-1 → 0  (Negative)
 0 → 1  (Neutral)
 1 → 2  (Positive)
```

**Metrics Computation:**
```python
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    accuracy = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, average="macro")
    return {"accuracy": acc, "f1_macro": f1}
```

**Callbacks Registered:**
1. `EarlyStoppingCallback` - Stops training if no improvement for `patience` epochs
2. `GUITrainerCallback` - Streams events to GUI
3. `StopCallback` - Checks for user stop request

**Error Handling:**

| Exception | Handling |
|-----------|----------|
| `FileNotFoundError` | User-friendly message, training aborted |
| `ValueError` | Invalid data/parameters message, training aborted |
| `Exception` | Full traceback logged, training aborted |

**Dependencies:**

| Library | Purpose |
|---------|---------|
| `pandas` | CSV loading and data manipulation |
| `sklearn` | Train/test split, metrics computation |
| `datasets` | HuggingFace dataset format |
| `transformers` | Tokenizer, model, training |
| `numpy` | Array operations for metrics |
| `PyQt6` | Threading and signals |

**Usage Example:**
```python
from services.training_service import TrainingService
from models.training_config import TrainingConfig

config = TrainingConfig(...)  # Configure parameters
service = TrainingService(config)

# Connect signals
service.log_signal.connect(on_log_message)
service.progress_signal.connect(on_progress_update)
service.finished_signal.connect(on_training_finished)
service.metrics_signal.connect(on_metrics_update)

# Start training
service.start()

# Stop training (optional)
service.request_stop()
```

## Design Patterns

- **Observer Pattern:** Qt signals notify GUI of training events
- **Strategy Pattern:** Different freeze strategies applied based on configuration
- **Template Method Pattern:** `TrainerCallback` hooks into specific training events
- **Decorator Pattern:** `StreamRedirector` wraps stdout/stderr
- **Command Pattern:** `request_stop()` encapsulates stop request

## Thread Safety

The service extends `QThread` to run training in a background thread. All GUI updates are performed through Qt signals, which are automatically marshaled to the main thread by Qt's event loop.

---

## TODO: Potential Improvements

- [ ] **TODO:** In `GUITrainerCallback.on_log()`, ALL float values in the logs dictionary are emitted as metrics, including `loss` and `learning_rate`. This causes the GUI to receive metrics that may not be relevant for display. Consider filtering to only emit `eval_*` metrics through `signal_metrics`, while sending all values to `signal_log`.

- [ ] **TODO:** The `StreamRedirector` class stores references to `original_stream`, but if an exception occurs during initialization before `old_stdout`/`old_stderr` are assigned in `run()`, the `finally` block may restore incorrect streams. Consider wrapping the stream assignment in a try-finally block immediately.

- [ ] **TODO:** The `StopCallback` class is defined inside `_execute_training()` method, making it inaccessible for testing. Extract it to a module-level class with proper unit tests.

- [ ] **TODO:** The label mapping `{-1: 0, 0: 1, 1: 2}` is hardcoded. This should be configurable or at least validated against the actual unique values in the dataset before mapping.

- [ ] **TODO:** The assertion `assert df[self.config.label_col].isin([0, 1, 2]).all()` will raise an unhandled `AssertionError` if labels are invalid. Replace with explicit validation and user-friendly error message.

- [ ] **TODO:** Consider adding GPU memory cleanup (`torch.cuda.empty_cache()`) after training completion for systems with limited VRAM.
