# Chromium Theme Studio V2

A professional, visual theme creator for Chromium-based browsers (Google Chrome, Brave, Microsoft Edge). Design your browser's look with a live preview and export it as a ready-to-install package.

## 📥 Download (For Users)
You do not need to know how to code to use this.

1. **[Download the latest .exe here](https://github.com/FreezingFire166/Chromium-Theme-Studio/releases)**
2. Run `ChromiumThemeStudio.exe`.
3. (Optional) If Windows protects your PC, click "More Info" -> "Run Anyway" (this is normal for new open-source software).

## ✨ Features
* **Live Preview**: See changes instantly on a mock browser canvas.
* **Multi-Browser Support**: Accurate previews for Chrome, Brave, and Edge.
* **Incognito Mode**: Design separate styles for private browsing windows.
* **Smart Colors**: Use the color picker, Hex codes, or RGB sliders.
* **Images**: Drag & drop images for the Toolbar or New Tab Page.
* **History**: Undo (Ctrl+Z) and Redo (Ctrl+Y) support.
* **Export**: Generates `.zip` (for sharing) or `.crx` (packed extension) files.

## 📖 How to Install a Theme
1. **Export** your theme from the app (save as `.zip`).
2. Open your browser (Chrome/Brave/Edge) and go to `chrome://extensions`.
3. Turn on **Developer Mode** (usually a toggle in the top right).
4. Drag and drop your `.zip` file directly onto that page.
5. If `.zip` does not work, try unpacking it first and loading the folder.

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