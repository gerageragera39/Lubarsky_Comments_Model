"""
Application Entry Point
Main module to run the YouTube Comment Predictor application.
"""

import sys
import os
from dotenv import load_dotenv

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor

from .gui.main_window import MainWindow, STYLESHEET
from .config import Config


def main():
    """
    Main entry point for the application.

    This function follows the Single Responsibility Principle by handling
    only the initialization and execution of the GUI application.
    """
    # Load environment variables from the executable's directory
    # For PyInstaller onedir builds, .env is copied to the output folder
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        bundle_dir = os.path.dirname(sys.executable)
        env_path = os.path.join(bundle_dir, '.env')
    else:
        # Running as script - look for .env in project root
        bundle_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env_path = os.path.join(bundle_dir, '.env')
    
    load_dotenv(env_path)

    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please ensure API_KEY is set in .env file")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)

    # Dark palette for Fusion
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#0d1117"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#c9d1d9"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#010409"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#0d1117"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#c9d1d9"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#c9d1d9"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#c9d1d9"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#21262d"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#c9d1d9"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#f85149"))
    palette.setColor(QPalette.ColorRole.Link, QColor("#58a6ff"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#1f6feb"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = MainWindow(Config.API_KEY)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
