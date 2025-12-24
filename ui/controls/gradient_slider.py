from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt

class GradientSlider(QSlider):
    def __init__(self, orientation, parent=None, mode="hue"):
        super().__init__(orientation, parent)
        self.mode = mode
        
        # 1. Define the base geometry for the groove
        # We use a CSS gradient for the background to ensure it always shows up
        groove_style = "border: 1px solid #bbb; height: 10px; border-radius: 5px;"
        
        # 2. Apply the specific gradient based on mode
        if self.mode == "hue":
            # Qt Stylesheet Gradient (Rainbow)
            # This replaces the manual QLinearGradient painting
            bg_gradient = (
                "qlineargradient(x1:0, y1:0, x2:1, y2:0, "
                "stop:0 #FF0000, stop:0.166 #FFFF00, stop:0.333 #00FF00, "
                "stop:0.5 #00FFFF, stop:0.666 #0000FF, stop:0.833 #FF00FF, stop:1 #FF0000)"
            )
            groove_style += f" background: {bg_gradient};"
        else:
            # Fallback for other modes (transparent or default)
            groove_style += " background: transparent;"

        # 3. Define the Handle style
        handle_style = (
            "background: white; border: 1px solid #777; width: 14px; "
            "margin: -5px 0; border-radius: 7px;"
        )

        # 4. Apply the full stylesheet
        self.setStyleSheet(f"""
            QSlider::groove:horizontal {{ {groove_style} }}
            QSlider::handle:horizontal {{ {handle_style} }}
        """)

    # NOTE: paintEvent is removed completely. 
    # We let Qt's stylesheet engine handle the drawing to prevent conflicts.