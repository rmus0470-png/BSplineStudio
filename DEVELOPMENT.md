# Development Notes

This file records development-environment findings, troubleshooting observations, workarounds, and other notes that may help future contributors.

## 2026-11-06: Numeric B-spline control-point editing and curve/sweep workflow

### Confirmed in FreeCAD 1.1.4

During hands-on work on the duct model, selecting the relevant Curves workbench `BezCurve003` object in the model tree and opening its **Data → Points** property with the ellipsis button opened a vector editor. The editor provides an ID selector and numeric X, Y, and Z fields, plus a **Table** view of all control points.

This is the native numeric editing route to use when the goal is to move an existing B-spline control point precisely. It avoids dragging a small on-screen marker. Do not confuse this with the similarly shaped vector editor opened for the **Comb** object: verify the Property View's **Label** says `BezCurve003` before editing.

A four-point cubic curve was visible in the editor during the duct session:

| Point ID | X (mm) | Y (mm) | Z (mm) |
|---:|---:|---:|---:|
| 1 | 47.05 | -18.88 | 17.95 |
| 2 | 43.58 | -7.26 | 8.07 |
| 3 | 49.18 | 6.32 | 12.94 |
| 4 | 26.87 | 5.37 | 3.95 |

These are a snapshot from one experimental curve, not universal defaults. Point 3 was previously identified in the viewport as `EditNode2`. No coordinate change was confirmed in this session; treat the table as a record, not a prescribed correction.

### Curve and surface diagnostics observed

- The Curves workbench's **Split Curve** operation was used to create separate curve objects and experimental sweep branches. The model tree showed `Sweep002`, `SplitCurve`, `Sweep004`, `SplitCurve001`, and an experimental `Sweep003`.
- A **Discretized_Edge** object and a **Comb** object were also present. The Comb is a curvature-visualization/analysis object, not the driving B-spline and not the place to edit the curve's control points.
- A dialog that initially looked like a point editor belonged to `Comb`; its Property View label exposed the mismatch. Cancel that editor rather than changing the comb's vectors.
- Keep the original good sweep intact while testing. A duplicated sweep may still reference shared Binder/profile/spine geometry; verify dependencies before editing shared inputs or assuming the duplicate is independent.
- The duct issue under investigation was a local crease/edge transition on a broad swept face. The desired correction is local and small. Avoid moving endpoints or changing the whole spine unless inspection shows that is necessary.

### BSplineStudio interface direction

The native Points vector editor confirms that FreeCAD exposes the control-point coordinates numerically, but the stock editor is cumbersome for repeated curve tuning. A proposed BSplineStudio panel should provide:

1. Clear selection and display of the active control-point ID.
2. Readouts and direct numeric entry for X, Y, and Z.
3. Small signed movement controls for each axis, with a user-selectable increment (for example 0.01, 0.1, 0.5, and 1.0 mm).
4. Two-axis/diagonal displacement by entering independent component offsets.
5. Relative movement as well as optional absolute coordinate positioning.
6. A live curve/sweep preview after each committed adjustment, with undo/reset-to-saved-position support.
7. A clear indication of the active coordinate frame and axis directions; do not label screen-left/right as model X/Y without checking the view orientation.
8. Larger, more visible control-point markers where FreeCAD's view-provider API permits it.

Preserve the existing BSplineStudio architecture and current curve-editing approach. This is an additive interface proposal, not authorization to redesign the workbench.

### Further tool research: leads, not yet validated

The following were discussed as possible ways to gain more control over section progression or surface boundaries. They have not yet been validated against the current duct model and should not be presented as proven solutions:

- Curves workbench **Pipeshell**, including its section-related output modes.
- Curves workbench **Sweep2Rails**, which may be useful when both surface boundaries need explicit guide control.
- The separate **CurvedShapes** workbench and its **InterpolatedMiddle** tool.
- FreeCAD Part sweep/loft workflows using intermediate profiles to control how a cross-section changes along a path.

Before using any of these, test on a copy and confirm the exact tool behavior in the installed FreeCAD version. The immediate duct task remains adjusting the existing experimental B-spline numerically, not rebuilding the sweep.

## 2026-11-03: GitHub Desktop and FreeCAD Flatpak repository paths

**Environment:** Fedora Linux, KDE Plasma, FreeCAD 1.1.4 installed as a Flatpak, and a Linux port of GitHub Desktop.

**Observed:** GitHub Desktop repeatedly failed to locate or consistently operate on the local repository when it was located inside FreeCAD's versioned Flatpak application-data directory. Its file-manager action did not open the expected folder, and at one point Git reported `fatal: unable to get current working directory: No such file or directory`. Git commands run in Konsole could fetch and pull successfully from the repository at that location.

**Development layout chosen:** Keep the actual repository at `~/Documents/GitHub/BSplineStudio` and place a symbolic link named `BSplineStudio` inside `~/.var/app/org.freecad.FreeCAD/data/FreeCAD/v1-1/Mod/`, pointing to the repository.

**Verification:** FreeCAD discovered and displayed the B-Spline Studio workbench through the symbolic link. Activation then failed with `attempted relative import with no known parent package`, a separate Python import issue. Successful full workbench initialization has not yet been verified.

**Scope:** The underlying cause of GitHub Desktop's path-handling failure was not established. These observations do not prove that all GitHub Desktop installations have this issue. The symbolic-link layout is a development workaround, not a recommended end-user installation process.

## Future notes

Add new findings under dated headings, including the environment, what was observed, the workaround, and what remains unverified.
