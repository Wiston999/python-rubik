import copy
from src.Move import Move
from .. import Solver
from ..Beginner import WhiteCrossSolver
from . import F2LSolver
from . import OLLSolver
from . import PLLSolver

class CFOPSolver(Solver):
    def solution(self):
        cube = copy.deepcopy(self.cube)
        solution = WhiteCrossSolver.WhiteCrossSolver(cube).solution()
        solution += F2LSolver.F2LSolver(cube).solution()
        # solution += OLLSolver.OLLSolver(cube).solution()
        # solution += PLLSolver.PLLSolver(cube).solution()
        return [Move(m) for m in solution]
