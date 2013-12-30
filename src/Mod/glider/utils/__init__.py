from _Classes import *
import FreeCAD
import FreeCADGui
from pivy.coin import SoMouseButtonEvent
from openglider.Vector import norm
from numpy import array


class RunXfoil:
    def __init__(self):
        self.pts = []
        pass
    def GetResources(self):
        return {'Pixmap': 'glider_profile_xfoil.svg', 'MenuText': 'run xfoil', 'ToolTip': 'run xfoil'}
    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True
    def Activated(self):
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.b=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Line")
        self.ml = moveableSpline(self.b, [])
        ViewProvidermoveableSpline(self.b.ViewObject)
        self.a1 = FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Point")
        moveablePoint(self.a1, 1., 1.)
        ViewProvidermoveablePoint(self.a1.ViewObject, self.ml)
        self.a2=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Point")
        moveablePoint(self.a2, 2., 2.)
        ViewProvidermoveablePoint(self.a2.ViewObject, self.ml)
        self.a3=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Point")
        moveablePoint(self.a3, 2., 0.)
        ViewProvidermoveablePoint(self.a3.ViewObject, self.ml)
        self.b.Proxy.addObject(self.a1)
        self.b.Proxy.addObject(self.a2)
        self.b.Proxy.addObject(self.a3)
        self.createcallback = self.view.addEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self._makepoint)

    def _makepoint(self,event_cb):
        event = event_cb.getEvent()
        if event.getState() == SoMouseButtonEvent.DOWN and event.wasCtrlDown():
            print(dir(self.b.Proxy))
            pos = event.getPosition()
            point = self.view.getPoint(pos[0],pos[1])
            self.x=point[0]
            self.y=point[1]
            if self.x != False and self.y!=False:

                self.a=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Point")
                moveablePoint(self.a, self.x, self.y)
                ViewProvidermoveablePoint(self.a.ViewObject, self.ml)
                self.ml.insertObject(self._mindist([self.x,self.y]),self.a)

    def _mindist(self, newpoint):
        np = array(newpoint)
        pts = array([[pt.x,pt.y] for pt in self.ml.Object.points])
        mindist0 = norm(pts[0] - np)
        print(mindist0)
        out = 0
        count = 0
        for pt in pts[1:]:
            count += 1
            mindist = norm(pt - np)
            if mindist< mindist0:
                out = count
        return(out)
