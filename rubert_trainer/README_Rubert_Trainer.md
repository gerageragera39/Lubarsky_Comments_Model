# ruBERT Trainer

**ruBERT Fine-Tuning Studio** — A professional desktop application for fine-tuning Russian BERT (ruBERT) models for text classification tasks.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![PyQt](https://img.shields.io/badge/PyQt-6.0-41CD52?style=flat&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

## 📖 Overview

ruBERT Trainer is a GUI-based application designed to simplify the process of fine-tuning pre-trained Russian language models from HuggingFace. It provides an intuitive interface for configuring training hyperparameters, monitoring training progress in real-time, and evaluating model performance.

### Key Features

- 🎯 **No Code Required** — Configure and run training through an intuitive GUI
- 📊 **Real-time Monitoring** — Live metrics dashboard showing loss, accuracy, and F1 scores
- 🧠 **Flexible Model Selection** — Support for any HuggingFace transformer model
- ❄️ **Parameter Freezing** — Multiple strategies for freezing/unfreezing model layers
- 🛑 **Early Stopping** — Automatic training termination when no improvement detected
- 📁 **Stratified Splitting** — Automatic 80/20 train/validation split with stratification
- 🎨 **Modern Dark Theme** — GitHub-inspired dark UI for comfortable extended use

## 🏗️ Architecture

The application follows the **MVC (Model-View-Controller)** architectural pattern with clean separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                         GUI Layer (View)                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  main_window.py │  │  metric_card.py │  │   (signals)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                      Controller Layer                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              training_controller.py                      │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                        Model Layer                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              training_config.py                          │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                      Service Layer                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              training_service.py                         │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                      Utility Layer                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  logging_utils  │  │   (future)      │  │   (future)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
rubert_trainer/
├── __main__.py              # Application entry point
├── setup.py                 # Package installation script
├── README.md                # This file
│
├── config/                  # Configuration management (planned)
│   ├── __init__.py
│   └── README.md
│
├── controllers/             # Controller layer (MVC)
│   ├── __init__.py
│   ├── training_controller.py
│   └── README.md
│
├── gui/                     # View layer (MVC) - User Interface
│   ├── __init__.py
│   ├── main_window.py       # Main application window
│   ├── metric_card.py       # Reusable metric display widget
│   └── README.md
│
├── models/                  # Model layer (MVC) - Data structures
│   ├── __init__.py
│   ├── training_config.py   # Configuration and metrics dataclasses
│   └── README.md
│
├── services/                # Service layer - Business logic
│   ├── __init__.py
│   ├── training_service.py  # Training execution engine
│   └── README.md
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── logging_utils.py     # Logging configuration
│   └── README.md
│
└── logs/                    # Generated log files (created at runtime)
```

## 📄 Root Files Description

| File | Purpose |
|------|---------|
| `__main__.py` | **Application Entry Point** — Initializes Qt application, sets up the dark theme palette, creates and displays the main window. Executed via `python -m rubert_trainer` |
| `setup.py` | **Package Installation** — Defines package metadata, dependencies, and installation configuration for pip installation |
| `README.md` | **Project Documentation** — This file containing project overview, installation instructions, and usage guide |

## 📦 Module Descriptions

### `config/` — Configuration Management

**Purpose:** Centralized configuration handling and presets.

**Status:** ⚠️ Under development — Currently a placeholder for future functionality.

**Planned Features:**
- Default configuration values
- YAML/JSON configuration file support
- Environment variable overrides
- Configuration presets (quick, standard, production)

📖 See [`config/README.md`](config/README.md) for details.

---

### `controllers/` — Controller Layer

**Purpose:** Coordinates user interactions and business logic execution.

**Key File:** `training_controller.py`

**Responsibilities:**
- File/directory selection dialogs
- Training configuration creation and validation
- Training lifecycle management (start/stop)
- Input validation before training initiation

**Main Class:** `TrainingController`

📖 See [`controllers/README.md`](controllers/README.md) for details.

---

### `gui/` — Graphical User Interface

**Purpose:** Provides the visual interface for the application.

**Key Files:**
- `main_window.py` — Main application window with all UI components
- `metric_card.py` — Reusable widget for displaying training metrics

**UI Components:**
- Dataset configuration panel (CSV path, column names)
- Model configuration panel (model name, max length, freeze strategy)
- Hyperparameters panel (learning rate, batch size, epochs, etc.)
- Real-time metrics dashboard (6 metric cards)
- Progress bar with gradient styling
- Console output panel with color-coded logs
- Start/Stop training controls

**Main Class:** `MainWindow`

📖 See [`gui/README.md`](gui/README.md) for details.

---

### `models/` — Data Models

**Purpose:** Defines data structures for configuration and metrics.

**Key File:** `training_config.py`

**Data Classes:**
- `TrainingConfig` — All training hyperparameters and settings
- `TrainingMetrics` — Training metrics collected during execution

**Validation:** Built-in parameter validation with constraints for each hyperparameter.

📖 See [`models/README.md`](models/README.md) for details.

---

### `services/` — Business Logic

**Purpose:** Implements core training functionality.

**Key File:** `training_service.py`

**Key Classes:**
- `TrainingService` — Main training orchestrator (extends `QThread`)
- `StreamRedirector` — Redirects stdout/stderr to GUI
- `GUITrainerCallback` — Bridges HuggingFace Trainer with Qt signals

**Training Pipeline:**
1. Load CSV dataset
2. Map labels (-1,0,1 → 0,1,2)
3. Stratified train/validation split (80/20)
4. Tokenize datasets
5. Load model and apply freeze strategy
6. Configure trainer with callbacks
7. Execute training with early stopping
8. Save best model

📖 See [`services/README.md`](services/README.md) for details.

---

### `utils/` — Utilities

**Purpose:** Shared utility functions across the application.

**Key File:** `logging_utils.py`

**Features:**
- Dual logging (console + file)
- Timestamped log files
- Automatic log directory creation
- Configurable log levels

**Classes:**
- `LoggerSetup` — Configures application logging
- `get_logger()` — Convenience function for obtaining loggers

📖 See [`utils/README.md`](utils/README.md) for details.

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/rubert_trainer.git
cd rubert_trainer

# Install dependencies
pip install -e .

# Or install dependencies manually
pip install pandas scikit-learn datasets transformers torch PyQt6
```

### Usage

```bash
# Run as module
python -m rubert_trainer

# Or run directly
python rubert_trainer/__main__.py
```

### Training Workflow

1. **Select Dataset** — Click "Обзор" to choose your CSV file
2. **Configure Columns** — Specify text and label column names
3. **Select Model** — Enter HuggingFace model (default: `ai-forever/ruBert-large`)
4. **Set Hyperparameters** — Configure learning rate, batch size, epochs, etc.
5. **Choose Freeze Strategy** — Select which layers to train
6. **Start Training** — Click "Начать обучение" and monitor progress

### Dataset Format

Your CSV file should contain:
- A text column with input text (e.g., comments, reviews)
- A label column with values: `-1` (negative), `0` (neutral), `1` (positive)

Example:
```csv
comment,target
"Отличный продукт!",1
"Ужасное качество",-1
"Нормально, ничего особенного",0
```

## 🎯 Training Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| Learning Rate | Optimizer learning rate | 2e-5 | 1e-7 – 1e-1 |
| Batch Size | Training batch size | 8 | 1 – 256 |
| Epochs | Number of training epochs | 50 | 1 – 500 |
| Max Length | Maximum token sequence length | 256 | 32 – 512 |
| Weight Decay | L2 regularization strength | 0.01 | 0 – 1 |
| Warmup Steps | LR warmup steps | 100 | 0 – 10000 |
| Patience | Early stopping patience | 20 | 1 – 100 |

## 📊 Metrics Dashboard

The application displays six real-time metrics:

| Metric | Description |
|--------|-------------|
| **LOSS** | Current training/validation loss |
| **ACCURACY** | Current evaluation accuracy |
| **F1 MACRO** | Current F1 macro score |
| **EPOCH** | Current epoch number |
| **MAX ACC** | Best accuracy achieved during training |
| **F1@MAX ACC** | F1 score at the epoch with best accuracy |

## 🛠️ Development

### Code Style

The project follows SOLID design principles:
- **Single Responsibility Principle** — Each class has one responsibility
- **Open/Closed Principle** — Open for extension, closed for modification
- **Dependency Inversion** — Depend on abstractions, not concretions

### Adding New Features

1. Create feature branch: `git checkout -b feature/your-feature`
2. Implement changes following existing patterns
3. Add documentation to relevant README.md
4. Submit pull request

## 📝 License

This project is licensed under the MIT License — see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

