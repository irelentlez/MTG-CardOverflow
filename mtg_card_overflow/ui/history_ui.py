import os
import subprocess
import sys
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QMessageBox

from mtg_card_overflow.logic.history import get_last_pdfs

def show_history(self):
        # Layout leeren
        for i in reversed(range(self.history_layout.count())):
            widget = self.history_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        output_dir = self.config.get("output_dir", "history")
        if not output_dir:
            output_dir = "history"
        os.makedirs(output_dir, exist_ok=True)
        last_pdfs = get_last_pdfs(output_dir)
        if not last_pdfs:
            label = QLabel("Keine PDFs gefunden.")
            label.setStyleSheet("color: white; font-size: 16px;")
            self.history_layout.addWidget(label)
            return
        label = QLabel("Deine letzten 10 erstellte PDFs:")
        label.setStyleSheet("color: white; background: transparent; font-size: 16px; font-weight: bold;")
        self.history_layout.addWidget(label)
        for idx, pdf_path in enumerate(last_pdfs):
            fname = os.path.basename(pdf_path)
            btn = QPushButton(f"{idx+1}. {fname}")
            btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
            btn.setStyleSheet("QPushButton { color: white; background: #444444; border-radius: 8px; padding: 10px; }"
                              "QPushButton:hover { background: #666666; }")
            btn.clicked.connect(lambda checked, p=pdf_path: open_pdf(self, p))  # <--- geändert!
            self.history_layout.addWidget(btn)

def open_pdf(self, pdf_path):
        try:
            if sys.platform.startswith('darwin'):
                subprocess.Popen(['open', pdf_path])
            elif os.name == 'nt':
                os.startfile(pdf_path)
            elif os.name == 'posix':
                subprocess.Popen(['xdg-open', pdf_path])
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"PDF konnte nicht geöffnet werden:\n{e}")