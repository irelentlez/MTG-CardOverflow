import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

def reset_processed_files(self):
    # Gehe zwei Ebenen nach oben zum Projekt-Hauptordner
    pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'processed_files.json'))
    if not os.path.exists(pfad):
        QMessageBox.warning(self, "Datei nicht gefunden", "Die Datei 'processed_files.json' existiert nicht.")
        return
    reply = QMessageBox.question(
        self,
        "Bestätigung",
        "Möchtest du wirklich alle verarbeiteten Dateien zurücksetzen?\n(processed_files.json wird geleert)",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump([], f)
        QMessageBox.information(self, "Zurückgesetzt", "Die Liste der verarbeiteten Dateien wurde geleert.")

def init_settings_tab(self):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
    label = QLabel("Settings")
    label.setStyleSheet("color: white; background:transparent; font-size: 30px;")
    layout.addWidget(label)

    btn_reset = QPushButton("Verarbeitete Dateien zurücksetzen")
    btn_reset.setStyleSheet(
        "QPushButton { color: white; background: #444444; border-radius: 8px; padding: 10px; }"
        "QPushButton:hover { background: #666666; }"
    )
    btn_reset.clicked.connect(lambda: reset_processed_files(self))
    layout.addWidget(btn_reset)

    self.settings_tab.setLayout(layout)