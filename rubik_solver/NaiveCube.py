from .Face import Face
from .FaceCube import FaceCube


class NaiveCube(object):
    def __init__(self, size=3):
        self.size = size
        self.faces = {
            'F': Face(self.size),
            'B': Face(self.size),
            'L': Face(self.size),
            'R': Face(self.size),
            'U': Face(self.size),
            'D': Face(self.size)
        }

    def set_cube(self, configuration):
        c = 0
        for face in 'ULFRBD':
            for i in range(self.size):
                for j in range(self.size):
                    self.faces[face].set_colour(i, j, configuration[c].lower())
                    c += 1

    def get_cube(self):
        configuration = ''
        for f in 'ULFRBD':
            configuration += self.faces[f].squares
        return configuration

    def to_face_cube(self):
        configuration = ''
        for f in 'URFDLB':
            configuration += self.faces[f].squares
        return FaceCube(self._from_color_to_facelet(configuration))

    def from_face_cube(self, fc):
        configuration = self._from_facelet_to_color(fc.to_String())
        c = 0
        for face in 'URFDLB':
            for i in range(self.size):
                for j in range(self.size):
                    self.faces[face].set_colour(i, j, configuration[c])
                    c += 1

        self.set_cube(configuration)

    @staticmethod
    def _from_facelet_to_color(configuration):
        return configuration.replace('D', 'w').replace('U', 'y').replace('R', 'g').replace('B', 'o').replace('F', 'r').replace('L', 'b')

    @staticmethod
    def _from_color_to_facelet(configuration):
        return configuration.replace('w', 'D').replace('y', 'U').replace('g', 'R').replace('o', 'B').replace('r', 'F').replace('b', 'L')

    def is_solved(self):
        return all(f.is_solved() for f in self.faces.values())
