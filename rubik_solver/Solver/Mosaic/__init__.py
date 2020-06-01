import copy
from rubik_solver.Move import Move
from rubik_solver.Cubie import Cubie
from .. import Solver
from ..Beginner import WhiteCrossSolver
from ..Beginner import WhiteFaceSolver

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
        target_cross = '{1}{3}{5}{7}'.format(*self.target)
        solution = self.place_target_face()
        # solution += WhiteCrossSolver.WhiteCrossSolver(cube).solution(target_cross)
        return [Move(m) for m in solution]

    def place_target_face(self):
        center_cubie = self.target[4]
        if center_cubie == 'Y':
            solution = ["Z2"]
        elif center_cubie == 'G':
            solution = ["X"]
        elif center_cubie == 'B':
            solution = ["X'"]
        elif center_cubie == 'O':
            solution = ["Z"]
        elif center_cubie == 'R':
            solution = ["Z'"]
        elif center_cubie == 'W':
            solution = []
        if center_cubie != 'W':
            self.cube.move(Move(solution[0]))
        return solution
