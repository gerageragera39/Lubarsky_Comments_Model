# YouTube Comment Classifier - Refactored

This is a refactored version of the YouTube Comment Classifier following SOLID principles and proper software architecture.

## Architecture Overview

The application is organized into several modules:

### 1. Configuration (`config.py`)
- Centralized configuration management
- Environment variable loading and validation

### 2. Data Models (`models.py`)
- Defines data structures for comments, videos, and sessions
- Uses dataclasses and enums for type safety

### 3. Utilities (`utils.py`)
- Helper functions for extracting video IDs and cleaning comments
- Pure functions with no side effects

### 4. API Client (`api_client.py`)
- Handles communication with YouTube API
- Responsible for fetching comments

### 5. Dataset Manager (`dataset_manager.py`)
- Manages the dataset CSV file
- Handles saving and retrieving classified comments

### 6. Session Manager (`session_manager.py`)
- Manages session state for resuming classification
- Handles saving and restoring progress

### 7. Controller (`classifier_controller.py`)
- Contains the business logic for comment classification
- Orchestrates the interaction between different components

### 8. GUI Constants (`gui_constants.py`)
- Defines colors, fonts, and key bindings
- Separates presentation concerns

### 9. GUI Application (`gui_app.py`)
- Implements the graphical user interface
- Follows MVC pattern by delegating business logic to the controller

## SOLID Principles Applied

1. **Single Responsibility Principle**: Each module has a single, well-defined responsibility.
2. **Open/Closed Principle**: Components are open for extension but closed for modification.
3. **Liskov Substitution Principle**: Interfaces are designed so derived classes can replace base classes.
4. **Interface Segregation Principle**: Small, focused interfaces rather than large, monolithic ones.
5. **Dependency Inversion Principle**: High-level modules don't depend on low-level modules; both depend on abstractions.

## Usage

Run the application with:

```bash
python -m data_hand_classifier.main
```

Make sure you have the required environment variables set in your `.env` file:

```env
API_KEY=your_youtube_api_key
DATASET_FILE=dataset.csv
MAX_COMMENTS=500
SESSION_FILE=session.json
```

## Dependencies

The application requires the following packages:

- `tkinter` (usually included with Python)
- `google-api-python-client`
- `emoji`
- `python-dotenv`