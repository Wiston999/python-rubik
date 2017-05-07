from rubik_solver.Cubie import Cube
from rubik_solver import utils
import timeout_decorator
import unittest
from rubik_solver.Solver import Beginner, CFOP, Kociemba

class MockSolver(object): pass

class TestUtils(unittest.TestCase):
    solve_methods = [
        Beginner.BeginnerSolver,
        CFOP.CFOPSolver,
        Kociemba.KociembaSolver,
    ]

    def test_solve(self):
        c = Cube()
        with self.assertRaises(TypeError):
            utils.solve(c, None)

        with self.assertRaises(ValueError):
            utils.solve(None, "INVALID SOLVER")

        with self.assertRaises(ValueError):
            utils.solve(None, MockSolver)

        with self.assertRaises(ValueError):
            utils.solve(None, self.solve_methods[0])

        with self.assertRaises(ValueError):
            utils.solve(1, self.solve_methods[0])

        for method in self.solve_methods:
            for i in range(10):
                c = Cube()
                ref_solution = method(c).solution()
                s1 = utils.solve(c, method)
                self.assertEqual(ref_solution, s1, msg = "Failed with Cubie.Cube and method %s" %
                    method.__class__.__name__
                )
                # Test with NaiveCube
                s2 = utils.solve(c.to_naive_cube(), method)
                self.assertEqual(ref_solution, s2, msg = "Failed with Cubie.Cube and method %s" %
                    method.__class__.__name__
                )

                # Test with string representation
                s3 = utils.solve(c.to_naive_cube().get_cube(), method)
                self.assertEqual(ref_solution, s3, msg = "Failed with Cubie.Cube and method %s" %
                    method.__class__.__name__
                )


    def test_pprint(self):
        c = Cube()
        with self.assertRaises(ValueError):
            utils.pprint(None)

        with self.assertRaises(ValueError):
            utils.pprint(1)
        # Just call it and wait not to fail
        utils.pprint(Cube())
