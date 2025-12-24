# Chromium Theme Studio V2

A professional, visual theme creator for Chromium-based browsers (Google Chrome, Brave, Microsoft Edge). Design your browser's look with a live preview and export it as a ready-to-install package.


## 📥 Download (For Users)
**You do not need to know how to code to use this.**

1. **[Download the latest .exe here](https://github.com/FreezingFire166/Chromium-Theme-Studio/releases)**
2. Run `ChromiumThemeStudio.exe`.
3. *(Optional)* If Windows protects your PC (SmartScreen), click **"More Info"** -> **"Run Anyway"**. This is normal for new open-source software that hasn't purchased a digital certificate yet.

## ✨ Key Features
* **🔦 Spotlight FX (NEW):** A premium, physics-based "Torch" effect that follows your mouse. It magnetically snaps to buttons and tiles, morphs shapes, and features dynamic "re-ignition" physics when moving between elements.
* **🎨 Live Preview**: See changes instantly on a mock browser canvas that simulates Chrome, Brave, and Edge.
* **🌗 Dark & Light Modes**: A fully responsive UI that adapts to your system theme. Now features consistent text styling and optimized backgrounds across all modes.
* **🛠️ Appearance Tab**: A new dedicated settings section to control the Spotlight's Radius, Magnetic Strength, Opacity, and custom colors for both Light and Dark themes.
* **🕵️ Incognito Mode**: Design separate styles for private browsing windows.
* **🌈 Smart Controls**: Use the new Gradient Hue Sliders, color pickers, or Hex codes to fine-tune your palette.
* **🖼️ Images**: Drag & drop images for the Toolbar or New Tab Page.
* **undo History**: Robust Undo (`Ctrl+Z`) and Redo (`Ctrl+Y`) support.

## 📖 How to Install a Theme
1. **Export** your theme from the app (save as `.zip`).
2. Open your browser (Chrome/Brave/Edge) and go to `chrome://extensions`.
3. Turn on **Developer Mode** (usually a toggle in the top right).
4. Drag and drop your `.zip` file directly onto that page.
   * *Note: If the .zip drag-and-drop doesn't work, extract the zip first and use the "Load Unpacked" button.*

## 🛠️ Development (For Programmers)
If you want to modify the source code or build it yourself.

### Requirements
* Python 3.10+
* `pip install PySide6`

### Running from Source
```bash
git clone [https://github.com/FreezingFire166/Chromium-Theme-Studio.git](https://github.com/FreezingFire166/Chromium-Theme-Studio.git)
cd Chromium-Theme-Studio
pip install -r requirements.txt
python main.py
