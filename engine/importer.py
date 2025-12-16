import os
import json
import zipfile
import tempfile
import shutil

from PySide6.QtGui import QColor


class ChromiumThemeImporter:
    def __init__(self, state):
        self.state = state

    # ── PUBLIC API ────────────────────────
    def import_zip(self, zip_path):
        if not zipfile.is_zipfile(zip_path):
            return False

        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(tmp)

            root = self._find_theme_root(tmp)
            if not root:
                return False

            theme_json_path = os.path.join(root, "theme.json")
            if not os.path.exists(theme_json_path):
                return False

            with open(theme_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self._apply_colors(data.get("colors", {}))
            self._apply_images(root, data)

        return True

    def import_preset_json(self, json_path):
        if not os.path.exists(json_path):
            return False

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.state.apply_preset(data)
        return True

    # ── INTERNALS ─────────────────────────
    def _find_theme_root(self, folder):
        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            if os.path.isdir(path):
                if os.path.exists(os.path.join(path, "theme.json")):
                    return path
        return None

    def _apply_colors(self, colors):
        mapping = {
            "frame": "frame",
            "toolbar": "toolbar",
            "tab_text": "tab_text",
            "toolbar_text": "toolbar_text",
            "bookmark_text": "bookmark_text",
            "tab_selected": "tab_active",
            "tab_background_text": "tab_inactive"
        }

        for chrom_key, app_key in mapping.items():
            if chrom_key not in colors:
                continue

            value = colors[chrom_key]

            # Chromium colors may be [r,g,b,a] or [r,g,b,alphaFloat]
            if len(value) == 4:
                r, g, b, a = value
                if isinstance(a, float):
                    a = int(a * 255)
                self.state.set_color(app_key, QColor(r, g, b, a))

    def _apply_images(self, root, data):
        images = data.get("images", {})

        # FRAME IMAGE
        if "theme_frame" in images:
            self._load_image(
                root,
                images["theme_frame"],
                "frame_image"
            )

        # BACKGROUND IMAGE
        if "theme_ntp_background" in images:
            self._load_image(
                root,
                images["theme_ntp_background"],
                "background_image"
            )

    def _load_image(self, root, rel_path, key):
        src = os.path.join(root, rel_path)
        if not os.path.exists(src):
            return

        # copy image to temp user location
        user_dir = os.path.join(
            os.path.expanduser("~"),
            "ChromiumThemeStudio",
            "ImportedImages"
        )
        os.makedirs(user_dir, exist_ok=True)

        dst = os.path.join(user_dir, os.path.basename(src))
        shutil.copy(src, dst)

        self.state.set_image(key, dst)
