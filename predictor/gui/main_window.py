"""
Main Window
The primary GUI component for the YouTube Comment Predictor.
"""

import os
import sys
from pathlib import Path
from typing import Tuple

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QProgressBar,
    QGroupBox,
    QFrame,
    QComboBox,
    QSplitter,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QFont

from ..models.prediction_result import PredictionBatch, TargetLabel
from ..controllers.prediction_controller import PredictionController
from ..utils.logging_utils import get_logger


# GitHub-inspired dark theme stylesheet
STYLESHEET = """
QMainWindow {
    background-color: #0d1117;
}

QWidget {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

QGroupBox {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 8px;
    color: #8b949e;
}

QLineEdit {
    background-color: #010409;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px 12px;
    color: #c9d1d9;
    selection-background-color: #1f6feb;
}

QLineEdit:focus {
    border: 1px solid #1f6feb;
}

QLineEdit:disabled {
    background-color: #161b22;
    color: #484f58;
}

QPushButton {
    background-color: #238636;
    color: #ffffff;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #2ea043;
    border: 1px solid #30363d;
}

QPushButton:pressed {
    background-color: #238636;
}

QPushButton:disabled {
    background-color: #161b22;
    color: #484f58;
    border: 1px solid #30363d;
}

QPushButton#secondaryBtn {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
}

QPushButton#secondaryBtn:hover {
    background-color: #30363d;
    border: 1px solid #8b949e;
}

QPushButton#dangerBtn {
    background-color: #da3633;
    color: #ffffff;
}

QPushButton#dangerBtn:hover {
    background-color: #f85149;
}

QComboBox {
    background-color: #010409;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px 12px;
    color: #c9d1d9;
    min-width: 200px;
}

QComboBox:hover {
    border: 1px solid #8b949e;
}

QComboBox:focus {
    border: 1px solid #1f6feb;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox::down-arrow {
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
    outline: none;
    padding: 4px;
}

QComboBox QAbstractItemView::item {
    padding: 6px 8px;
    border-radius: 4px;
}

QProgressBar {
    background-color: #21262d;
    border: 1px solid #30363d;
    border-radius: 6px;
    height: 20px;
    text-align: center;
    color: #c9d1d9;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #238636, stop:1 #2ea043);
    border-radius: 5px;
}

QTableWidget {
    background-color: #010409;
    alternate-background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    gridline-color: #21262d;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #1f6feb;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #161b22;
    color: #8b949e;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #30363d;
    border-right: 1px solid #21262d;
    font-weight: 600;
}

QHeaderView::section:hover {
    background-color: #21262d;
}

QHeaderView::section:pressed {
    background-color: #30363d;
}

QScrollBar:vertical {
    background-color: #0d1117;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #30363d;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #484f58;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #0d1117;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #30363d;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #484f58;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QLabel {
    color: #c9d1d9;
}

QLabel#titleLabel {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#subtitleLabel {
    font-size: 12px;
    color: #8b949e;
}

QLabel#progressLabel {
    font-size: 12px;
    color: #8b949e;
}

QFrame#separator {
    background-color: #30363d;
    max-height: 1px;
}

QFrame#card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
}
"""


class PredictionTable(QTableWidget):
    """
    Custom table widget for displaying prediction results.

    Features:
    - Sortable columns
    - Color-coded target labels
    - Auto-resizing columns
    """

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Setup table UI"""
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["#", "Comment", "Target", "Confidence"])

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSortIndicatorShown(True)
        header.setSectionsClickable(True)

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)

    def load_batch(self, batch: PredictionBatch):
        """Load prediction batch into table"""
        self.setRowCount(0)
        self.setRowCount(len(batch.results))

        for row, result in enumerate(batch.results):
            # Row number
            self.setItem(row, 0, QTableWidgetItem(str(row + 1)))

            # Comment text
            comment_item = QTableWidgetItem(result.comment)
            comment_item.setFlags(comment_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, 1, comment_item)

            # Target label with color
            target_item = QTableWidgetItem(result.target_display)
            target_item.setForeground(self._get_target_color(result.target))
            self.setItem(row, 2, target_item)

            # Confidence
            conf_item = QTableWidgetItem(f"{result.confidence:.2%}" if result.confidence else "N/A")
            conf_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, 3, conf_item)

        self.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def _get_target_color(self, target_label: TargetLabel) -> QColor:
        """Get color for target label"""
        colors = {
            TargetLabel.NEGATIVE: QColor("#f85149"),
            TargetLabel.NEUTRAL: QColor("#8b949e"),
            TargetLabel.POSITIVE: QColor("#3fb950"),
        }
        return colors.get(target_label, QColor("#c9d1d9"))


class SummaryCard(QFrame):
    """
    Card widget displaying prediction summary statistics.
    """

    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        self._setup_ui()

    def _setup_ui(self):
        """Setup summary UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(20)

        self.negative_frame, self.negative_lbl = self._create_label("Negative", "#f85149")
        self.neutral_frame, self.neutral_lbl = self._create_label("Neutral", "#8b949e")
        self.positive_frame, self.positive_lbl = self._create_label("Positive", "#3fb950")
        self.total_frame, self.total_lbl = self._create_label("Total", "#58a6ff")

        layout.addWidget(self.negative_frame)
        layout.addWidget(QFrame())  # Spacer
        layout.addWidget(self.neutral_frame)
        layout.addWidget(QFrame())  # Spacer
        layout.addWidget(self.positive_frame)
        layout.addWidget(QFrame())  # Spacer
        layout.addWidget(self.total_frame)

    def _create_label(self, title: str, color: str) -> Tuple[QFrame, QLabel]:
        """Create a summary label"""
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(12, 8, 12, 8)
        frame_layout.setSpacing(4)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("subtitleLabel")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value_lbl = QLabel("—")
        value_lbl.setObjectName("titleLabel")
        value_lbl.setProperty("color", color)
        value_lbl.setStyleSheet(f"color: {color}; font-size: 20px;")
        value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame_layout.addWidget(title_lbl)
        frame_layout.addWidget(value_lbl)

        return frame, value_lbl

    def update_summary(self, summary: dict[str, int], total: int):
        """Update summary with new values"""
        self.negative_lbl.setText(str(summary.get("Negative", 0)))
        self.neutral_lbl.setText(str(summary.get("Neutral", 0)))
        self.positive_lbl.setText(str(summary.get("Positive", 0)))
        self.total_lbl.setText(str(total))


class MainWindow(QMainWindow):
    """
    Main application window for YouTube Comment Predictor.

    This class follows the Single Responsibility Principle by handling
    only the user interface components.
    """

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.logger = get_logger(self.__class__.__name__)
        self.controller: Optional[PredictionController] = None

        self._setup_ui()
        self._setup_controller()
        self._connect_signals()

    def _setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("YouTube Comment Predictor")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Title
        title_lbl = QLabel("🎯 YouTube Comment Predictor")
        title_lbl.setObjectName("titleLabel")
        main_layout.addWidget(title_lbl)

        subtitle_lbl = QLabel("Predict sentiment of YouTube comments using trained models")
        subtitle_lbl.setObjectName("subtitleLabel")
        main_layout.addWidget(subtitle_lbl)

        # Main splitter
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Top section - Controls
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(16)

        # Model selection group
        model_group = self._create_model_group()
        top_layout.addWidget(model_group)

        # Video URL group
        url_group = self._create_url_group()
        top_layout.addWidget(url_group)

        # Progress section
        progress_group = self._create_progress_group()
        top_layout.addWidget(progress_group)

        # Action buttons
        btn_layout = self._create_button_layout()
        top_layout.addLayout(btn_layout)

        splitter.addWidget(top_widget)

        # Bottom section - Results table
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(12)

        # Summary cards
        self.summary_card = SummaryCard()
        bottom_layout.addWidget(self.summary_card)

        # Results table
        self.table = PredictionTable()
        bottom_layout.addWidget(self.table)

        splitter.addWidget(bottom_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

    def _create_model_group(self) -> QGroupBox:
        """Create model selection group"""
        group = QGroupBox("Model Selection")
        layout = QHBoxLayout(group)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Model:"))

        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(400)
        self.model_combo.addItem("Select a model...", "")
        layout.addWidget(self.model_combo)

        self.browse_model_btn = QPushButton("Browse...")
        self.browse_model_btn.setObjectName("secondaryBtn")
        self.browse_model_btn.setFixedWidth(100)
        layout.addWidget(self.browse_model_btn)

        return group

    def _create_url_group(self) -> QGroupBox:
        """Create URL input group"""
        group = QGroupBox("Video URL")
        layout = QHBoxLayout(group)
        layout.setSpacing(12)

        layout.addWidget(QLabel("YouTube URL:"))

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        layout.addWidget(self.url_input)

        return group

    def _create_progress_group(self) -> QGroupBox:
        """Create progress group"""
        group = QGroupBox("Progress")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Ready")
        layout.addWidget(self.progress_bar)

        self.progress_lbl = QLabel("Waiting to start prediction...")
        self.progress_lbl.setObjectName("progressLabel")
        layout.addWidget(self.progress_lbl)

        return group

    def _create_button_layout(self) -> QHBoxLayout:
        """Create action button layout"""
        layout = QHBoxLayout()
        layout.setSpacing(12)

        self.predict_btn = QPushButton("🚀 Start Prediction")
        self.predict_btn.setMinimumHeight(40)
        layout.addWidget(self.predict_btn)

        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setObjectName("dangerBtn")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setEnabled(False)
        layout.addWidget(self.cancel_btn)

        layout.addStretch()

        self.open_file_btn = QPushButton("📂 Open Output File")
        self.open_file_btn.setObjectName("secondaryBtn")
        self.open_file_btn.setMinimumHeight(40)
        layout.addWidget(self.open_file_btn)

        return layout

    def _setup_controller(self):
        """Setup the controller"""
        self.controller = PredictionController(self, self.api_key)

    def _connect_signals(self):
        """Connect UI signals"""
        # Button clicks
        self.predict_btn.clicked.connect(self._on_predict_clicked)
        self.cancel_btn.clicked.connect(self._on_cancel_clicked)
        self.browse_model_btn.clicked.connect(self._on_browse_model_clicked)
        self.open_file_btn.clicked.connect(self._on_open_file_clicked)

        # Controller signals
        self.controller.models_loaded.connect(self._on_models_loaded)
        self.controller.prediction_started.connect(self._on_prediction_started)
        self.controller.prediction_progress.connect(self._on_prediction_progress)
        self.controller.prediction_finished.connect(self._on_prediction_finished)
        self.controller.prediction_error.connect(self._on_prediction_error)

        # Load models on startup
        self.controller.load_models(".")

    def _on_models_loaded(self, models: list[str]):
        """Handle models loaded"""
        self.model_combo.clear()
        self.model_combo.addItem("Select a model...", "")
        for model in models:
            self.model_combo.addItem(model, model)

        if len(models) > 0:
            self.logger.info(f"Loaded {len(models)} model(s)")

    def _on_predict_clicked(self):
        """Handle predict button click"""
        model_path = self.model_combo.currentData()
        video_url = self.url_input.text().strip()

        if not model_path:
            QMessageBox.warning(self, "Warning", "Please select a model")
            return

        self.controller.start_prediction(
            model_path=model_path,
            video_url=video_url,
            output_file="predict.csv",
            max_comments=500,
        )

    def _on_cancel_clicked(self):
        """Handle cancel button click"""
        self.controller.cancel_prediction()
        self._reset_ui_state()

    def _on_browse_model_clicked(self):
        """Handle browse model button click"""
        model_path = self.controller.select_model_file(".")
        if model_path:
            # Check if model is already in combo
            for i in range(self.model_combo.count()):
                if self.model_combo.itemData(i) == model_path:
                    self.model_combo.setCurrentIndex(i)
                    return

            # Add new model to combo
            self.model_combo.addItem(model_path, model_path)
            self.model_combo.setCurrentIndex(self.model_combo.count() - 1)

    def _on_open_file_clicked(self):
        """Handle open file button click"""
        output_file = "predict.csv"
        if os.path.exists(output_file):
            os.startfile(output_file)
        else:
            QMessageBox.information(self, "Info", "No predictions file found yet")

    def _on_prediction_started(self):
        """Handle prediction started"""
        self.predict_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.model_combo.setEnabled(False)
        self.url_input.setEnabled(False)
        self.progress_bar.setValue(0)

    def _on_prediction_progress(self, current: int, total: int):
        """Handle prediction progress"""
        if total > 0:
            percent = int((current / total) * 100)
            self.progress_bar.setValue(percent)
            self.progress_lbl.setText(f"Processing comment {current} of {total}...")

    def _on_prediction_finished(self, batch: PredictionBatch):
        """Handle prediction finished"""
        self._reset_ui_state()
        self.progress_bar.setValue(100)
        self.progress_lbl.setText(f"Completed! Processed {batch.total_comments} comments")

        # Update table
        self.table.load_batch(batch)

        # Update summary
        self.summary_card.update_summary(batch.summary, batch.total_comments)

        # Show success message
        self.controller.show_success(
            f"Prediction completed!\n"
            f"Total comments: {batch.total_comments}\n"
            f"Results saved to: predict.csv"
        )

    def _on_prediction_error(self, error: str):
        """Handle prediction error"""
        self._reset_ui_state()
        self.progress_lbl.setText("Error occurred")
        self.controller.show_error(error)

    def _reset_ui_state(self):
        """Reset UI to initial state"""
        self.predict_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.model_combo.setEnabled(True)
        self.url_input.setEnabled(True)


def main():
    """Application entry point"""
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("API_KEY")
    if not api_key:
        QMessageBox.critical(None, "Error", "API_KEY environment variable is required")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)

    window = MainWindow(api_key)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
