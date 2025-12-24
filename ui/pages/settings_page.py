from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QCheckBox, 
                               QLineEdit, QScrollArea, QComboBox, QFormLayout, QGroupBox, 
                               QTabWidget, QColorDialog, QHBoxLayout, QSlider)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from ui.controls.settings_toggle import SettingsToggle

class SettingsPage(QWidget):
    def __init__(self, persistent_settings, parent=None):
        super().__init__(parent)
        self.p_settings = persistent_settings
        
        main_layout = QVBoxLayout(self); main_layout.setContentsMargins(10, 10, 10, 10)
        
        lbl_title = QLabel("Settings"); lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1A73E8; margin-bottom: 10px;")
        main_layout.addWidget(lbl_title)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tab_general = QWidget(); self.tabs.addTab(self.tab_general, "General"); self.init_general_tab()
        self.tab_appearance = QWidget(); self.tabs.addTab(self.tab_appearance, "Appearance"); self.init_appearance_tab()
        self.tab_advanced = QWidget(); self.tabs.addTab(self.tab_advanced, "Advanced"); self.init_advanced_tab()

    def init_general_tab(self):
        layout = QVBoxLayout(self.tab_general); layout.setSpacing(20)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget(); l = QVBoxLayout(content); l.setSpacing(20)
        
        grp_gen = self.create_group("General Behavior"); form = QFormLayout()
        self.inp_author = QLineEdit(self.p_settings.get_default_author())
        self.inp_author.textChanged.connect(self.p_settings.set_default_author)
        form.addRow(self.lbl("Default Author:"), self.inp_author)
        
        self.combo_fmt = QComboBox(); self.combo_fmt.addItems(["ZIP Archive", "CRX Package"])
        self.combo_fmt.setCurrentText(self.p_settings.get_export_format())
        self.combo_fmt.currentTextChanged.connect(self.p_settings.set_export_format)
        form.addRow(self.lbl("Default Export:"), self.combo_fmt)
        l.addWidget(grp_gen); grp_gen.layout().addLayout(form)

        grp_prev = self.create_group("Preview"); form = QFormLayout()
        self.combo_target = QComboBox(); self.combo_target.addItems(["Chrome", "Brave", "Edge"])
        self.combo_target.setCurrentText(self.p_settings.get_preview_target())
        self.combo_target.currentTextChanged.connect(self.p_settings.set_preview_target)
        form.addRow(self.lbl("Browser:"), self.combo_target)
        l.addWidget(grp_prev); grp_prev.layout().addLayout(form)

        grp_pre = self.create_group("Workflow"); form = QFormLayout()
        self.chk_preset = QCheckBox("Auto-apply last used preset")
        self.chk_preset.setChecked(self.p_settings.get_auto_preset())
        self.chk_preset.stateChanged.connect(lambda s: self.p_settings.set_auto_preset(bool(s)))
        form.addRow(self.lbl("Startup:"), self.chk_preset)
        l.addWidget(grp_pre); grp_pre.layout().addLayout(form)

        l.addStretch(); scroll.setWidget(content); layout.addWidget(scroll)

    def init_appearance_tab(self):
        layout = QVBoxLayout(self.tab_appearance); layout.setSpacing(20)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget(); l = QVBoxLayout(content); l.setSpacing(20)

        grp_ui = self.create_group("Theme & Canvas"); form = QFormLayout()
        self.toggle_dark = SettingsToggle()
        self.toggle_dark.setChecked(self.p_settings.get_dark_mode())
        form.addRow(self.lbl("Dark Mode:"), self.toggle_dark)
        
        self.combo_bg = QComboBox(); self.combo_bg.addItems(["Checkerboard", "Solid Dark", "Solid Light"])
        bg_map = {"checker": 0, "dark": 1, "light": 2}
        self.combo_bg.setCurrentIndex(bg_map.get(self.p_settings.get_canvas_bg(), 0))
        self.combo_bg.currentIndexChanged.connect(self._on_bg_changed)
        form.addRow(self.lbl("Canvas Background:"), self.combo_bg)
        l.addWidget(grp_ui); grp_ui.layout().addLayout(form)

        grp_spot = self.create_group("Spotlight FX"); form = QFormLayout()
        self.chk_spot = QCheckBox("Enable Spotlight")
        self.chk_spot.setChecked(self.p_settings.get_spotlight_enabled())
        self.chk_spot.stateChanged.connect(lambda s: self.p_settings.set_spotlight_enabled(bool(s)))
        form.addRow(self.lbl("Status:"), self.chk_spot)

        self.slider_rad = self.create_slider(20, 200, self.p_settings.get_spot_radius(), self._on_radius_change)
        form.addRow(self.lbl("Beam Radius:"), self.slider_rad)
        
        self.slider_op = self.create_slider(10, 100, int(self.p_settings.get_spot_opacity()*100), self._on_opacity_change)
        form.addRow(self.lbl("Intensity %:"), self.slider_op)

        self.slider_str = self.create_slider(1, 10, int(self.p_settings.get_spot_strength()*100), self._on_strength_change)
        form.addRow(self.lbl("Magnetic Pull:"), self.slider_str)

        c_layout = QHBoxLayout()
        self.btn_lb = self.create_color_btn(self.p_settings.get_spot_light_base(), lambda: self._pick_color("lb"))
        self.btn_la = self.create_color_btn(self.p_settings.get_spot_light_active(), lambda: self._pick_color("la"))
        self.btn_db = self.create_color_btn(self.p_settings.get_spot_dark_base(), lambda: self._pick_color("db"))
        self.btn_da = self.create_color_btn(self.p_settings.get_spot_dark_active(), lambda: self._pick_color("da"))
        
        l_light = QVBoxLayout(); l_light.addWidget(self.lbl("Light Mode (Base/Active)")); h1 = QHBoxLayout(); h1.addWidget(self.btn_lb); h1.addWidget(self.btn_la); l_light.addLayout(h1)
        l_dark = QVBoxLayout(); l_dark.addWidget(self.lbl("Dark Mode (Base/Active)")); h2 = QHBoxLayout(); h2.addWidget(self.btn_db); h2.addWidget(self.btn_da); l_dark.addLayout(h2)
        
        c_layout.addLayout(l_light); c_layout.addLayout(l_dark)
        grp_spot.layout().addLayout(form); grp_spot.layout().addLayout(c_layout)
        l.addWidget(grp_spot)
        
        grp_safe = self.create_group("Guides"); form = QFormLayout()
        self.chk_guides = QCheckBox("Show Safe Areas")
        self.chk_guides.setChecked(self.p_settings.get_show_guides())
        self.chk_guides.stateChanged.connect(lambda s: self.p_settings.set_show_guides(bool(s)))
        form.addRow(self.lbl("Overlay:"), self.chk_guides)
        l.addWidget(grp_safe); grp_safe.layout().addLayout(form)

        l.addStretch(); scroll.setWidget(content); layout.addWidget(scroll)

    def init_advanced_tab(self):
        layout = QVBoxLayout(self.tab_advanced); layout.setSpacing(20)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget(); l = QVBoxLayout(content); l.setSpacing(20)

        grp_adv = self.create_group("System"); form = QFormLayout()
        self.chk_logs = QCheckBox("Verbose Logs")
        self.chk_logs.setChecked(self.p_settings.get_verbose_logs())
        self.chk_logs.stateChanged.connect(lambda s: self.p_settings.set_verbose_logs(bool(s)))
        form.addRow(self.lbl("Debug:"), self.chk_logs)
        
        self.chk_json = QCheckBox("Manual JSON Override")
        self.chk_json.setChecked(self.p_settings.get_json_override())
        self.chk_json.stateChanged.connect(lambda s: self.p_settings.set_json_override(bool(s)))
        form.addRow(self.lbl("Manifest:"), self.chk_json)
        l.addWidget(grp_adv); grp_adv.layout().addLayout(form)

        grp_ab = self.create_group("Reset"); v = QVBoxLayout()
        btn_reset = QPushButton("Reset All Settings"); btn_reset.setProperty("class", "dangerBtn")
        btn_reset.clicked.connect(lambda: self.p_settings.settings.clear())
        v.addWidget(btn_reset); grp_ab.layout().addLayout(v)
        l.addWidget(grp_ab)

        l.addStretch(); scroll.setWidget(content); layout.addWidget(scroll)

    def create_group(self, title):
        frame = QGroupBox(title); l = QVBoxLayout(frame); l.setContentsMargins(15, 20, 15, 15)
        return frame

    # --- FIX: Removed manual coloring. Relies on Stylesheet now. ---
    def lbl(self, text):
        return QLabel(text)

    def create_slider(self, min_v, max_v, val, callback):
        s = QSlider(Qt.Horizontal); s.setRange(min_v, max_v); s.setValue(val)
        s.valueChanged.connect(callback)
        return s

    def create_color_btn(self, color_str, callback):
        b = QPushButton(); b.setFixedSize(50, 30); b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet(f"background-color: {color_str}; border: 1px solid #888; border-radius: 4px;")
        b.clicked.connect(callback)
        return b

    def _on_bg_changed(self, index):
        val = ["checker", "dark", "light"][index]
        self.p_settings.set_canvas_bg(val)
    
    def _on_radius_change(self, val): self.p_settings.set_spot_radius(val); self.update_spotlight_signal()
    def _on_strength_change(self, val): self.p_settings.set_spot_strength(val/100.0); self.update_spotlight_signal()
    def _on_opacity_change(self, val): self.p_settings.set_spot_opacity(val/100.0); self.update_spotlight_signal()
    
    def _pick_color(self, key):
        c = QColorDialog.getColor()
        if c.isValid():
            hex_c = c.name(QColor.HexArgb)
            if key == "lb": self.p_settings.set_spot_light_base(hex_c); self.btn_lb.setStyleSheet(f"background-color: {hex_c};")
            elif key == "la": self.p_settings.set_spot_light_active(hex_c); self.btn_la.setStyleSheet(f"background-color: {hex_c};")
            elif key == "db": self.p_settings.set_spot_dark_base(hex_c); self.btn_db.setStyleSheet(f"background-color: {hex_c};")
            elif key == "da": self.p_settings.set_spot_dark_active(hex_c); self.btn_da.setStyleSheet(f"background-color: {hex_c};")
            self.update_spotlight_signal()

    def update_spotlight_signal(self):
        mw = self.window()
        if hasattr(mw, 'apply_settings_changes'):
            mw.apply_settings_changes()