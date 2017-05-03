from rubik_solver.Cubie import Cube
from rubik_solver import utils
import timeout_decorator
import unittest
from rubik_solver.Solver import Beginner, CFOP, Kociemba


class TestUtils(unittest.TestCase):
    def test_solve(self):
        solve_methods = [
            Beginner.BeginnerSolver,
            CFOP.CFOPSolver,
            Kociemba.KociembaSolver,
        ]

        c = Cube()
        with self.assertRaises(ValueError):
            utils.solve(c, None)

        with self.assertRaises(ValueError):
            utils.solve(None, solve_methods[0])

        with self.assertRaises(ValueError):
            utils.solve(1, solve_methods[0])

        for method in solve_methods:
            for i in range(10):
                c = Cube()

                ref_solution = method(c).solution()
                s1 = utils.solve(c, method)
                self.assertEqual(ref_solution, s1)
                # Test with NaiveCube
                s2 = utils.solve(c.to_naive_cube(), method)
                self.assertEqual(ref_solution, s2)
                # Test with string representation
                s3 = utils.solve(c.to_naive_cube().get_cube(), method)
                self.assertEqual(ref_solution, s3)

    def test_pprint(self):
        c = Cube()
        with self.assertRaises(ValueError):
            utils.solve(c, None)

        with self.assertRaises(ValueError):
            utils.solve(None, solve_methods[0])

        with self.assertRaises(ValueError):
            utils.solve(1, solve_methods[0])
