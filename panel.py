"""B-Spline Studio: dockable curve inspection and Part B-spline pole editing."""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets

_dock = None

def bspline_of(obj, sub=None):
    shape = sub if sub is not None else getattr(obj, 'Shape', None)
    if shape is None:
        return None
    edges = getattr(shape, 'Edges', [])
    for edge in edges:
        curve = edge.Curve
        if 'BSplineCurve' in type(curve).__name__:
            return curve
    return None

class CurvePanel(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super().__init__('B-Spline Studio', parent)
        self.setObjectName('BSplineStudioDock')
        self.obj = None
        self.curve = None
        self.updating = False
        root = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(root)
        self.label = QtWidgets.QLabel('Select a B-spline edge or object, then Refresh.')
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        refresh = QtWidgets.QPushButton('Refresh selection')
        refresh.clicked.connect(self.refresh)
        layout.addWidget(refresh)
        self.info = QtWidgets.QLabel('')
        layout.addWidget(self.info)
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['Pole', 'X (mm)', 'Y (mm)', 'Z (mm)'])
        layout.addWidget(self.table)
        self.apply = QtWidgets.QPushButton('Apply pole coordinates (Part geometry only)')
        self.apply.clicked.connect(self.apply_poles)
        layout.addWidget(self.apply)
        self.details = QtWidgets.QPlainTextEdit()
        self.details.setReadOnly(True)
        self.details.setMaximumHeight(150)
        layout.addWidget(self.details)
        self.setWidget(root)
        self.refresh()

    def refresh(self):
        self.obj = None
        self.curve = None
        selection = Gui.Selection.getSelectionEx()
        if not selection:
            self.label.setText('Select a B-spline edge or object, then Refresh.')
            self.table.setRowCount(0)
            return
        sel = selection[0]
        obj = sel.Object
        sub = sel.SubObjects[0] if sel.SubObjects else None
        curve = bspline_of(obj, sub)
        self.obj, self.curve = obj, curve
        if curve is None:
            self.label.setText('No B-spline found in the selection.')
            self.table.setRowCount(0)
            return
        sketch = obj.isDerivedFrom('Sketcher::SketchObject')
        self.label.setText('%s | %s' % (obj.Label, 'Sketcher: inspect only' if sketch else 'Part geometry'))
        poles = curve.getPoles()
        self.info.setText('Degree: %s    Poles: %s' % (curve.Degree, len(poles)))
        self.table.setRowCount(len(poles))
        for i, p in enumerate(poles):
            for j, value in enumerate((str(i + 1), str(p.x), str(p.y), str(p.z))):
                item = QtWidgets.QTableWidgetItem(value)
                if j == 0:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.table.setItem(i, j, item)
        self.apply.setEnabled(not sketch)
        self.details.setPlainText('Knots: %s\nMultiplicities: %s\nWeights: %s' % (
            curve.getKnots(), curve.getMultiplicities(), curve.getWeights()))

    def apply_poles(self):
        if self.obj is None or self.curve is None:
            return
        if self.obj.isDerivedFrom('Sketcher::SketchObject'):
            self.label.setText('Sketcher editing is not enabled: constraints must be preserved.')
            return
        try:
            import Part
            points = []
            for i in range(self.table.rowCount()):
                coords = [float(self.table.item(i, j).text()) for j in (1, 2, 3)]
                points.append(App.Vector(*coords))
            curve = self.curve.copy()
            for i, point in enumerate(points, 1):
                curve.setPole(i, point)
            doc = self.obj.Document
            doc.openTransaction('B-Spline Studio: edit poles')
            try:
                # Never overwrite a generated feature or a parametric dependency.
                # Create an editable standalone copy instead.
                result = doc.addObject('PartDesign::Feature', 'EditedBSpline')
                result.Label = self.obj.Label + ' (edited spline copy)'
                result.Shape = curve.toShape()
                doc.recompute()
                doc.commitTransaction()
            except Exception:
                doc.abortTransaction()
                raise
            self.label.setText('Created editable copy: ' + result.Label)
        except Exception as exc:
            QtWidgets.QMessageBox.warning(self, 'B-Spline Studio', str(exc))

class OpenPanelCommand:
    def GetResources(self):
        return {'MenuText': 'Open B-Spline Studio', 'ToolTip': 'Open B-spline control panel'}
    def Activated(self):
        global _dock
        mw = Gui.getMainWindow()
        if _dock is None:
            _dock = CurvePanel(mw)
            mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, _dock)
        _dock.show()
        _dock.raise_()
    def IsActive(self):
        return True
