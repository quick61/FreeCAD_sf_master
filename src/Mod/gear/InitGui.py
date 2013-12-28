import FreeCADGui as Gui
import FreeCAD
import gearGui


class gearWorkbench(Workbench):
    """glider workbench"""
    MenuText = "gear"
    ToolTip = "gear workbench"
    Icon = "gearworkbench.svg"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        self.appendToolbar("Gear", ["CreateInvoluteGear", "CreateCycloideGear"])
        self.appendMenu("Gear", ["CreateInvoluteGear", "CreateCycloideGear"])

    def Activated(self):
        pass


    def Deactivated(self):
        pass

Gui.addWorkbench(gearWorkbench())
