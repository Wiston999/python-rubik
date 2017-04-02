import copy
from src.Move import Move
from .. import Solver
from . import WhiteCrossSolver
from . import WhiteFaceSolver
from . import SecondLayerSolver
from . import YellowCrossSolver
from . import YellowFaceSolver

class BeginnerSolver(Solver):
    def solution(self):
        from src.Printer import TtyPrinter
        cube = copy.deepcopy(self.cube)
        ppr = TtyPrinter(cube, True)
        solution = WhiteCrossSolver.WhiteCrossSolver(cube).solution()
        ppr.pprint()
        solution += WhiteFaceSolver.WhiteFaceSolver(cube).solution()
        ppr.pprint()
        solution += SecondLayerSolver.SecondLayerSolver(cube).solution()
        ppr.pprint()
        solution += YellowCrossSolver.YellowCrossSolver(cube).solution()
        ppr.pprint()
        solution += YellowFaceSolver.YellowFaceSolver(cube).solution()
        ppr.pprint()
        return [Move(m) for m in solution]
