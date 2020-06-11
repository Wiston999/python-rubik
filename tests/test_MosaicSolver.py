from rubik_solver.Move import Move
from rubik_solver.Cubie import Cube
from rubik_solver.Solver import Mosaic
from rubik_solver.Solver.Mosaic.CrossSolver import CrossSolver
from rubik_solver.Solver.Mosaic.FaceSolver import FaceSolver
import timeout_decorator
import unittest

class TestCrossSolver(unittest.TestCase):
    def test_solution(self):
        cases = [
            'WWWWWWWWW',
            'WYWYWYWYW',
            'WRWRWRWRW',
            'WBWBWBWBW',
            'WGWGWGWGW',
            'WOWOWOWOW',
            #  Random generated cases using
            # ['W{}W{}W{}W{}W'.format(*(random.choice('RGBOYW') for i in range(4))) for _ in range(20)]
            'WYWGWYWWW',
            'WWWWWYWYW',
            'WWWYWWWBW',
            'WBWWWGWWW',
            'WBWBWOWRW',
            'WWWGWGWBW',
            'WOWOWYWWW',
            'WOWWWWWWW',
            'WYWRWRWWW',
            'WRWBWGWBW',
            'WRWBWGWOW',
            'WGWYWYWOW',
            'WGWOWBWRW',
            'WBWOWYWBW',
            'WOWRWBWYW',
            'WYWRWYWWW',
            'WRWGWOWGW',
            'WOWGWGWGW',
            'WWWGWOWOW',
            'WRWBWGWRW'
        ]

        for c0 in cases:
            steps = CrossSolver(Cube()).solution('{1}{5}{7}{3}'.format(*c0))
            c = Cube()
            for s in steps:
                c.move(Move(s))
            naive = c.to_naive_cube()
            self.assertEqual('{1}{3}{5}{7}'.format(*c0), '{1}{3}{5}{7}'.format(*naive.get_cube()[45:].upper()))


class TestFaceSolver(unittest.TestCase):
    def test_solution(self):
        cases = [
            'WWWWWWWWW',
            'WYWYWYWYW',
            'WRWRWRWRW',
            'WBWBWBWBW',
            'WGWGWGWGW',
            'WOWOWOWOW',
            #  Random generated cases using
            # ['{}{}{}{}W{}{}{}{}'.format(*(random.choice('RGBOYW') for i in range(8))) for _ in range(20)]
            'OBOYWBOWO',
            'OGYYWRORG',
            'BWRWWGGYR',
            'OOWWWOBWR',
            'WYBOWBGBR',
            'WBRBWRORO',
            'ORWGWORYB',
            'ROORWWGBG',
            'YWWBWGBWG',
            'YGYGWYRYO',
            'WGROWRGYW',
            'WRBBWRRBG',
            'WWWOWOWYR',
            'YYBRWRRRO',
            'YWBBWWRWG',
            'RRWBWBBWB',
            'ORYWWYWWY',
            'YOROWWBGG',
            'BYWYWGOBY',
            'BWBWWRYGW'
        ]

        for c0 in cases:
            steps = FaceSolver(Cube()).solution('{2}{8}{6}{0}'.format(*c0))
            c = Cube()
            for s in steps:
                c.move(Move(s))
            naive = c.to_naive_cube()
            print (c0, naive.get_cube(), steps)
            print (c0, naive.get_cube()[45:].upper())
            self.assertEqual('{0}{2}{6}{8}'.format(*c0), '{0}{2}{6}{8}'.format(*naive.get_cube()[45:].upper()))

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

    def test_solution(self):
        cases = [
            # Generated using [''.join(random.choice('RGBOYW') for i in range(9)) for _ in range(30)]
            'OYRGWRGWB',
            'GWRYGBWOR',
            'BYYGOYBWO',
            'WBGBORWOB',
            'GBRBOOOYW',
            'BBWOGORRY',
            'WOBGRBOBY',
            'WWWBYBRBW',
            'YOYBYWYOO',
            'GWROBRYOW',
            'ROYRRRRYW',
            'WGWOBYOBG',
            'GGOYBORBY',
            'GWRWRBGYW',
            'WOWBOWWGB',
            'BGGWWBRYO',
            'OWRORGWYW',
            'YRYYOYBBW',
            'GRBRWGGOB',
            'GRGWGOBBG',
            'BYOOOOYGY',
            'GOOGOGRWG',
            'GBRGWYYBW',
            'OOWBYBOBO',
            'WBOBOBOBW',
            'BOBBOYGYG',
            'GYRWWOOYR',
            'GGYBOBGOY',
            'GBRYRGWBY',
            'YOGYYGROO',
        ]

        for c0 in cases:
            steps = Mosaic.MosaicSolver(Cube(), c0).solution()
            c = Cube()
            for s in steps:
                c.move(s)
            naive = c.to_naive_cube()
            self.assertEqual(c0, naive.get_cube()[45:].upper())

