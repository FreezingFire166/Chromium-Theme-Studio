from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QFontMetrics, QBrush, QPen
from PySide6.QtCore import QTimer, Qt, QRect

class PreviewRenderer:
    def __init__(self, window):
        self.w = window 
        self._pixmap_cache = {}
        self._render_timer = QTimer(); self._render_timer.setSingleShot(True)
        self._render_timer.timeout.connect(self._do_image_render)

    def c(self, key, default):
        d = self.w.theme_data 
        hex_val = d.get(key, default)
        if not hex_val or not hex_val.startswith("#") or len(hex_val) != 9: return QColor(default)
        try:
            r = int(hex_val[1:3], 16); g = int(hex_val[3:5], 16); b = int(hex_val[5:7], 16); a = int(hex_val[7:9], 16)
            return QColor(r, g, b, a)
        except ValueError: return QColor(default)

    def apply_theme(self):
        self._do_image_render()

    def apply_image(self, mode=None): self._do_image_render()

    def _do_image_render(self):
        self._render_ntp_layer()
        self._render_ui_layer()

    def _render_ntp_layer(self):
        is_incognito = self.w.chk_incognito.isChecked()
        if is_incognito:
            self.w.bg_img.hide()
            return
            
        mode = "ntp_image"
        
        # 1. Prepare Background Color
        col_bg = self.c("ntp_background", "#00000000") 
        
        canvas_w = self.w.canvas.width(); canvas_h = self.w.canvas.height()
        target_pix = QPixmap(canvas_w, canvas_h)
        target_pix.fill(col_bg) 

        # 2. Draw NTP Image
        path = self.w.theme_data.get(mode)
        if path:
            if path not in self._pixmap_cache: self._pixmap_cache[path] = QPixmap(path)
            pix = self._pixmap_cache[path]
            if not pix.isNull():
                props = self.w.theme_data.get(mode + "_properties")
                if mode == self.w.current_edit_mode:
                    scale = self.w.sl_scale.value() / 100.0; off_x = self.w.sl_x.value(); off_y = self.w.sl_y.value()
                elif props:
                    scale = props.get('scale', 100) / 100.0; off_x = props.get('x', 0); off_y = props.get('y', 0)
                else:
                    scale = max(self.w.canvas.width() / pix.width(), self.w.canvas.height() / pix.height()); off_x = 0; off_y = 0

                new_w = max(1, int(pix.width() * scale)); new_h = max(1, int(pix.height() * scale))
                scaled_pix = pix.scaled(new_w, new_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                draw_x = (canvas_w - new_w) // 2 + off_x; draw_y = (canvas_h - new_h) // 2 + off_y
                
                p = QPainter(target_pix); p.setRenderHint(QPainter.Antialiasing); p.setRenderHint(QPainter.SmoothPixmapTransform)
                p.drawPixmap(int(draw_x), int(draw_y), scaled_pix); p.end()
        
        self.w.bg_img.resize(canvas_w, canvas_h); self.w.bg_img.setPixmap(target_pix); self.w.bg_img.show(); self.w.bg_img.move(0, 0)

    def _render_ui_layer(self):
        w = self.w.canvas.width(); h = self.w.canvas.height()
        target_pix = QPixmap(w, h); target_pix.fill(Qt.transparent)
        p = QPainter(target_pix)
        p.setRenderHint(QPainter.Antialiasing); p.setRenderHint(QPainter.SmoothPixmapTransform)

        # -- Metrics & Setup --
        is_incognito = self.w.chk_incognito.isChecked()
        browser_mode = self.w.browser_combo.currentText() 
        
        frame_h = 56 if browser_mode != "Edge" else 48
        tabs_h = 38
        top_area_h = frame_h + tabs_h
        toolbar_h = 44
        
        k_frame = "frame_incognito" if is_incognito else "frame"
        k_inactive_tab = "inactive_tab_incognito" if is_incognito else "inactive_tab"
        
        col_frame = self.c(k_frame, '#CC0000FF')
        col_active_tab = self.c('active_tab', '#FFFFFFFF')
        col_inactive_tab = self.c(k_inactive_tab, '#E68A8AFF')
        col_tab_text = self.c('tab_text', '#000000FF')
        col_inactive_text = self.c('inactive_tab_text', '#555555FF')
        col_toolbar = self.c('toolbar', '#FFFFFFFF')
        col_toolbar_text = self.c('toolbar_text', '#333333FF')
        col_bookmark_text = self.c('bookmark_text', '#555555FF')
        col_button_tint = self.c('button_tint', '#555555FF') # NEW: for Nav buttons
        
        # Omnibox Colors: Auto-select based on incognito state
        if is_incognito:
            col_omni_bg = self.c('omnibox_background_incognito', '#3C4043FF')
            col_omni_text = self.c('omnibox_text_incognito', '#E8EAEDFF')
        else:
            col_omni_bg = self.c('omnibox_background', '#F0F0F0FF')
            col_omni_text = self.c('omnibox_text', '#000000FF')

        # 1. Background Color for Top Area
        p.fillRect(0, 0, w, top_area_h, col_frame)
        
        # 2. Frame Image
        k_frame_img = "frame_image_incognito" if is_incognito else "frame_image"
        img_path = self.w.theme_data.get(k_frame_img)
        has_image = False
        
        if img_path:
            if img_path not in self._pixmap_cache: self._pixmap_cache[img_path] = QPixmap(img_path)
            pix = self._pixmap_cache[img_path]
            if not pix.isNull():
                has_image = True
                props = self.w.theme_data.get(k_frame_img + "_properties")
                if k_frame_img == self.w.current_edit_mode:
                    scale = self.w.sl_scale.value() / 100.0; off_x = self.w.sl_x.value(); off_y = self.w.sl_y.value()
                elif props:
                    scale = props.get('scale', 100) / 100.0; off_x = props.get('x', 0); off_y = props.get('y', 0)
                else:
                    scale = 120.0 / pix.height(); off_x = 0; off_y = 0
                
                scaled = pix.scaled(int(pix.width() * scale), int(pix.height() * scale), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                sy = max(0, (scaled.height() - 120) // 2)
                src_rect = QRect(max(0, off_x), max(0, sy + off_y), w, top_area_h)
                p.drawPixmap(QRect(0, 0, w, top_area_h), scaled, src_rect)

        # 3. Tab Strip Background
        tabs_y = frame_h
        if not has_image:
             p.fillRect(0, tabs_y, w, tabs_h, col_frame.darker(108))

        font = QFont("Segoe UI", 9); bold = QFont("Segoe UI", 9, QFont.Bold)
        tab_w = 200 if browser_mode == "Edge" else 140
        tab_h = tabs_h - 8
        tab_y = tabs_y + 4
        fm = QFontMetrics(font)
        radius = 4 if browser_mode == "Edge" else 8

        # Inactive Tab
        p.setFont(font)
        x = 20
        rect = QRect(x, tab_y, tab_w, tab_h)
        p.setPen(Qt.NoPen); p.setBrush(col_inactive_tab)
        p.drawRoundedRect(rect, radius, radius)
        p.setPen(col_inactive_text)
        ty = rect.y() + (rect.height() + fm.ascent() - fm.descent()) // 2
        p.drawText(rect.x() + 14, ty, "Inactive Tab")

        # Active Tab
        x += tab_w + 10
        rect = QRect(x, tab_y, tab_w, tab_h)
        if browser_mode == "Chrome":
             p.setBrush(col_active_tab)
             p.drawRoundedRect(rect.x(), rect.y(), rect.width(), rect.height() + 5, radius, radius)
        else:
             p.setBrush(col_active_tab)
             p.drawRoundedRect(rect, radius, radius)

        p.setFont(bold); p.setPen(col_tab_text)
        ty = rect.y() + (rect.height() + fm.ascent() - fm.descent()) // 2
        p.drawText(rect.x() + 14, ty, "Active Tab")

        # 4. Toolbar
        toolbar_y = tabs_y + tabs_h
        p.fillRect(0, toolbar_y, w, toolbar_h, col_toolbar)

        # URL Bar (Search Bar)
        p.setFont(font); 
        
        # USE BUTTON TINT FOR ARROWS
        p.setPen(col_button_tint)
        p.drawText(15, toolbar_y + 28, "<")
        p.drawText(40, toolbar_y + 28, ">")
        
        url_rect = QRect(70, toolbar_y + 8, w - 140, toolbar_h - 16)
        
        p.setBrush(col_omni_bg)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(url_rect, 14, 14)
        
        p.setPen(col_omni_text)
        
        text_x = url_rect.x() + 12
        if browser_mode == "Brave":
            p.drawText(text_x, url_rect.y() + 20, "🦁")
            text_x += 20 

        p.drawText(text_x, url_rect.y() + 20, "https://example.com")

        # 5. Bookmarks
        by = toolbar_y + toolbar_h + 22
        p.setPen(col_bookmark_text)
        bx = 20
        for name in ["Gmail", "YouTube", "Maps"]:
            p.drawText(bx, by, name)
            bx += 80

        p.end()
        self.w.ui_layer.setPixmap(target_pix)
        self.w.ui_layer.resize(w, h)
        self.w.ui_layer.show()