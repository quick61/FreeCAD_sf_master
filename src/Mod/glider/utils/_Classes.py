import FreeCAD
import FreeCADGui
import PartGui
import numpy
from pivy import coin
from openglider.Utils import Bezier


class moveablePoint():

    """FreeCAD Point"""

    def __init__(self, obj, x, y):

        obj.addProperty("App::PropertyFloat", "x", "coor", "cor-x").x = x
        obj.addProperty("App::PropertyFloat", "y", "coor", "cor-y").y = y
        obj.Proxy = self

    def execute(self, fp):
        pass

    def onChanged(self, fp, prop):
        pass

class ViewProvidermoveablePoint():

    def __init__(self, obj, lineobject):
        self.lineobject = lineobject
        self.object = obj.Object
        self.highlightind = False
        self.drag = False
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.view.addEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.highlight_cb)
        self.view.addEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.begin_drag_cb)
        obj.Proxy = self

    def attach(self, vobj):
        self.out = coin.SoSeparator()
        self.point = coin.SoPointSet()
        self.data = coin.SoCoordinate3()
        self.drawstyle = coin.SoDrawStyle()
        self.color = coin.SoMaterial()
        self.color.diffuseColor.setValue(0, 0, 0)
        self.drawstyle.style = coin.SoDrawStyle.POINTS
        self.drawstyle.pointSize = 5.
        self.out.addChild(self.color)
        self.out.addChild(self.drawstyle)
        self.out.addChild(self.data)
        self.out.addChild(self.point)
        vobj.addDisplayMode(self.out, 'out')

    def updateData(self, fp, prop):
        if prop in ["x", "y"]:
            self.x = fp.x
            self.y = fp.y
            self.data.point.setValue(self.x, self.y, 0)
            self.lineobject.Object.ischanged = False

    def getDisplayModes(self, obj):
        "Return a list of display modes."
        modes = []
        modes.append("out")
        return modes
        pass

    def highlight_cb(self, event_callback):
        event = event_callback.getEvent()
        pos = event.getPosition()
        #FreeCAD.Console.PrintWarning(str(pos)+"bla")
        s = self.view.getPointOnScreen(self.x, self.y, 0.)
        if (abs(s[0] - pos[0]) ** 2 +  abs(s[1] - pos[1]) ** 2) < (15 ** 2):
            if self.highlightind:
                pass
            else:
                self.drawstyle.pointSize = 10.
                self.color.diffuseColor.setValue(0, 1, 1)
                self.highlightind = True
        else:
            if self.highlightind:
                self.drawstyle.pointSize = 5.
                self.highlightind = False
                self.color.diffuseColor.setValue(0, 0, 0)

    def begin_drag_cb(self, cb):
        event = cb.getEvent()
        if self.highlightind and event.getState() == coin.SoMouseButtonEvent.DOWN:
            if self.drag == 0:
                self.dragcb = self.view.addEventCallbackPivy(
                    coin.SoLocation2Event.getClassTypeId(), self.drag_cb)
                self.drag = 1
            elif self.drag == 1:
                self.view.removeEventCallbackPivy(
                    coin.SoLocation2Event.getClassTypeId(), self.dragcb)
                self.drag = 0

    def drag_cb(self, cb):
        event = cb.getEvent()
        pos = event.getPosition()
        point = self.view.getPoint(pos[0], pos[1])
        self.object.x = point[0]
        self.object.y = point[1]
        self.data.point.setValue(self.x, self.y, 0)


class moveableLine():

    """FreeCAD Point"""

    def __init__(self, obj, points):
        obj.addProperty("App::PropertyLinkList", "points", "test", "test")
        obj.addProperty("App::PropertyBool", "ischanged", "test", "test")

        obj.points = points
        obj.ischanged = True
        obj.Proxy = self
        self.Object = obj

    def execute(self, fp):
        pass

    def onChanged(self, fp, prop):
        pass

    def addObject(self, child):
        temp = self.Object.points
        temp.append(child)
        self.Object.points = temp

    def insertObject(self, pos, child):
        temp = self.Object.points
        temp.insert(pos, child)
        self.Object.points = temp

class ViewProvidermoveableLine():

    def __init__(self, obj):
        self.object = obj.Object
        obj.Proxy = self

    def claimChildren(self):
        return(self.object.points)

    def attach(self, vobj):
        self.seperator = coin.SoSeparator()
        self.point = coin.SoLineSet()
        self.data = coin.SoCoordinate3()
        self.color = coin.SoMaterial()
        self.color.diffuseColor.setValue(0, 0, 0)
        self.seperator.addChild(self.color)
        self.seperator.addChild(self.data)
        self.seperator.addChild(self.point)
        vobj.addDisplayMode(self.seperator, 'out')

    def updateData(self, fp, prop):
        p = [[i.x, i.y, 0] for i in fp.points]
        self.data.point.setValue(0, 0, 0)
        self.data.point.setValues(0, len(p), p)

    def getDisplayModes(self, obj):
        "Return a list of display modes."
        modes = []
        modes.append("out")
        return modes


class moveableSpline():

    """FreeCAD Point"""

    def __init__(self, obj, points):
        obj.addProperty("App::PropertyLinkList", "points", "test", "test")
        obj.addProperty("App::PropertyBool", "ischanged", "test", "test")

        obj.points = points
        obj.ischanged = True
        obj.Proxy = self
        self.Object = obj

    def execute(self, fp):
        pass

    def onChanged(self, fp, prop):
        pass

    def addObject(self, child):
        temp = self.Object.points
        temp.append(child)
        self.Object.points = temp

    def insertObject(self, pos, child):
        temp = self.Object.points
        temp.insert(pos, child)
        self.Object.points = temp

class ViewProvidermoveableSpline():

    def __init__(self, obj):
        self.object = obj.Object
        self.bezier = Bezier.BezierCurve([[0,1],[2,3],[3,0]])
        obj.Proxy = self

    def claimChildren(self):
        return(self.object.points)

    def attach(self, vobj):
        self.seperator = coin.SoSeparator()
        self.point = coin.SoLineSet()
        self.data = coin.SoCoordinate3()
        self.color = coin.SoMaterial()
        self.color.diffuseColor.setValue(0, 0, 0)
        self.seperator.addChild(self.color)
        self.seperator.addChild(self.data)
        self.seperator.addChild(self.point)
        vobj.addDisplayMode(self.seperator, 'out')

    def updateData(self, fp, prop):
        num = 20
        self.bezier.ControlPoints = [[i.x, i.y] for i in self.object.points]
        data = [self.bezier(i*1./(num-1)).tolist() + [0] for i in range(num)]
        self.data.point.setValue(0, 0, 0)
        self.data.point.setValues(0, len(data), data)

    def getDisplayModes(self, obj):
        "Return a list of display modes."
        modes = []
        modes.append("out")
        return modes