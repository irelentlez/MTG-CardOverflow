from mtg_card_overflow.logic.config import save_config
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QCheckBox, QFileDialog, QMessageBox, QTabWidget, QLabel, QSizePolicy, QScrollArea
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

def change_input_dir(self):
        new_dir = QFileDialog.getExistingDirectory(self, "Input-Ordner wählen")
        if new_dir:
            self.config["input_dir"] = new_dir
            save_config(self.config)
            QMessageBox.information(self, "Info", f"Input-Ordner geändert zu:\n{new_dir}")

def change_output_dir(self):
        new_dir = QFileDialog.getExistingDirectory(self, "Output-Ordner wählen")
        if new_dir:
            self.config["output_dir"] = new_dir
            save_config(self.config)
            QMessageBox.information(self, "Info", f"Output-Ordner geändert zu:\n{new_dir}")