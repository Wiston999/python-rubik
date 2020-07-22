from .. import Solver
from rubik_solver.Move import Move

class CrossSolver(Solver):
    '''
    This class solves the mosaic cross on the down face following a target pattern.
    It solves beginner white cross if no parameters are given
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
        return CrossSolver.STEPS[white_facing.upper()][color_facing.upper()]

    def solution(self, target='WWWW'):
        solution = []
        used_cubies = set()
        for color in target:
            # This for loop is a naive way of getting the target cubie to be placed.
            # It tries to find a valid cubie color combination by iterating over all possible
            # values, it starts with White color so the same algorithm is valid for the beginner
            # white cross method
            for aux_color in 'WYRGOB':
                if aux_color != color and ''.join(sorted(aux_color + color)) not in used_cubies:
                    cubie_position = self.cube.search_by_colors(aux_color, color)
                    if cubie_position is not None:
                        break

            used_cubies.add(''.join(sorted(aux_color + color)))

            orig_cubie = self.cube.cubies[cubie_position]
            white_facing = orig_cubie.color_facing(color)
            color_facing = orig_cubie.color_facing(aux_color)

            step_solution = CrossSolver.first_step(white_facing, color_facing)
            # First goal is to put white sticker on top face

            for m in step_solution:
                self.cube.move(Move(m))
            solution.extend(step_solution)

            # Second goal is to place the cubie on the top over its place
            while self.cube.cubies['FU'].facings['F'] != aux_color or self.cube.cubies['FU'].facings['U'] != color:
                solution.append('U')
                self.cube.move(Move('U'))
            # Third goal will be a F2 movement
            solution.append("F2")
            self.cube.move(Move("F2"))
            solution.append('Y')
            self.cube.move(Move("Y"))

        return solution

