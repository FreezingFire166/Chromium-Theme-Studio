from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt

class SmartSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.next_slider = None
        self.prev_slider = None

    def enterEvent(self, event):
        self.setFocus(); super().enterEvent(event)

    def keyPressEvent(self, event):
        step = 10 if (event.modifiers() & Qt.ControlModifier) else 1
        if event.key() == Qt.Key_Up: self.setValue(self.value() + step)
        elif event.key() == Qt.Key_Down: self.setValue(self.value() - step)
        elif event.key() == Qt.Key_Right: self.next_slider.setFocus() if self.next_slider else None
        elif event.key() == Qt.Key_Left: self.prev_slider.setFocus() if self.prev_slider else None
        else: super().keyPressEvent(event)