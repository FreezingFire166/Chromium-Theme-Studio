from PySide6.QtCore import Qt, QRect, Property, QPointF, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QPainter, QColor, QBrush, QPen

class SettingsToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 28)
        self.setCursor(Qt.PointingHandCursor)
        self._circle_position = 3.0
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)
        self.stateChanged.connect(self.start_transition)

    @Property(float)
    def circle_position(self): return self._circle_position
    @circle_position.setter
    def circle_position(self, pos): self._circle_position = pos; self.update()

    def start_transition(self, state):
        self.animation.stop()
        self.animation.setEndValue(self.width() - 25.0 if state else 3.0)
        self.animation.start()

    def hitButton(self, pos):
        return self.contentsRect().contains(pos.toPoint() if hasattr(pos, 'toPoint') else pos)

    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        if self.isChecked(): bg_color = QColor("#1A73E8")
        else:
            bg_color = QColor("#777777")
            if self.palette().window().color().value() > 128: bg_color = QColor("#E0E0E0")
        p.setPen(Qt.NoPen); p.setBrush(QBrush(bg_color))
        p.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)
        p.setBrush(QBrush(QColor("#FFFFFF"))); p.setPen(QPen(QColor(0,0,0, 30), 1))
        p.drawEllipse(self._circle_position, 3.0, 22, 22)