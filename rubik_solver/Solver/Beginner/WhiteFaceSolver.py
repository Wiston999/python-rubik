from .. import Solver
from rubik_solver.Move import Move


class WhiteFaceSolver(Solver):
    '''
    This solves the down face with the white color
    '''
    FIRST_STEP = {
        'DFR': {
            'F': ["R", "U'", "R'"],
            'R': ["R", "U", "R'", "U'"]
        },
        'DFL': {
            'F': ["L'", "U", "L", "U'"],
            'L': ["L'", "U'", "L"],
            'D': ["L'", "U'", "L"]
        },
        'BDL': {
            'B': ["B'", "U2", "B"],
            'D': ["B'", "U2", "B"],
            'L': ["B'", "U", "B", "U2"]
        },
        'BDR': {
            'B': ["B", "U", "B'"],
            'D': ["B", "U", "B'"],
            'R': ["B", "U'", "B'", "U"]
        },
        'BRU': {
            'B': ["U"],
            'R': ["U"],
            'U': ["U"],
        },
        'BLU': {
            'B': ["U2"],
            'L': ["U2"],
            'U': ["U2"],
        },
        'FLU': {
            'F': ["U'"],
            'L': ["U'"],
            'U': ["U'"],
        }
    }

    SECOND_STEP = {
        'F': ["F'", "U'", "F"],
        'R': ["R", "U", "R'"],
        'U': ["R", "U2", "R'", "U'", "R", "U", "R'"]
    }
    @staticmethod
    def first_step(goal_cubie, white_facing):
        try:
            solution = WhiteFaceSolver.FIRST_STEP[goal_cubie][white_facing]
        except KeyError:
            solution = []
        return solution

    @staticmethod
    def second_step(white_facing):
        try:
            solution = WhiteFaceSolver.SECOND_STEP[white_facing]
        except KeyError:
            solution = []
        return solution

    def solution(self):
        solution = []
        # There are 4 down-corners
        for _ in range(4):
            front_color = self.cube.cubies['F'].facings['F']
            right_color = self.cube.cubies['R'].facings['R']

            goal_cubie = self.cube.search_by_colors('W', front_color, right_color)
            goal_cubie_obj = self.cube.cubies[goal_cubie]

            step_solution = WhiteFaceSolver.first_step(goal_cubie, goal_cubie_obj.color_facing('W'))

            for move in step_solution:
                self.cube.move(Move(move))

            # If corner is not already well placed and oriented, continue
            if len(step_solution) > 0 or goal_cubie != 'DFR':
                # Cubie is at FRU, place it at DRU with correct orientation
                solution.extend(step_solution)
                step_solution = WhiteFaceSolver.second_step(self.cube.cubies['FRU'].color_facing('W'))

                for move in step_solution:
                    self.cube.move(Move(move))
                solution.extend(step_solution)
            # Cubie is placed, move to next

            solution.append('Y')
            self.cube.move(Move('Y'))

        return solution
