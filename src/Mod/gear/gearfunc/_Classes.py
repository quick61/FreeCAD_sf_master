# -*- coding: utf-8 -*-
from __future__ import division
import FreeCAD as App
from _shape2D import gearwheel, cycloidegear, bevelgear
from Part import BSplineCurve, Shape, Wire, Face, makePolygon, BRepOffsetAPI, Shell, Solid, makeLoft, show
from math import pi, cos, sin, tan


fcvec = lambda x: App.Vector(x[0],x[1],0)
fcvec3 = lambda x: App.Vector(x[0],x[1],x[2])

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
        obj.addProperty("App::PropertyPythonObject", "gear", "test", "test")
        obj.gear = self.gearwheel
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
        fp.gear.m_n = fp.modul
        fp.gear.z = fp.teeth
        fp.gear.undercut = fp.undercut
        fp.gear.shift = fp.shift
        fp.gear.alpha = fp.alpha * pi / 180.
        fp.gear.beta = fp.beta * pi / 180
        fp.gear.clearence = fp.clearence
        fp.gear._update()
        pts = fp.gear.points(num = fp.numpoints)
        w1 = []
        for i in pts:
            out = BSplineCurve()
            out.interpolate(map(fcvec,i))
            w1.append(out)
        s = Shape(w1)
        wi0 = Wire(s.Edges)
        wi=[]
        for i in range(fp.gear.z):
            rot = App.Matrix()
            rot.rotateZ(i*fp.gear.phipart)
            wi.append(wi0.transformGeometry(rot))
        wi = Wire(wi)
        if fp.beta == 0:
            sh = Face(wi)
            fp.Shape = sh.extrude(App.Vector(0,0,fp.hight))            
        else:
            fp.Shape = helicalextrusion(wi, fp.hight, fp.hight * tan(fp.gear.beta) * 2 / fp.gear.d)

    def onChanged(self, fp, prop):
        if abs(fp.shift) > 1.:
            App.Console.PrintWarning("shift!!!")
        if abs(fp.beta)> 45:
            App.Console.PrintWarning("beta!!!")
            fp.beta = 0.
        if  abs(fp.alpha) > 40:
            App.Console.PrintWarning("alpha!!!")
            fp.alpha = 0.
        if fp.modul <= 0.:
            App.Console.PrintWarning("modul!!!")
            fp.modul = 0.25
        if fp.clearence > 0.25:
            App.Console.PrintWarning("clearence!!!")
            fp.clearence = 0.25
        if fp.clearence < 0.00:
            App.Console.PrintWarning("clearence!!!")
            fp.clearence = 0.00


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

    def onChanged(self, fp, prop):
        if abs(fp.beta)> 45:
            App.Console.PrintWarning("beta!!!")
            fp.beta = 0.
        if fp.modul <= 0.:
            App.Console.PrintWarning("modul!!!")
            fp.modul = 0.25
        if fp.clearence > 0.25:
            App.Console.PrintWarning("clearence!!!")
            fp.clearence = 0.25
        if fp.clearence < 0.0:
            App.Console.PrintWarning("clearence!!!")
            fp.clearence = 0.0


class bevel_gear():
    """parameters:
        alpha:  pressureangle,   10-30°
        gamma:  cone angle,      0 < gamma < pi/4
    """
    def __init__(self, obj):
        self.bevelgear = bevelgear()
        obj.addProperty("App::PropertyInteger", "teeth","props", "number of teeth")
        obj.addProperty("App::PropertyFloat", "hight", "props","hight")
        obj.addProperty("App::PropertyAngle", "gamma", "props", "gamma")
        obj.addProperty("App::PropertyAngle", "alpha", "props", "alpha")
        obj.addProperty("App::PropertyFloat", "m", "props", "m")
        obj.addProperty("App::PropertyFloat", "c", "props", "clearence")
        obj.addProperty("App::PropertyInteger", "numpoints", "props", "number of points for spline")
        obj.m = 0.25
        obj.teeth = 15
        obj.alpha = 70.
        obj.gamma = 45.
        obj.hight = 1.
        obj.numpoints = 6
        self.obj = obj
        obj.Proxy = self

    def execute(self, fp):
        self.bevelgear.z = fp.teeth
        self.bevelgear.alpha = fp.alpha * pi / 180.
        self.bevelgear.gamma = fp.gamma * pi / 180
        self.bevelgear._update()
        pts = self.bevelgear.points(num = fp.numpoints)
        w1 = self.createteeths(pts, fp.m * fp.teeth / 2 + fp.hight / 2)  
        w2 = self.createteeths(pts, fp.m * fp.teeth / 2 - fp.hight / 2)
        fp.Shape = makeLoft([w1,w2],True)

    def createteeths(self, pts, pos):
        w1=[]
        for i in pts:
            scale = lambda x: x*pos
            i_scale = map(scale, i)
            out = BSplineCurve()
            out.interpolate(map(fcvec3,i_scale))
            w1.append(out)
        s = Shape(w1)
        wi0 = Wire(s.Edges)
        wi=[]
        for i in range(self.bevelgear.z):
            rot = App.Matrix()
            rot.rotateZ(-2*i*pi/self.bevelgear.z)
            wi.append(wi0.transformGeometry(rot)) 
        return(Wire(wi))


def helicalextrusion1(wire, height, angle, scale):
    faceb = wire
    faceu=faceb.copy()
    facescale=App.Matrix()
    facescale.scale(App.Vector(scale,scale,scale))
    faceu.transformShape(facescale)
    facetransform=App.Matrix()
    facetransform.rotateZ(angle)
    facetransform.move(App.Vector(0,0,height))
    faceu.transformShape(facetransform)
    # step = 2 + int(angle / pi * 4 )
    # angleinc = angle / (step - 1)
    # zinc = height / (step-1)
    # spine = makePolygon([(0, 0, i * zinc) for i in range(step)])
    # auxspine = makePolygon(
    #     [
    #         (cos(i * angleinc)*(2-i),
    #         sin(i * angleinc)*(2-i),
    #         i * height/(step-1))for i in range(step)
    #     ])
    # faces=[faceb,faceu]
    # pipeshell = BRepOffsetAPI.MakePipeShell(spine)
    # pipeshell.setSpineSupport(spine)
    # pipeshell.add(wire)
    # pipeshell.setAuxiliarySpine(auxspine,True,False)
    # assert(pipeshell.isReady())
    # pipeshell.build()
    # faces.extend(pipeshell.shape().Faces)

    # fullshell = Shell(faces)
    # solid = Solid(fullshell)
    # if solid.Volume < 0:
    #     solid.reverse()
    # assert(solid.Volume >= 0)
    return(makeLoft([faceb, faceu],True))