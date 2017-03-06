import copy
from .. import Solver
from . import WhiteCrossSolver
from . import WhiteFaceSolver

class BeginnerSolver(Solver):
    def solution(self):
        cube = copy.deepcopy(self.cube)
        solution = WhiteCrossSolver.WhiteCrossSolver(cube).solution()
        # solution += WhiteFaceSolver.WhiteFaceSolver(cube).solution()
        return solution
