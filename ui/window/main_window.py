import os
import json
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QFileDialog, QComboBox, QMessageBox)
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtCore import Qt

from ui.menu.top_bar import TopBar
from ui.pages.settings_page import SettingsPage
from ui.pages.export_page import ExportPage
from ui.pages.help_page import HelpPage
from ui.pages.home_page import HomePage
from ui.styles.app_styles import AppStyles
from logic.export_manager import ExportManager
from utils.history_manager import HistoryManager
from utils.persistent_settings import PersistentSettings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chromium Theme Studio V2")
        self.resize(1400, 950)
        self.setAcceptDrops(True)
        self.p_settings = PersistentSettings() 
        self.default_theme_data = {
            "frame": "#CC0000FF", "toolbar": "#FFFFFFFF", "tab_text": "#000000FF", 
            "active_tab": "#FFFFFFFF", "inactive_tab": "#E68A8AFF", "inactive_tab_text": "#555555FF", 
            "button_tint": "#555555FF", "bookmark_text": "#555555FF", "toolbar_text": "#333333FF",
            "ntp_image": None, "frame_image": None, "img_scale": 100, "img_off_x": 0, "img_off_y": 0,
            "frame_incognito": "#2B2E31FF", "inactive_tab_incognito": "#3C4043FF", "frame_image_incognito": None
        }
        self.theme_data = self.default_theme_data.copy()
        self.history = HistoryManager()

        central = QWidget(); self.setCentralWidget(central)
        self.root_layout = QVBoxLayout(central); self.root_layout.setContentsMargins(0, 0, 0, 0); self.root_layout.setSpacing(0)
        
        self.top_bar = TopBar()
        self.top_bar.settings_clicked.connect(lambda active: self.switch_view(1 if active else 0))
        self.top_bar.export_clicked.connect(lambda: self.switch_view(2)) 
        self.top_bar.load_clicked.connect(self.import_theme_json)
        self.top_bar.btn_reset.clicked.connect(self.reset_theme_defaults)
        self.top_bar.btn_help.clicked.connect(lambda: self.switch_view(3))
        
        self.combo_presets = QComboBox()
        self.combo_presets.addItems(["Presets...", "Dracula", "Midnight", "Solarized", "High Contrast"])
        self.combo_presets.currentIndexChanged.connect(self.apply_preset)
        self.combo_presets.setFixedWidth(110)
        self.top_bar.group_home.layout().insertWidget(0, self.combo_presets)
        self.root_layout.addWidget(self.top_bar)

        self.content_stack = QStackedWidget()
        self.root_layout.addWidget(self.content_stack)

        self.home_page = HomePage(self) 
        self.content_stack.addWidget(self.home_page)
        self.page_settings = SettingsPage(self.p_settings)
        self.page_settings.toggle_dark.stateChanged.connect(self.toggle_dark_mode)
        self.page_settings.combo_bg.currentIndexChanged.connect(self.apply_settings_changes)
        self.page_settings.chk_guides.stateChanged.connect(self.apply_settings_changes)
        self.page_settings.combo_target.currentTextChanged.connect(self.apply_settings_changes)
        self.content_stack.addWidget(self.page_settings)
        self.page_export = ExportPage(self.p_settings)
        self.page_export.start_export_signal.connect(self.handle_export_request)
        self.content_stack.addWidget(self.page_export)
        self.page_help = HelpPage()
        self.content_stack.addWidget(self.page_help)

        QShortcut(QKeySequence("Ctrl+Z"), self).activated.connect(self.perform_undo)
        QShortcut(QKeySequence("Ctrl+Y"), self).activated.connect(self.perform_redo)
        QShortcut(QKeySequence(Qt.Key_Escape), self).activated.connect(self.home_page.exit_fullscreen)

        self.apply_light_theme()
        self.save_state_to_history()
        self.home_page.refresh_from_data()
        self.apply_settings_changes() 

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls: return
        file_path = urls[0].toLocalFile()
        if not file_path.lower().endswith(('.png', '.jpg', '.jpeg')): return
        drop_pos = self.home_page.canvas.mapFrom(self, event.position().toPoint())
        if self.home_page.canvas.rect().contains(drop_pos):
            if self.home_page.frame_img_layer.geometry().contains(drop_pos): self.home_page.set_mode("frame_image")
            else: self.home_page.set_mode("ntp_image")
            self.home_page.load_image_from_path(file_path)
            event.accept()

    def switch_view(self, index):
        self.content_stack.setCurrentIndex(index)
        if index == 0:
            self.home_page.renderer.apply_theme()
            if self.top_bar.btn_settings.isChecked():
                 self.top_bar.btn_settings.setChecked(False)
                 self.top_bar.toggle_settings_view()

    def handle_export_request(self, export_data):
        ExportManager.run_export_process(self, self.theme_data, export_data, self.p_settings, self.home_page.renderer, self.page_settings.chk_logs.isChecked())

    def import_theme_json(self):
        f, _ = QFileDialog.getOpenFileName(self, "Import Theme JSON", self.p_settings.get_last_import_dir(), "JSON Files (*.json)")
        if f:
            self.p_settings.set_last_import_dir(os.path.dirname(f)) 
            try:
                with open(f, 'r') as file:
                    data = json.load(file); self.save_state_to_history()
                    self.theme_data.update({k: v for k, v in data.items() if k in self.default_theme_data})
                    self.home_page.refresh_from_data(); QMessageBox.information(self, "Success", "Theme imported!")
            except Exception as e: QMessageBox.critical(self, "Error", f"Could not load file: {e}")

    def save_state_to_history(self): self.history.push_state(self.theme_data)
    def perform_undo(self):
        prev = self.history.undo(self.theme_data)
        if prev: self.theme_data = prev; self.home_page.refresh_from_data()
    def perform_redo(self):
        nxt = self.history.redo(self.theme_data)
        if nxt: self.theme_data = nxt; self.home_page.refresh_from_data()
    
    def apply_preset(self):
        choice = self.combo_presets.currentText()
        presets = { 
            "Dracula": {"frame": "#282a36ff", "toolbar": "#44475aff", "tab_text": "#f8f8f2ff", "active_tab": "#44475aff", "inactive_tab": "#6272a4ff", "inactive_tab_text": "#bd93f9ff", "button_tint": "#f8f8f2ff", "bookmark_text": "#f8f8f2ff", "toolbar_text": "#f8f8f2ff"}, 
            "Midnight": {"frame": "#000000ff", "toolbar": "#1a1a1aff", "tab_text": "#ffffffff", "active_tab": "#1a1a1aff", "inactive_tab": "#333333ff", "inactive_tab_text": "#888888ff", "button_tint": "#ffffffff", "bookmark_text": "#ccccccff", "toolbar_text": "#ffffffff"}, 
            "Solarized": {"frame": "#002b36ff", "toolbar": "#073642ff", "tab_text": "#839496ff", "active_tab": "#073642ff", "inactive_tab": "#586e75ff", "inactive_tab_text": "#93a1a1ff", "button_tint": "#93a1a1ff", "bookmark_text": "#93a1a1ff", "toolbar_text": "#93a1a1ff"}, 
            "High Contrast": {"frame": "#000000ff", "toolbar": "#000000ff", "tab_text": "#ffff00ff", "active_tab": "#000000ff", "inactive_tab": "#ffffff", "inactive_tab_text": "#000000ff", "button_tint": "#ffff00ff", "bookmark_text": "#ffff00ff", "toolbar_text": "#ffff00ff"} 
        }
        if choice in presets: self.save_state_to_history(); self.theme_data.update(presets[choice]); self.home_page.refresh_from_data(); self.combo_presets.setCurrentIndex(0)

    def apply_settings_changes(self):
        bg_mode = self.page_settings.combo_bg.currentText()
        if bg_mode == "Solid Dark": self.home_page.canvas.setStyleSheet("background-color: #202124; border-radius: 6px;")
        elif bg_mode == "Solid Light": self.home_page.canvas.setStyleSheet("background-color: #FFFFFF; border-radius: 6px;")
        else: self.home_page.canvas.setStyleSheet("background-color: #E0E0E0; border-radius: 6px;")
        self.home_page.guides_layer.setVisible(self.page_settings.chk_guides.isChecked())
        target = self.page_settings.combo_target.currentText().split(" ")[0]
        if self.home_page.browser_combo.currentText() != target:
             idx = self.home_page.browser_combo.findText(target, Qt.MatchStartsWith)
             if idx >= 0: self.home_page.browser_combo.setCurrentIndex(idx)
        self.home_page.renderer.apply_theme()

    def toggle_main_toggle(self):
        state = self.home_page.theme_toggle.isChecked()
        if self.page_settings.toggle_dark.isChecked() != state: self.page_settings.toggle_dark.setChecked(state)
        self.toggle_dark_mode(state)

    def toggle_dark_mode(self, checked):
        if self.home_page.theme_toggle.isChecked() != checked: self.home_page.theme_toggle.setChecked(checked)
        if checked: self.apply_dark_theme()
        else: self.apply_light_theme()

    def apply_light_theme(self):
        self.setStyleSheet(AppStyles.get_light_stylesheet())
        self.home_page.menu_frame.setObjectName("menu_frame"); self.home_page.ctrl_frame.setObjectName("ctrl_frame")
        self.top_bar.btn_title.setStyleSheet("background: transparent; border: none; font-weight: bold; font-size: 15px; text-align: left; color: #202124;")
        self.top_bar.btn_settings.setStyleSheet("background: transparent; border: none; font-size: 13px; color: #5F6368; padding: 5px; font-weight: 600;")
    def apply_dark_theme(self):
        self.setStyleSheet(AppStyles.get_dark_stylesheet())
        self.home_page.menu_frame.setObjectName("menu_frame"); self.home_page.ctrl_frame.setObjectName("ctrl_frame")
        self.top_bar.btn_title.setStyleSheet("background: transparent; border: none; font-weight: bold; font-size: 15px; text-align: left; color: #E8EAED;")
        self.top_bar.btn_settings.setStyleSheet("background: transparent; border: none; font-size: 13px; color: #B0B3B8; padding: 5px; font-weight: 600;")

    def reset_theme_defaults(self):
        if QMessageBox.question(self, "Reset", "Reset to default?") == QMessageBox.Yes: self.theme_data = self.default_theme_data.copy(); self.home_page.refresh_from_data()