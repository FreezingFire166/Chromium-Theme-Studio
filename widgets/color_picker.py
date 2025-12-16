from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QSlider,
    QSpinBox,
    QStackedWidget,
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Signal

from engine.sections import SECTIONS, SectionType
from widgets.image_editor import ImageEditor


class ColorPicker(QWidget):
    colorChanged = Signal()

    def __init__(self, state):
        super().__init__()
        self.state = state
        self.current_key = None

        root = QVBoxLayout(self)
        root.setSpacing(12)

        # ── SECTION LIST ────────────────────
        self.section_list = QListWidget()
        self.section_list.setFixedWidth(200)

        for key, label, stype in SECTIONS:
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, (key, stype))
            self.section_list.addItem(item)

        self.section_list.currentItemChanged.connect(
            self.on_section_changed
        )

        # ── STACK ──────────────────────────
        self.stack = QStackedWidget()

        # ── COLOR PAGE ─────────────────────
        self.color_page = QWidget()
        cp_layout = QVBoxLayout(self.color_page)
        cp_layout.setSpacing(8)

        self.preview_box = QLabel()
        self.preview_box.setFixedHeight(60)
        self.preview_box.setStyleSheet(
            "border: 1px solid #666; border-radius: 6px;"
        )

        self.sliders = {}
        for name in ["R", "G", "B", "A"]:
            row = QHBoxLayout()

            lbl = QLabel(name)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 255)
            spin = QSpinBox()
            spin.setRange(0, 255)

            slider.valueChanged.connect(spin.setValue)
            spin.valueChanged.connect(slider.setValue)
            slider.valueChanged.connect(self.on_color_change)

            row.addWidget(lbl)
            row.addWidget(slider, 1)
            row.addWidget(spin)

            cp_layout.addLayout(row)
            self.sliders[name] = slider

        cp_layout.addWidget(self.preview_box)
        cp_layout.addStretch()

        # ── IMAGE PAGE ─────────────────────
        self.image_editor = ImageEditor(self.state)
        self.image_editor.imageChanged.connect(
            self.colorChanged.emit
        )

        self.stack.addWidget(self.color_page)
        self.stack.addWidget(self.image_editor)

        # ── MAIN LAYOUT ────────────────────
        main = QHBoxLayout()
        main.addWidget(self.section_list)
        main.addWidget(self.stack, 1)

        root.addLayout(main)

        # Select first section by default
        self.section_list.setCurrentRow(0)

    # ── SECTION CHANGE ────────────────────
    def on_section_changed(self, current, previous):
        if not current:
            return

        key, stype = current.data(Qt.UserRole)
        self.current_key = key

        if stype == SectionType.COLOR:
            self.stack.setCurrentWidget(self.color_page)
            self.load_color(key)
        else:
            self.stack.setCurrentWidget(self.image_editor)
            self.image_editor.set_section(key)

    # ── COLOR LOGIC ───────────────────────
    def load_color(self, key):
        color = self.state.get_color(key)

        for s in self.sliders.values():
            s.blockSignals(True)

        self.sliders["R"].setValue(color.red())
        self.sliders["G"].setValue(color.green())
        self.sliders["B"].setValue(color.blue())
        self.sliders["A"].setValue(color.alpha())

        for s in self.sliders.values():
            s.blockSignals(False)

        self.update_preview(color)

    def on_color_change(self):
        if not self.current_key:
            return

        color = QColor(
            self.sliders["R"].value(),
            self.sliders["G"].value(),
            self.sliders["B"].value(),
            self.sliders["A"].value(),
        )

        self.state.set_color(self.current_key, color)
        self.update_preview(color)
        self.colorChanged.emit()

    def update_preview(self, color):
        self.preview_box.setStyleSheet(
            f"""
            background-color: rgba(
                {color.red()},
                {color.green()},
                {color.blue()},
                {color.alpha()}
            );
            border: 1px solid #666;
            border-radius: 6px;
            """
        )

    # ── FORCE UI RELOAD (USED BY RESET / IMPORT) ──
    def reload_all(self):
        current = self.section_list.currentItem()
        if not current:
            return

        key, stype = current.data(Qt.UserRole)

        if stype == SectionType.COLOR:
            self.load_color(key)
        else:
            self.image_editor.set_section(key)
