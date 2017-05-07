from rubik_solver.Move import Move
from rubik_solver.Cubie import Cube
from rubik_solver.Solver import Beginner
from rubik_solver.Solver.Beginner.WhiteCrossSolver import WhiteCrossSolver
from rubik_solver.Solver.Beginner.WhiteFaceSolver import WhiteFaceSolver
from rubik_solver.Solver.Beginner.SecondLayerSolver import SecondLayerSolver
from rubik_solver.Solver.Beginner.YellowFaceSolver import YellowFaceSolver
import timeout_decorator
import unittest

class TestWhiteCrossSolver(unittest.TestCase):
    def test_solution(self):
        cases = [
            ('D', 'F'),
            ('D', 'B'),
            ('D', 'R'),
            ('D', 'L'),
            ('F', 'U'),
            ('F', 'D'),
            ('F', 'R'),
            ('F', 'L'),
            ('B', 'U'),
            ('B', 'D'),
            ('B', 'R'),
            ('B', 'L'),
            ('R', 'U'),
            ('R', 'D'),
            ('R', 'F'),
            ('R', 'B'),
            ('L', 'U'),
            ('L', 'D'),
            ('L', 'F'),
            ('L', 'B'),
        ]

        for c0, c1 in cases:
            c = Cube()
            # Use an "imposible" edge to move, so it is not duped in the cube
            c.cubies[c._t_key(c0+c1)].facings[c0].color = 'W'
            c.cubies[c._t_key(c0+c1)].facings[c1].color = 'Y'

            steps = WhiteCrossSolver.first_step(c0, c1)
            for step in steps:
                c.move(Move(step))

            place = c.search_by_colors('W', 'Y')
            self.assertEqual(c.cubies[place].facings['U'], 'W')
            # Weird, but works
            self.assertEqual(c.cubies[place].facings[place.replace('U', '')], 'Y')

class TestWhiteFaceSolver(unittest.TestCase):
    def test_first_step(self):
        goals = [
            'DFR',
            'DFL',
            'BDL',
            'BDR',
            'BRU',
            'BLU',
            'FLU',
        ]

        for goal in goals:
            c = Cube()
            solver = WhiteFaceSolver(c)
            # Muahaha at that range
            for i in range(1 if goal == 'DFR' else 0, 3):
                c.cubies[goal].facings[goal[i % 3]] = 'W'
                c.cubies[goal].facings[goal[(i + 1) % 3]] = 'Y'
                c.cubies[goal].facings[goal[(i + 2) % 3]] = 'O'

                steps = WhiteFaceSolver.first_step(goal, goal[i % 3])

                for s in steps:
                    c.move(Move(s))

                self.assertIn('W', c.cubies['FRU'].colors, "%s --> %d" %(goal, i))
                self.assertIn('Y', c.cubies['FRU'].colors, "%s --> %d" %(goal, i))
                self.assertIn('O', c.cubies['FRU'].colors, "%s --> %d" %(goal, i))

    def test_second_step(self):
        # Case 1
        c = Cube()
        c.cubies['FRU'].facings['F'] = 'W'
        c.cubies['FRU'].facings['R'] = 'Y'
        c.cubies['FRU'].facings['U'] = 'O'
        steps = WhiteFaceSolver.second_step('F')
        for s in steps:
            c.move(Move(s))

        self.assertEqual(c.cubies['DFR'].facings['D'], 'W')
        self.assertEqual(c.cubies['DFR'].facings['F'], 'O')
        self.assertEqual(c.cubies['DFR'].facings['R'], 'Y')
        # Case 2
        c = Cube()
        c.cubies['FRU'].facings['F'] = 'O'
        c.cubies['FRU'].facings['R'] = 'W'
        c.cubies['FRU'].facings['U'] = 'Y'
        steps = WhiteFaceSolver.second_step('R')
        for s in steps:
            c.move(Move(s))

        self.assertEqual(c.cubies['DFR'].facings['D'], 'W')
        self.assertEqual(c.cubies['DFR'].facings['F'], 'O')
        self.assertEqual(c.cubies['DFR'].facings['R'], 'Y')
        # Case 3
        c = Cube()
        c.cubies['FRU'].facings['F'] = 'O'
        c.cubies['FRU'].facings['R'] = 'Y'
        c.cubies['FRU'].facings['U'] = 'W'
        steps = WhiteFaceSolver.second_step('U')
        for s in steps:
            c.move(Move(s))

        self.assertEqual(c.cubies['DFR'].facings['D'], 'W')
        self.assertEqual(c.cubies['DFR'].facings['F'], 'Y')
        self.assertEqual(c.cubies['DFR'].facings['R'], 'O')

class TestSecondLayerSolver(unittest.TestCase):
    def test_is_solved(self):
        c = Cube()
        solver = SecondLayerSolver(c)
        self.assertTrue(solver.is_solved())

    # Dunno how to test the solution function

class TestYellowFaceSolver(unittest.TestCase):
    def test_edges_are_placed(self):
        c = Cube()
        solver = YellowFaceSolver(c)
        for _ in range(4):
            c.move(Move('U'))
            self.assertTrue(solver.edges_are_placed())

    def test_corner_is_placed(self):
        c = Cube()
        solver = YellowFaceSolver(c)
        for _ in range(4):
            c.move(Move('U'))
            for corner in ['FRU', 'FLU', 'BRU', 'BLU']:
                self.assertTrue(solver.corner_is_placed(corner))
            self.assertTrue(solver.placed_corners())

        for corner in ['FRU', 'FLU', 'BRU', 'BLU']:
            c = Cube()
            solver = YellowFaceSolver(c)
            c.cubies[corner].facings[corner[0]] = 'W'
            self.assertFalse(solver.corner_is_placed(corner))

class TestBeginnerSolver(unittest.TestCase):
    @timeout_decorator.timeout(10)
    def _test_solution(self, c):
        solver = Beginner.BeginnerSolver(c)
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
                self.assertEqual(cr.cubies[cubie].facings[facing], c.cubies[cubie].facings[facing])
