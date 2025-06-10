from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QCheckBox, QFileDialog, QMessageBox, QTabWidget, QLabel, QSizePolicy, QScrollArea
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from mtg_card_overflow.ui.dialogs import change_input_dir, change_output_dir
from mtg_card_overflow.ui.pdf_ui import select_and_generate

def init_start_tab(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Hauptbutton
        btn_main = QPushButton("PDF erstellen")
        btn_main.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_main.setStyleSheet(
            "QPushButton { color: white; background: transparent; border-radius: 12px; padding: 18px; }"
            "QPushButton:hover { background: #666666; }"
        )
        btn_main.clicked.connect(lambda: select_and_generate(self))  # <--- geändert
        btn_main.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(btn_main)
        layout.addSpacing(30)

        # Kleine Buttons nebeneinander
        btn_row = QHBoxLayout()
        btn_input = QPushButton("Input-Ordner")
        btn_input.setStyleSheet(
            "QPushButton { color: white; background: transparent; border-radius: 8px; padding: 10px; }"
            "QPushButton:hover { background: #666666; }"
        )
        btn_input.clicked.connect(lambda: change_input_dir(self))  # <--- geändert
        btn_output = QPushButton("Output-Ordner")
        btn_output.setStyleSheet(
            "QPushButton { color: white; background: transparent; border-radius: 8px; padding: 10px; }"
            "QPushButton:hover { background: #666666; }"
        )
        btn_output.clicked.connect(lambda: change_output_dir(self))  # <--- geändert
        btn_row.addWidget(btn_input)
        btn_row.addSpacing(20)
        btn_row.addWidget(btn_output)
        layout.addLayout(btn_row)
        layout.addSpacing(30)

        # Kontrollkästchen
        self.print_checkbox = QCheckBox("PDF nach Erstellung direkt drucken")
        self.print_checkbox.setStyleSheet(
            "QCheckBox { color: white; background: transparent; }"
            "QCheckBox::indicator { width: 22px; height: 22px; }"
        )
        layout.addWidget(self.print_checkbox)

        self.start_tab.setLayout(layout)
        pass