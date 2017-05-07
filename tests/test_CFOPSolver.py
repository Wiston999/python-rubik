from rubik_solver.Move import Move
from rubik_solver.Cubie import Cube
from rubik_solver.Cubie import Cubie
from rubik_solver.Solver import CFOP
from rubik_solver.Solver.CFOP.F2LSolver import F2LSolver
from rubik_solver.Solver.CFOP.OLLSolver import OLLSolver
from rubik_solver.Solver.CFOP.PLLSolver import PLLSolver
from rubik_solver.Solver.Beginner.WhiteCrossSolver import WhiteCrossSolver
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
        for i in range(1):
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

class TestOLLSolver(unittest.TestCase):
    def test_steps(self):
        for orientation, steps in OLLSolver.STEPS.items():
            c = Cube()
            for i, cubie in enumerate(['BLU', 'BU', 'BRU', 'LU', 'U', 'RU', 'FLU', 'FU', 'FRU']):
                for facing in cubie:
                    if facing == orientation[i]:
                        c.cubies[cubie].facings[facing].color = 'Y'
                    else:
                        c.cubies[cubie].facings[facing].color = 'W'

            for s in steps:
                c.move(Move(s))

            for i, cubie in enumerate(['BLU', 'BU', 'BRU', 'LU', 'U', 'RU', 'FLU', 'FU', 'FRU']):
                self.assertEqual(c.cubies[cubie].facings['U'].color, 'Y', msg = '%s != %s -> Fail OLL with %s orientation on cubie %s' % (
                    c.cubies[cubie].facings['U'],
                    'Y',
                    orientation,
                    cubie
                ))

class TestPLLSolver(unittest.TestCase):
    def test_steps(self):
        cubies = ['BLU', 'BU', 'BRU', 'LU', 'U', 'RU', 'FLU', 'FU', 'FRU']
        orientations = {
            2: {'1': 'BU', '3': 'LU', '5': 'RU', '7': 'FU'},
            3: {'0': 'BLU', '2': 'RBU', '6': 'LFU', '8': 'FRU'}
        }
        cr = Cube()
        for orientation, steps in PLLSolver.STEPS.items():
            c = Cube()
            for i, oriented in enumerate(orientation):
                if i != 4: # The center cubie doesn't need to be relocated
                    cubie_or = cubies[i]
                    cubie_dest = cubies[int(oriented)]
                    orient_or = orientations[len(cubie_or)][str(i)]
                    orient_dest = orientations[len(cubie_or)][oriented]
                    kwargs = {}
                    for j, orient in enumerate(orient_or):
                        kwargs[orient_dest[j]] = cr.cubies[cubie_or].facings[orient].color
                    c.cubies[cubie_dest] = Cubie(**kwargs)

            for s in steps:
                c.move(Move(s))

            while cr.cubies['F'].facings['F'] != c.cubies['F'].facings['F']:
                c.move(Move('Y'))

            for cubie in cr.cubies:
                for facing in cr.cubies[cubie].facings:
                    self.assertEqual(cr.cubies[cubie].facings[facing], c.cubies[cubie].facings[facing], msg = '%s != %s -> Fail PLL with %s orientation on cubie %s' % (
                    cr.cubies[cubie].facings[facing].color,
                    c.cubies[cubie].facings[facing].color,
                    orientation,
                    cubie
                ))

class TestCFOPSolver(unittest.TestCase):
    @timeout_decorator.timeout(300)
    def _test_solution(self, c):
        solver = CFOP.CFOPSolver(c)
        return solver.solution()

    def test_solved_solution(self):
        '''Try to solve an already solved cube'''
        c = Cube()
        solution = self._test_solution(c)
        self._check_solution(c, solution)

    def test_solution(self):
        for i in range(100):
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
                self.assertEqual(
                    cr.cubies[cubie].facings[facing],
                    c.cubies[cubie].facings[facing],
                    msg = 'Invalid solution at cubie %s --> %s != %s' %(cubie, cr.cubies[cubie].facings[facing], c.cubies[cubie].facings[facing])
                )
