from __future__ import division
import FreeCAD as App
from _shape2D import gearwheel, cycloidegear
from Part import BSplineCurve, Shape, Wire, Face, makePolygon, BRepOffsetAPI, Shell, Solid
from math import pi, cos, sin, tan


fcvec = lambda x: App.Vector(x[0],x[1],0)

class involute_gear():
    """FreeCAD gear"""
    def __init__(self, obj):
        self.gearwheel = gearwheel()
        obj.addProperty("App::PropertyInteger", "teeth","props", "number of teeth")
        obj.addProperty("App::PropertyFloat", "modul", "props","modul")
        obj.addProperty("App::PropertyBool", "undercut", "props","undercut")
        obj.addProperty("App::PropertyFloat", "shift", "props","shift")
        obj.addProperty("App::PropertyFloat", "hight", "props","hight")
        obj.addProperty("App::PropertyAngle", "alpha", "props", "alpha")
        obj.addProperty("App::PropertyFloat", "clearence", "props", "clearence")
        obj.addProperty("App::PropertyInteger", "numpoints", "props", "number of points for spline")
        obj.addProperty("App::PropertyAngle", "beta", "props", "beta ")
        obj.teeth = 15
        obj.modul = 0.25
        obj.undercut = True
        obj.shift = 0.
        obj.alpha = 20.
        obj.beta = 0.
        obj.hight = 1.
        obj.clearence = 0.12
        obj.numpoints = 6
        self.obj = obj
        obj.Proxy = self

    def execute(self, fp):
        self.gearwheel.m_n = fp.modul
        self.gearwheel.z = fp.teeth
        self.gearwheel.undercut = fp.undercut
        self.gearwheel.shift = fp.shift
        self.gearwheel.alpha = fp.alpha * pi / 180.
        self.gearwheel.beta = fp.beta * pi / 180
        self.gearwheel.clearence = fp.clearence
        self.gearwheel._update()
        pts = self.gearwheel.points(num = fp.numpoints)
        w1 = []
        for i in pts:
            out = BSplineCurve()
            out.interpolate(map(fcvec,i))
            w1.append(out)
        s = Shape(w1)
        wi0 = Wire(s.Edges)
        wi=[]
        for i in range(self.gearwheel.z):
            rot = App.Matrix()
            rot.rotateZ(i*self.gearwheel.phipart)
            wi.append(wi0.transformGeometry(rot))
        wi = Wire(wi)
        if fp.beta == 0:
            sh = Face(wi)
            fp.Shape = sh.extrude(App.Vector(0,0,fp.hight))            
        else:
            fp.Shape = helicalextrusion(wi, fp.hight, fp.hight * tan(self.gearwheel.beta) * 2 / self.gearwheel.d)


def helicalextrusion(wire, height, angle):
    faceb = Face(wire)
    faceu=faceb.copy()
    facetransform=App.Matrix()
    facetransform.rotateZ(angle)
    facetransform.move(App.Vector(0,0,height))
    faceu.transformShape(facetransform)
    step = 2 + int(angle / pi * 4 )
    angleinc = angle / (step - 1)
    zinc = height / (step-1)
    spine = makePolygon([(0, 0, i * zinc) for i in range(step)])
    auxspine = makePolygon(
        [
            (cos(i * angleinc),
            sin(i * angleinc),
            i * height/(step-1))for i in range(step)
        ])
    faces=[faceb,faceu]
    pipeshell = BRepOffsetAPI.MakePipeShell(spine)
    pipeshell.setSpineSupport(spine)
    pipeshell.add(wire)
    pipeshell.setAuxiliarySpine(auxspine,True,False)
    assert(pipeshell.isReady())
    pipeshell.build()
    faces.extend(pipeshell.shape().Faces)

    fullshell = Shell(faces)
    solid = Solid(fullshell)
    if solid.Volume < 0:
        solid.reverse()
    assert(solid.Volume >= 0)
    return(solid)


class cycloide_gear():
    """FreeCAD gear"""
    def __init__(self, obj):
        self.cycloidegear = cycloidegear()
        obj.addProperty("App::PropertyInteger", "teeth","props", "number of teeth")
        obj.addProperty("App::PropertyFloat", "modul", "props","modul")
        obj.addProperty("App::PropertyFloat", "d1", "props","d1")
        obj.addProperty("App::PropertyFloat", "d2", "props","d2")
        obj.addProperty("App::PropertyFloat", "hight", "props","hight")
        obj.addProperty("App::PropertyFloat", "clearence", "props", "clearence")
        obj.addProperty("App::PropertyInteger", "numpoints", "props", "number of points for spline")
        obj.addProperty("App::PropertyAngle", "beta", "props", "beta")
        obj.teeth = 15
        obj.modul = 0.25
        obj.d1 = 2
        obj.d2 = 2
        obj.beta = 0.
        obj.hight = 1.
        obj.clearence = 0.12
        obj.numpoints = 6
        obj.Proxy = self

    def execute(self, fp):
        self.cycloidegear.m = fp.modul
        self.cycloidegear.z = fp.teeth
        self.cycloidegear.d1 = fp.d1
        self.cycloidegear.d2 = fp.d2
        self.cycloidegear.clearence = fp.clearence
        self.cycloidegear._update()
        pts = self.cycloidegear.points(num = fp.numpoints)
        w1 = []
        for i in pts:
            out = BSplineCurve()
            out.interpolate(map(fcvec,i))
            w1.append(out)
        s = Shape(w1)
        wi0 = Wire(s.Edges)
        wi=[]
        for i in range(self.cycloidegear.z):
            rot = App.Matrix()
            rot.rotateZ(i*self.cycloidegear.phipart)
            wi.append(wi0.transformGeometry(rot))
        wi = Wire(wi)
        if fp.beta == 0:
            sh = Face(wi)
            fp.Shape = sh.extrude(App.Vector(0,0,fp.hight))            
        else:
            fp.Shape = helicalextrusion(wi, fp.hight, fp.hight * tan(fp.beta * pi / 180) * 2 / self.cycloidegear.d)