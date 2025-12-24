class AppStyles:
    @staticmethod
    def get_light_stylesheet():
        return """
        /* WINDOW STRUCTURE */
        QMainWindow {
            background-color: #F5F5F7; 
            color: #1a1a1a;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        
        /* SCROLL AREAS */
        QScrollArea { background-color: transparent; border: none; }
        QScrollArea > QWidget > QWidget { background-color: #F5F5F7; }

        /* TEXT COLORS (Explicit) */
        QLabel, QCheckBox, QRadioButton { color: #1a1a1a; }

        /* TABS */
        QTabWidget::pane {
            border: 1px solid #D0D0D0;
            background: #FFFFFF;
            border-radius: 6px;
            top: -1px; 
        }
        QTabWidget::tab-bar { left: 5px; }
        QTabBar::tab {
            background: #E0E0E0;
            color: #555;
            padding: 6px 16px;
            margin-right: 4px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background: #FFFFFF;
            color: #1A73E8;
            font-weight: 600;
            border-bottom: 2px solid #1A73E8;
        }

        /* BUTTONS */
        QPushButton {
            background-color: #FFFFFF;
            border: 1px solid #D1D1D1;
            border-radius: 5px;
            padding: 4px 10px;
            color: #333333;
            min-height: 18px;
        }
        QPushButton:hover { background-color: #F8F9FA; border-color: #B0B0B0; }
        QPushButton:pressed { background-color: #E8F0FE; border-color: #1A73E8; color: #1A73E8; }
        
        /* DANGER BUTTON */
        QPushButton[class="dangerBtn"] {
            background-color: #FFF0F0;
            color: #D32F2F;
            border: 1px solid #FFCDD2;
        }
        QPushButton[class="dangerBtn"]:hover { background-color: #FFCDD2; }

        /* INPUTS */
        QLineEdit, QComboBox {
            background-color: #FFFFFF;
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 4px;
            color: #1a1a1a;
            selection-background-color: #1A73E8;
        }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #1A73E8; }
        
        /* FRAMES & GROUPS */
        QGroupBox {
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            margin-top: 24px;
            background-color: #FFFFFF;
            font-weight: bold;
            color: #1a1a1a;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #1A73E8;
        }
        
        QFrame#menu_frame { background-color: #FFFFFF; border-right: 1px solid #E0E0E0; }
        QFrame#ctrl_frame { background-color: #FFFFFF; border-left: 1px solid #E0E0E0; }
        """

    @staticmethod
    def get_dark_stylesheet():
        return """
        /* WINDOW STRUCTURE */
        QMainWindow {
            background-color: #1E1E1E;
            color: #E0E0E0;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        
        /* SCROLL AREAS (Fixes Dark Background in Settings) */
        QScrollArea { background-color: transparent; border: none; }
        QScrollArea > QWidget > QWidget { background-color: #1E1E1E; }
        
        /* GENERAL TEXT RESET */
        QWidget { color: #E0E0E0; }
        QLabel, QCheckBox, QRadioButton { color: #E0E0E0; }

        /* TABS */
        QTabWidget::pane {
            border: 1px solid #333;
            background: #252526;
            border-radius: 6px;
            top: -1px;
        }
        QTabWidget::tab-bar { left: 5px; }
        QTabBar::tab {
            background: #2D2D2D;
            color: #888;
            padding: 6px 16px;
            margin-right: 4px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background: #252526;
            color: #4EC9B0;
            font-weight: bold;
            border-bottom: 2px solid #4EC9B0;
        }

        /* BUTTONS */
        QPushButton {
            background-color: #333333;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 4px 10px;
            color: #E0E0E0;
        }
        QPushButton:hover { background-color: #3E3E3E; border-color: #555; }
        QPushButton:pressed { background-color: #264F78; border-color: #4EC9B0; color: #FFFFFF; }

        /* DANGER BUTTON */
        QPushButton[class="dangerBtn"] {
            background-color: #3C1F1F;
            color: #FF6B6B;
            border: 1px solid #5C2B2B;
        }
        QPushButton[class="dangerBtn"]:hover { background-color: #4C2525; }

        /* INPUTS */
        QLineEdit, QComboBox {
            background-color: #2D2D2D;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 4px;
            color: #E0E0E0;
            selection-background-color: #264F78;
        }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #4EC9B0; }

        /* FRAMES & GROUPS */
        QGroupBox {
            border: 1px solid #444;
            border-radius: 6px;
            margin-top: 24px;
            background-color: #252526;
            color: #E0E0E0;
            font-weight: bold;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #4EC9B0;
        }
        
        QFrame#menu_frame { background-color: #252526; border-right: 1px solid #333; }
        QFrame#ctrl_frame { background-color: #252526; border-left: 1px solid #333; }
        """