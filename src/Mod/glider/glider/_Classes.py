from openglider import glider
import FreeCAD
import numpy
import Mesh


class Glider():

    def __init__(self):
        glider1 = glider.Glider()
        glider1.import_geometry("../tests/demokite.ods")
        glider1.close_rib(-1)
        glider1.recalc()
        self.polygons, self.points = glider1.return_polygons(2)
        self.execute()


    def execute(self):
        planarMesh = []
        for i in self.polygons:
            planarMesh.append(self.points[i[0]])
            planarMesh.append(self.points[i[2]])
            planarMesh.append(self.points[i[1]])
            planarMesh.append(self.points[i[0]])
            planarMesh.append(self.points[i[3]])
            planarMesh.append(self.points[i[2]])
        Mesh.show(Mesh.Mesh(planarMesh))
