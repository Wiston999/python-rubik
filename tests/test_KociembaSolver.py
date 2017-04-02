from src.Move import Move
from src.Cubie import Cube
from src.Solver import Kociemba
import timeout_decorator
import unittest


class TestKociembaSolver(unittest.TestCase):
    @timeout_decorator.timeout(10)
    def _test_solution(self, c):
        solver = Kociemba.KociembaSolver(c)
        return solver.solution()

    def test_solution(self):
        for i in range(100):
            c = Cube()
            cr = Cube()
            c.shuffle(i)
            print "Solving", i, "of 100", c.to_naive_cube().get_cube()
            solution = self._test_solution(c)
            for s in solution:
                c.move(s)
            # Align faces
            while cr.cubies['F'].facings['F'] != c.cubies['F'].facings['F']:
                c.move(Move('Y'))

            for cubie in cr.cubies:
                for facing in cr.cubies[cubie].facings:
                    self.assertEqual(cr.cubies[cubie].facings[facing], c.cubies[cubie].facings[facing])