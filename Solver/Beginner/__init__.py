import copy
from .. import Solver
from . import WhiteCrossSolver
from . import WhiteFaceSolver
from . import SecondLayerSolver

class BeginnerSolver(Solver):
    def solution(self):
        cube = copy.deepcopy(self.cube)
        solution = WhiteCrossSolver.WhiteCrossSolver(cube).solution()
        solution += WhiteFaceSolver.WhiteFaceSolver(cube).solution()
        solution += SecondLayerSolver.SecondLayerSolver(cube).solution()
        return solution
