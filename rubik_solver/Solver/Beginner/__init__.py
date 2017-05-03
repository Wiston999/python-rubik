import copy
from rubik_solver.Move import Move
from .. import Solver
from . import WhiteCrossSolver
from . import WhiteFaceSolver
from . import SecondLayerSolver
from . import YellowCrossSolver
from . import YellowFaceSolver

class BeginnerSolver(Solver):
    def solution(self):
        cube = copy.deepcopy(self.cube)
        solution = WhiteCrossSolver.WhiteCrossSolver(cube).solution()
        solution += WhiteFaceSolver.WhiteFaceSolver(cube).solution()
        solution += SecondLayerSolver.SecondLayerSolver(cube).solution()
        solution += YellowCrossSolver.YellowCrossSolver(cube).solution()
        solution += YellowFaceSolver.YellowFaceSolver(cube).solution()
        return [Move(m) for m in solution]
