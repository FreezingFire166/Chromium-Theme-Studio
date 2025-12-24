import math
from PySide6.QtWidgets import QWidget, QApplication, QAbstractButton
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF, QPoint
from PySide6.QtGui import QPainter, QBrush, QColor, QRadialGradient, QCursor, QRegion, QPainterPath

from ui.menu.bloom_tile import BloomTile

class SpotlightOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        # Default colors
        self.palette_light = {"base": QColor("#FBC02D"), "active": QColor("#F50057")}
        self.palette_dark = {"base": QColor("#FFD700"), "active": QColor("#00FFFF")}
        
        self.base_color = self.palette_light["base"]
        self.active_color = self.palette_light["active"]
        
        self.base_radius = 80.0
        self.magnetic_strength = 0.15
        self.opacity_factor = 0.85
        
        self.cursor_pos = QPointF(0, 0)
        self.light_pos = QPointF(0, 0)
        self.current_color = QColor(self.base_color)
        self.current_radius = self.base_radius
        
        self.target_path = None
        self.is_visible = True
        self.is_dark_mode = False
        
        # Track previous state to detect "Suck Out" event
        self.was_locked = False 
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_physics)
        self.timer.start(16) 

    def update_settings(self, radius, strength, opacity, c_lb, c_la, c_db, c_da):
        self.base_radius = float(radius)
        self.magnetic_strength = strength
        self.opacity_factor = opacity
        self.palette_light["base"] = QColor(c_lb)
        self.palette_light["active"] = QColor(c_la)
        self.palette_dark["base"] = QColor(c_db)
        self.palette_dark["active"] = QColor(c_da)
        self.set_theme_mode(self.is_dark_mode) 

    def set_theme_mode(self, is_dark):
        self.is_dark_mode = is_dark
        p = self.palette_dark if is_dark else self.palette_light
        self.base_color = p["base"]
        self.active_color = p["active"]

    def set_active_state(self, enabled):
        self.is_visible = enabled
        self.setVisible(enabled)
        if enabled: self.timer.start()
        else: self.timer.stop()

    def update_physics(self):
        if not self.is_visible or not self.isVisible(): return

        global_pos = QCursor.pos() 
        local_pos_int = self.mapFromGlobal(global_pos) 
        self.cursor_pos = QPointF(local_pos_int)

        hovered = self.parent().childAt(local_pos_int)
        final_target = None
        
        temp_w = hovered
        while temp_w:
            if isinstance(temp_w, BloomTile):
                final_target = temp_w; break
            elif isinstance(temp_w, QAbstractButton):
                final_target = temp_w; break
            temp_w = temp_w.parentWidget()
            if temp_w == self.parent(): break

        target_color = self.base_color
        target_pos = self.cursor_pos
        target_radius = self.base_radius
        self.target_path = None 

        apply_magnet = False
        
        if final_target:
            if isinstance(final_target, BloomTile):
                apply_magnet = True
            elif isinstance(final_target, QAbstractButton):
                # Exclusion Logic
                is_excluded = False
                p = final_target
                while p:
                    c_name = p.__class__.__name__
                    if c_name in ["TopBar", "SettingsPage", "ExportPage"]:
                        is_excluded = True
                        break
                    p = p.parentWidget()
                    if p == self.parent(): break
                
                if not is_excluded:
                    apply_magnet = True

        # --- FIX: Detect "Sucked Out" (Release) Event ---
        if self.was_locked and not apply_magnet:
            # We just broke the magnetic connection.
            # Instead of shrinking from Large -> Small, snap to 0 so it "ignites" back up.
            self.current_radius = 0.0
            
        self.was_locked = apply_magnet

        if apply_magnet:
            target_color = self.active_color
            
            tgt_global_tl = final_target.mapToGlobal(QPoint(0,0))
            tgt_local_tl = self.mapFromGlobal(tgt_global_tl)
            rect = QRectF(tgt_local_tl, final_target.size())
            center = rect.center()
            
            path = QPainterPath()
            path.addRoundedRect(rect, 8, 8) 
            self.target_path = path

            diff = self.cursor_pos - center
            factor = 0.5 - (self.magnetic_strength * 2.0)
            if factor < 0.1: factor = 0.1
            
            target_pos = center + (diff * factor)
            target_radius = max(rect.width(), rect.height()) * 0.9

        elif isinstance(final_target, QAbstractButton):
            # Fallback for excluded buttons (color change only)
            target_color = self.active_color
            target_pos = self.cursor_pos 

        t_pos = 0.2; t_col = 0.08; t_rad = 0.15

        self.light_pos = self.light_pos * (1 - t_pos) + target_pos * t_pos
        self.current_radius = self.current_radius * (1 - t_rad) + target_radius * t_rad

        r = self.current_color.red() * (1 - t_col) + target_color.red() * t_col
        g = self.current_color.green() * (1 - t_col) + target_color.green() * t_col
        b = self.current_color.blue() * (1 - t_col) + target_color.blue() * t_col
        self.current_color = QColor(int(r), int(g), int(b))

        self.update()

    def paintEvent(self, event):
        if not self.is_visible: return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

        if self.target_path:
            painter.setClipPath(self.target_path)

        gradient = QRadialGradient(self.light_pos, self.current_radius)
        c = self.current_color
        
        alpha_max = int(255 * self.opacity_factor)
        gradient.setColorAt(0.0, QColor(c.red(), c.green(), c.blue(), alpha_max))
        gradient.setColorAt(1.0, QColor(c.red(), c.green(), c.blue(), 0))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.light_pos, self.current_radius, self.current_radius)