from rubik_solver.Move import Move
from rubik_solver.NaiveCube import NaiveCube
from rubik_solver.Cubie import Cube
from rubik_solver.Solver import Kociemba
import timeout_decorator
import unittest


class TestKociembaSolver(unittest.TestCase):
    @timeout_decorator.timeout(300)
    def _test_solution(self, c):
        solver = Kociemba.KociembaSolver(c)
        return solver.solution()

    def test_solved_solution(self):
        '''Try to solve an already solved cube'''
        c = Cube()
        solution = self._test_solution(c)
        self._check_solution(c, solution)

    def test_solution(self):
        for i in range(10):
            c = Cube()
            c.shuffle(i)
            solution = self._test_solution(c)
            self._check_solution(c, solution)

    def _check_solution(self, c, solution):
        cr = Cube()
        for s in solution:
            c.move(s)
        # Align faces
        while cr.cubies['F'].facings['F'] != c.cubies['F'].facings['F']:
            c.move(Move('Y'))

        for cubie in cr.cubies:
            for facing in cr.cubies[cubie].facings:
                self.assertEqual(cr.cubies[cubie].facings[facing], c.cubies[cubie].facings[facing])

    def test_timeout(self):
        c = Cube()
        nc = NaiveCube()
        nc.set_cube("orgyyybbbwgobbbyrywowwrwrwyrorogboogwygyorrwobrggwgbgy")
        c.from_naive_cube(nc)
        with self.assertRaises(Kociemba.Search.SolverTimeoutError):
            solver = Kociemba.KociembaSolver(c)
            solver.solution(timeOut = 1)
