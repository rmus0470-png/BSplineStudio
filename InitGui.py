import FreeCADGui as Gui

class BSplineStudioWorkbench(Gui.Workbench):
    MenuText = 'B-Spline Studio'
    ToolTip = 'Inspect and edit B-spline geometry'

    def Initialize(self):
        from . import panel
        Gui.addCommand('BSplineStudio_Open', panel.OpenPanelCommand())
        self.appendToolbar('B-Spline Studio', ['BSplineStudio_Open'])
        self.appendMenu('B-Spline Studio', ['BSplineStudio_Open'])

    def GetClassName(self):
        return 'Gui::PythonWorkbench'

Gui.addWorkbench(BSplineStudioWorkbench())
