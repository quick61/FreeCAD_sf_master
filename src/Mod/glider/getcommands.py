import FreeCADGui as Gui
import FreeCAD


Gui.addIconPath(FreeCAD.getHomePath()+"Mod/glider/icons")

from profiles import LoadProfile
from glider import CreateGlider

Gui.addCommand('LoadProfile', LoadProfile())
Gui.addCommand('CreateGlider', CreateGlider())