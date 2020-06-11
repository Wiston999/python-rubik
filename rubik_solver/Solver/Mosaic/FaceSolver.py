from .. import Solver
from rubik_solver.Move import Move
from ..Beginner import WhiteFaceSolver

class FaceSolver(WhiteFaceSolver.WhiteFaceSolver):
    '''
    This class solves the mosaic face (placing corners) on the down face following a target pattern
    It inherits moving tables from Begginer.WhiteFaceSolver
    '''
    CORNERS = [
        'RGY', 'RBY', 'RGW', 'RBW',
        'OGY', 'OBY', 'OGW', 'OBW',
    ]

    def solution(self, target):
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
