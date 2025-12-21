from PySide6.QtWidgets import QSlider
from PySide6.QtGui import QPainter, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QRect

class GradientSlider(QSlider):
    def __init__(self, orientation, parent=None, mode="hue"):
        super().__init__(orientation, parent)
        self.mode = mode
        self.setStyleSheet("""
            QSlider::groove:horizontal { border: 1px solid #bbb; height: 10px; border-radius: 5px; }
            QSlider::handle:horizontal { background: white; border: 1px solid #777; width: 14px; margin: -5px 0; border-radius: 7px; }
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        groove = QRect(rect.left(), rect.center().y() - 5, rect.width(), 10)
        gradient = QLinearGradient(groove.left(), 0, groove.right(), 0)
        if self.mode == "hue":
            colors = [Qt.red, Qt.yellow, Qt.green, Qt.cyan, Qt.blue, Qt.magenta, Qt.red]
            for i, c in enumerate(colors): gradient.setColorAt(i / (len(colors) - 1), c)
        painter.setBrush(QBrush(gradient)); painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(groove, 5, 5)
        super().paintEvent(event)