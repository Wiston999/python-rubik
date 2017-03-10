from .. import Solver
from Move import Move

class WhiteCrossSolver(Solver):
    def solution(self):
        solution = []
        for color in 'RGOB':
            cubie_position = self.cube.search_by_colors('W', color)
            step_solution = []
            orig_cubie = self.cube.cubies[cubie_position]
            white_facing = orig_cubie.color_facing('W')
            color_facing = orig_cubie.color_facing(color)
            print "Putting", white_facing, color_facing
            # First goal is to put white sticker on top face
            if white_facing == 'D':
                step_solution.append("%s2" % color_facing)
            elif white_facing == 'F':
                if color_facing == 'U':
                    step_solution.append("F")
                    step_solution.append("R")
                    step_solution.append("U'")
                    step_solution.append("R'")
                    step_solution.append("F'")
                elif color_facing == 'D':
                    step_solution.append("F'")
                    step_solution.append("R")
                    step_solution.append("U'")
                    step_solution.append("R'")
                elif color_facing == 'R':
                    step_solution.append("R")
                    step_solution.append("U")
                    step_solution.append("R'")
                elif color_facing == 'L':
                    step_solution.append("L'")
                    step_solution.append("U'")
                    step_solution.append("L")
            elif white_facing == 'B':
                if color_facing == 'U':
                    step_solution.append("B")
                    step_solution.append("L")
                    step_solution.append("U'")
                    step_solution.append("L'")
                    step_solution.append("B'")
                elif color_facing == 'D':
                    step_solution.append("B")
                    step_solution.append("R'")
                    step_solution.append("U")
                    step_solution.append("R")
                elif color_facing == 'R':
                    step_solution.append("R'")
                    step_solution.append("U")
                    step_solution.append("R")
                elif color_facing == 'L':
                    step_solution.append("L")
                    step_solution.append("U'")
                    step_solution.append("L'")
            elif white_facing == 'L':
                if color_facing == 'U':
                    step_solution.append("L")
                    step_solution.append("F")
                    step_solution.append("U'")
                    step_solution.append("F'")
                    step_solution.append("L'")
                elif color_facing == 'D':
                    step_solution.append("L'")
                    step_solution.append("F")
                    step_solution.append("U'")
                    step_solution.append("F'")
                elif color_facing == 'F':
                    step_solution.append("F")
                    step_solution.append("U'")
                    step_solution.append("F'")
                elif color_facing == 'B':
                    step_solution.append("B'")
                    step_solution.append("U")
                    step_solution.append("B")
            elif white_facing == 'R':
                if color_facing == 'U':
                    step_solution.append("R'")
                    step_solution.append("F'")
                    step_solution.append("U")
                    step_solution.append("F")
                    step_solution.append("R")
                elif color_facing == 'D':
                    step_solution.append("R")
                    step_solution.append("F'")
                    step_solution.append("U")
                    step_solution.append("F")
                elif color_facing == 'F':
                    step_solution.append("F'")
                    step_solution.append("U")
                    step_solution.append("F")
                elif color_facing == 'B':
                    step_solution.append("B")
                    step_solution.append("U'")
                    step_solution.append("B'")

            for m in step_solution:
                self.cube.move(Move(m))
            solution.extend(step_solution)

            # Second goal is to place the cubie on the top over its place
            print "Placing on top", color
            while self.cube.cubies['FU'].facings['U'] != 'W' or self.cube.cubies['FU'].facings['F'] != color:
                solution.append('U')
                self.cube.move(Move('U'))
            # Third goal will be a F2 movement
            solution.append("F2")
            self.cube.move(Move("F2"))
            solution.append('Y')
            self.cube.move(Move("Y"))

        return solution
