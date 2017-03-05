from .. import Solver
from Move import Move
from Cubie import Sticker


class WhiteCrossSolver(Solver):
    def solution(self):
        solution = []
        # Use sorted edges notation
        for edge in ['DF', 'DR', 'DL', 'BD']:
            cubie = self.cube.cubies[edge]
            center_color = self.cube.cubies[edge.strip(
                'D')].facings[edge.strip('D')]
            cubie_position = self.cube.search_by_colors('W', str(center_color))
            print cubie_position

        return solution
