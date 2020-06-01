from rubik_solver.Move import Move
from rubik_solver.Cubie import Cube
from rubik_solver.Solver import Mosaic
import timeout_decorator
import unittest

class TestMosaicSolver(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            c = Cube()
            Mosaic.MosaicSolver(c, '')
            Mosaic.MosaicSolver(c, '123456789')
            Mosaic.MosaicSolver(c, 'RRRRRRRR9')
            Mosaic.MosaicSolver(c, 'RRRRRRRR.')
            Mosaic.MosaicSolver(c, True)
            Mosaic.MosaicSolver(c, 10)


