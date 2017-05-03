from .. import Solver
from rubik_solver.Move import Move


class WhiteCrossSolver(Solver):
    '''
    This class solves the white cross on the down face
    '''
    STEPS = {
        'U': {
            'R': [],
            'L': [],
            'F': [],
            'B': [],
        },
        'D': {
            'R': ['R2'],
            'L': ['L2'],
            'F': ['F2'],
            'B': ['B2']
        },
        'F': {
            'U': ["F", "R", "U'", "R'", "F'"],
            'D': ["F'", "R", "U'", "R'"],
            'R': ["R", "U", "R'"],
            'L': ["L'", "U'", "L"],
        },
        'B': {
            'U': ["B", "L", "U'", "L'", "B'"],
            'D': ["B", "R'", "U", "R"],
            'R': ["R'", "U", "R"],
            'L': ["L", "U'", "L'"],
        },
        'L': {
            'U': ["L", "F", "U'", "F'", "L'"],
            'D': ["L'", "F", "U'", "F'"],
            'F': ["F", "U'", "F'"],
            'B': ["B'", "U", "B"],
        },
        'R': {
            'U': ["R'", "F'", "U", "F", "R"],
            'D': ["R", "F'", "U", "F"],
            'F': ["F'", "U", "F"],
            'B': ["B", "U'", "B'"],
        }
    }
    @staticmethod
    def first_step(white_facing, color_facing):
        return WhiteCrossSolver.STEPS[white_facing.upper()][color_facing.upper()]


    def solution(self):
        solution = []
        for color in 'RGOB':
            cubie_position = self.cube.search_by_colors('W', color)

            orig_cubie = self.cube.cubies[cubie_position]
            white_facing = orig_cubie.color_facing('W')
            color_facing = orig_cubie.color_facing(color)
            step_solution = WhiteCrossSolver.first_step(white_facing, color_facing)
            # First goal is to put white sticker on top face

            for m in step_solution:
                self.cube.move(Move(m))
            solution.extend(step_solution)

            # Second goal is to place the cubie on the top over its place
            while self.cube.cubies['FU'].facings['U'] != 'W' or self.cube.cubies['FU'].facings['F'] != color:
                solution.append('U')
                self.cube.move(Move('U'))
            # Third goal will be a F2 movement
            solution.append("F2")
            self.cube.move(Move("F2"))
            solution.append('Y')
            self.cube.move(Move("Y"))

        return solution
