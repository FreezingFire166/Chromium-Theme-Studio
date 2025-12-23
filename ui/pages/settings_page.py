from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QCheckBox, QLineEdit, QScrollArea, QComboBox, QFormLayout, QGroupBox)
from PySide6.QtCore import Qt
from ui.controls.settings_toggle import SettingsToggle

class SettingsPage(QWidget):
    def __init__(self, persistent_settings, parent=None):
        super().__init__(parent)
        self.p_settings = persistent_settings
        main_layout = QVBoxLayout(self); main_layout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        content_widget = QWidget()
        self.layout = QVBoxLayout(content_widget); self.layout.setContentsMargins(40, 30, 40, 30); self.layout.setSpacing(25); self.layout.setAlignment(Qt.AlignTop)

        lbl_title = QLabel("Settings & Preferences"); lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1A73E8;"); self.layout.addWidget(lbl_title)
        self.init_general_section(); self.init_preview_section(); self.init_transparency_section()
        self.init_editor_section(); self.init_import_section(); self.init_presets_section()
        self.init_advanced_section(); self.init_ui_section(); self.init_about_section()
        self.layout.addStretch(); scroll.setWidget(content_widget); main_layout.addWidget(scroll)

    def init_general_section(self):
        grp = self.create_group("1. General Behavior"); form = QFormLayout()
        
        self.inp_author = QLineEdit(); self.inp_author.setText(self.p_settings.get_default_author())
        self.inp_author.textChanged.connect(self.p_settings.set_default_author)
        form.addRow("Default Author:", self.inp_author)
        
        self.combo_fmt = QComboBox(); self.combo_fmt.addItems(["ZIP Archive", "CRX Package"])
        self.combo_fmt.setCurrentText(self.p_settings.get_export_format())
        self.combo_fmt.currentTextChanged.connect(self.p_settings.set_export_format)
        form.addRow("Default Export:", self.combo_fmt)
        
        self.chk_inc = QCheckBox("Auto-increment Version"); self.chk_inc.setChecked(self.p_settings.get_auto_increment())
        self.chk_inc.stateChanged.connect(lambda s: self.p_settings.set_auto_increment(bool(s)))
        form.addRow("Versioning:", self.chk_inc)
        grp.layout().addLayout(form); self.layout.addWidget(grp)

    def init_preview_section(self):
        grp = self.create_group("2. Preview & Accuracy"); form = QFormLayout()
        
        self.combo_target = QComboBox(); self.combo_target.addItems(["Chrome", "Brave", "Edge"])
        self.combo_target.setCurrentText(self.p_settings.get_preview_target())
        self.combo_target.currentTextChanged.connect(self.p_settings.set_preview_target)
        form.addRow("Target Browser:", self.combo_target)
        
        self.combo_os = QComboBox(); self.combo_os.addItems(["Windows 10", "Windows 11", "macOS", "Linux"])
        self.combo_os.setCurrentText(self.p_settings.get_os_sim())
        self.combo_os.currentTextChanged.connect(self.p_settings.set_os_sim)
        form.addRow("OS Simulation:", self.combo_os)
        grp.layout().addLayout(form); self.layout.addWidget(grp)

    def init_transparency_section(self):
        grp = self.create_group("3. Transparency & Colors"); form = QFormLayout()
        
        self.chk_alpha = QCheckBox("Clamp Alpha (Prevent invisible text)")
        self.chk_alpha.setChecked(self.p_settings.get_clamp_alpha())
        self.chk_alpha.stateChanged.connect(lambda s: self.p_settings.set_clamp_alpha(bool(s)))
        form.addRow("Safety:", self.chk_alpha)
        grp.layout().addLayout(form); self.layout.addWidget(grp)

    def init_editor_section(self):
        grp = self.create_group("4. Canvas Defaults"); form = QFormLayout()
        
        self.combo_bg = QComboBox(); self.combo_bg.addItems(["Checkerboard", "Solid Dark", "Solid Light"])
        # Map stored value to index
        bg_map = {"checker": 0, "dark": 1, "light": 2}
        saved_bg = self.p_settings.get_canvas_bg()
        self.combo_bg.setCurrentIndex(bg_map.get(saved_bg, 0))
        
        self.combo_bg.currentIndexChanged.connect(self._on_bg_changed)
        form.addRow("Background:", self.combo_bg)
        
        self.chk_guides = QCheckBox("Show Safe Areas")
        self.chk_guides.setChecked(self.p_settings.get_show_guides())
        self.chk_guides.stateChanged.connect(lambda s: self.p_settings.set_show_guides(bool(s)))
        form.addRow("Guides:", self.chk_guides)
        grp.layout().addLayout(form); self.layout.addWidget(grp)

    def _on_bg_changed(self, index):
        val = ["checker", "dark", "light"][index]
        self.p_settings.set_canvas_bg(val)

    def init_import_section(self):
        grp = self.create_group("5. Import Rules"); form = QFormLayout()
        
        self.chk_resize = QCheckBox("Auto-resize huge images")
        self.chk_resize.setChecked(self.p_settings.get_resize_large())
        self.chk_resize.stateChanged.connect(lambda s: self.p_settings.set_resize_large(bool(s)))
        form.addRow("Optimization:", self.chk_resize)
        
        self.chk_meta = QCheckBox("Strip Metadata (EXIF)")
        self.chk_meta.setChecked(self.p_settings.get_strip_meta())
        self.chk_meta.stateChanged.connect(lambda s: self.p_settings.set_strip_meta(bool(s)))
        form.addRow("Privacy:", self.chk_meta)
        grp.layout().addLayout(form); self.layout.addWidget(grp)

    def init_presets_section(self):
        grp = self.create_group("6. Presets Workflow"); form = QFormLayout()
        
        self.chk_preset = QCheckBox("Auto-apply last used preset")
        self.chk_preset.setChecked(self.p_settings.get_auto_preset())
        self.chk_preset.stateChanged.connect(lambda s: self.p_settings.set_auto_preset(bool(s)))
        form.addRow("Startup:", self.chk_preset)
        grp.layout().addLayout(form); self.layout.addWidget(grp)

    def init_advanced_section(self):
        grp = self.create_group("7. Advanced (Power User)"); form = QFormLayout()
        
        self.chk_json = QCheckBox("Allow Manual JSON Override")
        self.chk_json.setChecked(self.p_settings.get_json_override())
        self.chk_json.stateChanged.connect(lambda s: self.p_settings.set_json_override(bool(s)))
        form.addRow("Manifest:", self.chk_json)
        
        self.chk_logs = QCheckBox("Verbose Export Logs")
        self.chk_logs.setChecked(self.p_settings.get_verbose_logs())
        self.chk_logs.stateChanged.connect(lambda s: self.p_settings.set_verbose_logs(bool(s)))
        form.addRow("Debugging:", self.chk_logs)
        grp.layout().addLayout(form); self.layout.addWidget(grp)

    def init_ui_section(self):
        grp = self.create_group("8. UI Preferences"); form = QFormLayout()
        
        self.toggle_dark = SettingsToggle()
        self.toggle_dark.setChecked(self.p_settings.get_dark_mode())
        form.addRow("Always Dark Mode:", self.toggle_dark)
        
        self.chk_anim = QCheckBox("Enable Animations")
        self.chk_anim.setChecked(self.p_settings.get_animations())
        self.chk_anim.stateChanged.connect(lambda s: self.p_settings.set_animations(bool(s)))
        form.addRow("Visuals:", self.chk_anim)
        grp.layout().addLayout(form); self.layout.addWidget(grp)

    def init_about_section(self):
        grp = self.create_group("9. About"); l = QVBoxLayout()
        l.addWidget(QLabel("Chromium Theme Studio V2"))
        btn_reset = QPushButton("Reset All Settings"); btn_reset.setProperty("class", "dangerBtn")
        btn_reset.clicked.connect(lambda: self.p_settings.settings.clear())
        l.addWidget(btn_reset); grp.layout().addLayout(l); self.layout.addWidget(grp)

    def create_group(self, title):
        frame = QGroupBox(title); l = QVBoxLayout(frame); l.setContentsMargins(15, 20, 15, 15)
        return frame