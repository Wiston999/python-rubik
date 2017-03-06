from .. import Solver
from Move import Move
from Cubie import Sticker

class WhiteFaceSolver(Solver):
    def solution(self):
        solution = []
        # There are 4 down-corners
        for i in range(4):
            front_color = self.cube.cubies['F'].facings['F']
            right_color = self.cube.cubies['R'].facings['R']

            goal_cubie = self.cube.search_by_colors('W', front_color, right_color)
            print "Colors (F)", front_color, "(R)", right_color
            print "Goal cubie is at", goal_cubie

            solution.append('Y')
            self.cube.move(Move('Y'))
        return solution