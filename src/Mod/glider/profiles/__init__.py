import FreeCAD
from _Classes import Airfoil, ViewProviderAirfoil
# import FreeCADGui


class LoadProfile:
    def __init__(self):
        pass

    def GetResources(self):
        return {'Pixmap': 'glider_import_profile.svg', 'MenuText': 'load profile', 'ToolTip': 'load profile'}
    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True
    def Activated(self):
        a=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Profile")
        Airfoil(a)
        ViewProviderAirfoil(a.ViewObject)
        FreeCAD.ActiveDocument.recompute()
