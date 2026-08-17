# 🎨 PPP — Python Pixel Paint

A lightweight, performant, and expandable pixel art canvas editor built using **Python** and **Pygame**.

> ⚠️ **Project Status:** Under Active Development. The core grid matrix and camera system are functional, with advanced painting tools and layer support currently in progress.

---

## ✨ Current Features
* **Optimized Grid Engine:** Custom `Grid`, `Cell`, and `Camera` OOP structure with **Frustum Culling** for high-FPS rendering.
* **Camera Controls:** Smooth zoom (`Mouse Wheel`) and pan (`Middle Mouse` or `Space + Left Click`).
* **Interactive Canvas:** Real-time painting, cell resetting, and bulk clear (`Shift + DEL`).
* **Quick Palettes:** Instant color switching mapped to `F1`–`F10` hotkeys.

---

## 🎯 Roadmap & Final Goals
- [ ] **Essential Tools:** Flood Fill (Bucket), Line/Rectangle/Circle tools, Color Picker (Eyedropper), Eraser.
- [ ] **Layer System:** Multi-layer support with visibility, opacity, and reordering.
- [ ] **History:** Complete Undo / Redo (`Ctrl+Z` / `Ctrl+Y`) state tracking.
- [ ] **Export & Storage:** Save/Load native project files and export high-res PNGs.
- [ ] **UI Polish:** Symmetry draw modes, toggleable grid lines, and interactive color picker UI.

---

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/PPP-python-pixel-paint.git](https://github.com/your-username/PPP-python-pixel-paint.git)
   cd PPP-python-pixel-paint