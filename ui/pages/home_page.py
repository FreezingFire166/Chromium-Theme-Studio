import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox, QButtonGroup, QSizePolicy, QColorDialog, QFileDialog, QStackedWidget)
from PySide6.QtGui import QPixmap, QColor, QIntValidator
from PySide6.QtCore import Qt, Signal

from render.preview_renderer import PreviewRenderer
from ui.controls.smart_slider import SmartSlider
from ui.controls.gradient_slider import GradientSlider
from ui.controls.theme_toggle import ThemeToggle
from ui.menu.bloom_tile import BloomTile
from utils.color_utils import get_color_name

class FullscreenWindow(QWidget):
    closed_signal = Signal()
    def __init__(self, content, parent=None):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #18191A;")
        self.layout = QVBoxLayout(self); self.layout.setContentsMargins(0,0,0,0)
        self.content = content; self.layout.addWidget(self.content)
        self.btn_exit = QPushButton("×", self); self.btn_exit.setFixedSize(60, 60); self.btn_exit.setCursor(Qt.PointingHandCursor)
        self.btn_exit.setStyleSheet("QPushButton { background-color: rgba(220, 20, 60, 0.9); color: white; border-radius: 30px; font-size: 32px; font-weight: bold; border: 2px solid white; } QPushButton:hover { background-color: red; }")
        self.btn_exit.clicked.connect(self.close); self.btn_exit.move(self.screen().size().width() - 80, 20)
    
    def resizeEvent(self, event): self.btn_exit.move(self.width() - 80, 20); super().resizeEvent(event)
    def keyPressEvent(self, event): 
        if event.key() == Qt.Key_Escape: self.close()
    def closeEvent(self, event): self.closed_signal.emit(); super().closeEvent(event)

class MenuHeader(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True); self.setChecked(False); self.setFixedHeight(35); self.setCursor(Qt.PointingHandCursor); self.setProperty("class", "menuHeader")

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window 
        self.current_base_mode = "frame"; self.current_edit_mode = "frame"; self.fs_window = None
        outer_layout = QVBoxLayout(self); outer_layout.addStretch()
        self.layout_inner = QHBoxLayout(); self.layout_inner.setContentsMargins(0,0,0,0); self.layout_inner.setSpacing(0)
        self.init_ui()
        outer_layout.addLayout(self.layout_inner); outer_layout.addStretch()
        self.renderer = PreviewRenderer(self)
    
    @property
    def theme_data(self): return self.mw.theme_data
    @property
    def p_settings(self): return self.mw.p_settings
        
    def init_ui(self):
        col_prev_container = QWidget(); self.col_prev_layout = QVBoxLayout(col_prev_container); self.col_prev_layout.setContentsMargins(20, 20, 20, 20); self.col_prev_layout.setSpacing(15)
        hdr = QHBoxLayout()
        self.browser_combo = QComboBox(); self.browser_combo.addItems(["Chrome", "Brave", "Edge"]); self.browser_combo.currentIndexChanged.connect(self.update_browser_skin); self.browser_combo.setFixedWidth(120); self.browser_combo.setFixedHeight(30)
        self.chk_incognito = QCheckBox("Incognito Mode"); self.chk_incognito.setStyleSheet("font-weight: bold; color: #5F6368;"); self.chk_incognito.toggled.connect(self.on_incognito_toggled)
        hdr.addStretch(); hdr.addWidget(QLabel("Preview Mode:")); hdr.addWidget(self.browser_combo); hdr.addSpacing(10); hdr.addWidget(self.chk_incognito)
        self.theme_toggle = ThemeToggle(); self.theme_toggle.clicked.connect(self.mw.toggle_main_toggle); hdr.addWidget(self.theme_toggle); self.col_prev_layout.addLayout(hdr)

        self.canvas_container = QFrame(); self.canvas_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas_center = QVBoxLayout(self.canvas_container); canvas_center.setAlignment(Qt.AlignCenter)
        self.canvas = QFrame(); self.canvas.setFixedSize(1000, 562); self.canvas.setStyleSheet("background-color: #CC0000; border-radius: 6px;")
        canvas_inner = QVBoxLayout(self.canvas); canvas_inner.setContentsMargins(0,0,0,0)
        self.frame_img_layer = QLabel(self.canvas); self.frame_img_layer.setFixedSize(1000, 120); self.frame_img_layer.lower()
        self.ui_layer = QFrame(); self.ui_layer.setStyleSheet("background: transparent;")
        ui_lay = QVBoxLayout(self.ui_layer); ui_lay.setContentsMargins(0,0,0,0); ui_lay.setSpacing(0)
        tab_row = QHBoxLayout(); tab_row.setContentsMargins(8, 8, 0, 0); tab_row.setAlignment(Qt.AlignLeft); tab_row.setSpacing(0)
        self.lbl_inactive = QLabel("Inactive Tab"); self.lbl_active = QLabel("Active Tab")
        tab_row.addWidget(self.lbl_inactive); tab_row.addWidget(self.lbl_active); ui_lay.addLayout(tab_row)
        self.toolbar = QFrame(); self.toolbar.setFixedHeight(80); tb_layout = QVBoxLayout(self.toolbar); tb_layout.setContentsMargins(0,0,0,0); tb_layout.setSpacing(0)
        top_strip = QHBoxLayout(); top_strip.setContentsMargins(15, 8, 15, 0); top_strip.setSpacing(12)
        self.btn_back = QLabel("<"); self.btn_fwd = QLabel(">")
        self.url_box = QFrame(); self.url_box.setFixedHeight(34); url_lay = QHBoxLayout(self.url_box); url_lay.setContentsMargins(12,0,12,0)
        self.lion_icon = QLabel("🦁"); self.lion_icon.hide(); self.url_text = QLabel("https://example.com")
        url_lay.addWidget(self.lion_icon); url_lay.addWidget(self.url_text); url_lay.addStretch()
        top_strip.addWidget(self.btn_back); top_strip.addWidget(self.btn_fwd); top_strip.addWidget(self.url_box, 1)
        tb_layout.addLayout(top_strip); bm_strip = QHBoxLayout(); bm_strip.setContentsMargins(15, 4, 15, 8); bm_strip.setSpacing(10)
        self.bms = [QLabel("Gmail"), QLabel("YouTube"), QLabel("Maps")]; 
        for b in self.bms: bm_strip.addWidget(b)
        bm_strip.addStretch(); tb_layout.addLayout(bm_strip); ui_lay.addWidget(self.toolbar); ui_lay.addStretch()
        self.guides_layer = QFrame(self.ui_layer); self.guides_layer.setStyleSheet("border: 2px dashed rgba(255, 0, 0, 0.4); background: transparent;"); self.guides_layer.setGeometry(0, 0, 1000, 562); self.guides_layer.setAttribute(Qt.WA_TransparentForMouseEvents); self.guides_layer.raise_()
        self.bg_img = QLabel(self.canvas); self.bg_img.setScaledContents(False); self.bg_img.lower(); self.bg_img.resize(0,0)
        self.frame_img_layer.raise_(); canvas_inner.addWidget(self.ui_layer); canvas_center.addWidget(self.canvas); self.col_prev_layout.addWidget(self.canvas_container)
        
        res_row = QHBoxLayout(); res_row.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        b1 = QPushButton("Default (16:9)"); b1.clicked.connect(lambda: self.set_aspect_ratio(16, 9))
        b2 = QPushButton("Ultrawide (21:9)"); b2.clicked.connect(lambda: self.set_aspect_ratio(21, 9))
        b3 = QPushButton("Custom..."); b3.clicked.connect(self.toggle_custom_res_inputs)
        self.res_custom_container = QWidget(); self.res_custom_container.hide()
        rc_lay = QVBoxLayout(self.res_custom_container); rc_lay.setContentsMargins(0,0,0,0); rc_lay.setSpacing(2); rc_lay.setAlignment(Qt.AlignTop) 
        self.res_w_input = QLineEdit("1000"); self.res_w_input.setPlaceholderText("W"); self.res_w_input.setFixedWidth(50)
        self.res_h_input = QLineEdit("562"); self.res_h_input.setPlaceholderText("H"); self.res_h_input.setFixedWidth(50)
        self.res_w_input.setValidator(QIntValidator(100, 5000)); self.res_h_input.setValidator(QIntValidator(100, 5000))
        self.res_w_input.editingFinished.connect(self.apply_custom_res); self.res_h_input.editingFinished.connect(self.apply_custom_res)
        rc_lay.addWidget(self.res_w_input); rc_lay.addWidget(self.res_h_input)
        for b in [b1, b2, b3]: b.setProperty("class", "resBtn"); res_row.addWidget(b)
        res_row.addWidget(self.res_custom_container); res_row.addStretch()
        btn_fs = QPushButton("⛶"); btn_fs.setFixedSize(35,35); btn_fs.clicked.connect(self.toggle_fullscreen)
        btn_fs.setStyleSheet("font-size: 16px; font-weight: bold; border-radius: 4px; border: 1px solid #888;"); res_row.addWidget(btn_fs)
        self.col_prev_layout.addLayout(res_row); self.layout_inner.addWidget(col_prev_container, 1)

        self.menu_frame = QFrame(); self.menu_frame.setFixedWidth(220)
        self.menu_layout = QVBoxLayout(self.menu_frame); self.menu_layout.setAlignment(Qt.AlignTop); self.menu_layout.setSpacing(8); self.menu_layout.setContentsMargins(15, 20, 15, 20)
        self.btn_group = QButtonGroup(); self.btn_group.setExclusive(True); self.menu_tiles = []; self.menu_map = {} 
        self.add_menu_item("Frame", "frame")
        tab_group = self.add_menu_group("Tabs"); self.add_sub_item(tab_group, "Active Tab", "active_tab"); self.add_sub_item(tab_group, "Active Text", "tab_text")
        self.add_sub_item(tab_group, "Inactive Tab", "inactive_tab"); self.add_sub_item(tab_group, "Inactive Text", "inactive_tab_text")
        tb_group = self.add_menu_group("Toolbar"); self.add_sub_item(tb_group, "Background", "toolbar"); self.add_sub_item(tb_group, "Text", "toolbar_text")
        self.add_sub_item(tb_group, "Buttons", "button_tint"); self.add_sub_item(tb_group, "Bookmarks", "bookmark_text")
        img_group = self.add_menu_group("Images"); self.add_sub_item(img_group, "Frame Image", "frame_image"); self.add_sub_item(img_group, "NTP Image", "ntp_image")
        self.menu_layout.addStretch(); self.layout_inner.addWidget(self.menu_frame)

        self.ctrl_frame = QFrame(); self.ctrl_frame.setFixedWidth(320)
        ctrl_lay = QVBoxLayout(self.ctrl_frame); ctrl_lay.setContentsMargins(20, 0, 20, 20); ctrl_lay.setAlignment(Qt.AlignTop); ctrl_lay.addSpacing(20)
        self.stack = QStackedWidget()
        pg_color = QWidget(); l_col = QVBoxLayout(pg_color); l_col.setAlignment(Qt.AlignTop); l_col.setContentsMargins(0,0,0,0)
        l_col.addWidget(QLabel("CURRENT COLOR", objectName="sectionHeader"))
        row_prev = QHBoxLayout(); row_prev.setSpacing(10)
        self.color_preview_box = QLabel(); self.color_preview_box.setFixedSize(60, 60); self.color_preview_box.setStyleSheet("background-color: #CC0000; border: 1px solid #ccc; border-radius: 4px;")
        info_col = QVBoxLayout(); info_col.setContentsMargins(0,0,0,0)
        self.lbl_color_name = QLabel("Red"); self.lbl_color_name.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.hex_input = QLineEdit("#CC0000"); self.hex_input.textChanged.connect(self.hex_changed)
        info_col.addWidget(self.lbl_color_name); info_col.addWidget(self.hex_input)
        btn_pick = QPushButton("Pick"); btn_pick.setFixedHeight(60); btn_pick.setProperty("class", "resBtn"); btn_pick.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed); btn_pick.clicked.connect(self.open_color_dialog)
        row_prev.addWidget(self.color_preview_box); row_prev.addLayout(info_col); row_prev.addWidget(btn_pick); l_col.addLayout(row_prev); l_col.addSpacing(20)
        self.hue_slider = GradientSlider(Qt.Horizontal, mode="hue"); self.hue_slider.setRange(0, 359); self.hue_slider.valueChanged.connect(self.hue_changed)
        l_col.addWidget(self.hue_slider); l_col.addSpacing(15)
        self.sl_r, self.inp_r = self.make_smart_row("R", l_col); self.sl_g, self.inp_g = self.make_smart_row("G", l_col); self.sl_b, self.inp_b = self.make_smart_row("B", l_col); self.sl_a, self.inp_a = self.make_smart_row("A", l_col) 
        self.sl_r.next_slider = self.sl_g; self.sl_g.prev_slider = self.sl_r; self.sl_g.next_slider = self.sl_b; self.sl_b.prev_slider = self.sl_g; self.sl_b.next_slider = self.sl_a; self.sl_a.prev_slider = self.sl_b
        row_ur = QHBoxLayout(); row_ur.addStretch()
        btn_undo = QPushButton("Undo"); btn_undo.clicked.connect(self.mw.perform_undo); btn_undo.setProperty("class", "resBtn")
        btn_redo = QPushButton("Redo"); btn_redo.clicked.connect(self.mw.perform_redo); btn_redo.setProperty("class", "resBtn")
        row_ur.addWidget(btn_undo); row_ur.addWidget(btn_redo); l_col.addSpacing(10); l_col.addLayout(row_ur); l_col.addStretch()
        
        pg_img = QWidget(); l_img = QVBoxLayout(pg_img); l_img.setAlignment(Qt.AlignTop); l_img.setContentsMargins(0,0,0,0)
        l_img.addWidget(QLabel("IMAGE PREVIEW", objectName="sectionHeader"))
        self.mini_preview = QLabel("No Image"); self.mini_preview.setFixedSize(260, 130); self.mini_preview.setAlignment(Qt.AlignCenter); self.mini_preview.setScaledContents(True); self.mini_preview.setStyleSheet("border: 2px dashed #ccc; border-radius: 8px;")
        l_img.addWidget(self.mini_preview); l_img.addSpacing(15)
        img_btn_row = QHBoxLayout()
        btn_up = QPushButton("Select Image..."); btn_up.clicked.connect(self.upload_img); btn_up.setMinimumHeight(35)
        btn_clr = QPushButton("Remove Image"); btn_clr.clicked.connect(self.remove_img); btn_clr.setMinimumHeight(35)
        img_btn_row.addWidget(btn_up); img_btn_row.addWidget(btn_clr); l_img.addLayout(img_btn_row); l_img.addSpacing(20)
        self.sl_scale, _ = self.make_smart_row("Scale", l_img, 100, 10, 300); self.sl_x, _ = self.make_smart_row("X", l_img, 0, -1000, 1000); self.sl_y, _ = self.make_smart_row("Y", l_img, 0, -1000, 1000); l_img.addStretch()
        self.stack.addWidget(pg_color); self.stack.addWidget(pg_img); ctrl_lay.addWidget(self.stack); self.layout_inner.addWidget(self.ctrl_frame)
        if self.menu_tiles: self.menu_tiles[0].setChecked(True)

    def add_menu_item(self, label, mode_key):
        btn = BloomTile(label); btn.clicked.connect(lambda: self.set_mode(mode_key))
        self.menu_layout.addWidget(btn); self.btn_group.addButton(btn); self.menu_tiles.append(btn); self.menu_map[label] = mode_key; return btn
    def add_menu_group(self, title):
        header = MenuHeader(title); self.menu_layout.addWidget(header)
        container = QWidget(); layout = QVBoxLayout(container); layout.setContentsMargins(10, 0, 0, 10); layout.setSpacing(5); container.hide() 
        header.toggled.connect(lambda c: container.setVisible(c)); self.menu_layout.addWidget(container); return layout
    def add_sub_item(self, layout, label, mode_key):
        btn = BloomTile(label); btn.setFixedHeight(35); btn.clicked.connect(lambda: self.set_mode(mode_key))
        layout.addWidget(btn); self.btn_group.addButton(btn); self.menu_tiles.append(btn); self.menu_map[label] = mode_key 

    def set_mode(self, mode):
        self.current_base_mode = mode 
        real_mode = mode
        if self.chk_incognito.isChecked():
            if mode == "frame": real_mode = "frame_incognito"
            elif mode == "inactive_tab": real_mode = "inactive_tab_incognito"
            elif mode == "frame_image": real_mode = "frame_image_incognito"
        self.current_edit_mode = real_mode
        if "image" in real_mode: 
            self.stack.setCurrentIndex(1)
            path = self.theme_data.get(real_mode)
            self.mini_preview.setPixmap(QPixmap(path)) if path and os.path.exists(path) else self.mini_preview.setText("No Image")
        else: 
            self.stack.setCurrentIndex(0)
            c = self.color_from_rgba_hex(self.theme_data.get(real_mode, "#FFFFFFFF"))
            self.block_signals(True)
            self.hue_slider.setValue(c.hsvHue()); self.sl_r.setValue(c.red()); self.sl_g.setValue(c.green()); self.sl_b.setValue(c.blue()); self.sl_a.setValue(c.alpha())
            self.update_color_info(c); self.block_signals(False)
        for tile in self.menu_tiles:
             if self.menu_map.get(tile.text()) == self.current_base_mode: tile.setChecked(True)

    def refresh_from_data(self):
        self.set_mode(self.current_base_mode); self.renderer.apply_theme(); self.renderer.apply_image("ntp_image"); self.renderer.apply_image("frame_image")
    def on_incognito_toggled(self, checked): self.renderer.apply_theme(); self.set_mode(self.current_base_mode)
    def update_browser_skin(self): self.lion_icon.setVisible(self.browser_combo.currentText() == "Brave"); self.renderer.apply_theme()
    def load_image_from_path(self, path):
        self.p_settings.set_last_import_dir(os.path.dirname(path))
        pix = QPixmap(path)
        if self.mw.page_settings.chk_resize.isChecked() and (pix.width() > 3000 or pix.height() > 3000): pix = pix.scaled(3000, 3000, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.theme_data[self.current_edit_mode] = path; self.mini_preview.setPixmap(pix)
        if not pix.isNull():
            self.sl_scale.blockSignals(True); self.sl_x.blockSignals(True); self.sl_y.blockSignals(True)
            if "ntp_image" in self.current_edit_mode:
                scale = max(self.canvas.width() / pix.width(), self.canvas.height() / pix.height()) * 100
                self.sl_scale.setValue(int(scale)); self.sl_x.setValue(0); self.sl_y.setValue(0)
            elif "frame_image" in self.current_edit_mode:
                scale = (120 / pix.height()) * 100; self.sl_scale.setValue(int(scale))
                center_x = (self.canvas.width() - (pix.width() * (scale/100.0))) // 2
                self.sl_x.setValue(int(center_x)); self.sl_y.setValue(0)
            else: self.sl_scale.setValue(100); self.sl_x.setValue(0); self.sl_y.setValue(0)
            self.sl_scale.blockSignals(False); self.sl_x.blockSignals(False); self.sl_y.blockSignals(False)
        self.renderer.apply_image(self.current_edit_mode)

    def color_from_rgba_hex(self, text):
        if not isinstance(text, str) or not text.startswith("#") or len(text) != 9: return QColor(255, 255, 255, 255)
        try: return QColor(int(text[1:3], 16), int(text[3:5], 16), int(text[5:7], 16), int(text[7:9], 16))
        except ValueError: return QColor(255, 255, 255, 255)
    def hue_changed(self):
        c = QColor(self.sl_r.value(), self.sl_g.value(), self.sl_b.value()); h = self.hue_slider.value(); s = c.hsvSaturation() if c.hsvSaturation() > 0 else 150; v = c.value(); new_c = QColor.fromHsv(h, s, v); self.block_signals(True); self.sl_r.setValue(new_c.red()); self.sl_g.setValue(new_c.green()); self.sl_b.setValue(new_c.blue()); self.block_signals(False); self.slider_color_changed()
    def slider_color_changed(self): r, g, b, a = self.sl_r.value(), self.sl_g.value(), self.sl_b.value(), self.sl_a.value(); c = QColor(r, g, b, a); hex_val = f"#{r:02X}{g:02X}{b:02X}{a:02X}"; self.theme_data[self.current_edit_mode] = hex_val; self.update_color_info(c); self.renderer.apply_theme()
    def update_color_info(self, c): self.hex_input.blockSignals(True); self.hex_input.setText(f"#{c.red():02X}{c.green():02X}{c.blue():02X}{c.alpha():02X}"); self.hex_input.blockSignals(False); alpha_f = c.alpha() / 255.0; self.color_preview_box.setStyleSheet(f"background-color: rgba({c.red()}, {c.green()}, {c.blue()}, {alpha_f:.3f}); border: 1px solid #ccc; border-radius: 4px;"); self.lbl_color_name.setText(get_color_name(c.red(), c.green(), c.blue(), c.alpha()))
    def hex_changed(self, text):
        if len(text) != 9 or not text.startswith("#"): return
        try: r, g, b, a = int(text[1:3], 16), int(text[3:5], 16), int(text[5:7], 16), int(text[7:9], 16)
        except ValueError: return
        self.block_signals(True); self.sl_r.setValue(r); self.sl_g.setValue(g); self.sl_b.setValue(b); self.sl_a.setValue(a); self.block_signals(False); c = QColor(r, g, b, a); self.theme_data[self.current_edit_mode] = text; self.update_color_info(c); self.renderer.apply_theme(); self.mw.save_state_to_history() 
    def open_color_dialog(self):
        curr_hex = self.theme_data.get(self.current_edit_mode, "#CC0000FF"); init_c = self.color_from_rgba_hex(curr_hex)
        c = QColorDialog.getColor(init_c, self, "Pick Color", QColorDialog.ShowAlphaChannel)
        if c.isValid(): hex_val = f"#{c.red():02X}{c.green():02X}{c.blue():02X}{c.alpha():02X}"; self.mw.save_state_to_history(); self.hex_changed(hex_val)
    def upload_img(self): f, _ = QFileDialog.getOpenFileName(self, "Select Image", self.p_settings.get_last_import_dir(), "Images (*.png *.jpg)"); self.load_image_from_path(f) if f else None
    def remove_img(self): self.theme_data[self.current_edit_mode] = None; self.mini_preview.setText("No Image"); self.bg_img.hide() if self.current_edit_mode == "ntp_image" else self.frame_img_layer.hide()
    def toggle_fullscreen(self):
        if self.fs_window and self.fs_window.isVisible(): self.exit_fullscreen()
        else: self.fs_window = FullscreenWindow(self.canvas_container); self.fs_window.closed_signal.connect(self.restore_canvas); self.fs_window.showFullScreen()
    def exit_fullscreen(self):
        if self.fs_window: self.fs_window.close()
    def restore_canvas(self): self.col_prev_layout.insertWidget(1, self.canvas_container); self.fs_window = None
    def set_aspect_ratio(self, w, h): self.res_custom_container.hide(); self.canvas.setFixedSize(1000, int(1000*(h/w))); self.renderer.apply_image(self.current_edit_mode)
    def toggle_custom_res_inputs(self): self.res_custom_container.setVisible(not self.res_custom_container.isVisible()); self.apply_custom_res() if self.res_custom_container.isVisible() else None
    def apply_custom_res(self):
        try: w = int(self.res_w_input.text()); h = int(self.res_h_input.text()); self.canvas.setFixedSize(w, h); self.renderer.apply_image(self.current_edit_mode)
        except ValueError: pass
    def slider_released(self): self.mw.save_state_to_history()
    def block_signals(self, b): 
        for w in [self.sl_r, self.sl_g, self.sl_b, self.sl_a, self.hue_slider]: w.blockSignals(b)
    def make_smart_row(self, label, layout, val=0, min_v=0, max_v=255):
        row = QHBoxLayout(); lbl = QLabel(label); lbl.setFixedWidth(35); btn_l = QPushButton("<"); btn_l.setFixedSize(24, 24); btn_l.setProperty("class", "arrowBtn"); sl = SmartSlider(Qt.Horizontal); sl.setRange(min_v, max_v); sl.setValue(val); sl.sliderReleased.connect(self.slider_released); btn_r = QPushButton(">"); btn_r.setFixedSize(24, 24); btn_r.setProperty("class", "arrowBtn"); inp = QLineEdit(str(val)); inp.setFixedWidth(45); inp.setAlignment(Qt.AlignCenter)
        if max_v == 255: sl.valueChanged.connect(self.slider_color_changed); inp.setValidator(QIntValidator(0, 255))
        else: sl.valueChanged.connect(lambda: self.renderer.apply_image(self.current_edit_mode))
        sl.valueChanged.connect(lambda v: inp.setText(str(v))); inp.textChanged.connect(lambda t: sl.setValue(int(t)) if t and (t.isdigit() or t.startswith('-')) else None); btn_l.clicked.connect(lambda: sl.setValue(sl.value() - 1)); btn_r.clicked.connect(lambda: sl.setValue(sl.value() + 1))
        row.addWidget(lbl); row.addWidget(btn_l); row.addWidget(sl); row.addWidget(btn_r); row.addWidget(inp); layout.addLayout(row)
        return sl, inp