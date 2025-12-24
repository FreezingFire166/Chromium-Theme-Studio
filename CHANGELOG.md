***

### `CHANGELOG.md`

```markdown
# Changelog

All notable changes to the "Chromium Theme Studio" project will be documented in this file.

## [v2.3.7] - 2025-12-24

### ✨ New Features
- **Spotlight FX (Torch Mode):**
    - Introduced a physics-based visual overlay where the cursor acts as a dynamic light source.
    - **Universal Magnetism:** The light now magnetically snaps to *all* buttons and tiles, not just presets.
    - **Re-Ignition Physics:** Added a "Pop" effect where the light resets its radius to 0 and grows back when disconnecting from a target.
    - **Shape Morphing:** The spotlight smoothly transforms into a rounded rectangle (8px radius) when locked onto targets.
- **Settings Overhaul:**
    - Refactored Settings into tabs: **General**, **Appearance**, and **Advanced**.
    - **Spotlight Customization:** Added sliders for Beam Radius, Magnetic Pull Strength, and **Intensity (Opacity)**.
    - Added dedicated color pickers for Spotlight states in both Light and Dark modes.

### ⚡ Improvements & Fixes
- **UI/UX Polish:**
    - **Gradient Sliders:** Rewrote `GradientSlider` to use native Qt Stylesheets, fixing visibility issues where the track appeared white/transparent.
    - **Button Padding:** Optimized padding on small buttons so navigation symbols (`<`, `>`) are no longer clipped.
    - **Dark Mode Consistency:** Fixed inconsistent text colors on labels and checkboxes when switching themes.
- **Light Mode Fixes:**
    - Solved an issue where the Settings Page background remained dark in Light Mode.
    - Fixed "White-on-White" text visibility issues by enforcing explicit stylesheet rules.
    - Changed Spotlight blend mode from `Overlay` to `SourceOver` to ensure visibility on light backgrounds.
- **Performance:**
    - Added exclusion zones to prevent the Spotlight from magnetizing to the Top Bar or Settings/Export pages.
    - Optimized mouse tracking to use `QCursor.pos()` for accurate global coordinates.

---

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
- **Export Logic:** Added safety checks to prevent crashes if metadata fields are empty.

---

## [v2.1.0] - 2025-12-22

### ✨ Features
- **Undo/Redo System:** Implemented a robust History Manager.
    - Use `Ctrl+Z` to Undo.
    - Use `Ctrl+Y` to Redo.
- **App Styling:**
    - Added a comprehensive `AppStyles` class to centralize Light/Dark themes.
    - Improved scrollbar styling for a modern feel.

### 🐛 Bug Fixes
- Fixed an issue where the preview would desync after loading a saved JSON file.
- Corrected the `manifest.json` generation logic for "Incognito" frame colors.

---

## [v2.0.0] - 2025-12-20

### 🚀 Major Release (Re-write)
- **New Architecture:** Completely rewrote the codebase from scratch using `PySide6` (Qt for Python).
- **Modular Design:** Split the monolithic script into `ui/`, `logic/`, `render/`, and `utils/` packages.
- **Live Preview Engine:** Created a `PreviewRenderer` that accurately mimics Chrome's UI layering (Frame -> Tab -> Toolbar -> NTP).
- **Drag & Drop:** Added support for dropping images directly onto the canvas.