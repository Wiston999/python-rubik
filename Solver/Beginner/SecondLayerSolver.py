from .. import Solver
from Move import Move
from Cubie import Sticker

class SecondLayerSolver(Solver):
    def solution(self):
        solution = []
        # There are 4 down-corners
        