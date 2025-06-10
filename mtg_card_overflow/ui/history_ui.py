import os
import subprocess
import sys
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QMessageBox, QHBoxLayout, QWidget

from mtg_card_overflow.logic.history import get_last_pdfs

# --- NEU: Methode zum Löschen einer PDF ---
def delete_pdf(self, pdf_path):
    reply = QMessageBox.question(
        self,
        "PDF löschen",
        f"Möchtest du die Datei wirklich löschen?\n{os.path.basename(pdf_path)}",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        try:
            os.remove(pdf_path)
            QMessageBox.information(self, "Gelöscht", f"{os.path.basename(pdf_path)} wurde gelöscht.")
            show_history(self)  # Liste aktualisieren
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"PDF konnte nicht gelöscht werden:\n{e}")

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
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(10)

        btn = QPushButton(f"{idx+1}. {fname}")
        btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        btn.setStyleSheet(
            "QPushButton { color: white; background: transparent; border-radius: 8px; padding: 10px; }"
            "QPushButton:hover { background: #666666; }"
        )
        btn.clicked.connect(lambda checked, p=pdf_path: open_pdf(self, p))

        # Papierkorb-Button
        trash_btn = QPushButton()
        trash_btn.setToolTip("PDF löschen")
        trash_btn.setFixedSize(32, 32)
        trash_icon_path = os.path.join(os.path.dirname(__file__), "trash.png")
        if os.path.exists(trash_icon_path):
            trash_btn.setIcon(QIcon(trash_icon_path))
            trash_btn.setIconSize(trash_btn.size())
        else:
            trash_btn.setText("🗑")  # Fallback-Emoji
        trash_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; }"
            "QPushButton:hover { background: #aa2222; }"
        )
        trash_btn.clicked.connect(lambda checked, p=pdf_path: delete_pdf(self, p))

        row_layout.addWidget(btn)
        row_layout.addWidget(trash_btn)
        row_layout.addStretch()
        self.history_layout.addWidget(row_widget)

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