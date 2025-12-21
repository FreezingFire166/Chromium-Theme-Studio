from PySide6.QtWidgets import (QFrame, QHBoxLayout, QPushButton, QWidget, QStackedWidget)
from PySide6.QtCore import (Qt, Signal, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint)

class SlidingStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_speed = 400; self.m_easing = QEasingCurve.OutCubic; self.m_active = False

    def slide_to_index(self, index):
        if self.m_active or index == self.currentIndex(): return
        self.m_active = True
        _now = self.currentIndex(); _next = index
        width = self.frameRect().width(); height = self.frameRect().height()
        current_widget = self.widget(_now); next_widget = self.widget(_next)
        next_widget.setGeometry(0, 0, width, height)
        offset_x = width if _next > _now else -width
        next_widget.move(offset_x, 0); next_widget.show(); next_widget.raise_()
        
        self.anim_group = QParallelAnimationGroup(self)
        anim_now = QPropertyAnimation(current_widget, b"pos")
        anim_now.setDuration(self.m_speed); anim_now.setEasingCurve(self.m_easing)
        anim_now.setStartValue(QPoint(0, 0)); anim_now.setEndValue(QPoint(-offset_x, 0))
        anim_next = QPropertyAnimation(next_widget, b"pos")
        anim_next.setDuration(self.m_speed); anim_next.setEasingCurve(self.m_easing)
        anim_next.setStartValue(QPoint(offset_x, 0)); anim_next.setEndValue(QPoint(0, 0))
        
        self.anim_group.addAnimation(anim_now); self.anim_group.addAnimation(anim_next)
        self.anim_group.finished.connect(lambda: self._on_slide_finished(index))
        self.anim_group.start()
        
    def _on_slide_finished(self, index):
        self.setCurrentIndex(index); self.m_active = False
        for i in range(self.count()): 
            if i != index: self.widget(i).hide(); self.widget(i).move(0,0)

class TopBar(QFrame):
    settings_clicked = Signal(bool); load_clicked = Signal(); export_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        layout = QHBoxLayout(self); layout.setContentsMargins(20, 0, 20, 0); layout.setSpacing(15)

        self.btn_title = QPushButton("Chromium Theme Studio V2")
        self.btn_title.setCursor(Qt.PointingHandCursor); self.btn_title.clicked.connect(self.go_home)
        layout.addWidget(self.btn_title)

        line = QFrame(); line.setFrameShape(QFrame.VLine); line.setFrameShadow(QFrame.Sunken); line.setFixedHeight(20)
        line.setStyleSheet("background-color: #ccc;"); layout.addWidget(line)

        self.btn_settings = QPushButton("Settings")
        self.btn_settings.setCursor(Qt.PointingHandCursor); self.btn_settings.setCheckable(True)
        self.btn_settings.clicked.connect(self.toggle_settings_view)
        layout.addWidget(self.btn_settings)

        self.slider_stack = SlidingStackedWidget()
        self.group_home = QWidget(); home_lay = QHBoxLayout(self.group_home); home_lay.setContentsMargins(0, 0, 0, 0); home_lay.setAlignment(Qt.AlignLeft)
        self.btn_inject = QPushButton("Inject"); self.btn_import = QPushButton("Import"); self.btn_export = QPushButton("Export")
        self.btn_import.clicked.connect(self.load_clicked.emit); self.btn_export.clicked.connect(self.export_clicked.emit)
        home_lay.addWidget(self.btn_inject); home_lay.addWidget(self.btn_import); home_lay.addWidget(self.btn_export)
        
        self.group_set = QWidget(); set_lay = QHBoxLayout(self.group_set); set_lay.setContentsMargins(0, 0, 0, 0); set_lay.setAlignment(Qt.AlignLeft)
        self.btn_reset = QPushButton("Reset Defaults"); self.btn_help = QPushButton("Help")
        set_lay.addWidget(self.btn_reset); set_lay.addWidget(self.btn_help)

        self.slider_stack.addWidget(self.group_home); self.slider_stack.addWidget(self.group_set)
        layout.addWidget(self.slider_stack, 1)

        for btn in [self.btn_inject, self.btn_import, self.btn_export, self.btn_reset, self.btn_help]:
            btn.setProperty("class", "topBtn"); btn.setCursor(Qt.PointingHandCursor)

    def toggle_settings_view(self):
        is_settings = self.btn_settings.isChecked()
        self.settings_clicked.emit(is_settings)
        if is_settings: self.slider_stack.slide_to_index(1)
        else: self.slider_stack.slide_to_index(0)

    def go_home(self):
        if self.btn_settings.isChecked():
            self.btn_settings.setChecked(False); self.toggle_settings_view()