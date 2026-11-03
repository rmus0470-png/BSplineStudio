# Development Notes

This file records development-environment findings, troubleshooting observations, workarounds, and other notes that may help future contributors.

## 2026-11-03: GitHub Desktop and FreeCAD Flatpak repository paths

**Environment:** Fedora Linux, KDE Plasma, FreeCAD 1.1.4 installed as a Flatpak, and a Linux port of GitHub Desktop.

**Observed:** GitHub Desktop repeatedly failed to locate or consistently operate on the local repository when it was located inside FreeCAD's versioned Flatpak application-data directory. Its file-manager action did not open the expected folder, and at one point Git reported `fatal: unable to get current working directory: No such file or directory`. Git commands run in Konsole could fetch and pull successfully from the repository at that location.

**Development layout chosen:** Keep the actual repository at `~/Documents/GitHub/BSplineStudio` and place a symbolic link named `BSplineStudio` inside `~/.var/app/org.freecad.FreeCAD/data/FreeCAD/v1-1/Mod/`, pointing to the repository.

**Verification:** FreeCAD discovered and displayed the B-Spline Studio workbench through the symbolic link. Activation then failed with `attempted relative import with no known parent package`, a separate Python import issue. Successful full workbench initialization has not yet been verified.

**Scope:** The underlying cause of GitHub Desktop's path-handling failure was not established. These observations do not prove that all GitHub Desktop installations have this issue. The symbolic-link layout is a development workaround, not a recommended end-user installation process.

## Future notes

Add new findings under dated headings, including the environment, what was observed, the workaround, and what remains unverified.
