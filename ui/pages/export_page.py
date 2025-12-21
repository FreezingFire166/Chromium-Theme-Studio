from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QFormLayout, QPlainTextEdit, QRadioButton, QButtonGroup, QFileDialog)
from PySide6.QtCore import Qt, Signal
import os

class ExportPage(QWidget):
    start_export_signal = Signal(dict) 

    def __init__(self, persistent_settings, parent=None):
        super().__init__(parent)
        self.p_settings = persistent_settings
        layout = QVBoxLayout(self); layout.setContentsMargins(40, 30, 40, 30); layout.setSpacing(25); layout.setAlignment(Qt.AlignTop)

        lbl_title = QLabel("Export Theme Package"); lbl_title.setStyleSheet("font-size: 22px; font-weight: bold;"); layout.addWidget(lbl_title)
        grp_meta = self.create_group("1. Theme Metadata")
        form_meta = QFormLayout(); form_meta.setVerticalSpacing(15)
        self.inp_name = QLineEdit(); self.inp_name.setPlaceholderText("My Cool Theme")
        self.inp_author = QLineEdit()
        self.inp_version = QLineEdit("1.0"); self.inp_version.setFixedWidth(100)
        self.inp_desc = QPlainTextEdit(); self.inp_desc.setFixedHeight(60)
        form_meta.addRow("Theme Name:", self.inp_name); form_meta.addRow("Author (Optional):", self.inp_author)
        form_meta.addRow("Version:", self.inp_version); form_meta.addRow("Description (Optional):", self.inp_desc)
        grp_meta.layout().addLayout(form_meta); layout.addWidget(grp_meta)

        grp_dest = self.create_group("2. Format & Destination"); dest_lay = QVBoxLayout()
        lbl_fmt = QLabel("Export Format:")
        self.rb_zip = QRadioButton("ZIP Archive (Recommended for sharing)"); self.rb_crx = QRadioButton("CRX Package (Requires manual packing in Chrome)")
        self.rb_zip.setChecked(True)
        self.fmt_group = QButtonGroup(); self.fmt_group.addButton(self.rb_zip); self.fmt_group.addButton(self.rb_crx)
        dest_lay.addWidget(lbl_fmt); dest_lay.addWidget(self.rb_zip); dest_lay.addWidget(self.rb_crx); dest_lay.addSpacing(15)
        lbl_path = QLabel("Save Location:"); path_row = QHBoxLayout()
        self.inp_path = QLineEdit(); self.inp_path.setReadOnly(True)
        btn_browse = QPushButton("Browse..."); btn_browse.setProperty("class", "resBtn"); btn_browse.clicked.connect(self.browse_dest)
        path_row.addWidget(self.inp_path); path_row.addWidget(btn_browse)
        dest_lay.addWidget(lbl_path); dest_lay.addLayout(path_row); grp_dest.layout().addLayout(dest_lay); layout.addWidget(grp_dest)
        
        layout.addStretch()
        btn_row = QHBoxLayout(); btn_row.addStretch()
        self.btn_do_export = QPushButton("Generate Package"); self.btn_do_export.setProperty("class", "saveBtn")
        self.btn_do_export.setFixedSize(180, 45); self.btn_do_export.clicked.connect(self.on_export_clicked)
        btn_row.addWidget(self.btn_do_export); layout.addLayout(btn_row)

    def create_group(self, title):
        frame = QFrame(); frame.setObjectName("settingsGroup")
        l = QVBoxLayout(frame); l.setContentsMargins(20, 20, 20, 20)
        lbl = QLabel(title); lbl.setObjectName("groupTitle"); l.addWidget(lbl)
        return frame

    def browse_dest(self):
        start_dir = self.p_settings.get_last_export_dir(); ext = "zip" if self.rb_zip.isChecked() else "crx"
        default_name = self.inp_name.text().replace(" ", "_").lower() or "theme"
        f, _ = QFileDialog.getSaveFileName(self, f"Save {ext.upper()}", os.path.join(start_dir, f"{default_name}.{ext}"), f"{ext.upper()} Files (*.{ext})")
        if f: self.inp_path.setText(f); self.p_settings.set_last_export_dir(os.path.dirname(f))

    def on_export_clicked(self):
        if not self.inp_path.text(): self.browse_dest()
        if not self.inp_path.text(): return
        export_data = { "meta_name": self.inp_name.text() or "Untitled Theme", "meta_author": self.inp_author.text(), "meta_version": self.inp_version.text() or "1.0", "meta_desc": self.inp_desc.toPlainText(), "format": "zip" if self.rb_zip.isChecked() else "crx", "dest_path": self.inp_path.text() }
        self.start_export_signal.emit(export_data)