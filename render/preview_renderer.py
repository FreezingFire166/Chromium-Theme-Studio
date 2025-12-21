from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import QTimer, Qt

class PreviewRenderer:
    def __init__(self, window):
        self.w = window # This will now be the HomePage instance
        self._pixmap_cache = {}
        self._render_timer = QTimer(); self._render_timer.setSingleShot(True)
        self._render_timer.timeout.connect(self._do_image_render)

    def c(self, key, default):
        d = self.w.theme_data # Accessed via property in HomePage
        hex_val = d.get(key, default)
        if not hex_val or not hex_val.startswith("#") or len(hex_val) != 9: return hex_val 
        try:
            r = int(hex_val[1:3], 16); g = int(hex_val[3:5], 16); b = int(hex_val[5:7], 16); a = int(hex_val[7:9], 16)
            return f"rgba({r}, {g}, {b}, {a})"
        except ValueError: return default

    def apply_theme(self):
        mode = self.w.browser_combo.currentText()
        is_incognito = self.w.chk_incognito.isChecked()
        
        if mode == "Edge": radius = "4px"; margin_bottom = "0px"
        else: radius = "12px"; margin_bottom = "-1px"

        k_frame = "frame_incognito" if is_incognito else "frame"
        k_inactive_tab = "inactive_tab_incognito" if is_incognito else "inactive_tab"
        
        self.w.canvas.setStyleSheet(f"background-color: {self.c(k_frame, '#CC0000FF')}; border-radius: 6px;")
        self.w.toolbar.setStyleSheet(f"background-color: {self.c('toolbar', '#FFFFFFFF')};")
        
        self.w.lbl_active.setStyleSheet(f"""
            background-color: {self.c('active_tab', '#FFFFFFFF')}; color: {self.c('tab_text', '#000000FF')};
            padding: 8px 20px; border-top-left-radius: {radius}; border-top-right-radius: {radius};
            border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;
            font-weight: bold; font-family: 'Segoe UI', sans-serif; margin-bottom: {margin_bottom}; 
        """)
        self.w.lbl_inactive.setStyleSheet(f"""
            background-color: {self.c(k_inactive_tab, '#E68A8AFF')}; color: {self.c('inactive_tab_text', '#555555FF')};
            padding: 8px 20px; border-radius: {radius}; margin-top: 4px; margin-bottom: 4px; font-family: 'Segoe UI', sans-serif;
        """)
        tint = self.c("button_tint", "#555555FF")
        btn_style = f"font-size: 16px; font-weight: bold; color: {tint}; border-radius: 14px; padding: 4px;"
        self.w.btn_back.setStyleSheet(btn_style); self.w.btn_fwd.setStyleSheet(btn_style)
        bm_color = self.c("bookmark_text", "#555555FF")
        for b in self.w.bms: b.setStyleSheet(f"font-size: 11px; color: {bm_color}; padding: 4px 8px; border-radius: 4px;")
        tb_text = self.c("toolbar_text", "#333333FF")
        self.w.url_text.setStyleSheet(f"border: none; color: {tb_text}; font-size: 12px;")
        self._do_image_render()

    def apply_image(self, mode=None): self._do_image_render()

    def _do_image_render(self):
        is_incognito = self.w.chk_incognito.isChecked()
        k_frame_img = "frame_image_incognito" if is_incognito else "frame_image"
        self._render_layer(k_frame_img, self.w.frame_img_layer)
        if is_incognito: self.w.bg_img.hide()
        else: self._render_layer("ntp_image", self.w.bg_img)

    def _render_layer(self, mode, target_widget):
        path = self.w.theme_data.get(mode)
        if not path: target_widget.hide(); return
        if path not in self._pixmap_cache: self._pixmap_cache[path] = QPixmap(path)
        pix = self._pixmap_cache[path]
        if pix.isNull(): return

        if mode == self.w.current_edit_mode:
            scale = self.w.sl_scale.value() / 100.0; off_x = self.w.sl_x.value(); off_y = self.w.sl_y.value()
        else:
            off_x = 0; off_y = 0
            if "ntp_image" in mode: scale = max(self.w.canvas.width() / pix.width(), self.w.canvas.height() / pix.height())
            else: scale = 120.0 / pix.height() 

        new_w = max(1, int(pix.width() * scale)); new_h = max(1, int(pix.height() * scale))
        scaled_pix = pix.scaled(new_w, new_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        if "frame_image" in mode:
            canvas_w = self.w.canvas.width(); canvas_h = 120 
            target_pix = QPixmap(canvas_w, canvas_h); target_pix.fill(Qt.transparent)
            draw_x = (canvas_w - new_w) // 2 + off_x if new_w < canvas_w else off_x; draw_y = off_y
        else:
            canvas_w = self.w.canvas.width(); canvas_h = self.w.canvas.height()
            target_pix = QPixmap(canvas_w, canvas_h); target_pix.fill(Qt.transparent)
            draw_x = (canvas_w - new_w) // 2 + off_x; draw_y = (canvas_h - new_h) // 2 + off_y

        p = QPainter(target_pix); p.setRenderHint(QPainter.Antialiasing); p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.drawPixmap(int(draw_x), int(draw_y), scaled_pix); p.end()
        target_widget.resize(canvas_w, canvas_h); target_widget.setPixmap(target_pix); target_widget.show(); target_widget.move(0, 0)

    def get_processed_pixmap(self, mode):
        path = self.w.theme_data.get(mode)
        if not path: return None
        pix = QPixmap(path)
        if pix.isNull(): return None
        
        if mode == self.w.current_edit_mode:
            scale = self.w.sl_scale.value() / 100.0; off_x = self.w.sl_x.value(); off_y = self.w.sl_y.value()
        else:
            off_x = 0; off_y = 0
            if "ntp_image" in mode: scale = max(self.w.canvas.width() / pix.width(), self.w.canvas.height() / pix.height())
            else: scale = 120.0 / pix.height()

        new_w = max(1, int(pix.width() * scale)); new_h = max(1, int(pix.height() * scale))
        if "frame_image" in mode:
            canvas_w = self.w.canvas.width(); canvas_h = 120 
            draw_x = (canvas_w - new_w) // 2 + off_x if new_w < canvas_w else off_x; draw_y = off_y
        else:
            canvas_w = self.w.canvas.width(); canvas_h = self.w.canvas.height()
            draw_x = (canvas_w - new_w) // 2 + off_x; draw_y = (canvas_h - new_h) // 2 + off_y

        target_pix = QPixmap(canvas_w, canvas_h); target_pix.fill(Qt.transparent)
        p = QPainter(target_pix); p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.drawPixmap(int(draw_x), int(draw_y), new_w, new_h, pix); p.end()
        return target_pix