import FreeCAD
from _Classes import Glider

class CreateGlider():
    def __init__(self):
        pass

    def GetResources(self):
        return {'Pixmap': 'involutegear.svg', 'MenuText': 'CreateGlider', 'ToolTip': 'CreateGlider'}

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True

    def Activated(self):
        Glider()
        FreeCAD.ActiveDocument.recompute()