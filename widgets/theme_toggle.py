from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

from engine.app_theme import DARK_THEME, LIGHT_THEME


class ThemeToggleButton(QPushButton):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setFixedSize(46, 46)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("border: none;")

        self._angle = 0.0
        self.is_dark = True

        self.anim = QPropertyAnimation(self, b"angle")
        self.anim.setDuration(450)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

        self.clicked.connect(self.toggle)

    def toggle(self):
        self.is_dark = not self.is_dark

        self.anim.stop()
        self.anim.setStartValue(self._angle)
        self.anim.setEndValue(self._angle + 180)
        self.anim.start()

        self.app.setStyleSheet(
            DARK_THEME if self.is_dark else LIGHT_THEME
        )

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.translate(self.width() / 2, self.height() / 2)
        p.rotate(self._angle)
        p.translate(-self.width() / 2, -self.height() / 2)

        if self.is_dark:
            # Moon
            p.setBrush(QColor(220, 220, 220))
            p.setPen(Qt.NoPen)
            p.drawEllipse(14, 14, 18, 18)
        else:
            # Sun
            p.setBrush(QColor(255, 200, 0))
            p.setPen(Qt.NoPen)
            p.drawEllipse(14, 14, 18, 18)

    def get_angle(self):
        return self._angle

    def set_angle(self, value):
        self._angle = value
        self.update()

    angle = Property(float, get_angle, set_angle)
