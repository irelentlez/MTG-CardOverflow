from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar

class ProgressDialog(QDialog):
    def __init__(self, title="Verarbeite PDFs...", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(400, 100)
        layout = QVBoxLayout(self)
        self.label = QLabel("Bitte warten...", self)
        self.progress = QProgressBar(self)
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)  # 0 = unbestimmt/animiert!
        layout.addWidget(self.label)
        layout.addWidget(self.progress)

    def set_text(self, text):
        self.label.setText(text)