\# Changelog




All notable changes to the "Chromium Theme Studio" project will be documented in this file.



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

