import os
import json
import tempfile
import zipfile
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt

class ExportManager:
    @staticmethod
    def run_export_process(parent_window, theme_data, export_data, p_settings, renderer, is_log_enabled):
        dest_path = export_data["dest_path"]
        fmt = export_data["format"]
        
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                images_dir = os.path.join(tmp_dir, "images")
                os.makedirs(images_dir, exist_ok=True)
                
                ver = export_data["meta_version"]
                if p_settings.get_auto_increment():
                    parts = ver.split('.')
                    if len(parts) > 0 and parts[-1].isdigit(): 
                        parts[-1] = str(int(parts[-1]) + 1)
                        ver = ".".join(parts)

                overlay_pix = QPixmap(1, 1); overlay_pix.fill(Qt.transparent)
                overlay_pix.save(os.path.join(images_dir, "theme_frame_overlay.png"), "PNG")

                colors = { 
                    "frame": ExportManager._hex_to_rgb_list(theme_data.get("frame", "#CC0000FF")), 
                    "toolbar": ExportManager._hex_to_rgb_list(theme_data.get("toolbar", "#FFFFFFFF")), 
                    "tab_text": ExportManager._hex_to_rgb_list(theme_data.get("tab_text", "#000000FF")), 
                    "tab_background_text": ExportManager._hex_to_rgb_list(theme_data.get("inactive_tab_text", "#555555FF")), 
                    "tab_background": ExportManager._hex_to_rgb_list(theme_data.get("inactive_tab", "#E68A8AFF")), 
                    "bookmark_text": ExportManager._hex_to_rgb_list(theme_data.get("bookmark_text", "#555555FF")), 
                    "ntp_text": ExportManager._hex_to_rgb_list(theme_data.get("toolbar_text", "#333333FF")), 
                    "button_background": ExportManager._hex_to_rgb_list(theme_data.get("button_tint", "#555555FF")) 
                }
                if theme_data.get("frame_incognito"): colors["frame_incognito"] = ExportManager._hex_to_rgb_list(theme_data["frame_incognito"])
                if theme_data.get("frame_incognito_inactive"): colors["frame_incognito_inactive"] = ExportManager._hex_to_rgb_list(theme_data["frame_incognito_inactive"])

                manifest = { 
                    "manifest_version": 3, "version": ver, "name": export_data["meta_name"], "description": export_data["meta_desc"],
                    "theme": { "colors": colors, "images": { "theme_frame_overlay": "images/theme_frame_overlay.png" } } 
                }
                
                if theme_data.get("frame_image"):
                    pix = renderer.get_processed_pixmap("frame_image")
                    if pix: pix.save(os.path.join(images_dir, "theme_frame.png"), "PNG"); manifest["theme"]["images"]["theme_frame"] = "images/theme_frame.png"
                if theme_data.get("ntp_image"):
                    pix = renderer.get_processed_pixmap("ntp_image")
                    if pix: pix.save(os.path.join(images_dir, "theme_ntp_background.png"), "PNG"); manifest["theme"]["images"]["theme_ntp_background"] = "images/theme_ntp_background.png"; manifest["theme"]["properties"] = { "ntp_background_alignment": "center bottom", "ntp_background_repeat": "no-repeat" }
                if theme_data.get("frame_image_incognito"):
                    pix = renderer.get_processed_pixmap("frame_image_incognito")
                    if pix: pix.save(os.path.join(images_dir, "theme_frame_incognito.png"), "PNG"); manifest["theme"]["images"]["theme_frame_incognito"] = "images/theme_frame_incognito.png"

                indent = None if is_log_enabled else 4
                with open(os.path.join(tmp_dir, "manifest.json"), 'w') as f: json.dump(manifest, f, indent=indent)
                
                final_zip_path = dest_path
                if fmt == 'crx' and not dest_path.endswith('.zip'): final_zip_path = os.path.splitext(dest_path)[0] + ".zip"
                with zipfile.ZipFile(final_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(tmp_dir):
                        for file in files: zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), tmp_dir))
                
                if fmt == 'crx':
                     if os.path.exists(dest_path): os.remove(dest_path)
                     os.rename(final_zip_path, dest_path)
                     QMessageBox.information(parent_window, "CRX Generated", f"Package saved to {dest_path}.")
                else: QMessageBox.information(parent_window, "ZIP Generated", f"Theme package saved successfully to {dest_path}.")
                if p_settings.get_val("open_after_export", "true") == "true": os.startfile(os.path.dirname(dest_path))     
        except Exception as e: QMessageBox.critical(parent_window, "Export Failed", f"An error occurred: {e}")

    @staticmethod
    def _hex_to_rgb_list(hex_str):
        c = ExportManager.color_from_rgba_hex(hex_str); return [c.red(), c.green(), c.blue()]
    @staticmethod
    def color_from_rgba_hex(text):
        if not isinstance(text, str) or not text.startswith("#") or len(text) != 9: return QColor(255, 255, 255, 255)
        try: return QColor(int(text[1:3], 16), int(text[3:5], 16), int(text[5:7], 16), int(text[7:9], 16))
        except ValueError: return QColor(255, 255, 255, 255)