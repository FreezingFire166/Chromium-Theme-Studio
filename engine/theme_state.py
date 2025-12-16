from PySide6.QtGui import QColor, QPixmap


class ThemeState:
    def __init__(self):
        self.colors = self._default_colors()
        self.images = {
            "frame_image": self._default_image(),
            "background_image": self._default_image()
        }

    # ── DEFAULTS ──────────────────────────
    def _default_colors(self):
        return {
            "frame": QColor(60, 180, 120),
            "tab_active": QColor(40, 40, 40),
            "tab_inactive": QColor(120, 120, 120),
            "toolbar": QColor(32, 32, 32),
            "tab_text": QColor(255, 255, 255),
            "toolbar_text": QColor(230, 230, 230),
            "bookmark_text": QColor(200, 200, 200),
        }

    def _default_image(self):
        return {
            "path": None,
            "scale": 1.0,
            "offset_x": 0,
            "offset_y": 0,
            "fit": "cover",
            "anchor": "top",
            "cached": None,
        }

    # ── COLOR API ─────────────────────────
    def get_color(self, key):
        return self.colors[key]

    def set_color(self, key, color):
        self.colors[key] = color

    # ── IMAGE API ─────────────────────────
    def set_image(self, key, path):
        self.images[key]["path"] = path
        self.images[key]["cached"] = None

    def clear_image(self, key):
        self.images[key] = self._default_image()

    def set_image_param(self, key, param, value):
        self.images[key][param] = value
        self.images[key]["cached"] = None

    def get_image_params(self, key):
        return self.images[key]

    def get_cached_pixmap(self, key):
        img = self.images[key]
        if not img["path"]:
            return None

        if img["cached"] is None:
            pix = QPixmap(img["path"])
            if pix.isNull():
                return None
            img["cached"] = pix

        return img["cached"]

    # ── PRESET APPLY ──────────────────────
    def apply_preset(self, data):
        for key, rgba in data.get("colors", {}).items():
            if len(rgba) == 4:
                self.colors[key] = QColor(*rgba)

        for key, img in data.get("images", {}).items():
            if key not in self.images:
                continue

            self.images[key]["path"] = img.get("path")
            self.images[key]["scale"] = img.get("scale", 1.0)
            self.images[key]["offset_x"] = img.get("offset_x", 0)
            self.images[key]["offset_y"] = img.get("offset_y", 0)

            if key == "frame_image":
                self.images[key]["anchor"] = img.get("anchor", "top")
            else:
                self.images[key]["fit"] = img.get("fit", "cover")

            self.images[key]["cached"] = None

    # ── RESET THEME ───────────────────────
    def reset_theme(self):
        self.colors = self._default_colors()
        self.images = {
            "frame_image": self._default_image(),
            "background_image": self._default_image()
        }
