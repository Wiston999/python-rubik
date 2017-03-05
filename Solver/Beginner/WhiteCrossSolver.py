from .. import Solver
from Move import Move
from Cubie import Sticker


class WhiteCrossSolver(Solver):
    def solution(self):
        solution = []
        # Use sorted edges notation
        for edge in ['DF', 'DR', 'DL', 'BD']:
            goal_cubie = self.cube.cubies[edge]
            center_color = self.cube.cubies[edge.strip('D')].facings[edge.strip('D')]
            cubie_position = self.cube.search_by_colors('W', str(center_color))
            print "Center color is", center_color
            print "Cubie is at", cubie_position
            step_solution = []
            # If cubie not in position
            if cubie_position != edge:
                orig_cubie = self.cube.cubies[cubie_position]
                white_facing = orig_cubie.color_facing('W')
                color_facing = orig_cubie.color_facing(str(center_color))
                print white_facing, color_facing
                # First goal is to put white sticker on top face
                if white_facing == 'D':
                    step_solution.append("%s2" % color_facing)
                elif white_facing == 'F':
                    if color_facing == 'U':
                        step_solution.append("F")
                        step_solution.append("R")
                        step_solution.append("F'")
                        step_solution.append("U")
                        step_solution.append("R'")
                    elif color_facing == 'D':
                        step_solution.append("F")
                        step_solution.append("L'")
                        step_solution.append("F'")
                        step_solution.append("U'")
                        step_solution.append("L")
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
                        step_solution.append("B'")
                        step_solution.append("U'")
                        step_solution.append("L'")
                    elif color_facing == 'D':
                        step_solution.append("B")
                        step_solution.append("R'")
                        step_solution.append("B'")
                        step_solution.append("U'")
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
                        step_solution.append("L'")
                        step_solution.append("U")
                        step_solution.append("F'")
                    elif color_facing == 'D':
                        step_solution.append("L'")
                        step_solution.append("F")
                        step_solution.append("L")
                        step_solution.append("U")
                        step_solution.append("F'")
                    elif color_facing == 'F':
                        step_solution.append("F")
                        step_solution.append("U")
                        step_solution.append("F'")
                    elif color_facing == 'B':
                        step_solution.append("B'")
                        step_solution.append("U'")
                        step_solution.append("B")
                elif white_facing == 'R':
                    if color_facing == 'U':
                        step_solution.append("R'")
                        step_solution.append("F'")
                        step_solution.append("R'")
                        step_solution.append("U")
                        step_solution.append("F")
                    elif color_facing == 'D':
                        step_solution.append("R")
                        step_solution.append("F'")
                        step_solution.append("R'")
                        step_solution.append("U")
                        step_solution.append("F")
                    elif color_facing == 'F':
                        step_solution.append("F'")
                        step_solution.append("U")
                        step_solution.append("F")
                    elif color_facing == 'B':
                        step_solution.append("B'")
                        step_solution.append("U'")
                        step_solution.append("B")
            step_solution.append('Y')
            for m in step_solution:
                self.cube.move(Move(m))
            solution.extend(step_solution)    

            # Second goal is to place the cubie on the top over its place

            # Third goal will be a F2 movement
            print '-' * 100
        return solution
