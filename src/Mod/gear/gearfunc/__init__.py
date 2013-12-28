import FreeCAD
from _Classes import involute_gear, cycloide_gear


class CreateInvoluteGear():
    def __init__(self):
        pass

    def GetResources(self):
        return {'Pixmap': 'involutegear.svg', 'MenuText': 'involute gear', 'ToolTip': 'involute gear'}

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True

    def Activated(self):
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "involute_gear")
        involute_gear(a)
        a.ViewObject.Proxy = 0.
        FreeCAD.ActiveDocument.recompute()


class CreateCycloideGear():
    def __init__(self):
        pass

    def GetResources(self):
        return {'Pixmap': 'cycloidegear.svg', 'MenuText': 'cycloide gear', 'ToolTip': 'cycloide gear'}

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True

    def Activated(self):
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "cycloide_gear")
        cycloide_gear(a)
        a.ViewObject.Proxy = 0.
        FreeCAD.ActiveDocument.recompute()
