from src.Move import Move
from src.Cubie import Cube
from src.Solver import CFOP
from src.Solver.CFOP.F2LSolver import F2LSolver
from src.Solver.Beginner.WhiteCrossSolver import WhiteCrossSolver
import timeout_decorator
import unittest

class TestF2LSolver(unittest.TestCase):
    def test_get_step(self):
        for corner in F2LSolver.STEPS:
            for edge, steps in F2LSolver.STEPS[corner].items():
                self.assertEqual(steps, F2LSolver.get_step(corner, edge))

    def test_steps(self):
        for corner in F2LSolver.STEPS:
            for edge, steps in F2LSolver.STEPS[corner].items():
                c = Cube()
                tmp = c.cubies[Cube._t_key(corner)]
                orig_corner = ''.join([
                    tmp.facings[corner[0]].color,
                    tmp.facings[corner[1]].color,
                    tmp.facings[corner[2]].color
                ])
                tmp = c.cubies[Cube._t_key(edge)]
                orig_edge = ''.join([
                    tmp.facings[edge[0]].color,
                    tmp.facings[edge[1]].color,
                ])

                for s in steps:
                    c.move(Move(s))

                dest_corner = ''.join([
                    c.cubies['DFR'].facings['F'].color,
                    c.cubies['DFR'].facings['R'].color,
                    c.cubies['DFR'].facings['D'].color,
                ])

                dest_edge = ''.join([
                    c.cubies['FR'].facings['F'].color,
                    c.cubies['FR'].facings['R'].color,
                ])

                self.assertEqual(dest_corner, orig_corner, msg = 'Failed F2L corner check corner:%s edge:%s (%s != %s)' % (corner, edge, dest_corner, orig_corner))
                self.assertEqual(dest_edge, orig_edge, msg = 'Failed F2L edge check corner:%s edge:%s (%s != %s)' % (corner, edge, dest_edge, orig_edge))

    @timeout_decorator.timeout(300)
    def _test_solution(self, c):
        solver = F2LSolver(c)
        return solver.solution()

    def test_solution(self):
        for i in range(500):
            c = Cube()
            cr = Cube()
            c.shuffle(i)
            cross_steps = WhiteCrossSolver(c).solution()
            solution = self._test_solution(c)
            # Align faces
            while cr.cubies['F'].facings['F'] != c.cubies['F'].facings['F']:
                c.move(Move('Y'))

            for cubie in cr.cubies:
                for facing in cr.cubies[cubie].facings:
                    # Upper cubies aren't positioned
                    if 'U' not in cubie:
                        self.assertEqual(cr.cubies[cubie].facings[facing], c.cubies[cubie].facings[facing])


class TestCFOPSolver(unittest.TestCase):
    @timeout_decorator.timeout(300)
    def _test_solution(self, c):
        solver = CFOP.CFOPSolver(c)
        return solver.solution()

    def test_solution(self):
        for i in range(10):
            c = Cube()
            cr = Cube()
            c.shuffle(i)
            solution = self._test_solution(c)
            for s in solution:
                c.move(s)
            # Align faces
            while cr.cubies['F'].facings['F'] != c.cubies['F'].facings['F']:
                c.move(Move('Y'))

            for cubie in cr.cubies:
                for facing in cr.cubies[cubie].facings:
                    self.assertEqual(cr.cubies[cubie].facings[facing], c.cubies[cubie].facings[facing])

