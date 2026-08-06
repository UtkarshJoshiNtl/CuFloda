# S-Stream GUI Redesign — Master Implementation Plan & Research Summary

## Executive Summary
This document synthesizes research from 9 professional scientific and media tools (ParaView, Blender, DaVinci Resolve, TouchDesigner, Ableton Live, ANSYS Fluent, COMSOL, OpenFOAM, MATLAB/Simulink) and establishes a phase-by-phase execution plan for rebuilding the S-Stream fluid dynamics workbench GUI.

---

## 1. Key Research Findings & Design Principles

### Comparative Insights Across 9 Professional Tools
1. **Blender**: Uses persistent vertical accordion sections (never tabbed out of view). Sliders support middle-click value ladder fine-tuning. Viewport overlays are cleanly toggleable.
2. **DaVinci Resolve**: Anchors transport controls (play, reset, step) to the bottom of the screen with dedicated timecode/step counters and J-K-L shuttle shortcuts. Modeless parameter editing provides immediate feedback.
3. **ANSYS Fluent**: Residual/stability strip charts are auto-shown during simulation solves. Pre-run check ("Check Mesh / Check Setup") validates state before launching computation.
4. **TouchDesigner**: Every pipeline stage is live and modeless. Instant live feedback on parameter updates.
5. **Ableton Live**: Fixed status/control bar containing live system readouts (BPM, CPU %, transport controls) anchored permanently.

### S-Stream Anti-Pattern Removals
- ❌ **Toolbar Overcrowding**: Replace 20-button toolbar strip with bottom transport bar + accordion sidebar + minimal canvas overlay tool strip.
- ❌ **Tabbed Hidden Dock Panels**: Replace tabbed right docks with a single unified 280px left accordion sidebar.
- ❌ **Viewport Aspect Distortion**: Replace naive window-fill viewport mapping with aspect-preserving, letterboxed `_compute_canvas_rect()` coordinates.
- ❌ **Blind Simulation Execution**: Auto-show a 128px stability strip chart (`max |u|` vs step) in the Analysis section so users instantly see convergence or divergence.

---

## 2. Visual Design System

| Token | Value | Description / Usage |
|---|---|---|
| `bg-base` | `#0d1117` | GitHub Dark base background (canvas & window backdrop) |
| `bg-panel` | `#161b22` | Surface background for sidebar & transport bar |
| `bg-elevated` | `#21262d` | Input fields, dropdowns, headers |
| `border` | `#30363d` | Subtle 1px structural separators |
| `text-primary` | `#e6edf3` | Primary UI text |
| `text-secondary` | `#8b949e` | Labels, units, secondary captions |
| `accent-blue` | `#58a6ff` | Selection highlights, active tool state |
| `accent-green` | `#3fb950` | Stable state, playing transport state |
| `accent-yellow` | `#d29922` | Transition state, near-instability warning |
| `accent-red` | `#f85149` | Divergence / error state |
| `font-ui` | `"Inter", system-ui, sans-serif` | Interface labels & headers |
| `font-mono` | `"JetBrains Mono", monospace` | Monospace numeric readouts (steps, Re, FPS, Cd) |

---

## 3. Target Layout Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  [≡]  S-STREAM  v0.x     [●] Re: 340    FPS: 48    Step: 4,200       │  40px Header
├────────────────────────┬─────────────────────────────────────────────┤
│  LEFT SIDEBAR (280px)  │   VIEWPORT AREA                             │
│                        │                                             │
│  ┌── SCENE ──────────┐ │  [⬤ Circle][▭ Rect][⬠ Poly][⊕ Probe]      │  ← Tool strip (28px)
│  │ Preset▾           │ │  ┌──────────────────────────────────┐       │
│  │ ○ Cylinder  [✕]   │ │  │                                  │       │
│  │ ⊕ Probe 1   [✕]   │ │  │   OpenGL Fluid Canvas            │       │
│  │ [+ Add ▾]         │ │  │   (aspect-preserving, centered)  │       │
│  └───────────────────┘ │  │                                  │       │
│                        │  │   [Colorbar: right edge 12px]    │       │
│  ┌── PARAMETERS ─────┐ │  └──────────────────────────────────┘       │
│  │ ν  ════●════ 0.005 │ │                                             │
│  │ u₀ ════●════ 0.150 │ │  [Hover Inspector Card near cursor]         │
│  │ Re: 340  ● STABLE │ │                                             │
│  └───────────────────┘ │                                             │
│                        │                                             │
│  ┌── VISUALIZE ──────┐ │                                             │
│  │ Field: Vorticity▾  │ │                                             │
│  │ ☑ Streamlines      │ │                                             │
│  │ ☐ Velocity arrows  │ │                                             │
│  └───────────────────┘ │                                             │
│                        │                                             │
│  ┌── ANALYSIS ───────┐ │                                             │
│  │ ● Vortex Shedding  │ │                                             │
│  │ Cd: 1.24  St: 0.21 │ │                                             │
│  │  Stability         │ │                                             │
│  │  ┌─────────────┐  │ │                                             │
│  │  │ max|u| ~~~~  │  │ │                                             │  ← Stability strip chart
│  │  └─────────────┘  │ │                                             │
│  └───────────────────┘ │                                             │
├────────────────────────┴─────────────────────────────────────────────┤
│ [▶][⏮][→|]  ════════════●════════════  ×1▾  Step: 4,200  48 FPS    │  44px Transport
└──────────────────────────────────────────────────────────────────────┘
```

---

## 4. Phased Implementation Strategy (Git Commit Per Phase)

### Phase 1: Global Stylesheet & Splitter Layout Structure
- **Tasks**:
  - Implement design tokens in `resources/style.qss`.
  - Refactor `workbench/app.py` from `QMainWindow` dock-based layout to a clean `QSplitter` layout (280px left sidebar + central viewport container + bottom transport bar).
  - Remove overcrowded top toolbar and tabbed dock widgets.
  - Implement top header bar with live Re, FPS, Step counter.
- **Verification**: `python main.py --headless` builds; app launches with dark theme styling.
- **Commit Message**: `feat(gui): Phase 1 - global stylesheet & splitter layout architecture`

### Phase 2: Aspect-Correct Viewport & Hover Inspector
- **Tasks**:
  - Implement `_compute_canvas_rect()` in `workbench/viewport.py` to preserve grid intrinsic aspect ratio.
  - Update `_widget_to_grid` and `_grid_to_widget` to use canvas bounding box.
  - Implement hover inspector floating card (`QPainter` overlay in `paintGL`).
  - Add minimal canvas tool strip (`[⬤ Circle] [▭ Rect] [⬠ Poly] [⊕ Probe]`) and canvas overlay colorbar.
- **Verification**: Drawing circles produces perfect circles on canvas regardless of window dimensions.
- **Commit Message**: `feat(gui): Phase 2 - aspect-correct viewport, hover inspector & canvas tool strip`

### Phase 3: Accordion Sidebar & Section Modules
- **Tasks**:
  - Create `workbench/panels/sidebar.py` containing `SidebarSection` collapsible accordion widgets.
  - Build `SceneSection`, `ParametersSection`, `VisualizeSection`, and `AnalysisSection`.
  - Wire parameters (viscosity, inflow, Re pill indicator) to simulation engine.
- **Verification**: Expanding/collapsing sections works smoothly; parameter updates immediately reflect in physics engine.
- **Commit Message**: `feat(gui): Phase 3 - accordion sidebar with collapsible scene & parameter panels`

### Phase 4: Transport Bar & Stability Strip Chart
- **Tasks**:
  - Create `workbench/widgets/transport_bar.py` with Play/Pause (green active state), Reset, Step, timeline scrubber, speed dropdown (`×0.25`..`×4`), step counter, and FPS indicator.
  - Build live `max |u|` stability strip chart in `AnalysisSection`.
  - Implement pre-run sanity check banner at Step 0.
- **Verification**: Simulation plays/pauses smoothly, timeline scrubbing works, stability chart live-scrolls without performance drop.
- **Commit Message**: `feat(gui): Phase 4 - bottom transport bar & live stability strip chart`

### Phase 5: Keyboard Shortcuts, Menu Bar & Final Polish
- **Tasks**:
  - Wire full keyboard map (`Space` play/pause, `.` step, `J/K/L` shuttle, `1-4` draw tools, `V` field toggle, `S` streamlines, `Esc` cancel).
  - Refactor header menu `[≡]` with export/preset options.
  - Clean up legacy/dead UI components.
  - Verify overall application functionality and test suite (`pytest`).
- **Verification**: All `pytest` tests pass cleanly; full interactive desktop UI walkthrough.
- **Commit Message**: `feat(gui): Phase 5 - keyboard shortcuts, menu bar refactor & UI polish`
