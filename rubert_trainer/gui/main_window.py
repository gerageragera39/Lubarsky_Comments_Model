"""
Main Window
The primary GUI component for the ruBERT Fine-Tuning Studio.
"""

import os
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QProgressBar,
    QGroupBox,
    QFrame,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QSplitter,
    QMessageBox,
    QTextBrowser
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor, QTextCursor, QIcon, QPalette, QTextCharFormat

from .metric_card import MetricCard
from ..controllers.training_controller import TrainingController
from ..models.training_config import TrainingConfig
from ..utils.logging_utils import LoggerSetup


# Define custom signals class
class Signals(QObject):
    """Signals for communication between threads and GUI."""
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    metrics_signal = pyqtSignal(dict)


# Define styles
STYLESHEET = """
QMainWindow {
    background-color: #0d1117;
}

QWidget {
    color: #c9d1d9;
    font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
    font-size: 13px;
}

QGroupBox {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    margin-top: 14px;
    padding: 18px 14px 14px 14px;
    font-weight: 600;
    font-size: 14px;
    color: #58a6ff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    padding: 0 8px;
    background-color: #161b22;
    color: #58a6ff;
}

QLabel {
    color: #8b949e;
    font-size: 12px;
}

QLabel#titleLabel {
    color: #f0f6fc;
    font-size: 22px;
    font-weight: 700;
    padding: 4px 0;
}

QLabel#subtitleLabel {
    color: #8b949e;
    font-size: 13px;
    font-weight: 400;
}

QLabel#statusLabel {
    color: #8b949e;
    font-size: 13px;
    padding: 4px 8px;
}

QLabel#metricTitle {
    color: #8b949e;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
}

QLabel#metricValue {
    color: #f0f6fc;
    font-size: 28px;
    font-weight: 700;
}

QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px 12px;
    color: #c9d1d9;
    font-size: 13px;
    selection-background-color: #1f6feb;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border-color: #58a6ff;
    outline: none;
}

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background-color: #21262d;
    border: none;
    border-radius: 3px;
    width: 20px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #30363d;
}

QPushButton#primaryBtn {
    background-color: #238636;
    color: #ffffff;
    border: 1px solid #2ea043;
    border-radius: 8px;
    padding: 12px 32px;
    font-size: 15px;
    font-weight: 600;
    min-height: 20px;
}

QPushButton#primaryBtn:hover {
    background-color: #2ea043;
    border-color: #3fb950;
}

QPushButton#primaryBtn:pressed {
    background-color: #238636;
}

QPushButton#primaryBtn:disabled {
    background-color: #21262d;
    color: #484f58;
    border-color: #30363d;
}

QPushButton#dangerBtn {
    background-color: #da3633;
    color: #ffffff;
    border: 1px solid #f85149;
    border-radius: 8px;
    padding: 12px 32px;
    font-size: 15px;
    font-weight: 600;
    min-height: 20px;
}

QPushButton#dangerBtn:hover {
    background-color: #f85149;
}

QPushButton#dangerBtn:disabled {
    background-color: #21262d;
    color: #484f58;
    border-color: #30363d;
}

QPushButton#fileBtn {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#fileBtn:hover {
    background-color: #30363d;
    border-color: #8b949e;
}

QTextEdit#console {
    background-color: #0d1117;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
    font-family: 'Cascadia Code', 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 12px;
    selection-background-color: #1f6feb;
}

QProgressBar {
    background-color: #21262d;
    border: none;
    border-radius: 5px;
    height: 10px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1f6feb, stop:0.5 #58a6ff, stop:1 #79c0ff);
    border-radius: 5px;
}

QSplitter::handle {
    background-color: #30363d;
    height: 2px;
}

QFrame#separator {
    background-color: #30363d;
    max-height: 1px;
}

QFrame#metricCard {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
}
"""


class MainWindow(QMainWindow):
    """
    Main application window for the ruBERT Fine-Tuning Studio.
    
    This class follows the Single Responsibility Principle by managing
    only the main application window and its associated UI elements.
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize logging
        logger_setup = LoggerSetup()
        logger_setup.setup_logging()
        
        self.signals = Signals()
        self.controller = TrainingController(self)
        self.training_service = None
        
        # Variables to track maximum metrics during training
        self.max_accuracy = 0.0
        self.max_f1_for_max_acc_epoch = 0.0
        
        self.setup_ui()
        self.connect_signals()
        self._log_welcome()

    def setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("ruBERT Fine-Tuning Studio")
        self.setMinimumSize(960, 780)
        self.resize(1100, 860)

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(20, 16, 20, 16)
        root_layout.setSpacing(12)

        # Header
        header = QVBoxLayout()
        header.setSpacing(2)
        title = QLabel("🧠  ruBERT Fine-Tuning Studio")
        title.setObjectName("titleLabel")
        subtitle = QLabel(
            "Настройте гиперпараметры, выберите датасет и запустите обучение"
        )
        subtitle.setObjectName("subtitleLabel")
        header.addWidget(title)
        header.addWidget(subtitle)
        root_layout.addLayout(header)

        # Separator
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        root_layout.addWidget(sep)

        # Content splitter
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(6)

        # Top section: settings
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)

        # Row 1: Dataset + Model
        row1 = QHBoxLayout()
        row1.setSpacing(12)

        # Dataset group
        ds_group = QGroupBox("📁  Датасет")
        ds_grid = QGridLayout(ds_group)
        ds_grid.setHorizontalSpacing(10)
        ds_grid.setVerticalSpacing(8)

        ds_grid.addWidget(QLabel("CSV-файл:"), 0, 0)
        self.csv_edit = QLineEdit("dataset.csv")
        self.csv_edit.setPlaceholderText("Путь к CSV-файлу")
        self.csv_browse_btn = QPushButton("Обзор…")
        self.csv_browse_btn.setObjectName("fileBtn")
        self.csv_browse_btn.clicked.connect(self._browse_csv)
        ds_grid.addWidget(self.csv_edit, 0, 1)
        ds_grid.addWidget(self.csv_browse_btn, 0, 2)

        ds_grid.addWidget(QLabel("Колонка текста:"), 1, 0)
        self.text_col_edit = QLineEdit("comment")
        ds_grid.addWidget(self.text_col_edit, 1, 1, 1, 2)

        ds_grid.addWidget(QLabel("Колонка метки:"), 2, 0)
        self.label_col_edit = QLineEdit("target")
        ds_grid.addWidget(self.label_col_edit, 2, 1, 1, 2)

        row1.addWidget(ds_group, stretch=3)

        # Model group
        mdl_group = QGroupBox("🤖  Модель")
        mdl_grid = QGridLayout(mdl_group)
        mdl_grid.setHorizontalSpacing(10)
        mdl_grid.setVerticalSpacing(8)

        mdl_grid.addWidget(QLabel("Модель HF:"), 0, 0)
        self.model_edit = QLineEdit("ai-forever/ruBert-large")
        mdl_grid.addWidget(self.model_edit, 0, 1)

        mdl_grid.addWidget(QLabel("Max length:"), 1, 0)
        self.maxlen_spin = QSpinBox()
        self.maxlen_spin.setRange(32, 512)
        self.maxlen_spin.setValue(256)
        self.maxlen_spin.setSingleStep(32)
        mdl_grid.addWidget(self.maxlen_spin, 1, 1)

        mdl_grid.addWidget(QLabel("Заморозка:"), 2, 0)
        self.freeze_combo = QComboBox()
        self.freeze_combo.addItems([
            "Голова + последние N слоёв",
            "Только голова (classifier)",
            "Без заморозки (full fine-tune)",
        ])
        self.freeze_combo.currentIndexChanged.connect(self._on_freeze_changed)
        mdl_grid.addWidget(self.freeze_combo, 2, 1)

        mdl_grid.addWidget(QLabel("Разморозить слоёв:"), 3, 0)
        self.unfreeze_spin = QSpinBox()
        self.unfreeze_spin.setRange(1, 24)
        self.unfreeze_spin.setValue(3)
        mdl_grid.addWidget(self.unfreeze_spin, 3, 1)

        row1.addWidget(mdl_group, stretch=2)
        top_layout.addLayout(row1)

        # Row 2: Hyperparams
        hp_group = QGroupBox("⚙️  Гиперпараметры")
        hp_grid = QGridLayout(hp_group)
        hp_grid.setHorizontalSpacing(16)
        hp_grid.setVerticalSpacing(8)

        # Learning rate
        hp_grid.addWidget(QLabel("Learning rate:"), 0, 0)
        self.lr_spin = QDoubleSpinBox()
        self.lr_spin.setDecimals(7)
        self.lr_spin.setRange(1e-7, 1e-1)
        self.lr_spin.setSingleStep(1e-6)
        self.lr_spin.setValue(2e-5)
        hp_grid.addWidget(self.lr_spin, 0, 1)

        # Batch size
        hp_grid.addWidget(QLabel("Batch size:"), 0, 2)
        self.bs_spin = QSpinBox()
        self.bs_spin.setRange(1, 256)
        self.bs_spin.setValue(8)
        self.bs_spin.setSingleStep(2)
        hp_grid.addWidget(self.bs_spin, 0, 3)

        # Epochs
        hp_grid.addWidget(QLabel("Epochs:"), 0, 4)
        self.epochs_spin = QSpinBox()
        self.epochs_spin.setRange(1, 500)
        self.epochs_spin.setValue(50)
        hp_grid.addWidget(self.epochs_spin, 0, 5)

        # Weight decay
        hp_grid.addWidget(QLabel("Weight decay:"), 1, 0)
        self.wd_spin = QDoubleSpinBox()
        self.wd_spin.setDecimals(5)
        self.wd_spin.setRange(0, 1)
        self.wd_spin.setSingleStep(0.001)
        self.wd_spin.setValue(0.01)
        hp_grid.addWidget(self.wd_spin, 1, 1)

        # Warmup steps
        hp_grid.addWidget(QLabel("Warmup steps:"), 1, 2)
        self.warmup_spin = QSpinBox()
        self.warmup_spin.setRange(0, 10000)
        self.warmup_spin.setValue(100)
        self.warmup_spin.setSingleStep(50)
        hp_grid.addWidget(self.warmup_spin, 1, 3)

        # Early stopping patience
        hp_grid.addWidget(QLabel("ES patience:"), 1, 4)
        self.patience_spin = QSpinBox()
        self.patience_spin.setRange(1, 100)
        self.patience_spin.setValue(20)
        hp_grid.addWidget(self.patience_spin, 1, 5)

        # Output dir
        hp_grid.addWidget(QLabel("Output dir:"), 2, 0)
        self.outdir_edit = QLineEdit("./rubert_cls")
        hp_grid.addWidget(self.outdir_edit, 2, 1, 1, 3)
        self.outdir_btn = QPushButton("Обзор…")
        self.outdir_btn.setObjectName("fileBtn")
        self.outdir_btn.clicked.connect(self._browse_outdir)
        hp_grid.addWidget(self.outdir_btn, 2, 4, 1, 2)

        top_layout.addWidget(hp_group)

        # Metric cards
        metrics_row = QHBoxLayout()
        metrics_row.setSpacing(10)
        self.card_loss = MetricCard("LOSS", "—", "#f85149")
        self.card_acc = MetricCard("ACCURACY", "—", "#3fb950")
        self.card_f1 = MetricCard("F1 MACRO", "—", "#d2a8ff")
        self.card_epoch = MetricCard("EPOCH", "—", "#79c0ff")
        # Additional cards for max metrics
        self.card_max_acc = MetricCard("MAX ACC", "—", "#a371f7")
        self.card_max_f1_for_max_acc = MetricCard("F1@MAX ACC", "—", "#7ee787")
        
        metrics_row.addWidget(self.card_loss)
        metrics_row.addWidget(self.card_acc)
        metrics_row.addWidget(self.card_f1)
        metrics_row.addWidget(self.card_epoch)
        metrics_row.addWidget(self.card_max_acc)
        metrics_row.addWidget(self.card_max_f1_for_max_acc)
        top_layout.addLayout(metrics_row)

        # Progress bar + buttons
        bar_row = QHBoxLayout()
        bar_row.setSpacing(12)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        bar_row.addWidget(self.progress, stretch=1)

        self.start_btn = QPushButton("▶  Начать обучение")
        self.start_btn.setObjectName("primaryBtn")
        self.start_btn.clicked.connect(self._start_training)
        bar_row.addWidget(self.start_btn)

        self.stop_btn = QPushButton("■  Остановить")
        self.stop_btn.setObjectName("dangerBtn")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._stop_training)
        bar_row.addWidget(self.stop_btn)

        top_layout.addLayout(bar_row)

        splitter.addWidget(top_widget)

        # Bottom section: console
        console_group = QGroupBox("🖥  Консоль")
        console_layout = QVBoxLayout(console_group)
        console_layout.setContentsMargins(8, 12, 8, 8)

        self.console = QTextEdit()
        self.console.setObjectName("console")
        self.console.setReadOnly(True)
        console_layout.addWidget(self.console)

        splitter.addWidget(console_group)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        root_layout.addWidget(splitter, stretch=1)

        # Status bar
        self.status_lbl = QLabel("Готов к работе")
        self.status_lbl.setObjectName("statusLabel")
        root_layout.addWidget(self.status_lbl)

    def connect_signals(self):
        """Connect signals to their respective handlers."""
        self.signals.log_signal.connect(self._on_log)
        self.signals.progress_signal.connect(self._on_progress)
        self.signals.finished_signal.connect(self._on_finished)
        self.signals.metrics_signal.connect(self._on_metrics)

    def _log_welcome(self):
        """Display welcome message in console."""
        self._console_append(
            "╔══════════════════════════════════════════════════════╗\n"
            "║         ruBERT Fine-Tuning Studio v1.0              ║\n"
            "║   Настройте параметры и нажмите «Начать обучение»   ║\n"
            "╚══════════════════════════════════════════════════════╝\n",
            color="#58a6ff",
        )

    def _console_append(self, text: str, color: str = None):
        """Append text to the console with optional coloring."""
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        fmt = QTextCharFormat()
        if color:
            fmt.setForeground(QColor(color))
        else:
            # Color based on content
            if any(sym in text for sym in ("✔", "✅", "💾")):
                fmt.setForeground(QColor("#3fb950"))
            elif any(sym in text for sym in ("❌", "⚠️")):
                fmt.setForeground(QColor("#f85149"))
            elif any(sym in text for sym in ("▶", "🚀")):
                fmt.setForeground(QColor("#d2a8ff"))
            elif text.strip().startswith("━") or text.strip().startswith("┌") or text.strip().startswith("└"):
                fmt.setForeground(QColor("#6e7681"))
            else:
                fmt.setForeground(QColor("#c9d1d9"))
        cursor.setCharFormat(fmt)
        cursor.insertText(text + "\n")
        self.console.setTextCursor(cursor)
        self.console.ensureCursorVisible()

    def _on_freeze_changed(self, idx):
        """Handle freeze mode change."""
        # Show unfreeze spin only if "Head + N layers" is selected
        self.unfreeze_spin.setEnabled(idx == 0)

    def _browse_csv(self):
        """Browse for CSV file."""
        path = self.controller.browse_csv_file()
        if path:
            self.csv_edit.setText(path)

    def _browse_outdir(self):
        """Browse for output directory."""
        path = self.controller.browse_output_directory()
        if path:
            self.outdir_edit.setText(path)

    def _set_controls_enabled(self, enabled: bool):
        """Enable/disable controls based on training state."""
        for w in (
            self.csv_edit,
            self.csv_browse_btn,
            self.text_col_edit,
            self.label_col_edit,
            self.model_edit,
            self.maxlen_spin,
            self.freeze_combo,
            self.unfreeze_spin,
            self.lr_spin,
            self.bs_spin,
            self.epochs_spin,
            self.wd_spin,
            self.warmup_spin,
            self.patience_spin,
            self.outdir_edit,
            self.outdir_btn,
        ):
            w.setEnabled(enabled)
        self.start_btn.setEnabled(enabled)
        self.stop_btn.setEnabled(not enabled)

    def _start_training(self):
        """Start the training process."""
        csv_path = self.csv_edit.text().strip()
        if not csv_path or not os.path.isfile(csv_path):
            QMessageBox.warning(self, "Ошибка", f"CSV-файл не найден:\n{csv_path}")
            return

        self.console.clear()
        self._log_welcome()
        self.progress.setValue(0)
        self.card_loss.set_value("—")
        self.card_acc.set_value("—")
        self.card_f1.set_value("—")
        self.card_epoch.set_value("—")
        self.card_max_acc.set_value("—")
        self.card_max_f1_for_max_acc.set_value("—")
        
        # Reset max metrics tracking
        self.max_accuracy = 0.0
        self.max_f1_for_max_acc_epoch = 0.0

        self._set_controls_enabled(False)
        self.status_lbl.setText("⏳  Тренировка запущена…")

        self._console_append(
            f"  Параметры:\n"
            f"    lr={self.lr_spin.value():.2e}  batch={self.bs_spin.value()}  "
            f"epochs={self.epochs_spin.value()}\n"
            f"    weight_decay={self.wd_spin.value():.4f}  "
            f"warmup={self.warmup_spin.value()}  patience={self.patience_spin.value()}\n"
            f"    freeze={self.freeze_combo.currentText()}\n",
            color="#8b949e",
        )

        # Create training config
        config = self.controller.create_training_config(
            csv_path=csv_path,
            text_col=self.text_col_edit.text().strip(),
            label_col=self.label_col_edit.text().strip(),
            model_name=self.model_edit.text().strip(),
            max_len=self.maxlen_spin.value(),
            lr=self.lr_spin.value(),
            batch_size=self.bs_spin.value(),
            epochs=self.epochs_spin.value(),
            weight_decay=self.wd_spin.value(),
            warmup_steps=self.warmup_spin.value(),
            patience=self.patience_spin.value(),
            output_dir=self.outdir_edit.text().strip(),
            freeze_mode=self.freeze_combo.currentText(),
            unfreeze_layers=self.unfreeze_spin.value(),
        )

        # Start training
        self.training_service = self.controller.start_training(config)
        
        # Connect signals
        if self.training_service:
            self.training_service.log_signal.connect(self.signals.log_signal.emit)
            self.training_service.progress_signal.connect(self.signals.progress_signal.emit)
            self.training_service.finished_signal.connect(self.signals.finished_signal.emit)
            # Pass metrics as object since we're using object type for the signal
            self.training_service.metrics_signal.connect(lambda m: self.signals.metrics_signal.emit(m))
            self.training_service.start()

    def _stop_training(self):
        """Stop the training process."""
        if self.controller.stop_training():
            self.stop_btn.setEnabled(False)
            self.status_lbl.setText("⏳  Останавливаем…")
            self._console_append("\n⏳  Запрошена остановка, ждём завершения шага…", color="#f0883e")

    def _on_log(self, text: str):
        """Handle log messages."""
        self._console_append(text)

    def _on_progress(self, value: int):
        """Handle progress updates."""
        self.progress.setValue(value)

    def _on_metrics(self, metrics: dict):
        """Handle metrics updates."""
        # Update cards
        if "loss" in metrics:
            self.card_loss.set_value(f"{metrics['loss']:.4f}")
        if "eval_loss" in metrics:
            self.card_loss.set_value(f"{metrics['eval_loss']:.4f}")
        if "eval_accuracy" in metrics:
            accuracy = metrics['eval_accuracy']
            self.card_acc.set_value(f"{accuracy:.2%}")
            
            # Update max accuracy if current is higher
            if accuracy > self.max_accuracy:
                self.max_accuracy = accuracy
                self.card_max_acc.set_value(f"{self.max_accuracy:.2%}")
                
                # Also update the F1 value that corresponds to the max accuracy epoch
                if "eval_f1_macro" in metrics:
                    self.max_f1_for_max_acc_epoch = metrics['eval_f1_macro']
                    self.card_max_f1_for_max_acc.set_value(f"{self.max_f1_for_max_acc_epoch:.4f}")
        if "eval_f1_macro" in metrics:
            f1_value = metrics['eval_f1_macro']
            self.card_f1.set_value(f"{f1_value:.4f}")
        if "epoch" in metrics:
            self.card_epoch.set_value(f"{int(metrics['epoch'])}")

    def _on_finished(self, success: bool, msg: str):
        """Handle training completion."""
        self._set_controls_enabled(True)
        if success:
            self.status_lbl.setText(f"✅  Готово! Модель: {msg}")
            self.progress.setValue(100)
            # Optionally show final max metrics in status
            self._console_append(f"\n📈  ИТОГОВЫЕ МЕТРИКИ: Max Accuracy = {self.max_accuracy:.2%}, F1@MaxAcc = {self.max_f1_for_max_acc_epoch:.4f}", color="#7ee787")
        else:
            self.status_lbl.setText(f"❌  Ошибка: {msg}")