import os
from mtg_card_overflow.logic import tracking
from mtg_card_overflow.logic.directprint import print_pdf
from mtg_card_overflow.logic.pdf_generator import generate_pdf
from PyQt5.QtWidgets import (QMessageBox)
from mtg_card_overflow.ui.progress_ui import ProgressDialog
from PyQt5.QtWidgets import QApplication


def select_and_generate(self):
    input_path = self.config.get("input_dir", "")
    if not input_path or not os.path.isdir(input_path):
        QMessageBox.critical(self, "Fehler", "Input-Ordner ist ungültig oder nicht gesetzt.")
        return

    input_files = [
        os.path.join(input_path, f)
        for f in os.listdir(input_path)
        if f.lower().endswith(".png") or f.lower().endswith(".jpg") or f.lower().endswith(".jpeg")
    ]
    to_process = [f for f in input_files if not tracking.is_processed(f)]

    if not to_process:
        QMessageBox.information(self, "Keine neuen Karten", "Alle Karten wurden bereits verarbeitet.")
        return

    output_dir = self.config.get("output_dir", "history")
    os.makedirs(output_dir, exist_ok=True)
    existing_pdfs = set(os.listdir(output_dir))

    # Fortschrittsdialog anzeigen (nur ein Schritt, da alles auf einmal)
    progress = ProgressDialog(parent=self)
    progress.set_text("PDF wird erstellt...")
    progress.show()
    QApplication.processEvents()

    # PDF-Erstellung (dauert ggf. etwas)
    generate_pdf(to_process, output_dir=output_dir)
    for file in to_process:
        tracking.mark_as_processed(file)

    progress.set_text("Fertig!")
    QApplication.processEvents()
    progress.close()

    new_pdfs = [os.path.join(output_dir, f) for f in os.listdir(output_dir)
                if f.lower().endswith(".pdf") and f not in existing_pdfs]
    QMessageBox.information(self, "Fertig", f"{len(to_process)} Karten verarbeitet.")

    # Direktdruck
    if self.print_checkbox.isChecked() and new_pdfs:
        for pdf in new_pdfs:
            try:
                print_pdf(pdf)
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"PDF konnte nicht gedruckt werden:\n{e}")