import FreeCADGui as Gui
from gearfunc import CreateCycloideGear, CreateInvoluteGear, CreateBevelGear


Gui.addCommand('CreateInvoluteGear', CreateInvoluteGear())
Gui.addCommand('CreateCycloideGear', CreateCycloideGear())
Gui.addCommand('CreateBevelGear', CreateBevelGear())