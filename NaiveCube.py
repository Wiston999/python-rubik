import random
import copy
from Face import Face
from Move import Move
from FaceCube import FaceCube
from CubieCube import CubieCube
from CoordCube import CoordCube


class NaiveCube(object):
    DEFAULT_COLORS = {
        'F': 'r',
        'B': 'o',
        'L': 'b',
        'R': 'g',
        'U': 'y',
        'D': 'w'
    }

    MOVE_IMPLICATIONS = {
        'F': ['U', 'R', 'D', 'L'],
        'B': ['U', 'L', 'D', 'R'],
        'L': ['U', 'F', 'D', 'B'],
        'R': ['U', 'B', 'D', 'F'],
        'U': ['B', 'R', 'F', 'L'],
        'D': ['B', 'L', 'F', 'R']
    }

    MOVE_DIRECTIONS = {
        'F': [('x', -1), ('y',  0), ('x',  0), ('y', -1)],
        'B': [('x',  0), ('y',  0), ('x', -1), ('y', -1)],
        'L': [('y',  0), ('y',  0), ('y',  0), ('y', -1)],
        'R': [('y', -1), ('y',  0), ('y', -1), ('y', -1)],
        'U': [('x',  0), ('x',  0), ('x',  0), ('x',  0)],
        'D': [('x', -1), ('x', -1), ('x', -1), ('x', -1)]
    }

    @staticmethod
    def straightLine(face, coordinate, row):
        for i, colour in enumerate(row):
            if coordinate[0] == 'x':
                face.set_colour(
                    0 if coordinate[1] == 0 else face.size - 1,
                    i,
                    colour
                )
            else:
                face.set_colour(
                    i,
                    0 if coordinate[1] == 0 else face.size - 1,
                    colour
                )

    @staticmethod
    def reverseLine(face, coordinate, row):
        for i, colour in enumerate(row):
            if coordinate[0] == 'x':
                face.set_colour(
                    0 if coordinate[1] == 0 else face.size - 1,
                    face.size - 1 - i,
                    colour
                )
            else:
                face.set_colour(
                    face.size - 1 - i,
                    0 if coordinate[1] == 0 else face.size - 1,
                    colour
                )

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

        self.MOVE_FUNCTIONS = {
            'F': [NaiveCube.reverseLine,  NaiveCube.straightLine, NaiveCube.reverseLine,  NaiveCube.straightLine],
            'B': [NaiveCube.straightLine, NaiveCube.reverseLine,  NaiveCube.straightLine, NaiveCube.reverseLine],
            'L': [NaiveCube.reverseLine,  NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.reverseLine],
            'R': [NaiveCube.straightLine, NaiveCube.reverseLine,  NaiveCube.reverseLine,  NaiveCube.straightLine],
            'U': [NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.straightLine],
            'D': [NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.straightLine]
        }

        self.REVERSE_MOVE_FUNCTIONS = {
            'F': [NaiveCube.straightLine, NaiveCube.reverseLine,  NaiveCube.straightLine, NaiveCube.reverseLine],
            'B': [NaiveCube.reverseLine,  NaiveCube.straightLine, NaiveCube.reverseLine,  NaiveCube.straightLine],
            'L': [NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.reverseLine,  NaiveCube.reverseLine],
            'R': [NaiveCube.reverseLine,  NaiveCube.reverseLine,  NaiveCube.straightLine, NaiveCube.straightLine],
            'U': [NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.straightLine],
            'D': [NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.straightLine, NaiveCube.straightLine]
        }

        self.solved()

    def set_cube(self, configuration):
        c = 0
        for f, face in enumerate('ULFRBD'):
            for i in range(self.size):
                for j in range(self.size):
                    self.faces[face].set_colour(i, j, configuration[c])
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
        return FaceCube(Cube._from_color_to_facelet(configuration))

    def from_face_cube(self, fc):
        configuration = Cube._from_facelet_to_color(fc.to_String())
        c = 0
        for f, face in enumerate('URFDLB'):
            for i in range(self.size):
                for j in range(self.size):
                    self.faces[face].set_colour(i, j, configuration[c])
                    c += 1

        self.set_cube(configuration)

    def to_cubie_cube(self):
        pass

    def from_cubie_cube(self, fc):
        pass

    @staticmethod
    def _from_facelet_to_color(configuration):
        return configuration.replace('D', 'w').replace('U', 'y').replace('R', 'g').replace('B', 'o').replace('F', 'r').replace('L', 'b')

    @staticmethod
    def _from_color_to_facelet(configuration):
        return configuration.replace('w', 'D').replace('y', 'U').replace('g', 'R').replace('o', 'B').replace('r', 'F').replace('b', 'L')

    def shuffle(self, seed=None):
        self.solved()
        random.seed(seed)
        for _ in range(random.randint(100, 150)):
            m = Move(random.choice(self.DEFAULT_COLORS.keys()) +
                     random.choice(" 2'"))
            self.move(m)

    def move(self, movement):
        if not isinstance(movement, Move):
            raise ValueError(
                "Movement must be instance of Move, got %s" % movement.__class__.__name__)

        move_faces = self.MOVE_IMPLICATIONS[movement.face][:]
        move_directions = self.MOVE_DIRECTIONS[movement.face][:]
        move_functions = self.MOVE_FUNCTIONS[movement.face][:]

        reversed = False
        if movement.clockwise:
            move_faces.reverse()
            move_directions.reverse()
            move_functions.reverse()
        else:
            move_functions = self.REVERSE_MOVE_FUNCTIONS[movement.face][:]

        first_row = []
        for i in range(self.size):
            if move_directions[0][0] == 'x':
                first_row.append(self.faces[move_faces[0]].get_colour(
                    0 if move_directions[0][1] == 0 else self.size - 1, i))
            else:
                first_row.append(self.faces[move_faces[0]].get_colour(
                    i, 0 if move_directions[0][1] == 0 else self.size - 1))

        for fIndex in range(1, len(move_faces)):
            current_row = []
            current_direction, next_direction = move_directions[fIndex], move_directions[fIndex - 1]
            for i in range(self.size):
                if current_direction[0] == 'x':
                    current_row.append(self.faces[move_faces[fIndex]].get_colour(
                        0 if current_direction[1] == 0 else self.size - 1, i))
                else:
                    current_row.append(self.faces[move_faces[fIndex]].get_colour(
                        i, 0 if current_direction[1] == 0 else self.size - 1))

            move_functions[fIndex - 1](self.faces[move_faces[fIndex - 1]],
                                       next_direction, current_row)

        move_functions[-1](self.faces[move_faces[-1]],
                           move_directions[-1], first_row)

        original_face = [self.faces[movement.face].squares[i:i + 3]
                         for i in range(0, 9, 3)]

        self.faces[movement.face].set_colour(
            0,
            0,
            original_face[2 if movement.clockwise else 0][0 if movement.clockwise else 2]
        )

        self.faces[movement.face].set_colour(
            0,
            1,
            original_face[1 if movement.clockwise else 1][0 if movement.clockwise else 2]
        )

        self.faces[movement.face].set_colour(
            0,
            2,
            original_face[0 if movement.clockwise else 2][0 if movement.clockwise else 2]
        )

        self.faces[movement.face].set_colour(
            1,
            0,
            original_face[2 if movement.clockwise else 0][1 if movement.clockwise else 1]
        )

        self.faces[movement.face].set_colour(
            1,
            2,
            original_face[0 if movement.clockwise else 2][1 if movement.clockwise else 1]
        )

        self.faces[movement.face].set_colour(
            2,
            0,
            original_face[2 if movement.clockwise else 0][2 if movement.clockwise else 0]
        )

        self.faces[movement.face].set_colour(
            2,
            1,
            original_face[1 if movement.clockwise else 1][2 if movement.clockwise else 0]
        )

        self.faces[movement.face].set_colour(
            2,
            2,
            original_face[0 if movement.clockwise else 2][2 if movement.clockwise else 0]
        )

        if movement.double:
            self.move(Move(movement.face))

    def is_solved(self):
        return all(f.is_solved() for f in self.faces.values())

    def solved(self):
        for faceName, face in self.faces.items():
            for i in range(self.size):
                for j in range(self.size):
                    face.set_colour(i, j, self.DEFAULT_COLORS[faceName])
