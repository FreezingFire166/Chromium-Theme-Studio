from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QInputDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt, QTimer

from engine.theme_state import ThemeState
from engine.exporter import ChromiumThemeExporter
from engine.importer import ChromiumThemeImporter

from widgets.chromium_preview import ChromiumPreview
from widgets.color_picker import ColorPicker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chromium Theme Studio")
        self.resize(1200, 800)

        # ── STATE & ENGINES ─────────────────
        self.state = ThemeState()
        self.exporter = ChromiumThemeExporter(self.state)
        self.importer = ChromiumThemeImporter(self.state)

        # ── CENTRAL WIDGET ──────────────────
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setSpacing(8)
        root.setContentsMargins(8, 8, 8, 8)

        # ── TOP BAR ─────────────────────────
        top = QHBoxLayout()

        title = QLabel("Chromium Theme Studio")
        title.setStyleSheet("font-size:18px;font-weight:bold;")
        top.addWidget(title)

        top.addStretch()

        self.reset_btn = QPushButton("New Theme")
        self.load_btn = QPushButton("Load Theme")
        self.export_btn = QPushButton("Export Theme")

        self.reset_btn.clicked.connect(self.reset_theme)
        self.load_btn.clicked.connect(self.load_theme)
        self.export_btn.clicked.connect(self.export_theme)

        top.addWidget(self.reset_btn)
        top.addWidget(self.load_btn)
        top.addWidget(self.export_btn)

        root.addLayout(top)

        # ── MAIN AREA ───────────────────────
        main = QHBoxLayout()

        self.preview = ChromiumPreview(self.state)
        main.addWidget(self.preview, 2)

        self.picker = ColorPicker(self.state)
        main.addWidget(self.picker, 1)

        root.addLayout(main, 1)

        # ── PREVIEW DEBOUNCE (FINAL & SMOOTH) ──
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)

        def _final_preview_update():
            # Switch back to high-quality render
            self.preview.fast_mode = False
            self.preview.update()

        self._preview_timer.timeout.connect(_final_preview_update)

        # While dragging → fast preview
        self.picker.colorChanged.connect(self.schedule_preview_update)
        self.picker.image_editor.imageChanged.connect(
            self.schedule_preview_update
        )

    # ── PREVIEW UPDATE (FAST → FINAL) ─────
    def schedule_preview_update(self):
        # Enable fast mode while user is interacting
        self.preview.fast_mode = True
        # Restart debounce timer (≈ 60 FPS)
        self._preview_timer.start(16)

    # ── RESET THEME ───────────────────────
    def reset_theme(self):
        reply = QMessageBox.question(
            self,
            "New Theme",
            "This will clear all colors and images.\nContinue?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        self.state.reset_theme()
        self.picker.reload_all()
        self.preview.fast_mode = False
        self.preview.update()

    # ── EXPORT THEME ──────────────────────
    def export_theme(self):
        default_name = self.exporter._default_name()

        name, ok = QInputDialog.getText(
            self,
            "Theme Name",
            "Enter theme name:",
            text=default_name,
        )
        if not ok or not name:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Theme",
            name + ".zip",
            "ZIP Archive (*.zip)",
        )
        if not path:
            return

        try:
            self.exporter.export(path, name)
            QMessageBox.information(
                self,
                "Export Complete",
                "Theme exported successfully.",
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                str(e),
            )

    # ── LOAD THEME ────────────────────────
    def load_theme(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Theme",
            "",
            "Theme Files (*.zip *.json)",
        )
        if not path:
            return

        ok = False
        if path.lower().endswith(".zip"):
            ok = self.importer.import_zip(path)
        elif path.lower().endswith(".json"):
            ok = self.importer.import_preset_json(path)

        if not ok:
            QMessageBox.warning(
                self,
                "Load Failed",
                "Could not load the selected theme.",
            )
            return

        self.picker.reload_all()
        self.preview.fast_mode = False
        self.preview.update()

        QMessageBox.information(
            self,
            "Theme Loaded",
            "Theme loaded successfully.",
        )
