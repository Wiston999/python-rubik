import copy
from Move import Move
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
        print "WhiteCross"
        solution += WhiteFaceSolver.WhiteFaceSolver(cube).solution()
        print "WhiteFace"
        solution += SecondLayerSolver.SecondLayerSolver(cube).solution()
        print "SecondLayer"
        solution += YellowCrossSolver.YellowCrossSolver(cube).solution()
        print "YellowCross"
        solution += YellowFaceSolver.YellowFaceSolver(cube).solution()
        return [Move(m) for m in solution]
