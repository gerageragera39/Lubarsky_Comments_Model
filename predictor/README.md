# YouTube Comment Predictor

Production GUI Application for predicting sentiment of YouTube comments using trained ruBERT models.

## 📖 Overview

YouTube Comment Predictor is a GUI-based application designed to predict the sentiment of YouTube video comments using previously trained models. It provides an intuitive interface for selecting trained models, fetching comments from YouTube videos, and viewing prediction results in a sortable table.

### Key Features

- 🎯 **Model Selection** — Choose from any previously trained model directories
- 📊 **Real-time Progress** — Live progress bar showing prediction status
- 🎨 **Beautiful Dark Theme** — GitHub-inspired dark UI for comfortable use
- 📋 **Sortable Table** — PyCharm-like table with column sorting and color-coded labels
- 💾 **CSV Export** — Automatic saving of predictions to predict.csv
- 🔄 **Background Processing** — Non-blocking prediction in a separate thread

## 🏗️ Architecture

The application follows the **MVC (Model-View-Controller)** architectural pattern with clean separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                         GUI Layer                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  main_window.py (MainWindow, PredictionTable)           │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      Controller Layer                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  prediction_controller.py (PredictionController)        │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                       Service Layer                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  prediction_service.py (PredictionService,              │    │
│  │     YouTubeCommentFetcher, ModelPredictor)              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
predictor/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration management
├── models/
│   ├── __init__.py
│   ├── prediction_config.py    # PredictionConfig dataclass
│   └── prediction_result.py    # PredictionResult, PredictionBatch
├── services/
│   ├── __init__.py
│   └── prediction_service.py   # Core prediction logic
├── controllers/
│   ├── __init__.py
│   └── prediction_controller.py # UI coordination
├── gui/
│   ├── __init__.py
│   └── main_window.py          # Main window and widgets
└── utils/
    ├── __init__.py
    ├── logging_utils.py        # Logging configuration
    └── video_utils.py          # Video ID extraction

run_prediction.py               # Application entry point
run_prediction.spec             # PyInstaller specification
```

## 📦 Modules

### Models
- `prediction_config.py`: Contains `PredictionConfig` dataclass for prediction parameters
- `prediction_result.py`: Contains `PredictionResult`, `PredictionBatch`, and `TargetLabel` enum

### Services
- `prediction_service.py`: Implements core prediction logic with:
  - `YouTubeCommentFetcher`: Fetches comments via YouTube API
  - `ModelPredictor`: Handles model loading and inference
  - `PredictionService`: Coordinates the prediction workflow

### Controllers
- `prediction_controller.py`: Manages UI interactions and prediction workflow:
  - Input validation
  - Background worker management
  - File dialogs for model/output selection

### GUI
- `main_window.py`: Main application window with:
  - Model selection dropdown
  - YouTube URL input
  - Progress bar with status
  - Sortable results table
  - Summary cards with statistics

### Utils
- `logging_utils.py`: Application-wide logging configuration
- `video_utils.py`: YouTube URL validation and video ID extraction

## 🚀 Usage

### Running the Application

```bash
# Using Python directly
python run_prediction.py

# Or as a module
python -m predictor.gui.main_window
```

### Building Executable

```bash
# Using PyInstaller with the spec file
pyinstaller run_prediction.spec
```

The executable will be created in the `dist/` directory.

### Configuration

Create a `.env` file in the project root:

```env
API_KEY=your_youtube_api_key_here
OUTPUT_FILE=predict.csv
MAX_COMMENTS=500
BATCH_SIZE=32
LOG_DIR=./logs
MODEL_SEARCH_DIR=.
```

## 🎨 GUI Features

### Model Selection
- Dropdown with auto-discovered trained models
- Browse button to manually select model directories
- Models are discovered by searching for `config.json` and model files

### Video URL Input
- Supports all YouTube URL formats:
  - `https://www.youtube.com/watch?v=VIDEO_ID`
  - `https://youtu.be/VIDEO_ID`
  - `https://www.youtube.com/embed/VIDEO_ID`

### Results Table
- **Sortable Columns**: Click column headers to sort
- **Color-coded Labels**:
  - 🟢 Green: Positive
  - ⚪ Gray: Neutral
  - 🔴 Red: Negative
- **Confidence Scores**: Displayed as percentages
- **Alternating Row Colors**: For better readability

### Summary Cards
- Real-time statistics showing distribution of predictions
- Total comment count
- Count per sentiment category

## 📋 Output Format

The `predict.csv` file contains:

| comment | target | confidence |
|---------|--------|------------|
| Great video! | 2 | 0.9534 |
| It's okay | 1 | 0.7821 |
| Terrible content | 0 | 0.8912 |

Target values:
- `0`: Negative
- `1`: Neutral
- `2`: Positive

## 🔧 SOLID Principles

This application follows SOLID design principles:

### Single Responsibility Principle (SRP)
- Each class has one responsibility:
  - `YouTubeCommentFetcher`: Only fetches comments
  - `ModelPredictor`: Only handles model inference
  - `PredictionController`: Only coordinates UI and service
  - `MainWindow`: Only handles UI components

### Open/Closed Principle (OCP)
- Services can be extended without modifying existing code
- New prediction strategies can be added via inheritance

### Liskov Substitution Principle (LSP)
- Data classes can be substituted with derived types
- Service interfaces are consistent

### Interface Segregation Principle (ISP)
- Small, focused interfaces for each component
- No unnecessary dependencies

### Dependency Inversion Principle (DIP)
- Services depend on configuration objects, not concrete implementations
- Controller depends on abstractions

## 📝 Requirements

- Python 3.10+
- PyQt6
- transformers
- torch
- google-api-python-client
- python-dotenv

## 📄 License

MIT License
