"""
Application Entry Point
Main module to run the ruBERT Fine-Tuning Studio application.
"""

import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor

from .gui.main_window import MainWindow, STYLESHEET


def main():
    """
    Main entry point for the application.
    
    This function follows the Single Responsibility Principle by handling
    only the initialization and execution of the GUI application.
    """
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)

    # Dark palette for Fusion
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#0d1117"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#c9d1d9"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#0d1117"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#161b22"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#161b22"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#c9d1d9"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#c9d1d9"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#21262d"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#c9d1d9"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#f0f6fc"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#1f6feb"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()