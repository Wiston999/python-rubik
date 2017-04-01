from src.Move import Move
from src.Cubie import Cube
from src.Solver import Beginner
from src.Solver.Beginner.WhiteCrossSolver import WhiteCrossSolver
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


class TestBeginnerSolver(unittest.TestCase):
    def test_solution(self):
        pass

