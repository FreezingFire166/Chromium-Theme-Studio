# Chromium Theme Studio

Chromium Theme Studio is a lightweight Windows desktop application that lets you
create themes for Chromium-based browsers (Chrome, Brave, Edge) with a live preview,
full image control, and precise color editing — no coding required.

This project is open source and designed to be simple for users and flexible for developers.

---

## ✨ Features

- Live Chromium-style preview
- Frame and background image support
- Precise color editor (no AI or gradient presets)
- Image positioning, scaling, and anchoring
- Export themes as installable Chromium theme ZIPs
- Standalone Windows EXE (~45 MB)
- No Python or setup required for end users

---

## 📦 Download (For Non-Coders)

You can download the ready-to-use Windows application from the **Releases** page.

➡ **Download here:**  
https://github.com/FreezingFire166/Chromium-Theme-Studio/releases

Just download the `.exe` file and run it — nothing else is required.

---

## 🧑‍💻 For Developers

### Requirements
- Python 3.10 or newer
- PySide6

### Run from source

```bash
pip install -r requirements.txt
python -m app.main

Build the Windows EXE
python -m PyInstaller --noconsole --onefile --icon assets/app_icon.ico \
  --name "Chromium Theme Studio" app/main.py
 Project Structure
Chromium-Theme-Studio/
├─ app/        # Application entry point
├─ ui/         # Main window and layouts
├─ widgets/    # Custom widgets and preview renderer
├─ engine/     # Theme state, import/export logic
├─ assets/     # Icons and static resources

License
This project is licensed under the MIT License.
You are free to use, modify, and distribute it.

 Credits
Created and maintained by FreezingFire166.
Thank you.
