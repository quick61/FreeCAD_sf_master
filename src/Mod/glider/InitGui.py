import FreeCADGui as Gui
import getcommands


class gliderWorkbench(Workbench):
    """probe workbench object"""
    MenuText = "glider"
    ToolTip = "glider workbench"
    Icon = "glider_workbench.svg"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        #load the module
        self.appendToolbar("Glider", ["LoadProfile", "CreateGlider"])
        self.appendMenu("Glider", ["LoadProfile"])

    def Activated(self):
        pass

    def Deactivated(self):
        pass

Gui.addWorkbench(gliderWorkbench())
