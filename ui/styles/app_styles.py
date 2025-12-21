class AppStyles:
    @staticmethod
    def get_light_stylesheet():
        return """
            QMainWindow { background-color: #F0F2F5; }
            QWidget { font-family: 'Segoe UI', sans-serif; font-size: 11px; color: #202124; }
            TopBar { background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0; }
            QPushButton.topBtn { background: transparent; color: #5F6368; font-weight: 600; padding: 6px 12px; border-radius: 4px; }
            QPushButton.topBtn:hover { background: #F1F3F4; color: #202124; }
            QFrame#menu_frame, QFrame#ctrl_frame, QFrame#settingsGroup { background-color: #FFFFFF; border-radius: 8px; border: 1px solid #E0E0E0; }
            QDialog, QMessageBox { background-color: #FFFFFF; color: #202124; }
            QPushButton.saveBtn { background: #1A73E8; color: white; border: none; border-radius: 4px; font-weight: bold; font-size: 13px; padding: 8px; }
            QPushButton.saveBtn:hover { background: #1557B0; }
            QPushButton.dangerBtn { background: transparent; color: #D93025; border: 1px solid #D93025; border-radius: 4px; font-weight: 600; padding: 8px; }
            QPushButton.dangerBtn:hover { background: #FCE8E6; }
            QPushButton.resBtn { background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 4px; padding: 6px 12px; color: #5F6368; }
            QPushButton.resBtn:hover { background: #F1F3F4; color: #202124; }
            QPushButton.arrowBtn { background: #F1F3F4; border: none; border-radius: 12px; }
            QLineEdit, QPlainTextEdit { border: 1px solid #DADCE0; border-radius: 4px; background: #FFFFFF; padding: 6px; color: #202124; }
            QLabel#sectionHeader, QLabel#groupTitle { color: #5F6368; font-weight: 700; font-size: 12px; letter-spacing: 0.5px; }
            QComboBox { background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 4px; padding: 4px; color: #202124; }
            QComboBox QAbstractItemView { background-color: #FFFFFF; border: 1px solid #DADCE0; color: #202124; selection-background-color: #E8F0FE; selection-color: #1967D2; outline: none; }
            QTextBrowser { background-color: #FFFFFF; color: #202124; border: none; }
            QGroupBox { font-weight: bold; border: 1px solid #ddd; border-radius: 6px; margin-top: 10px; padding: 10px; background-color: #FFFFFF; color: #202124; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
            SettingsPage QScrollArea, SettingsPage QScrollArea > QWidget, SettingsPage QScrollArea > QWidget > QWidget { background-color: transparent; }
            QPushButton.menuHeader { text-align: left; padding: 5px; font-weight: bold; border: none; background: transparent; color: #5F6368; }
            QPushButton.menuHeader:checked { color: #1A73E8; }
        """

    @staticmethod
    def get_dark_stylesheet():
        return """
            QMainWindow { background-color: #18191A; }
            QWidget { font-family: 'Segoe UI', sans-serif; font-size: 11px; color: #E8EAED; }
            TopBar { background-color: #242526; border-bottom: 1px solid #3E4042; }
            QPushButton.topBtn { background: transparent; color: #B0B3B8; font-weight: 600; padding: 6px 12px; border-radius: 4px; }
            QPushButton.topBtn:hover { background: #3A3B3C; color: #E8EAED; }
            QFrame#menu_frame, QFrame#ctrl_frame, QFrame#settingsGroup { background-color: #242526; border-radius: 8px; border: 1px solid #3E4042; }
            QDialog, QMessageBox { background-color: #242526; color: #E8EAED; }
            QPushButton.saveBtn { background: #8AB4F8; color: #202124; border: none; border-radius: 4px; font-weight: bold; font-size: 13px; padding: 8px; }
            QPushButton.saveBtn:hover { background: #AECBFA; }
            QPushButton.dangerBtn { background: transparent; color: #F28B82; border: 1px solid #F28B82; border-radius: 4px; font-weight: 600; padding: 8px; }
            QPushButton.dangerBtn:hover { background: #3C1F1F; }
            QPushButton.resBtn { background: #292A2D; border: 1px solid #5F6368; border-radius: 4px; padding: 6px 12px; color: #E8EAED; }
            QPushButton.resBtn:hover { background: #3C4043; }
            QPushButton.arrowBtn { background: #3C4043; border: none; border-radius: 12px; }
            QLineEdit, QPlainTextEdit { border: 1px solid #3E4042; border-radius: 4px; background: #3A3B3C; padding: 6px; color: #E8EAED; }
            QLabel#sectionHeader, QLabel#groupTitle { color: #B0B3B8; font-weight: 700; font-size: 12px; letter-spacing: 0.5px; }
            QComboBox { background-color: #3A3B3C; border: 1px solid #3E4042; border-radius: 4px; padding: 4px; color: #E8EAED; }
            QComboBox QAbstractItemView { background-color: #292A2D; border: 1px solid #3C4043; color: #E8EAED; selection-background-color: #3C4043; selection-color: #FFFFFF; outline: none; }
            QTextBrowser { background-color: #18191A; color: #E8EAED; border: none; }
            QGroupBox { font-weight: bold; border: 1px solid #3E4042; border-radius: 6px; margin-top: 10px; padding: 10px; background-color: #242526; color: #E8EAED; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #B0B3B8; }
            SettingsPage QScrollArea, SettingsPage QScrollArea > QWidget, SettingsPage QScrollArea > QWidget > QWidget { background-color: transparent; }
            QPushButton.menuHeader { text-align: left; padding: 5px; font-weight: bold; border: none; background: transparent; color: #B0B3B8; }
            QPushButton.menuHeader:checked { color: #8AB4F8; }
        """