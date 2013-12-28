import FreeCADGui as Gui
import FreeCAD
from gearfunc import CreateCycloideGear, CreateInvoluteGear

Gui.addIconPath(FreeCAD.getHomePath()+"Mod/gear/icons/")
Gui.addCommand('CreateInvoluteGear', CreateInvoluteGear())
Gui.addCommand('CreateCycloideGear', CreateCycloideGear())