# ruBERT Fine-Tuning Studio

Production GUI Application for fine-tuning ruBERT-large with hyperparameter tuning and built-in console output.

## Architecture

The application follows SOLID principles with a clean separation of concerns:

- **Models**: Data classes for training configurations
- **Services**: Core training logic implementation
- **Controllers**: Coordination between GUI and services
- **GUI**: User interface components
- **Utils**: Helper functions and utilities

## Modules

### Models
- `training_config.py`: Contains data classes for training configurations and metrics

### Services  
- `training_service.py`: Implements the core training logic in a separate thread

### Controllers
- `training_controller.py`: Manages interaction between GUI and training service

### GUI
- `main_window.py`: Main application window
- `metric_card.py`: Reusable widget for displaying metrics

### Utils
- `logging_utils.py`: Provides application logging functionality

## Features

- Configurable hyperparameters for fine-tuning
- Multiple freezing strategies for transfer learning
- Real-time training metrics visualization
- Progress tracking
- Built-in console output
- Error handling and logging

## Usage

Run the application with:

```bash
python -m rubert_trainer
```

Or install and run as a package:

```bash
pip install .
rubert-trainer
```