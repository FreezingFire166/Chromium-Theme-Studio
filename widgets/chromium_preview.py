from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QPainter,
    QFont,
    QFontMetrics,
    QPixmap,
)
from PySide6.QtCore import Qt, QRect, QSize, Signal

from engine.browser import Browser


class ChromiumPreview(QWidget):
    sectionClicked = Signal(str)

    def __init__(self, state):
        super().__init__()
        self.state = state
        self.browser = Browser.CHROME
        self.fast_mode = False

        # Logical canvas (browser content)
        self.canvas_size = QSize(1600, 900)
        self.canvas = QPixmap(self.canvas_size)
        self.canvas.fill(Qt.transparent)

        self.setMinimumHeight(260)

    # ── PUBLIC API ─────────────────────────
    def set_canvas_size(self, w, h):
        self.canvas_size = QSize(w, h)
        self.canvas = QPixmap(self.canvas_size)
        self.canvas.fill(Qt.transparent)
        self.update()

    def set_browser(self, browser):
        self.browser = browser
        self.update()

    # ── CLICK → SECTION ────────────────────
    def mousePressEvent(self, e):
        scale = min(
            self.width() / self.canvas.width(),
            self.height() / self.canvas.height(),
        )

        cx = int(e.position().x() / scale)
        cy = int(e.position().y() / scale)

        frame_h = 56
        tabs_h = 38
        toolbar_h = 44

        if cy < frame_h:
            self.sectionClicked.emit("frame")
        elif cy < frame_h + tabs_h:
            self.sectionClicked.emit("tab_active")
        elif cy < frame_h + tabs_h + toolbar_h:
            self.sectionClicked.emit("toolbar")
        else:
            self.sectionClicked.emit("bookmark_text")

    # ── IMAGE HELPERS ──────────────────────
    def _draw_frame_image(self, p, rect):
        pix = self.state.get_cached_pixmap("frame_image")
        if not pix:
            return

        data = self.state.get_image_params("frame_image")
        scale = data["scale"]
        ox = data["offset_x"]
        oy = data["offset_y"]
        anchor = data["anchor"]

        scaled = pix.scaled(
            int(pix.width() * scale),
            int(pix.height() * scale),
            Qt.KeepAspectRatio,
            Qt.FastTransformation if self.fast_mode else Qt.SmoothTransformation,
        )

        if anchor == "top":
            sy = 0
        elif anchor == "center":
            sy = max(0, (scaled.height() - rect.height()) // 2)
        else:
            sy = max(0, scaled.height() - rect.height())

        src = QRect(
            max(0, ox),
            max(0, sy + oy),
            rect.width(),
            rect.height(),
        )

        p.drawPixmap(rect, scaled, src)

    def _draw_background_image(self, p, rect):
        pix = self.state.get_cached_pixmap("background_image")
        if not pix:
            return

        data = self.state.get_image_params("background_image")
        scale = data["scale"]
        ox = data["offset_x"]
        oy = data["offset_y"]
        fit = data["fit"]

        iw, ih = pix.width(), pix.height()
        cw, ch = rect.width(), rect.height()

        if fit == "original":
            tw = int(iw * scale)
            th = int(ih * scale)
        else:
            ratio = iw / ih
            canvas_ratio = cw / ch

            if (fit == "cover" and ratio < canvas_ratio) or \
               (fit == "contain" and ratio > canvas_ratio):
                th = ch
                tw = int(ch * ratio)
            else:
                tw = cw
                th = int(cw / ratio)

            tw = int(tw * scale)
            th = int(th * scale)

        x = (cw - tw) // 2 + ox
        y = (ch - th) // 2 + oy

        scaled = pix.scaled(
            tw,
            th,
            Qt.IgnoreAspectRatio,
            Qt.FastTransformation if self.fast_mode else Qt.SmoothTransformation,
        )

        p.drawPixmap(x, y, scaled)

    # ── CANVAS RENDER ──────────────────────
    def _render_canvas(self):
        self.canvas.fill(Qt.transparent)

        p = QPainter(self.canvas)
        try:
            p.setRenderHint(QPainter.Antialiasing)

            w = self.canvas.width()
            h = self.canvas.height()

            # Layout metrics (Chromium-like)
            frame_h = 56
            tabs_h = 38
            toolbar_h = 44

            # Colors
            frame = self.state.get_color("frame")
            tab_active = self.state.get_color("tab_active")
            tab_inactive = self.state.get_color("tab_inactive")
            toolbar = self.state.get_color("toolbar")
            tab_text = self.state.get_color("tab_text")
            toolbar_text = self.state.get_color("toolbar_text")
            bookmark_text = self.state.get_color("bookmark_text")

            # Background
            self._draw_background_image(p, QRect(0, 0, w, h))

            # Frame
            frame_rect = QRect(0, 0, w, frame_h)
            p.fillRect(frame_rect, frame)
            self._draw_frame_image(p, frame_rect)

            # Tabs strip
            tabs_y = frame_h
            p.fillRect(0, tabs_y, w, tabs_h, frame.darker(108))

            font = QFont("Segoe UI", 9)
            bold = QFont("Segoe UI", 9, QFont.Bold)

            tab_w = 140
            tab_h = tabs_h - 8
            tab_y = tabs_y + 4

            # Inactive tabs
            p.setFont(font)
            fm = QFontMetrics(font)

            for i in range(2):
                x = 20 + i * (tab_w + 10)
                rect = QRect(x, tab_y, tab_w, tab_h)

                p.setPen(Qt.NoPen)
                p.setBrush(tab_inactive)
                p.drawRoundedRect(rect, 8, 8)

                p.setPen(tab_text)
                ty = rect.y() + (rect.height() + fm.ascent() - fm.descent()) // 2
                p.drawText(rect.x() + 14, ty, "Inactive")

            # Active tab
            active_x = 20 + 2 * (tab_w + 10)
            rect = QRect(active_x, tab_y, tab_w, tab_h)

            p.setBrush(tab_active)
            p.drawRoundedRect(rect, 8, 8)

            p.setFont(bold)
            fm = QFontMetrics(bold)
            p.setPen(tab_text)
            ty = rect.y() + (rect.height() + fm.ascent() - fm.descent()) // 2
            p.drawText(rect.x() + 14, ty, "Active Tab")

            # Toolbar
            toolbar_y = tabs_y + tabs_h
            p.fillRect(0, toolbar_y, w, toolbar_h, toolbar)

            p.setFont(font)
            p.setPen(toolbar_text)
            fm = QFontMetrics(font)
            p.drawText(
                120,
                toolbar_y + (toolbar_h + fm.ascent() - fm.descent()) // 2,
                "https://example.com",
            )

            # Bookmarks
            bx = 20
            by = toolbar_y + toolbar_h + 22 + fm.ascent()
            p.setPen(bookmark_text)
            for name in ("Google", "GitHub", "Docs"):
                p.drawText(bx, by, name)
                bx += 100

        finally:
            p.end()

    # ── FINAL PAINT ────────────────────────
    def paintEvent(self, event):
        self._render_canvas()

        p = QPainter(self)
        try:
            scale = min(
                self.width() / self.canvas.width(),
                self.height() / self.canvas.height(),
            )

            dw = int(self.canvas.width() * scale)
            dh = int(self.canvas.height() * scale)
            dx = (self.width() - dw) // 2
            dy = (self.height() - dh) // 2

            p.drawPixmap(
                dx,
                dy,
                self.canvas.scaled(
                    dw,
                    dh,
                    Qt.IgnoreAspectRatio,
                    Qt.FastTransformation,
                ),
            )

            # Canvas border
            p.setPen(Qt.gray)
            p.setBrush(Qt.NoBrush)
            p.drawRect(dx, dy, dw, dh)
        finally:
            p.end()
