'''
Cubie: Implements a Cube and movements at Cubie level
'''
import random
from copy import deepcopy
from Move import Move
from NaiveCube import NaiveCube


class Sticker(object):
    COLOURS = ['w', 'r', 'b', 'g', 'y', 'o', '.']

    def __init__(self, color):
        if color.lower() not in self.COLOURS:
            raise ValueError("Color %s is not one of %s" %
                             (color, ', '.join(self.COLOURS)))

        self.color = color

    def __repr__(self):
        return self.color.upper()


class Cubie(object):
    FACINGS = 'FBRLUD'
    COLORS = 'ROGBYW'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.FACINGS:
                raise ValueError("Face %s is not one of %s" %
                                 (key, ', '.join(list(self.FACINGS))))

            kwargs[key] = Sticker(value)

        self.facings = deepcopy(kwargs)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, ', '.join(['%s: %s' % (k, v) for k, v in self.facings.items()]))

    @property
    def faces(self):
        return self.facings.keys()

    @property
    def colors(self):
        return self.facings.values()

    @staticmethod
    def facing_to_color(facing):
        return Cubie.COLORS[Cubie.FACINGS.index(facing.upper())]

    @staticmethod
    def color_to_facing(color):
        return Cubie.FACINGS[Cubie.COLORS.index(color.upper())]

    def color_facing(self, c):
        for facing, color in self.facings.items():
            if str(color) == c:
                return facing

        return None

class Center(Cubie):
    def __init__(self, **kwargs):
        if len(kwargs) != 1:
            raise ValueError("Center must have only 1 Sticker")
        super(Center, self).__init__(**kwargs)


class Edge(Cubie):
    def __init__(self, **kwargs):
        if len(kwargs) != 2:
            raise ValueError("Center must have only 2 Stickers")
        super(Edge, self).__init__(**kwargs)


class Corner(Cubie):
    def __init__(self, **kwargs):
        if len(kwargs) != 3:
            raise ValueError("Center must have only 3 Stickers")
        super(Corner, self).__init__(**kwargs)


class Cube(object):
    CUBIES = [
        'FLU', 'FU', 'FRU', 'FL', 'F', 'FR', 'FLD', 'FD', 'FRD',
        'BLU', 'BU', 'BRU', 'BL', 'B', 'BR', 'BLD', 'BD', 'BRD',
        'UL', 'L', 'DL',
        'UR', 'R', 'DR',
        'D', 'U'
    ]

    CUBE_MAP = [
        # UP
        ('BLU', 'U'), ('BU', 'U'), ('BRU', 'U'),
        ('UL', 'U'), ('U', 'U'), ('UR', 'U'),
        ('FLU', 'U'), ('FU', 'U'), ('FRU', 'U'),
        # LEFT
        ('BLU', 'L'), ('UL', 'L'), ('FLU', 'L'),
        ('BL', 'L'), ('L', 'L'), ('FL', 'L'),
        ('BLD', 'L'), ('DL', 'L'), ('FLD', 'L'),
        # FRONT
        ('FLU', 'F'), ('FU', 'F'), ('FRU', 'F'),
        ('FL', 'F'), ('F', 'F'), ('FR', 'F'),
        ('FLD', 'F'), ('FD', 'F'), ('FRD', 'F'),
        # RIGHT
        ('FRU', 'R'), ('UR', 'R'), ('BRU', 'R'),
        ('FR', 'R'), ('R', 'R'), ('BR', 'R'),
        ('FRD', 'R'), ('DR', 'R'), ('BRD', 'R'),
        # BACK
        ('BRU', 'B'), ('BU', 'B'), ('BLU', 'B'),
        ('BR', 'B'), ('B', 'B'), ('BL', 'B'),
        ('BRD', 'B'), ('BD', 'B'), ('BLD', 'B'),
        # DOWN
        ('FLD', 'D'), ('FD', 'D'), ('FRD', 'D'),
        ('DL', 'D'), ('D', 'D'), ('DR', 'D'),
        ('BLD', 'D'), ('BD', 'D'), ('BRD', 'D'),
    ]

    MOVES = {
        'F': [
            ('FLU', 'FUR'),
            ('FUR', 'FRD'),
            ('FRD', 'FDL'),
            ('FDL', 'FLU'),
            ('FU', 'FR'),
            ('FR', 'FD'),
            ('FD', 'FL'),
            ('FL', 'FU'),
        ],
        'B': [
            ('BLU', 'BDL'),
            ('BDL', 'BRD'),
            ('BRD', 'BUR'),
            ('BUR', 'BLU'),
            ('BU', 'BL'),
            ('BL', 'BD'),
            ('BD', 'BR'),
            ('BR', 'BU'),
        ],
        'R': [
            ('RFU', 'RUB'),
            ('RUB', 'RBD'),
            ('RBD', 'RDF'),
            ('RDF', 'RFU'),
            ('RU', 'RB'),
            ('RB', 'RD'),
            ('RD', 'RF'),
            ('RF', 'RU'),
        ],
        'L': [
            ('LFU', 'LDF'),
            ('LDF', 'LBD'),
            ('LBD', 'LUB'),
            ('LUB', 'LFU'),
            ('LU', 'LF'),
            ('LF', 'LD'),
            ('LD', 'LB'),
            ('LB', 'LU'),
        ],
        'U': [
            ('ULB', 'UBR'),
            ('UBR', 'URF'),
            ('URF', 'UFL'),
            ('UFL', 'ULB'),
            ('UB', 'UR'),
            ('UR', 'UF'),
            ('UF', 'UL'),
            ('UL', 'UB'),
        ],
        'D': [
            ('DFL', 'DRF'),
            ('DRF', 'DBR'),
            ('DBR', 'DLB'),
            ('DLB', 'DFL'),
            ('DF', 'DR'),
            ('DR', 'DB'),
            ('DB', 'DL'),
            ('DL', 'DF'),
        ],
        'X': [

        ],
        'Y': [

        ],
        'Z': [

        ]
    }

    def __init__(self, size=3):
        self.__reset_cube()
        # It currently has no sense
        self.size = size

    def __reset_cube(self):
        self.cubies = {}
        for cubie in self.CUBIES:
            # Sorting the key allows to access the dict in an unified manner
            cubie = self.__t_key(cubie)
            if len(cubie) == 3:
                self.cubies[cubie] = Corner(
                    **dict([(face, Cubie.facing_to_color(face)) for face in cubie]))
            elif len(cubie) == 2:
                self.cubies[cubie] = Edge(
                    **dict([(face, Cubie.facing_to_color(face)) for face in cubie]))
            else:
                self.cubies[cubie] = Center(
                    **dict([(face, Cubie.facing_to_color(face)) for face in cubie]))

    @staticmethod
    def __t_key(key):
        return ''.join(sorted(key))

    def from_naive_cube(self, cube):
        for i, color in enumerate(cube.get_cube()):
            cube_map = self.CUBE_MAP[i]
            cube_map[0] = self.__t_key(cube_map[0])
            self.cubies[cube_map[0]].facings[cube_map[1]] = Sticker(color)

    def to_naive_cube(self):
        configuration = ''
        for cubie, face in self.CUBE_MAP:
            cubie = self.__t_key(cubie)
            configuration += self.cubies[cubie].facings[face].color
        nc = NaiveCube(self.size)
        nc.set_cube(configuration)
        return nc

    @staticmethod
    def move_changes(move):
        if not isinstance(move, Move):
            raise ValueError("Move must be an instance of Move")
        changes = Cube.MOVES[move.face]
        if move.counterclockwise:
            changes = [(c1, c0) for c0, c1 in changes]

        return changes

    def move(self, move):
        changes = Cube.move_changes(move)
        original_cubies = {}
        for c_origin, c_dest in changes:
            c_t_origin = self.__t_key(c_origin)
            origin_cubie = original_cubies[c_t_origin] if c_t_origin in original_cubies else self.cubies[c_t_origin]
            dest_cubie = self.cubies[self.__t_key(c_dest)]
            original_cubies[self.__t_key(c_dest)] = deepcopy(dest_cubie)

            for i, origin_facing in enumerate(c_origin):
                dest_facing = c_dest[i]
                dest_cubie.facings[dest_facing] = origin_cubie.facings[origin_facing]

        if move.double:
            self.move(Move(move.face))

    def shuffle(self, seed=None):
        self.__reset_cube()
        random.seed(seed)
        sequence = []
        for i in range(random.randint(100, 150)):
            m = Move(random.choice(Cubie.FACINGS) + random.choice(" 2'"))
            sequence.append(m)
            self.move(m)

        return sequence

    def search_by_colors(self, *args):
        args = sorted(args)
        print "Searching", args
        for key, cubie in self.cubies.items():
            cubie_colors = tuple([str(c) for c in cubie.facings.values()])
            if args == sorted(cubie_colors):
                return key
        return None


# Build Cube Axis MOVES
Cube.MOVES['X'].extend(Cube.move_changes(Move("R")))
Cube.MOVES['X'].extend(Cube.move_changes(Move("L'")))
Cube.MOVES['X'].extend([
    ('FU', 'UB'),
    ('UB', 'BD'),
    ('BD', 'DF'),
    ('DF', 'FU'),
    ('F', 'U'),
    ('U', 'B'),
    ('B', 'D'),
    ('D', 'F'),
])

Cube.MOVES['Y'].extend(Cube.move_changes(Move("U")))
Cube.MOVES['Y'].extend(Cube.move_changes(Move("D'")))
Cube.MOVES['Y'].extend([
    ('FR', 'LF'),
    ('LF', 'BL'),
    ('BL', 'RB'),
    ('RB', 'FR'),
    ('F', 'L'),
    ('L', 'B'),
    ('B', 'R'),
    ('R', 'F'),
])

Cube.MOVES['Z'].extend(Cube.move_changes(Move("F")))
Cube.MOVES['Z'].extend(Cube.move_changes(Move("B'")))
Cube.MOVES['Z'].extend([
    ('UL', 'RU'),
    ('RU', 'DR'),
    ('DR', 'LD'),
    ('LD', 'UL'),
    ('U', 'R'),
    ('R', 'D'),
    ('D', 'L'),
    ('L', 'U'),
])
