# GUI Module

## Overview

The `gui` module implements the **View layer** of the MVC (Model-View-Controller) architecture. It provides all user interface components for the YouTube Comment Predictor application, including the main window, custom widgets, and visual styling.

## Architecture

This module follows the **Single Responsibility Principle** and **Separation of Concerns** from SOLID design patterns. Each GUI component is responsible for a specific visual element, ensuring modularity and reusability.

## Files

### `__init__.py`

Package initialization file that exports GUI classes for external module access.

### `main_window.py`

**Purpose:** Defines the main application window and coordinates all GUI components.

**Stylesheet:**

The module includes a GitHub-inspired dark theme stylesheet (`STYLESHEET`) providing:
- Dark color scheme (#0d1117 background)
- Rounded corners on all elements
- Consistent spacing and padding
- Hover and focus states
- Custom scrollbar styling
- Table grid styling

**Key Components:**

#### `PredictionTable`

A custom `QTableWidget` for displaying prediction results.

**Features:**
- 4 columns: #, Comment, Target, Confidence
- Sortable columns (click header to sort)
- Color-coded target labels
- Auto-resizing columns
- Alternating row colors
- Single row selection

**Methods:**

| Method | Parameters | Description |
|--------|------------|-------------|
| `load_batch` | `batch: PredictionBatch` | Load predictions into table |
| `_get_target_color` | `target_label: TargetLabel` | Get color for label |

**Target Colors:**
- Negative: Red (#f85149)
- Neutral: Gray (#8b949e)
- Positive: Green (#3fb950)

#### `SummaryCard`

A card widget displaying prediction summary statistics.

**Features:**
- 4 summary labels: Negative, Neutral, Positive, Total
- Color-coded values
- Horizontal layout with spacers
- Card-style border

**Methods:**

| Method | Parameters | Description |
|--------|------------|-------------|
| `update_summary` | `summary: dict`, `total: int` | Update displayed values |

#### `MainWindow`

The main application window.

**UI Sections:**

1. **Header**
   - Title: "🎯 YouTube Comment Predictor"
   - Subtitle with description

2. **Model Selection Group**
   - Dropdown with discovered models
   - Browse button for manual selection

3. **Video URL Group**
   - Text input for YouTube URL
   - Placeholder text with example format

4. **Progress Group**
   - Progress bar (0-100%)
   - Status label with current operation

5. **Action Buttons**
   - Start Prediction (primary green)
   - Cancel (danger red)
   - Open Output File (secondary)

6. **Results Section**
   - Summary cards (top)
   - Sortable table (bottom)

**Signals Handled:**

| Signal | Source | Handler |
|--------|--------|---------|
| `models_loaded` | Controller | `_on_models_loaded` |
| `prediction_started` | Controller | `_on_prediction_started` |
| `prediction_progress` | Controller | `_on_prediction_progress` |
| `prediction_finished` | Controller | `_on_prediction_finished` |
| `prediction_error` | Controller | `_on_prediction_error` |

**User Actions:**

| Action | Handler | Description |
|--------|---------|-------------|
| Click Predict | `_on_predict_clicked` | Validate and start prediction |
| Click Cancel | `_on_cancel_clicked` | Cancel ongoing prediction |
| Click Browse | `_on_browse_model_clicked` | Select model directory |
| Click Open File | `_on_open_file_clicked` | Open predict.csv |

## Usage Example

```python
from predictor.gui.main_window import MainWindow, STYLESHEET
from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
app.setStyle("Fusion")
app.setStyleSheet(STYLESHEET)

window = MainWindow(api_key="your_api_key")
window.show()

sys.exit(app.exec())
```

## Styling Guidelines

All colors follow the GitHub dark theme:

| Purpose | Color |
|---------|-------|
| Background | #0d1117 |
| Card background | #161b22 |
| Input background | #010409 |
| Border | #30363d |
| Primary text | #c9d1d9 |
| Secondary text | #8b949e |
| Accent (link) | #58a6ff |
| Success | #3fb950 |
| Danger | #f85149 |
| Warning | #d29922 |
