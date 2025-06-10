from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt
import os

class BackgroundTab(QWidget):
    def __init__(self, bg_path, parent=None):
        super().__init__(parent)
        self.bg_path = bg_path
        self.bg_pixmap = QPixmap(bg_path) if os.path.exists(bg_path) else None

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.bg_pixmap:
            painter = QPainter(self)
            scaled = self.bg_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled)