\# Changelog




All notable changes to the "Chromium Theme Studio" project will be documented in this file.



## [v2.2.0] - 2025-12-23

### 🚀 New Features
- **True Fullscreen Mode:** The preview now resizes to fill your entire monitor (fixing previous letterboxing). Added keyboard shortcuts (`F11`, `F`) to toggle and `ESC` to exit, along with a helpful overlay.
- **Advanced Customization:**
    - Added **NTP Background** color support.
    - Added full control over **Search Bar (Omnibox)** background and text colors.
    - Added **Incognito Defaults** for the search bar to prevent style mismatches.
- **Professional Presets:** Replaced legacy presets with a modern collection: *Matte Black, Clean White, Nordic, Slate Pro, and Soft Dark*.
- **Welcome Experience:** Added a friendly "Welcome" greeting that appears only on the very first app launch.

### ⚡ Improvements & Changes
- **UI Polish:**
    - Replaced the debug "red dotted line" with a clean, theme-aware boundary for the preview area.
    - Navigation buttons (`< >`) now correctly respect the **"Buttons"** tint color.
    - Restyled the **Fullscreen** button to match the app's professional aesthetic.
    - Reverted the selection indicator line on menu tiles to its optimal position.
- **Menu UX:** Implemented "Accordion" behavior—opening one menu group (like "Basic") now automatically closes others to keep the interface clean.
- **Export Engine:** Updated `ExportManager` to fully support the new Omnibox and Background keys in the generated `manifest.json`.

### 🐛 Bug Fixes
- **Settings Persistence:** Fixed a critical issue where "Always Dark Mode" and other preferences were not saving to disk or restoring upon restart.
- **Search Bar Logic:** Removed automatic color override on the search bar; it now strictly follows user settings.
- **Menu Organization:** Moved "Frame" into a new **"Basic"** group and removed the redundant "Text" button from the Toolbar section.



## [2.0.5] - 22/12/2025

### 🐛 Bug Fixes
* **Image Persistence:** Fixed a bug where image parameters (scale/position) were resetting to defaults when switching editing modes.
* **NTP Image Visibility:** Fixed an issue where the New Tab Page background image was hidden behind the UI layer in the preview.
* **Guide Resize:** The red dotted guide overlay now correctly resizes when applying custom resolutions.



\## \[2.0.0] - 21/12/2025

\### 🚀 Major Rewrite (V2)

We have completely structured the application from a single script into a professional, modular architecture. This improves stability, performance, and makes future updates much faster.



\### ✨ New Features

\* \*\*Incognito Mode Support:\*\* You can now design the "Incognito" (Private) window style separately from the normal window.

\* \*\*Undo/Redo System:\*\* Made a mistake? Use `Ctrl+Z` to Undo and `Ctrl+Y` to Redo your changes.

\* \*\*Settings Page:\*\* A new dedicated settings tab allows you to:

&nbsp;   \* Toggle the app's own Dark/Light mode.

&nbsp;   \* Enable "Auto-increment Version" to automatically bump version numbers on export.

&nbsp;   \* Choose your preferred target browser for previews (Chrome, Brave, Edge).

\* \*\*Theme Presets:\*\* Added a "Presets" dropdown with popular styles (Dracula, Midnight, Solarized, High Contrast) to help you get started quickly.

\* \*\*Fullscreen Preview:\*\* Added a fullscreen button (`⛶`) to inspect your theme on a clean, black canvas.



\### ⚡ Improvements

\* \*\*Visual Overhaul:\*\* The UI has been refreshed with a cleaner "Top Bar" layout, sliding animations, and improved spacing.

\* \*\*Brave \& Edge Support:\*\* The preview engine now accurately simulates the tab shapes and colors of Brave and Microsoft Edge.

\* \*\*Smart Sliders:\*\* RGB sliders now support direct text input and keyboard navigation.



\### 🛠️ Technical

\* \*\*Refactored Codebase:\*\* Split the monolithic `main\_window.py` into separate modules (`ui/`, `logic/`, `render/`) for better maintainability.

\* \*\*Windows Integration:\*\* Added `AppUserModelID` support to fix taskbar icon grouping on Windows 10/11.

\* \*\*Manifest V3:\*\* The exporter now generates fully compliant Manifest V3 theme packages.

