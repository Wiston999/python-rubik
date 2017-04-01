from .. import Solver
from src.Move import Move


class WhiteCrossSolver(Solver):
    '''
    This class solves the white cross on the down face
    '''
    @staticmethod
    def first_step(white_facing, color_facing):
        if white_facing == 'D':
            solution = "%s2" % color_facing
        elif white_facing == 'F':
            if color_facing == 'U':
                solution = ["F", "R", "U'", "R'", "F'"]
            elif color_facing == 'D':
                solution = ["F'", "R", "U'", "R'"]
            elif color_facing == 'R':
                solution = ["R", "U", "R'"]
            elif color_facing == 'L':
                solution = ["L'", "U'", "L"]
        elif white_facing == 'B':
            if color_facing == 'U':
                solution = ["B", "L", "U'", "L'", "B'"]
            elif color_facing == 'D':
                solution = ["B", "R'", "U", "R"]
            elif color_facing == 'R':
                solution = ["R'", "U", "R"]
            elif color_facing == 'L':
                solution = ["L", "U'", "L'"]
        elif white_facing == 'L':
            if color_facing == 'U':
                solution = ["L", "F", "U'", "F'", "L'"]
            elif color_facing == 'D':
                solution = ["L'", "F", "U'", "F'"]
            elif color_facing == 'F':
                solution = ["F", "U'", "F'"]
            elif color_facing == 'B':
                solution = ["B'", "U", "B"]
        elif white_facing == 'R':
            if color_facing == 'U':
                solution = ["R'", "F'", "U", "F", "R"]
            elif color_facing == 'D':
                solution = ["R", "F'", "U", "F"]
            elif color_facing == 'F':
                solution = ["F'", "U", "F"]
            elif color_facing == 'B':
                solution = ["B", "U'", "B'"]
        return solution

        
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
