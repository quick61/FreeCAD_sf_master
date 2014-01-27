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

        from gearfunc import CreateCycloideGear, CreateInvoluteGear, CreateBevelGear

        self.appendToolbar("Gear", ["CreateInvoluteGear", "CreateCycloideGear", "CreateBevelGear"])
        self.appendMenu("Gear", ["CreateInvoluteGear", "CreateCycloideGear","CreateBevelGear"])
        Gui.addIconPath(FreeCAD.getHomePath()+"Mod/gear/icons/")
        Gui.addCommand('CreateInvoluteGear', CreateInvoluteGear())
        Gui.addCommand('CreateCycloideGear', CreateCycloideGear())
        Gui.addCommand('CreateBevelGear', CreateBevelGear())

    def Activated(self):
        pass


    def Deactivated(self):
        pass

Gui.addWorkbench(gearWorkbench())
