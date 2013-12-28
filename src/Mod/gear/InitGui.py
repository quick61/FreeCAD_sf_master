import FreeCADGui as Gui
import FreeCAD
import gear_rc


class gearWorkbench(Workbench):
    """glider workbench"""
    MenuText = "gear"
    ToolTip = "gear workbench"
    Icon = "gearworkbench.svg"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):

        from gearfunc import CreateCycloideGear, CreateInvoluteGear

        self.appendToolbar("Gear", ["CreateInvoluteGear", "CreateCycloideGear"])
        self.appendMenu("Gear", ["CreateInvoluteGear", "CreateCycloideGear"])
        Gui.addIconPath(FreeCAD.getHomePath()+"Mod/gear/icons/")
        Gui.addCommand('CreateInvoluteGear', CreateInvoluteGear())
        Gui.addCommand('CreateCycloideGear', CreateCycloideGear())

    def Activated(self):
        pass


    def Deactivated(self):
        pass

Gui.addWorkbench(gearWorkbench())
