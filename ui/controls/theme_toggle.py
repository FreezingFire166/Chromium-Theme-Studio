from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QColor, QBrush

class ThemeToggle(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True); self.setFixedSize(50, 28); self.setCursor(Qt.PointingHandCursor)
        self._circle_x = 3; self._rotation = 0
        self.anim_x = QPropertyAnimation(self, b"circle_x", self)
        self.anim_x.setDuration(400); self.anim_x.setEasingCurve(QEasingCurve.OutBack) 
        self.anim_rot = QPropertyAnimation(self, b"rotation", self)
        self.anim_rot.setDuration(400); self.anim_rot.setEasingCurve(QEasingCurve.OutCubic)
        self.toggled.connect(self.start_anim)

    def start_anim(self, checked):
        self.anim_x.stop(); self.anim_x.setEndValue(self.width() - 25 if checked else 3); self.anim_x.start()
        self.anim_rot.stop(); self.anim_rot.setStartValue(0); self.anim_rot.setEndValue(180 if checked else -180); self.anim_rot.start()

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        track_color = QColor("#1A1A1A") if self.isChecked() else QColor("#E0E0E0")
        p.setBrush(QBrush(track_color)); p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)
        circle_color = QColor("#333") if self.isChecked() else QColor("#FFD700")
        icon = "🌙" if self.isChecked() else "☀"
        p.save()
        cx = self._circle_x + 11; cy = self.height() / 2
        p.translate(cx, cy); p.rotate(self._rotation); p.translate(-cx, -cy)
        p.setBrush(QBrush(circle_color)); p.drawEllipse(int(self._circle_x), 3, 22, 22)
        p.setPen(QColor("#FFF") if self.isChecked() else QColor("#F39C12"))
        font = p.font(); font.setPixelSize(14); p.setFont(font)
        p.drawText(int(self._circle_x), 3, 22, 22, Qt.AlignCenter, icon)
        p.restore()

    def get_circle_x(self): return self._circle_x
    def set_circle_x(self, x): self._circle_x = x; self.update()
    circle_x = Property(float, get_circle_x, set_circle_x)
    def get_rotation(self): return self._rotation
    def set_rotation(self, r): self._rotation = r; self.update()
    rotation = Property(float, get_rotation, set_rotation)