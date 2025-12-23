from PySide6.QtCore import QSettings

class PersistentSettings:
    def __init__(self):
        self.settings = QSettings("ChromiumThemeStudio", "V2")

    # --- Generic Helper ---
    def get_val(self, key, default=None): return self.settings.value(key, default)
    def set_val(self, key, value): self.settings.setValue(key, value)

    # --- Directories ---
    def get_last_import_dir(self): return self.settings.value("last_import_dir", "")
    def set_last_import_dir(self, path): self.settings.setValue("last_import_dir", path)
    def get_last_export_dir(self): return self.settings.value("last_export_dir", "")
    def set_last_export_dir(self, path): self.settings.setValue("last_export_dir", path)

    # --- General ---
    def get_default_author(self): return self.settings.value("default_author", "")
    def set_default_author(self, val): self.settings.setValue("default_author", val)
    
    def get_export_format(self): return self.settings.value("def_export_fmt", "ZIP Archive")
    def set_export_format(self, val): self.settings.setValue("def_export_fmt", val)
    
    def get_auto_increment(self): return self.settings.value("auto_increment", "false") == "true"
    def set_auto_increment(self, val): self.settings.setValue("auto_increment", "true" if val else "false")

    # --- Preview ---
    def get_preview_target(self): return self.settings.value("preview_target", "Chrome")
    def set_preview_target(self, val): self.settings.setValue("preview_target", val)
    
    def get_os_sim(self): return self.settings.value("os_sim", "Windows 10")
    def set_os_sim(self, val): self.settings.setValue("os_sim", val)

    # --- Transparency ---
    def get_clamp_alpha(self): return self.settings.value("clamp_alpha", "true") == "true"
    def set_clamp_alpha(self, val): self.settings.setValue("clamp_alpha", "true" if val else "false")

    # --- Editor ---
    def get_canvas_bg(self): return self.settings.value("canvas_bg", "checker")
    def set_canvas_bg(self, val): self.settings.setValue("canvas_bg", val)
    
    def get_show_guides(self): return self.settings.value("show_guides", "true") == "true"
    def set_show_guides(self, val): self.settings.setValue("show_guides", "true" if val else "false")

    # --- Import ---
    def get_resize_large(self): return self.settings.value("resize_large", "true") == "true"
    def set_resize_large(self, val): self.settings.setValue("resize_large", "true" if val else "false")
    
    def get_strip_meta(self): return self.settings.value("strip_meta", "true") == "true"
    def set_strip_meta(self, val): self.settings.setValue("strip_meta", "true" if val else "false")

    # --- Presets ---
    def get_auto_preset(self): return self.settings.value("auto_preset", "false") == "true"
    def set_auto_preset(self, val): self.settings.setValue("auto_preset", "true" if val else "false")

    # --- Advanced ---
    def get_json_override(self): return self.settings.value("json_override", "false") == "true"
    def set_json_override(self, val): self.settings.setValue("json_override", "true" if val else "false")
    
    def get_verbose_logs(self): return self.settings.value("verbose_logs", "false") == "true"
    def set_verbose_logs(self, val): self.settings.setValue("verbose_logs", "true" if val else "false")

    # --- UI ---
    def get_dark_mode(self): return self.settings.value("dark_mode", "false") == "true"
    def set_dark_mode(self, val): self.settings.setValue("dark_mode", "true" if val else "false")
    
    def get_animations(self): return self.settings.value("animations", "true") == "true"
    def set_animations(self, val): self.settings.setValue("animations", "true" if val else "false")

    # --- First Run ---
    def get_first_run(self): return self.settings.value("first_run", "true") == "true"
    def set_first_run(self, val): self.settings.setValue("first_run", "true" if val else "false")