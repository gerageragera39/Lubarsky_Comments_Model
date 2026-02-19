# Comment Network

A comprehensive toolkit for YouTube comment analysis, including data collection, sentiment classification, and model training capabilities.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [YouTube Data API Key Setup](#youtube-data-api-key-setup)
- [Programs](#programs)
  - [Comment Classifier (GUI)](#1-comment-classifier---gui)
  - [Model Trainer](#2-model-trainer)
  - [Comment Predictor](#3-comment-predictor)
- [Building Executables](#building-executables)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## Overview

Comment Network provides three integrated tools for working with YouTube comments:

1. **Comment Classifier** – A graphical application to fetch, view, and manually label YouTube comments for sentiment (positive/neutral/negative)
2. **Model Trainer** – Train a custom sentiment classification model using your labeled dataset
3. **Comment Predictor** – Batch-predict sentiments for unlabeled comments using your trained model

---

## 📥 Download Pre-built Executables

Want to skip the setup? Download ready-to-use `.exe` files for all applications:

🔗 **[https://huggingface.co/herman3996/comments_classifier](https://huggingface.co/herman3996/comments_classifier)**

All executables are pre-built and ready to run—no installation required!

---

## Features

- 🎯 Fetch comments from any YouTube video via API
- 🏷️ Manual sentiment labeling with a user-friendly GUI
- 📊 Export labeled datasets for model training
- 🤖 Train custom RuBERT-based classification models
- 🔮 Batch prediction on unlabeled comment data
- 📦 Standalone executable builds for all tools

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/gerageragera39/Lubarsky_Comments_Model.git
   cd comment_network
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   copy .env-example .env    # Windows
   cp .env-example .env      # Linux/macOS
   ```

---

## YouTube Data API Key Setup

To fetch YouTube comments, you need a valid YouTube Data API v3 key. Follow these steps:

### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **New Project**
3. Enter a project name (e.g., "Comment Network")
4. Click **Create**

### Step 2: Enable the YouTube Data API v3

1. In the Google Cloud Console, navigate to **APIs & Services** → **Library**
2. Search for **"YouTube Data API v3"**
3. Click on it and press **Enable**

   🔗 Direct link: [YouTube Data API Overview](https://console.developers.google.com/apis/api/youtube.googleapis.com/overview)

### Step 3: Create API Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **API Key**
3. Copy the generated API key (looks like: `AIzaSy...`)

### Step 4: Configure the API Key (Recommended)

For security, restrict your API key:

1. Click the pencil icon next to your API key
2. Under **Application restrictions**, select your app type (e.g., Desktop app)
3. Under **API restrictions**, select **Restrict key** and choose **YouTube Data API v3**
4. Click **Save**

### Step 5: Add the API Key to Your Project

1. Open the `.env` file in the project root
2. Replace the placeholder with your actual API key:

   ```env
   API_KEY=YourActualKeyHere
   ```

> ⚠️ **Security Warning:** Never commit your `.env` file to version control. It is already listed in `.gitignore`.

---

## Programs

### 1. Comment Classifier (GUI)

**Entry Point:** `run_classifier.py`

A graphical user interface for fetching YouTube comments and labeling them with sentiment.

#### Features

- Fetch up to 500 comments from a YouTube video
- View comments in a clean, scrollable interface
- Label comments as **Positive (+1)**, **Neutral (0)**, or **Negative (-1)**
- Automatically saves labeled comments to `dataset.csv`
- Session tracking to avoid re-labeling

#### Usage

```bash
python run_classifier.py
```

#### Workflow

1. Enter a YouTube video URL
2. Click **Fetch Comments**
3. Review each comment and assign a sentiment label
4. Labeled data is saved to `dataset.csv`

---

### 2. Model Trainer

**Entry Point:** `run_trainer.py`

Trains a sentiment classification model using the RuBERT transformer architecture on your labeled dataset.

#### Features

- Fine-tunes RuBERT for Russian-language sentiment analysis
- Reads labeled data from `dataset.csv`
- Saves trained model to `rubert_trainer/model/`
- Generates training metrics and visualizations

#### Usage

```bash
python run_trainer.py
```

#### Requirements

- A labeled `dataset.csv` file with columns: `comment`, `target`
- Target values: `1` (positive), `0` (neutral), `-1` (negative)

#### Output

- Trained model files in `rubert_trainer/model/`
- Training history and metrics

---

### 3. Comment Predictor

**Entry Point:** `run_prediction.py`

Applies a trained model to predict sentiments for unlabeled comments.

#### Features

- Loads trained model from `rubert_trainer/model/`
- Reads unlabeled comments from `predict.csv`
- Outputs predictions to `result.csv`
- Supports batch processing

#### Usage

```bash
python run_prediction.py
```

#### Requirements

- Trained model in `rubert_trainer/model/`
- Input file `predict.csv` with a `comment` column

#### Output

- `result.csv` containing comments and predicted sentiments

---

## Building Executables

All three programs can be compiled into standalone `.exe` files using PyInstaller. Each program has a corresponding `.spec` file.

### Prerequisites

```bash
pip install pyinstaller
```

### Build Commands

#### 1. Build Comment Classifier

```bash
pyinstaller run_classifier.spec
```

**Output:**
- `dist/run_classifier/run_classifier.exe`
- `dist/run_classifier/_internal/` (dependencies)

**Includes:**
- `dataset.csv` (embedded)
- `.env` (embedded)

---

#### 2. Build Model Trainer

```bash
pyinstaller run_trainer.spec
```

**Output:**
- `dist/run_trainer/run_trainer.exe`
- `dist/run_trainer/_internal/` (dependencies)

---

#### 3. Build Comment Predictor

```bash
pyinstaller run_prediction.spec
```

**Output:**
- `dist/run_prediction/run_prediction.exe`
- `dist/run_prediction/_internal/` (dependencies)

---

### Distribution

To distribute the application:

1. Copy the entire folder from `dist/<program_name>/` (contains `.exe` + `_internal/`)
2. Ensure `.env` and `dataset.csv` are present (if not embedded)
3. Run the `.exe` file

> 📌 **Note:** The `_internal` folder is required. Do not separate it from the `.exe` file.

---

## Project Structure

```
comment_network/
├── .env                  # Environment variables (API key, paths)
├── .env-example          # Template for .env file
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── dataset.csv           # Labeled comments dataset
├── predict.csv           # Input for prediction
├── result.csv            # Prediction output
├── run_classifier.py     # GUI classifier entry point
├── run_classifier.spec   # PyInstaller spec for classifier
├── run_trainer.py        # Model trainer entry point
├── run_trainer.spec      # PyInstaller spec for trainer
├── run_prediction.py     # Predictor entry point
├── run_prediction.spec   # PyInstaller spec for predictor
├── data_hand_classifier/ # GUI classifier module
│   ├── gui_app.py        # Main GUI application
│   ├── dataset_manager.py# Dataset handling
│   ├── session_manager.py# Session tracking
│   └── config.py         # Configuration
├── rubert_trainer/       # Model training module
│   ├── __main__.py       # Trainer entry point
│   └── model/            # Trained model output
└── predictor/            # Prediction module
    ├── __main__.py       # Predictor entry point
    └── ...
```

---

## Troubleshooting

### Error: `FileNotFoundError: /app/dataset.csv`

**Cause:** The executable cannot find the dataset file.

**Solution:**
- Ensure `dataset.csv` exists in the project root before building
- The file is embedded during build; rebuild if missing

---

### Error: `API_KEY environment variable is required`

**Cause:** API key not configured in `.env`.

**Solution:**
1. Copy `.env-example` to `.env`
2. Add your YouTube API key:
   ```env
   API_KEY=YourKeyHere
   ```

---

### Error: `ModuleNotFoundError`

**Cause:** Missing dependencies.

**Solution:**
```bash
pip install -r requirements.txt
```

---

### Executable Won't Start

**Cause:** Missing `_internal` folder or antivirus blocking.

**Solution:**
- Ensure the `_internal` folder is in the same directory as the `.exe`
- Add an exception in your antivirus software

---

## License

This project is licensed under the MIT License.

---

## Support

For issues or questions, please open an issue on the [GitHub repository](<https://github.com/gerageragera39/Lubarsky_Comments_Model>).
