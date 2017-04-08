from .. import Solver
from src.Move import Move


class WhiteFaceSolver(Solver):
    '''
    This solves the down face with the white color
    '''
    @staticmethod
    def first_step(goal_cubie, white_facing):
        solution = []
        if goal_cubie == 'DFR':
            if white_facing == 'F':
                solution = ["R", "U'", "R'"]
            elif white_facing == 'R':
                solution = ["R", "U", "R'", "U'"]
        elif goal_cubie == 'DFL':
            if white_facing == 'F':
                solution = ["L'", "U", "L", "U'"]
            elif white_facing in ['L', 'D']:
                solution = ["L'", "U'", "L"]
        elif goal_cubie == 'BDL':
            if white_facing in ['B', 'D']:
                solution = ["B'", "U2", "B"]
            elif white_facing == 'L':
                solution = ["B'", "U", "B", "U2"]
        elif goal_cubie == 'BDR':
            if white_facing in ['B', 'D']:
                solution = ["B", "U", "B'"]
            elif white_facing == 'R':
                solution = ["B", "U'", "B'", "U"]
        # Cubie is in upper face, place it on FRU
        elif goal_cubie == 'BRU':
            solution = ["U"]
        elif goal_cubie == 'BLU':
            solution = ["U2"]
        elif goal_cubie == 'FLU':
            solution = ["U'"]
        return solution

    @staticmethod
    def second_step(white_facing):
        solution = []
        if white_facing == 'F':
            solution = ["F'", "U'", "F"]
        elif white_facing == 'R':
            solution = ["R", "U", "R'"]
        elif white_facing == 'U':
            solution = ["R", "U2", "R'", "U'", "R", "U", "R'"]
        
        return solution

    def solution(self):
        solution = []
        # There are 4 down-corners
        for i in range(4):
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
