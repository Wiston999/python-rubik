from .. import Solver
from rubik_solver.Move import Move

class FaceSolver(Solver):
    '''
    This class solves the mosaic face (placing corners) on the down face following a target pattern
    '''

    # The order of corners ensures that the solver can be used to solve whiteface too
    CORNERS = [
        'WRG', 'WGO', 'WOB', 'WBR',
        'RGY', 'RBY', 'OGY', 'OBY',
    ]

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
            solution = FaceSolver.FIRST_STEP[goal_cubie][white_facing]
        except KeyError:
            solution = []
        return solution

    @staticmethod
    def second_step(white_facing):
        try:
            solution = FaceSolver.SECOND_STEP[white_facing]
        except KeyError:
            solution = []
        return solution

    def solution(self, target='WWWW'):
        solution = []
        used_cubies = set()
        # No more than 4 iterations can be done
        for color in target[:4]:
            # Search for a free corner with target color
            for goal_corner in FaceSolver.CORNERS:
                if color in goal_corner and goal_corner not in used_cubies:
                    break

            used_cubies.add(goal_corner)

            goal_cubie = self.cube.search_by_colors(*goal_corner)
            goal_cubie_obj = self.cube.cubies[goal_cubie]

            step_solution = FaceSolver.first_step(goal_cubie, goal_cubie_obj.color_facing(color))

            for move in step_solution:
                self.cube.move(Move(move))

            # If corner is not already well placed and oriented, continue
            if len(step_solution) > 0 or goal_cubie != 'DFR':
                # Cubie is at FRU, place it at DRU with correct orientation
                solution.extend(step_solution)
                step_solution = FaceSolver.second_step(self.cube.cubies['FRU'].color_facing(color))

                for move in step_solution:
                    self.cube.move(Move(move))
                solution.extend(step_solution)
            # Cubie is placed, move to next

            solution.append('Y')
            self.cube.move(Move('Y'))

        return solution
