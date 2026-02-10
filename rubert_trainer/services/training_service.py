"""
Training Service
Implements the core training logic following SOLID principles.
"""

import os
import sys
import io
import traceback
from typing import Tuple, Optional, Dict, Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    TrainerCallback,
)

from PyQt6.QtCore import QThread, pyqtSignal

from ..models.training_config import TrainingConfig, TrainingMetrics
from ..utils.logging_utils import get_logger


class StreamRedirector(io.StringIO):
    """
    Redirects stdout/stderr to Qt signals.
    
    This class follows the Single Responsibility Principle by handling
    only the redirection of streams to GUI signals.
    """

    def __init__(self, signal, original_stream=None):
        super().__init__()
        self.signal = signal
        self.original = original_stream

    def write(self, text):
        if text and text.strip():
            self.signal.emit(text)
        if self.original:
            self.original.write(text)

    def flush(self):
        if self.original:
            self.original.flush()


class GUITrainerCallback(TrainerCallback):
    """
    Trainer callback that sends events to GUI through signals.
    
    This class follows the Single Responsibility Principle by handling
    only the communication between the trainer and the GUI.
    """

    def __init__(self, signal_log, signal_progress, signal_metrics):
        self.signal_log = signal_log
        self.signal_progress = signal_progress
        self.signal_metrics = signal_metrics
        self._current_epoch = 0

    def on_epoch_begin(self, args, state, control, **kw):
        self._current_epoch = int(state.epoch) + 1 if state.epoch is not None else 0
        self.signal_log.emit(
            f"\n{'━' * 60}\n"
            f"  ▶  Эпоха {self._current_epoch} / {int(args.num_train_epochs)}\n"
            f"{'━' * 60}"
        )

    def on_log(self, args, state, control, logs=None, **kw):
        if logs is None:
            return
        parts = []
        metrics_payload = {}
        for k, v in logs.items():
            if isinstance(v, float):
                parts.append(f"  {k}: {v:.6f}")
                metrics_payload[k] = v
            else:
                parts.append(f"  {k}: {v}")
        if parts:
            self.signal_log.emit("\n".join(parts))
        if metrics_payload:
            self.signal_metrics.emit(metrics_payload)

    def on_evaluate(self, args, state, control, metrics=None, **kw):
        if metrics is None:
            return
        self.signal_log.emit(
            f"\n  ┌─────────── Validation ───────────┐"
        )
        metrics_payload = {}
        for k, v in metrics.items():
            if isinstance(v, float):
                self.signal_log.emit(f"  │  {k}: {v:.6f}")
                metrics_payload[k] = v
            else:
                self.signal_log.emit(f"  │  {k}: {v}")
        self.signal_log.emit(f"  └──────────────────────────────────┘")
        if metrics_payload:
            self.signal_metrics.emit(metrics_payload)

    def on_step_end(self, args, state, control, **kw):
        if state.max_steps > 0:
            pct = int(state.global_step / state.max_steps * 100)
            self.signal_progress.emit(pct)


class TrainingService(QThread):
    """
    Service class that handles the model training process.
    
    This class follows the Single Responsibility Principle by managing
    only the training workflow and delegates other concerns to other classes.
    """
    
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    metrics_signal = pyqtSignal(object)  # Using object to pass dictionary

    def __init__(self, config: TrainingConfig):
        super().__init__()
        self.config = config
        self._stop_requested = False
        self.logger = get_logger(self.__class__.__name__)

    def request_stop(self):
        """Request the training to stop."""
        self._stop_requested = True

    def run(self):
        """Execute the training process in a separate thread."""
        self.logger.info("Starting training process")
        
        # Redirect stdout/stderr
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = StreamRedirector(self.log_signal, old_stdout)
        sys.stderr = StreamRedirector(self.log_signal, old_stderr)

        try:
            self.logger.info("Executing training...")
            self._execute_training()
            self.logger.info("Training completed successfully")
        except FileNotFoundError as e:
            error_msg = f"File not found: {str(e)}"
            self.logger.error(error_msg)
            self.log_signal.emit(f"\n❌ ОШИБКА: Файл не найден\n{error_msg}")
            self.finished_signal.emit(False, str(e))
        except ValueError as e:
            error_msg = f"Invalid value: {str(e)}"
            self.logger.error(error_msg)
            self.log_signal.emit(f"\n❌ ОШИБКА: Некорректное значение\n{error_msg}")
            self.finished_signal.emit(False, str(e))
        except Exception as e:
            tb = traceback.format_exc()
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            self.log_signal.emit(f"\n❌ ОШИБКА:\n{tb}")
            self.finished_signal.emit(False, str(e))
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            self.logger.info("Training process finished")

    def _execute_training(self):
        """Internal method to execute the training process."""
        SEED = 42
        self.logger.info(f"Starting training with config: {self.config}")
        
        self.log_signal.emit("📂  Загрузка датасета…")
        self.logger.debug(f"Loading dataset from: {self.config.csv_path}")
        
        df = pd.read_csv(self.config.csv_path)
        self.log_signal.emit(f"    Строк: {len(df)}")
        self.logger.info(f"Dataset loaded with {len(df)} rows")

        label_map = {-1: 0, 0: 1, 1: 2}
        df[self.config.label_col] = df[self.config.label_col].map(label_map)
        assert df[self.config.label_col].isin([0, 1, 2]).all(), "Неверные метки!"
        self.log_signal.emit("    Метки -1/0/1 → 0/1/2  ✔")
        self.logger.info("Labels mapped successfully")

        self.log_signal.emit("📊  Stratified split 80/20…")
        self.logger.debug("Performing stratified split")
        
        train_df, val_df = train_test_split(
            df, test_size=0.2, random_state=SEED, stratify=df[self.config.label_col]
        )
        self.log_signal.emit(f"    Train: {len(train_df)}  |  Val: {len(val_df)}")
        self.logger.info(f"Split completed: {len(train_df)} train, {len(val_df)} validation")

        train_ds = Dataset.from_pandas(train_df, preserve_index=False)
        val_ds = Dataset.from_pandas(val_df, preserve_index=False)

        self.log_signal.emit(f"🔤  Загрузка токенизатора: {self.config.model_name}")
        self.logger.debug(f"Loading tokenizer: {self.config.model_name}")
        
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)

        text_col = self.config.text_col
        max_len = self.config.max_len

        def tokenize(batch):
            return tokenizer(batch[text_col], truncation=True, max_length=max_len)

        self.log_signal.emit("    Токенизация…")
        self.logger.debug("Tokenizing datasets")
        
        train_ds = train_ds.map(tokenize, batched=True)
        val_ds = val_ds.map(tokenize, batched=True)

        train_ds = train_ds.rename_column(self.config.label_col, "labels")
        val_ds = val_ds.rename_column(self.config.label_col, "labels")

        train_ds.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
        val_ds.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
        self.log_signal.emit("    Токенизация  ✔")
        self.logger.info("Tokenization completed")

        self.log_signal.emit(f"🧠  Загрузка модели: {self.config.model_name}")
        self.logger.debug(f"Loading model: {self.config.model_name}")
        
        model = AutoModelForSequenceClassification.from_pretrained(
            self.config.model_name, num_labels=3
        )
        self.logger.info("Model loaded successfully")

        # Apply freezing strategy
        self._apply_freeze_strategy(model)

        trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total = sum(p.numel() for p in model.parameters())
        self.log_signal.emit(
            f"    Параметры: {trainable:,} обучаемых / {total:,} всего "
            f"({trainable / total * 100:.1f}%)"
        )
        self.logger.info(f"Model parameters: {trainable} trainable out of {total} total")

        # Metrics computation function
        def compute_metrics(eval_pred):
            logits, labels = eval_pred
            preds = np.argmax(logits, axis=-1)
            acc = accuracy_score(labels, preds)
            f1 = f1_score(labels, preds, average="macro")
            self.logger.debug(f"Computed metrics - Accuracy: {acc}, F1: {f1}")
            return {"accuracy": acc, "f1_macro": f1}

        # Training arguments
        self.logger.debug("Setting up training arguments")
        training_args = TrainingArguments(
            output_dir=self.config.output_dir,
            eval_strategy="epoch",
            save_strategy="epoch",
            learning_rate=self.config.lr,
            per_device_train_batch_size=self.config.batch_size,
            per_device_eval_batch_size=self.config.batch_size,
            num_train_epochs=self.config.epochs,
            weight_decay=self.config.weight_decay,
            warmup_steps=self.config.warmup_steps,
            logging_steps=50,
            load_best_model_at_end=True,
            metric_for_best_model="f1_macro",
            greater_is_better=True,
            seed=SEED,
            report_to="none",
        )

        gui_cb = GUITrainerCallback(
            self.log_signal, self.progress_signal, self.metrics_signal
        )

        # Custom callback for stopping
        class StopCallback(TrainerCallback):
            def __init__(self, training_service):
                self.training_service = training_service

            def on_step_end(self, args, state, control, **kw):
                if self.training_service._stop_requested:
                    self.training_service.logger.info("Stop requested, terminating training")
                    control.should_training_stop = True

        self.logger.info("Initializing trainer")
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=val_ds,
            data_collator=DataCollatorWithPadding(tokenizer),
            compute_metrics=compute_metrics,
            callbacks=[
                EarlyStoppingCallback(early_stopping_patience=self.config.patience),
                gui_cb,
                StopCallback(self),
            ],
        )

        self.log_signal.emit("\n🚀  Начало тренировки!\n")
        self.logger.info("Starting training process")
        
        trainer.train()

        if self._stop_requested:
            self.log_signal.emit("\n⚠️  Тренировка остановлена пользователем.")
            self.logger.info("Training stopped by user request")
            self.finished_signal.emit(False, "Остановлено пользователем")
            return

        self.progress_signal.emit(100)
        self.logger.info("Training completed, saving model")

        save_path = os.path.join(self.config.output_dir, "best")
        trainer.save_model(save_path)
        tokenizer.save_pretrained(save_path)
        self.log_signal.emit(f"\n💾  Модель сохранена: {save_path}")
        self.logger.info(f"Model saved to: {save_path}")
        
        self.log_signal.emit("\n✅  Тренировка завершена успешно!")
        self.logger.info("Training process completed successfully")
        
        self.finished_signal.emit(True, save_path)

    def _apply_freeze_strategy(self, model):
        """Apply the selected freezing strategy to the model."""
        if self.config.freeze_mode == "Только голова (classifier)":
            for param in model.parameters():
                param.requires_grad = False
            for param in model.classifier.parameters():
                param.requires_grad = True
            self.log_signal.emit("    🔒 Заморожено всё, кроме classifier head")

        elif self.config.freeze_mode == "Голова + последние N слоёв":
            for param in model.parameters():
                param.requires_grad = False
            for param in model.classifier.parameters():
                param.requires_grad = True
            n = self.config.unfreeze_layers
            encoder_layers = model.bert.encoder.layer
            for layer in encoder_layers[-n:]:
                for param in layer.parameters():
                    param.requires_grad = True
            self.log_signal.emit(
                f"    🔒 Заморожено всё, кроме classifier + последние {n} слоёв"
            )

        else:
            self.log_signal.emit("    🔓 Все параметры обучаемые (full fine-tune)")