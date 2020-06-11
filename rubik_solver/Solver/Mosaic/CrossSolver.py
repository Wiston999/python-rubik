from .. import Solver
from rubik_solver.Move import Move
from ..Beginner import WhiteCrossSolver

# TODO: WhiteCrossSolver should inherit from CrossSolver, as WhiteCross is 
# a specific case where `target` is default value (RGOB) and aux_color is always White
class CrossSolver(WhiteCrossSolver.WhiteCrossSolver):
    '''
    This class solves the mosaic cross on the down face following a target pattern
    It inherits moving tables from Begginer.WhiteCrossSolver
    '''

    def solution(self, target='RGOB'):
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
            white_facing = orig_cubie.color_facing(aux_color)
            color_facing = orig_cubie.color_facing(color)
            step_solution = CrossSolver.first_step(color_facing, white_facing)
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

