from PySide6.QtCore import QSettings

class PersistentSettings:
    def __init__(self):
        self.settings = QSettings("ChromiumThemeStudio", "V2")

    def get_val(self, key, default=None): return self.settings.value(key, default)
    def set_val(self, key, value): self.settings.setValue(key, value)
    def get_last_import_dir(self): return self.settings.value("last_import_dir", "")
    def set_last_import_dir(self, path): self.settings.setValue("last_import_dir", path)
    def get_last_export_dir(self): return self.settings.value("last_export_dir", "")
    def set_last_export_dir(self, path): self.settings.setValue("last_export_dir", path)
    def get_canvas_bg(self): return self.settings.value("canvas_bg", "checker")
    def get_export_format(self): return self.settings.value("def_export_fmt", "zip")
    def get_auto_increment(self): return self.settings.value("auto_increment", "false") == "true"
    def get_animations(self): return self.settings.value("animations", "true") == "true"