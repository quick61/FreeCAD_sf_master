# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

from __future__ import division
import FreeCAD as App
from _shape2D import gearwheel, cycloidegear, bevelgear
from Part import BSplineCurve, Shape, Wire, Face, makePolygon, BRepOffsetAPI, Shell, Solid, makeLoft
from math import pi, cos, sin, tan


fcvec = lambda x: App.Vector(x[0],x[1],0)
fcvec3 = lambda x: App.Vector(x[0],x[1],x[2])

class involute_gear():
    """FreeCAD gear"""
    def __init__(self, obj):
        self.gearwheel = gearwheel()
        obj.addProperty("App::PropertyInteger", "teeth","gear_parameter", "number of teeth")
        obj.addProperty("App::PropertyFloat", "module", "gear_parameter","module")
        obj.addProperty("App::PropertyBool", "undercut", "gear_parameter","undercut")
        obj.addProperty("App::PropertyFloat", "shift", "gear_parameter","shift")
        obj.addProperty("App::PropertyFloat", "height", "gear_parameter","height")
        obj.addProperty("App::PropertyAngle", "alpha", "involute_parameter", "alpha")
        obj.addProperty("App::PropertyFloat", "clearence", "gear_parameter", "clearence")
        obj.addProperty("App::PropertyInteger", "numpoints", "gear_parameter", "number of points for spline")
        obj.addProperty("App::PropertyAngle", "beta", "gear_parameter", "beta ")
        obj.addProperty("App::PropertyPythonObject", "gear", "test", "test")
        obj.addProperty("App::PropertyFloat", "backslash", "gear_parameter", "backslash in mm")
        obj.gear = self.gearwheel
        obj.teeth = 15
        obj.module = 0.25
        obj.undercut = True
        obj.shift = 0.
        obj.alpha = 20.
        obj.beta = 0.
        obj.height = 1.
        obj.clearence = 0.12
        obj.numpoints = 6
        obj.backslash = 0.01
        self.obj = obj
        obj.Proxy = self

    def execute(self, fp):
        fp.gear.m_n = fp.module
        fp.gear.z = fp.teeth
        fp.gear.undercut = fp.undercut
        fp.gear.shift = fp.shift
        fp.gear.alpha = fp.alpha * pi / 180.
        fp.gear.beta = fp.beta * pi / 180
        fp.gear.clearence = fp.clearence
        fp.gear.backslash = fp.backslash
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
            fp.Shape = sh.extrude(App.Vector(0,0,fp.height))            
        else:
            fp.Shape = helicalextrusion(wi, fp.height, fp.height * tan(fp.gear.beta) * 2 / fp.gear.d)

    def onChanged(self, fp, prop):
        if abs(fp.shift) > 1.:
            App.Console.PrintWarning("shift!!!")
        if abs(fp.beta)> 45:
            App.Console.PrintWarning("beta!!!")
            fp.beta = 0.
        if  abs(fp.alpha) > 40:
            App.Console.PrintWarning("alpha!!!")
            fp.alpha = 0.
        if fp.module <= 0.:
            App.Console.PrintWarning("module!!!")
            fp.module = 0.25
        if fp.clearence > 0.25:
            App.Console.PrintWarning("clearence!!!")
            fp.clearence = 0.25
        if fp.clearence < 0.00:
            App.Console.PrintWarning("clearence!!!")
            fp.clearence = 0.00


class cycloide_gear():
    """FreeCAD gear"""
    def __init__(self, obj):
        self.cycloidegear = cycloidegear()
        obj.addProperty("App::PropertyInteger", "teeth","gear_parameter", "number of teeth")
        obj.addProperty("App::PropertyFloat", "module", "gear_parameter","module")
        obj.addProperty("App::PropertyFloat", "inner_diameter", "cycloid_parameter","inner_diameter")
        obj.addProperty("App::PropertyFloat", "outer_diameter", "cycloid_parameter","outer_diameter")
        obj.addProperty("App::PropertyFloat", "height", "gear_parameter","height")
        obj.addProperty("App::PropertyFloat", "clearence", "gear_parameter", "clearence")
        obj.addProperty("App::PropertyInteger", "numpoints", "gear_parameter", "number of points for spline")
        obj.addProperty("App::PropertyAngle", "beta", "gear_parameter", "beta")
        obj.addProperty("App::PropertyFloat", "backslash", "gear_parameter", "backslash in mm")
        obj.teeth = 15
        obj.module = 0.25
        obj.inner_diameter = 2
        obj.outer_diameter = 2
        obj.beta = 0.
        obj.height = 1.
        obj.clearence = 0.12
        obj.numpoints = 6
        obj.backslash = 0.01
        obj.Proxy = self

    def execute(self, fp):
        self.cycloidegear.m = fp.module
        self.cycloidegear.z = fp.teeth
        self.cycloidegear.d1 = fp.inner_diameter
        self.cycloidegear.d2 = fp.outer_diameter
        self.cycloidegear.clearence = fp.clearence
        self.cycloidegear.backslash = fp.backslash
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
            fp.Shape = sh.extrude(App.Vector(0,0,fp.height))            
        else:
            fp.Shape = helicalextrusion(wi, fp.height, fp.height * tan(fp.beta * pi / 180) * 2 / self.cycloidegear.d)

    def onChanged(self, fp, prop):
        if abs(fp.beta)> 45:
            App.Console.PrintWarning("beta!!!")
            fp.beta = 0.
        if fp.module <= 0.:
            App.Console.PrintWarning("module!!!")
            fp.module = 0.25
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
        obj.addProperty("App::PropertyInteger", "teeth","gear_parameter", "number of teeth")
        obj.addProperty("App::PropertyFloat", "height", "gear_parameter","height")
        obj.addProperty("App::PropertyAngle", "gamma", "involute_parameter", "gamma")
        obj.addProperty("App::PropertyAngle", "alpha", "involute_parameter", "alpha")
        obj.addProperty("App::PropertyFloat", "m", "gear_parameter", "m")
        obj.addProperty("App::PropertyFloat", "c", "gear_parameter", "clearence")
        obj.addProperty("App::PropertyInteger", "numpoints", "gear_parameter", "number of points for spline")
        obj.addProperty("App::PropertyFloat", "backslash", "gear_parameter", "backslash in mm")
        obj.m = 0.25
        obj.teeth = 15
        obj.alpha = 70.
        obj.gamma = 45.
        obj.height = 1.
        obj.numpoints = 6
        obj.backslash = 0.01
        self.obj = obj
        obj.Proxy = self

    def execute(self, fp):
        self.bevelgear.z = fp.teeth
        self.bevelgear.alpha = fp.alpha * pi / 180.
        self.bevelgear.gamma = fp.gamma * pi / 180
        self.bevelgear.backslash = fp.backslash
        self.bevelgear._update()
        pts = self.bevelgear.points(num = fp.numpoints)
        w1 = self.createteeths(pts, fp.m * fp.teeth / 2 / tan(fp.gamma * pi / 180) + fp.height / 2)  
        w2 = self.createteeths(pts, fp.m * fp.teeth / 2 / tan(fp.gamma * pi / 180) - fp.height / 2)
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


def helicalextrusion(wire, height, angle):
    face_a = Face(wire)
    face_b = face_a.copy()
    face_transform = App.Matrix()
    face_transform.rotateZ(angle)
    face_transform.move(App.Vector(0,0,height))
    face_b . transformShape(face_transform)
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
    faces=[face_a,face_b ] 
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