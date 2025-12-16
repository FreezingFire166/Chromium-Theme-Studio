import os
import json

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QSlider,
    QSpinBox,
    QComboBox
)
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt, Signal

from engine.persistence import Persistence


class ImageEditor(QWidget):
    imageChanged = Signal()

    def __init__(self, state):
        super().__init__()
        self.state = state
        self.current_key = None
        self.persistence = Persistence()
        self.fast_mode = False


        root = QVBoxLayout(self)
        root.setSpacing(10)

        # ── FILE CONTROLS ───────────────────
        file_row = QHBoxLayout()
        self.pick_btn = QPushButton("Choose Image")
        self.clear_btn = QPushButton("Clear Image")
        self.pick_btn.clicked.connect(self.pick_image)
        self.clear_btn.clicked.connect(self.clear_image)
        file_row.addWidget(self.pick_btn)
        file_row.addWidget(self.clear_btn)
        root.addLayout(file_row)

        # ── MINI SOURCE PREVIEW (STATIC) ────
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(220, 140)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet(
            "border: 1px solid #666; border-radius: 6px;"
        )
        root.addWidget(self.preview_label)

        # ── SCALE ──────────────────────────
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setRange(10, 300)
        self.scale_spin = QSpinBox()
        self.scale_spin.setRange(10, 300)
        self.scale_spin.setSuffix("%")

        self.scale_slider.valueChanged.connect(self.scale_spin.setValue)
        self.scale_spin.valueChanged.connect(self.scale_slider.setValue)
        self.scale_slider.valueChanged.connect(self.on_scale_change)

        scale_row = QHBoxLayout()
        scale_row.addWidget(QLabel("Scale"))
        scale_row.addWidget(self.scale_slider, 1)
        scale_row.addWidget(self.scale_spin)
        root.addLayout(scale_row)

        # ── OFFSET X ────────────────────────
        self.offx_slider = QSlider(Qt.Horizontal)
        self.offx_slider.setRange(-1000, 1000)
        self.offx_spin = QSpinBox()
        self.offx_spin.setRange(-1000, 1000)

        self.offx_slider.valueChanged.connect(self.offx_spin.setValue)
        self.offx_spin.valueChanged.connect(self.offx_slider.setValue)
        self.offx_slider.valueChanged.connect(self.on_offset_change)

        ox_row = QHBoxLayout()
        ox_row.addWidget(QLabel("Offset X"))
        ox_row.addWidget(self.offx_slider, 1)
        ox_row.addWidget(self.offx_spin)
        root.addLayout(ox_row)

        # ── OFFSET Y ────────────────────────
        self.offy_slider = QSlider(Qt.Horizontal)
        self.offy_slider.setRange(-1000, 1000)
        self.offy_spin = QSpinBox()
        self.offy_spin.setRange(-1000, 1000)

        self.offy_slider.valueChanged.connect(self.offy_spin.setValue)
        self.offy_spin.valueChanged.connect(self.offy_slider.setValue)
        self.offy_slider.valueChanged.connect(self.on_offset_change)

        oy_row = QHBoxLayout()
        oy_row.addWidget(QLabel("Offset Y"))
        oy_row.addWidget(self.offy_slider, 1)
        oy_row.addWidget(self.offy_spin)
        root.addLayout(oy_row)

        # ── MODE ───────────────────────────
        self.mode_combo = QComboBox()
        self.mode_combo.currentIndexChanged.connect(self.on_mode_change)
        root.addWidget(self.mode_combo)

        root.addStretch()

    # ── SECTION SWITCH ────────────────────
    def set_section(self, key):
        self.current_key = key
        self.load_state()
        self.update_mini_preview()

    # ── LOAD STATE ────────────────────────
    def load_state(self):
        if not self.current_key:
            return

        data = self.state.get_image_params(self.current_key)

        self.scale_slider.blockSignals(True)
        self.offx_slider.blockSignals(True)
        self.offy_slider.blockSignals(True)

        self.scale_slider.setValue(int(data["scale"] * 100))
        self.offx_slider.setValue(data["offset_x"])
        self.offy_slider.setValue(data["offset_y"])

        self.scale_slider.blockSignals(False)
        self.offx_slider.blockSignals(False)
        self.offy_slider.blockSignals(False)

        self.mode_combo.blockSignals(True)
        self.mode_combo.clear()

        if self.current_key == "frame_image":
            self.mode_combo.addItems(["top", "center", "bottom"])
            self.mode_combo.setCurrentText(data["anchor"])
        else:
            self.mode_combo.addItems(["cover", "contain", "original"])
            self.mode_combo.setCurrentText(data["fit"])

        self.mode_combo.blockSignals(False)

    # ── IMAGE PICKER ──────────────────────
    def pick_image(self):
        last_dir = self.persistence.get_last_image_dir()

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            last_dir if last_dir else "",
            "Images (*.png *.jpg *.jpeg *.webp)"
        )

        if not path:
            return

        self.persistence.set_last_image_dir(os.path.dirname(path))

        if not self.persistence.was_default_preset_used():
            default_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "presets",
                    "default.json"
                )
            )
            if os.path.exists(default_path):
                with open(default_path, "r", encoding="utf-8") as f:
                    self.state.apply_preset(json.load(f))
            self.persistence.mark_default_preset_used()

        self.state.set_image(self.current_key, path)
        self.update_mini_preview()
        self.imageChanged.emit()

    # ── STATIC MINI PREVIEW ───────────────
    def update_mini_preview(self):
        pix = self.state.get_cached_pixmap(self.current_key)
        if not pix:
            self.preview_label.clear()
            return

        w = self.preview_label.width()
        h = self.preview_label.height()

        scale = min(w / pix.width(), h / pix.height())
        tw = int(pix.width() * scale)
        th = int(pix.height() * scale)

        canvas = QPixmap(w, h)
        canvas.fill(Qt.transparent)

        p = QPainter(canvas)
        p.drawPixmap(
            (w - tw) // 2,
            (h - th) // 2,
            pix.scaled(
                tw, th,
                Qt.KeepAspectRatio,
                Qt.FastTransformation if self.fast_mode else Qt.SmoothTransformation            )
        )
        p.end()

        self.preview_label.setPixmap(canvas)

    # ── CLEAR ─────────────────────────────
    def clear_image(self):
        if not self.current_key:
            return

        self.state.clear_image(self.current_key)
        self.preview_label.clear()
        self.imageChanged.emit()

    # ── PARAM CHANGES ─────────────────────
    def on_scale_change(self, value):
        self.state.set_image_param(
            self.current_key, "scale", value / 100.0
        )
        self.imageChanged.emit()

    def on_offset_change(self, value):
        self.state.set_image_param(
            self.current_key, "offset_x", self.offx_slider.value()
        )
        self.state.set_image_param(
            self.current_key, "offset_y", self.offy_slider.value()
        )
        self.imageChanged.emit()

    def on_mode_change(self):
        if self.current_key == "frame_image":
            self.state.set_image_param(
                self.current_key, "anchor",
                self.mode_combo.currentText()
            )
        else:
            self.state.set_image_param(
                self.current_key, "fit",
                self.mode_combo.currentText()
            )
        self.imageChanged.emit()
