from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QColor

class BloomTile(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True); self.setFixedHeight(45); self.setCursor(Qt.PointingHandCursor)
        self._indent = 15; self._hover_progress = 0.0
        self.anim_indent = QPropertyAnimation(self, b"indent")
        self.anim_indent.setDuration(200); self.anim_indent.setEasingCurve(QEasingCurve.OutQuint)
        self.anim_hover = QPropertyAnimation(self, b"hover_progress")
        self.anim_hover.setDuration(150); self.anim_hover.setEasingCurve(QEasingCurve.OutQuad)
        self.toggled.connect(self.on_toggled)

    def on_toggled(self, checked):
        if not checked:
            self.anim_indent.stop(); self.set_indent(15) 
            self.anim_hover.stop(); self.set_hover_progress(0.0)

    def get_indent(self): return self._indent
    def set_indent(self, v): self._indent = v; self.update()
    indent = Property(int, get_indent, set_indent)
    def get_hover_progress(self): return self._hover_progress
    def set_hover_progress(self, v): self._hover_progress = v; self.update()
    hover_progress = Property(float, get_hover_progress, set_hover_progress)

    def enterEvent(self, event):
        if not self.isChecked():
            self.anim_indent.stop(); self.anim_indent.setEndValue(25); self.anim_indent.start()
            self.anim_hover.stop(); self.anim_hover.setEndValue(1.0); self.anim_hover.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.isChecked():
            self.anim_indent.stop(); self.anim_indent.setEndValue(15); self.anim_indent.start()
            self.anim_hover.stop(); self.anim_hover.setEndValue(0.0); self.anim_hover.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        palette = self.palette(); text_color = palette.text().color()
        is_dark_mode = text_color.value() > 128
        
        if self.isChecked():
            bg = QColor("#3A3B3C") if is_dark_mode else QColor("#FFFFFF")
            accent = QColor("#8AB4F8") if is_dark_mode else QColor("#1A73E8")
            p.setBrush(bg); p.setPen(Qt.NoPen); p.drawRoundedRect(self.rect(), 8, 8)
            p.setBrush(accent); p.drawRoundedRect(0, 10, 4, 25, 2, 2)
            final_text_color = QColor("#E8EAED") if is_dark_mode else QColor("#000000")
            font = self.font(); font.setBold(True); p.setFont(font)
        else:
            if self._hover_progress > 0.01:
                hover_c = QColor("#4E4F50") if is_dark_mode else QColor("#F1F3F4")
                p.setBrush(hover_c); p.setPen(Qt.NoPen)
                p.setOpacity(self._hover_progress); p.drawRoundedRect(self.rect(), 8, 8); p.setOpacity(1.0)
            final_text_color = text_color
            font = self.font(); font.setBold(False); p.setFont(font)

        p.setPen(final_text_color)
        r = self.rect(); r.setLeft(self._indent)
        p.drawText(r, Qt.AlignVCenter | Qt.AlignLeft, self.text())