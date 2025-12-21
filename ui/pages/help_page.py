from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from PySide6.QtCore import Qt

class HelpPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        
        lbl = QTextBrowser()
        lbl.setOpenExternalLinks(True)
        # Fix: Removed hardcoded 'color' attributes so text inherits from the AppStyles stylesheet.
        # Added explicit color for .key to ensure readability on its specific background.
        lbl.setHtml("""
        <style>
            h1 { font-weight: bold; margin-bottom: 5px; }
            h3 { margin-top: 20px; border-bottom: 1px solid #888; padding-bottom: 5px; }
            p, li { font-size: 13px; line-height: 1.6; }
            b { font-weight: bold; }
            .key { 
                color: #000000; 
                background-color: #eeeeee; 
                border: 1px solid #cccccc; 
                border-radius: 3px; 
                padding: 0 4px; 
                font-family: monospace; 
            }
        </style>
        
        <h1>Chromium Theme Studio V2</h1>
        <p>Welcome! This tool allows you to design and export professional themes for Chrome, Brave, Edge, and other Chromium browsers.</p>
        
        <h3>🛠️ How to Use</h3>
        <ul>
            <li><b>Select a Target:</b> Use the menu on the left to choose what you want to edit (e.g., <i>Frame</i>, <i>Active Tab</i>, <i>Toolbar</i>).</li>
            <li><b>Pick a Color:</b>
                <ul>
                    <li>Click the <b>Pick</b> button to use a standard color wheel.</li>
                    <li>Use the <b>RGB/Alpha Sliders</b> on the right for precise adjustments.</li>
                    <li>Enter a specific <b>Hex Code</b> (e.g., #FF0000FF) directly in the text box.</li>
                </ul>
            </li>
            <li><b>Preview:</b> The central canvas updates instantly. Use the dropdown at the top to check how it looks in <i>Chrome</i> vs <i>Edge</i> vs <i>Brave</i>.</li>
        </ul>

        <h3>🖼️ Images & Backgrounds</h3>
        <ul>
            <li><b>Drag & Drop:</b> Simply drag any JPG or PNG image directly onto the preview area.
                <ul>
                    <li>Drop on the <b>Header</b> to set the Frame Image.</li>
                    <li>Drop on the <b>Background</b> to set the New Tab Page (NTP) image.</li>
                </ul>
            </li>
            <li><b>Positioning:</b> Once an image is loaded, use the <b>Scale</b>, <b>X</b>, and <b>Y</b> sliders in the "Image Preview" panel to fit it perfectly.</li>
            <li><b>Remove:</b> Click "Remove Image" to revert to a solid color.</li>
        </ul>

        <h3>🕵️ Incognito & Modes</h3>
        <ul>
            <li><b>Incognito Mode:</b> Check the "Incognito Mode" box in the top bar to design your private browsing style separately.</li>
            <li><b>Preview Resolution:</b> Click the resolution buttons (16:9, Ultra) to ensure your theme looks good on different screen sizes.</li>
        </ul>

        <h3>⚡ Shortcuts & Advanced</h3>
        <ul>
            <li><b>Undo/Redo:</b> Made a mistake? Press <span class="key">Ctrl+Z</span> to Undo and <span class="key">Ctrl+Y</span> to Redo.</li>
            <li><b>Fullscreen:</b> Click the <b>⛶</b> icon to inspect your theme in full detail.</li>
            <li><b>Export:</b> Go to the <b>Export</b> tab to generate a <code>.crx</code> (installable) or <code>.zip</code> (store ready) file.</li>
        </ul>

        <hr>
        <h3>📞 Contact & Support</h3>
        <p>Found a bug or have a suggestion? We want to hear from you!</p>
        <p>
            <a href="https://github.com/FreezingFire166/Chromium-Theme-Studio/issues" style="font-size: 16px; font-weight: bold; color: #1A73E8; text-decoration: none;">
            👉 Open an Issue on GitHub
            </a>
        </p>
        """)
        layout.addWidget(lbl)