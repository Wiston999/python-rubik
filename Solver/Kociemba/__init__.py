from .. import Solver
from . import Search

class KociembaSolver(Solver):
    def solution(self, maxDepth = 21, timeOut = 100):
        self.cube.get_cube()
        return Search.Search.solution(
            self.cube.to_face_cube().to_String(),
            maxDepth,
            timeOut
        )