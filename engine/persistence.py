import json
import os

from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor


# ── SETTINGS KEYS ────────────────────────
SETTINGS_ORG = "ChromiumThemeStudio"
SETTINGS_APP = "ThemeBuilder"

KEY_LAST_IMAGE_DIR = "last_image_dir"
KEY_DEFAULT_PRESET_USED = "default_preset_used"


class Persistence:
    def __init__(self):
        self.settings = QSettings(SETTINGS_ORG, SETTINGS_APP)

    # ── APP SETTINGS ──────────────────────
    def get_last_image_dir(self):
        return self.settings.value(KEY_LAST_IMAGE_DIR, "", type=str)

    def set_last_image_dir(self, path):
        if path and os.path.isdir(path):
            self.settings.setValue(KEY_LAST_IMAGE_DIR, path)

    def was_default_preset_used(self):
        return self.settings.value(KEY_DEFAULT_PRESET_USED, False, type=bool)

    def mark_default_preset_used(self):
        self.settings.setValue(KEY_DEFAULT_PRESET_USED, True)

    # ── PRESET SAVE / LOAD ────────────────
    def save_preset(self, filepath, state):
        data = {
            "colors": {},
            "images": {}
        }

        # Save colors
        for key, color in state.colors.items():
            data["colors"][key] = [
                color.red(),
                color.green(),
                color.blue(),
                color.alpha()
            ]

        # Save images
        for key, img in state.images.items():
            entry = {
                "path": img["path"],
                "scale": img["scale"],
                "offset_x": img["offset_x"],
                "offset_y": img["offset_y"]
            }

            if key == "frame_image":
                entry["anchor"] = img["anchor"]
            else:
                entry["fit"] = img["fit"]

            data["images"][key] = entry

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_preset(self, filepath, state):
        if not os.path.exists(filepath):
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Load colors
        for key, rgba in data.get("colors", {}).items():
            if len(rgba) == 4:
                state.colors[key] = QColor(*rgba)

        # Load images
        for key, img in data.get("images", {}).items():
            if key not in state.images:
                continue

            state.images[key]["path"] = img.get("path")
            state.images[key]["scale"] = img.get("scale", 1.0)
            state.images[key]["offset_x"] = img.get("offset_x", 0)
            state.images[key]["offset_y"] = img.get("offset_y", 0)

            if key == "frame_image":
                state.images[key]["anchor"] = img.get("anchor", "top")
            else:
                state.images[key]["fit"] = img.get("fit", "cover")

            # force pixmap reload
            state.images[key]["cached"] = None

        return True
