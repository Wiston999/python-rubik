from rubik_solver.Move import Move
from .. import Solver
from . import Search


class KociembaSolver(Solver):
    def solution(self, maxDepth=23, timeOut=100):
        solution = Search.Search.solution(
            self.cube.to_naive_cube().to_face_cube().to_String(),
            maxDepth,
            timeOut
        )

        return [Move(m) for m in solution]
