import os
import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QCheckBox, QFileDialog, QMessageBox, QTabWidget, QLabel, QSizePolicy, QScrollArea
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

from mtg_card_overflow.logic import tracking, history
from mtg_card_overflow.logic.pdf_generator import generate_pdf
from mtg_card_overflow.logic.config import load_config, save_config
from mtg_card_overflow.logic.history import get_last_pdfs
from mtg_card_overflow.logic.directprint import print_pdf
from mtg_card_overflow.ui.baclground_tab import BackgroundTab
from mtg_card_overflow.ui.history_ui import show_history, open_pdf
from mtg_card_overflow.ui.dialogs import change_input_dir, change_output_dir
from mtg_card_overflow.ui.pdf_ui import select_and_generate
from mtg_card_overflow.ui.settings_tab import init_settings_tab
from mtg_card_overflow.ui.start_tab import init_start_tab

def set_tab_background(tab_widget, bg_path):
    if os.path.exists(bg_path):
        tab_widget.setStyleSheet(
    f"QWidget {{ background-image: url('{bg_path.replace(os.sep, '/')}'); background-repeat: no-repeat; background-position: center; }}"
)
    else:
        tab_widget.setStyleSheet("QWidget { background: #222; }")

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("MTG-CardOverflow")

        self.bg_path = os.path.join(os.path.dirname(__file__), "background.png")

        # Fenstergröße auf Bildgröße setzen
        if os.path.exists(self.bg_path):
            from PIL import Image
            img = Image.open(self.bg_path)
            width, height = img.size
            self.resize(width, height)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Start-Tab
        self.start_tab = BackgroundTab(self.bg_path)
        self.tabs.addTab(self.start_tab, "Start")
        init_start_tab(self)

        # History-Tab
        self.history_tab = BackgroundTab(self.bg_path)
        self.tabs.addTab(self.history_tab, "History")
        self.init_history_tab()

        # Settings-Tab
        self.settings_tab = BackgroundTab(self.bg_path)
        self.tabs.addTab(self.settings_tab, "Settings")
        init_settings_tab(self)
        # Icon setzen
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'mtg_card_printer_icon.ico'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.tabs.currentChanged.connect(self.on_tab_changed)

    def init_history_tab(self):
        self.history_layout = QVBoxLayout()
        self.history_layout.setAlignment(Qt.AlignTop)
        self.history_scroll = QScrollArea()
        self.history_scroll.setWidgetResizable(True)
        self.history_scroll.setStyleSheet("background: transparent; border: none;")  # <--- NEU
        self.history_content = QWidget()
        self.history_content.setStyleSheet("background: transparent;")  # <--- NEU
        self.history_content.setLayout(self.history_layout)
        self.history_scroll.setWidget(self.history_content)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.history_scroll)
        self.history_tab.setLayout(main_layout)

    def on_tab_changed(self, idx):
        # History-Tab aktualisieren
        if idx == 1:
            show_history(self)

def run_gui(config):
    app = QApplication(sys.argv)
    window = MainWindow(config)
    window.show()
    app.exec_()