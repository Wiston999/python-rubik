import copy
from rubik_solver.Move import Move
from rubik_solver.Cubie import Cubie
from .. import Solver
from . import CrossSolver
from . import FaceSolver

class MosaicSolver(Solver):
    '''
    This class is used to find a solution to generate a mosaic on a given face.
    Mosaic is generated in the bottom face.
    `target_solution` must be a 9 length string with any combination of Cube colors.
    No cubies must be empty.
    '''
    def __init__(self, cube, target_solution):
        if not isinstance(target_solution, str) or len(target_solution) != 9:
            raise ValueError('target_solution must be a 9 length string')

        if any(c.upper() not in Cubie.COLORS for c in target_solution):
            raise ValueError('target_solution values must be one of %s, got %s', Cubie.COLORS, target_solution)

        self.target = target_solution.upper()

        super(MosaicSolver, self).__init__(cube)

    def solution(self):
        cube = copy.deepcopy(self.cube)
        # Build target cross, getting the edge cubies colors and sorting them in
        # an iterative way
        target_cross = '{1}{5}{7}{3}'.format(*self.target)
        target_corners = '{2}{8}{6}{0}'.format(*self.target)
        solution = MosaicSolver.place_target_face(self.target[4])
        if len(solution) > 0:
            cube.move(Move(solution[0]))
        solution += CrossSolver.CrossSolver(cube).solution(target_cross)
        solution += FaceSolver.FaceSolver(cube).solution(target_corners)
        return [Move(m) for m in solution]

    @staticmethod
    def place_target_face(target):
        center_cubie = target
        if center_cubie == 'Y':
            solution = ["Z2"]
        elif center_cubie == 'G':
            solution = ["Z"]
        elif center_cubie == 'B':
            solution = ["Z'"]
        elif center_cubie == 'O':
            solution = ["X"]
        elif center_cubie == 'R':
            solution = ["X'"]
        elif center_cubie == 'W':
            solution = []
        return solution
