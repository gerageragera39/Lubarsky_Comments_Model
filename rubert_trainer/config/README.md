# Config Module

## Overview

The `config` module is a placeholder for future configuration management functionality. It is designed to eventually contain configuration file parsers, default settings, and environment-based configuration handling.

## Current State

**Status:** ⚠️ **Under Development**

Currently, this module contains only the package initialization file:

### `__init__.py`

Package initialization file. Currently empty, reserved for future exports.

## Planned Functionality

The following features are planned for this module:

### 1. Default Configuration

A module or class providing sensible default values for training hyperparameters:

```python
# Planned API
from config.defaults import DEFAULT_CONFIG

DEFAULT_CONFIG = {
    "model_name": "ai-forever/ruBert-large",
    "max_len": 256,
    "lr": 2e-5,
    "batch_size": 8,
    "epochs": 50,
    "weight_decay": 0.01,
    "warmup_steps": 100,
    "patience": 20,
    "freeze_mode": "Голова + последние N слоёв",
    "unfreeze_layers": 3,
}
```

### 2. Configuration File Support

Support for loading configuration from external files (YAML, JSON, TOML):

```python
# Planned API
from config.loader import ConfigLoader

loader = ConfigLoader()
config = loader.from_yaml("config/training.yaml")
config = loader.from_json("config/training.json")
```

### 3. Environment Variable Support

Override configuration via environment variables:

```python
# Planned API
from config.env import apply_env_overrides

config = apply_env_overrides(config)
# Reads: RUBERT_MODEL_NAME, RUBERT_LR, RUBERT_BATCH_SIZE, etc.
```

### 4. Configuration Validation Schema

Centralized validation rules (potentially using Pydantic):

```python
# Planned API
from config.schema import TrainingConfigSchema

schema = TrainingConfigSchema()
validated_config = schema.validate(config_dict)
```

## Directory Structure (Planned)

```
config/
├── __init__.py          # Package init
├── defaults.py          # Default configuration values
├── loader.py            # Configuration file loaders
├── env.py               # Environment variable handling
├── schema.py            # Validation schemas
└── presets/             # Pre-defined configuration presets
    ├── quick.yaml       # Quick training (few epochs, small batch)
    ├── standard.yaml    # Standard training configuration
    └── production.yaml  # Production-grade training
```

## Example Configuration File (Planned)

```yaml
# config/presets/standard.yaml
model:
  name: "ai-forever/ruBert-large"
  max_length: 256

training:
  learning_rate: 0.00002
  batch_size: 8
  epochs: 50
  weight_decay: 0.01
  warmup_steps: 100
  early_stopping_patience: 20

freeze_strategy:
  mode: "classifier_plus_n"
  unfreeze_layers: 3

output:
  directory: "./models/output"
  save_best_only: true
  checkpoint_every: 1
```

---

## TODO: Potential Improvements

- [ ] **TODO:** Create `defaults.py` with a `DEFAULT_CONFIG` dictionary containing sensible default values for all training parameters. This would allow users to quickly start training without configuring every parameter.

- [ ] **TODO:** Implement configuration file loading using `pyyaml` for YAML support. This would enable users to save and share training configurations.

- [ ] **TODO:** Add environment variable override support following the Twelve-Factor App methodology. This would enable different configurations for development, staging, and production environments.

- [ ] **TODO:** Consider integrating with Pydantic for runtime configuration validation with detailed error messages. This would provide better user feedback for invalid configurations.

- [ ] **TODO:** Add support for configuration presets that users can load and customize. Common presets could include "quick_test", "standard", and "production" configurations.

- [ ] **TODO:** Implement configuration export functionality to save current GUI settings as a configuration file for reproducibility.
