from .. import Solver
from . import WhiteCrossSolver
from . import WhiteFaceSolver

class BegginerSolver(Solver):
    def solution(self):
        cube = deepcopy(self.cube.get_cube())
        solution = WhiteCrossSolver.WhiteCrossSolver(cube).solution()
        solution += WhiteFaceSolver.WhiteFaceSolver(cube).solution()
        return []
