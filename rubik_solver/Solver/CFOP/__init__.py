import copy
from rubik_solver.Move import Move
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
        solution += OLLSolver.OLLSolver(cube).solution()
        solution += PLLSolver.PLLSolver(cube).solution()
        # Align top layer
        while cube.cubies['F'].facings['F'] != cube.cubies['FU'].facings['F']:
            cube.move(Move('U'))
        return [Move(m) for m in solution]
