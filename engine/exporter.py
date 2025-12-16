import os
import json
import zipfile
import tempfile
from datetime import datetime

from PySide6.QtGui import QImage, QPainter, QColor
from PySide6.QtCore import Qt


class ChromiumThemeExporter:
    def __init__(self, state):
        self.state = state

    # ── PUBLIC API ────────────────────────
    def export(self, out_zip_path, theme_name=None):
        if not theme_name:
            theme_name = self._default_name()

        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, theme_name)
            img_dir = os.path.join(root, "images")
            os.makedirs(img_dir, exist_ok=True)

            theme_json = self._build_theme_json(img_dir)
            manifest = self._build_manifest(theme_name, theme_json)

            with open(os.path.join(root, "theme.json"), "w", encoding="utf-8") as f:
                json.dump(theme_json, f, indent=2)

            with open(os.path.join(root, "manifest.json"), "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)

            self._zip_dir(root, out_zip_path)

    # ── INTERNALS ─────────────────────────
    def _default_name(self):
        return "ChromiumTheme_" + datetime.now().strftime("%Y-%m-%d_%H-%M")

    def _zip_dir(self, folder, zip_path):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(folder):
                for file in files:
                    full = os.path.join(root, file)
                    rel = os.path.relpath(full, folder)
                    z.write(full, rel)

    # ── THEME.JSON ────────────────────────
    def _build_theme_json(self, img_dir):
        data = {
            "colors": {},
            "images": {},
            "properties": {}
        }

        # Colors
        c = self.state.colors
        data["colors"] = {
            "frame": self._rgba(c["frame"]),
            "toolbar": self._rgba(c["toolbar"]),
            "tab_text": self._rgba(c["tab_text"]),
            "toolbar_text": self._rgba(c["toolbar_text"]),
            "bookmark_text": self._rgba(c["bookmark_text"]),
            "tab_selected": self._rgba(c["tab_active"]),
            "tab_background_text": self._rgba(c["tab_inactive"]),
        }

        # Images
        if self.state.images["frame_image"]["path"]:
            fname = "theme_frame.png"
            self._bake_image("frame_image", img_dir, fname)
            data["images"]["theme_frame"] = "images/" + fname
            data["properties"]["theme_frame_alignment"] = "top"

        if self.state.images["background_image"]["path"]:
            fname = "theme_ntp_background.png"
            self._bake_image("background_image", img_dir, fname)
            data["images"]["theme_ntp_background"] = "images/" + fname
            data["properties"]["ntp_background_alignment"] = "center"
            data["properties"]["ntp_background_repeat"] = "no-repeat"

        return data

    # ── IMAGE BAKING ──────────────────────
    def _bake_image(self, key, img_dir, out_name):
        img_data = self.state.images[key]
        src = img_data["path"]
        pix = self.state.get_cached_pixmap(key)
        if not pix:
            return

        # Canvas size for baking
        canvas_w = 2000
        canvas_h = 1200

        canvas = QImage(canvas_w, canvas_h, QImage.Format_ARGB32)
        canvas.fill(Qt.transparent)

        p = QPainter(canvas)

        scale = img_data["scale"]
        ox = img_data["offset_x"]
        oy = img_data["offset_y"]

        tw = int(pix.width() * scale)
        th = int(pix.height() * scale)

        x = (canvas_w - tw) // 2 + ox
        y = (canvas_h - th) // 2 + oy

        p.drawPixmap(x, y, pix.scaled(
            tw, th,
            Qt.IgnoreAspectRatio,
            Qt.FastTransformation))
        p.end()

        out_path = os.path.join(img_dir, out_name)
        canvas.save(out_path)

    # ── UTIL ──────────────────────────────
    def _rgba(self, color: QColor):
        return [
            color.red(),
            color.green(),
            color.blue(),
            round(color.alpha() / 255, 2)
        ]
    def _build_manifest(self, theme_name, theme_json):
        return {
            "manifest_version": 3,
            "name": theme_name,
            "version": "1.0",
            "description": "Theme created with Chromium Theme Studio",
            "theme": {
                "colors": theme_json.get("colors", {}),
                "images": theme_json.get("images", {}),
                "properties": theme_json.get("properties", {})
            }
        }
