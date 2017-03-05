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
            # If cubie not in position
            if cubie_position != edge:
                orig_cubie = self.cube.cubies[cubie_position]
                white_facing = orig_cubie.color_facing('W')
                color_facing = orig_cubie.color_facing(str(center_color))
                print white_facing, color_facing
                # First goal is to put white sticker on top face
                if white_facing == 'D':
                    solution.append("%s2" % color_facing)
                elif white_facing == 'F':
                    if color_facing == 'U':
                        solution.append("F")
                        solution.append("R")
                        solution.append("F'")
                        solution.append("U")
                        solution.append("R'")
                    elif color_facing == 'D':
                        solution.append("F")
                        solution.append("L'")
                        solution.append("F'")
                        solution.append("U'")
                        solution.append("L")
                    elif color_facing == 'R':
                        solution.append("R")
                        solution.append("U")
                        solution.append("R'")
                    elif color_facing == 'L':
                        solution.append("L'")
                        solution.append("U'")
                        solution.append("L")
                elif white_facing == 'B':
                    if color_facing == 'U':
                        solution.append("B")
                        solution.append("L")
                        solution.append("B'")
                        solution.append("U'")
                        solution.append("L'")
                    elif color_facing == 'D':
                        solution.append("B")
                        solution.append("R'")
                        solution.append("B'")
                        solution.append("U'")
                        solution.append("R")
                    elif color_facing == 'R':
                        solution.append("R'")
                        solution.append("U")
                        solution.append("R")
                    elif color_facing == 'L':
                        solution.append("L")
                        solution.append("U'")
                        solution.append("L'")
                elif white_facing == 'L':
                    if color_facing == 'U':
                        solution.append("L")
                        solution.append("F")
                        solution.append("L'")
                        solution.append("U")
                        solution.append("F'")
                    elif color_facing == 'D':
                        solution.append("L'")
                        solution.append("F")
                        solution.append("L")
                        solution.append("U")
                        solution.append("F'")
                    elif color_facing == 'F':
                        solution.append("F")
                        solution.append("U")
                        solution.append("F'")
                    elif color_facing == 'B':
                        solution.append("B'")
                        solution.append("U'")
                        solution.append("B")
                elif white_facing == 'R':
                    if color_facing == 'U':
                        solution.append("R'")
                        solution.append("F'")
                        solution.append("R'")
                        solution.append("U")
                        solution.append("F")
                    elif color_facing == 'D':
                        solution.append("R")
                        solution.append("F'")
                        solution.append("R'")
                        solution.append("U")
                        solution.append("F")
                    elif color_facing == 'F':
                        solution.append("F'")
                        solution.append("U")
                        solution.append("F")
                    elif color_facing == 'B':
                        solution.append("B'")
                        solution.append("U'")
                        solution.append("B")
                # Second goal is to place the cubie on the top over its place

                # Third goal will be a F2 movement
        return solution
