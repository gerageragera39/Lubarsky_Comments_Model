"""
Metric Card Widget
A reusable widget for displaying training metrics.
"""

from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class MetricCard(QFrame):
    """
    A widget that displays a single training metric.
    
    This class follows the Single Responsibility Principle by handling
    only the display of a single metric value.
    """
    
    def __init__(self, title: str, initial: str = "—", color: str = "#58a6ff"):
        super().__init__()
        self.setObjectName("metricCard")
        self.setMinimumWidth(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("metricTitle")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_lbl = QLabel(initial)
        self.value_lbl.setObjectName("metricValue")
        self.value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_lbl.setStyleSheet(f"color: {color};")

        layout.addWidget(self.title_lbl)
        layout.addWidget(self.value_lbl)

    def set_value(self, text: str):
        """Update the displayed value."""
        self.value_lbl.setText(text)