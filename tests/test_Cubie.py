import rubik_solver.Cubie as Cubie
import rubik_solver.Move as Move
import unittest

class TestSticker(unittest.TestCase):
    allowed_chars = 'rgbywo.'

    def test_init(self):
        not_allowed_chars = 'acdefhijklmnpqstuvxz'

        for c in not_allowed_chars:
            self.assertRaises(ValueError, Cubie.Sticker, c)
            self.assertRaises(ValueError, Cubie.Sticker, c.upper())

        for c in self.allowed_chars:
            s = Cubie.Sticker(c)
            self.assertEqual(s.color, c)
            self.assertEqual(Cubie.Sticker(c.upper()).color, c)

    def test_eq(self):
        for c in self.allowed_chars:
            s = Cubie.Sticker(c)
            self.assertTrue(s == c)
            self.assertTrue(c == s)
            self.assertTrue(s == Cubie.Sticker(c.upper()))
            self.assertFalse(s == 'a')
            self.assertRaises(TypeError, s.__eq__, 1)

    def test_eq(self):
        for c in self.allowed_chars:
            s = Cubie.Sticker(c)
            self.assertEqual(s < c, s.color < c)
            self.assertEqual(s <= c, s.color <= c)
            self.assertEqual(s > c, s.color > c)
            self.assertEqual(s >= c, s.color >= c)
            self.assertEqual(c < s, c < s.color)
            self.assertEqual(c <= s, c <= s.color)
            self.assertEqual(c > s, c > s.color)
            self.assertEqual(c >= s, c >= s.color)
            self.assertEqual(s < Cubie.Sticker(c.upper()), s.color < Cubie.Sticker(c.upper()).color)
            self.assertEqual(s <= Cubie.Sticker(c.upper()), s.color <= Cubie.Sticker(c.upper()).color)
            self.assertEqual(s > Cubie.Sticker(c.upper()), s.color > Cubie.Sticker(c.upper()).color)
            self.assertEqual(s >= Cubie.Sticker(c.upper()), s.color >= Cubie.Sticker(c.upper()).color)

            with self.assertRaises(TypeError):
                s < 1

            with self.assertRaises(TypeError):
                s > 1

            with self.assertRaises(TypeError):
                s <= 1

            with self.assertRaises(TypeError):
                s >= 1

class TestCubie(unittest.TestCase):
    allowed_chars = 'bdflru'

    def test_init(self):
        not_allowed_chars = 'aceghijkmnopqstvwxyz'

        for c in not_allowed_chars:
            # Color here is irrelevant as it is checked in TestSticker
            with self.assertRaises(ValueError):
                Cubie.Cubie(**{c: 'r'})
            with self.assertRaises(ValueError):
                Cubie.Cubie(**{c.upper(): 'r'})

        for c in self.allowed_chars:
            s = Cubie.Cubie(**{c: 'r'})
            self.assertEqual(s.facings[c.upper()], 'r')
            s1 = Cubie.Cubie(**{c.upper(): 'r'})
            self.assertEqual(s.facings[c.upper()], 'r')

    def test_faces(self):
        c = Cubie.Cubie(F = 'r', B = 'r', U = 'r', D = 'r', L = 'r', R = 'r')
        self.assertIn('F', c.faces)
        self.assertIn('B', c.faces)
        self.assertIn('U', c.faces)
        self.assertIn('D', c.faces)
        self.assertIn('L', c.faces)
        self.assertIn('R', c.faces)
    
    def test_colors(self):
        c = Cubie.Cubie(F = 'r', B = 'g', U = 'b', D = 'w', L = 'y', R = 'o')
        self.assertIn('r', c.colors)
        self.assertIn('g', c.colors)
        self.assertIn('b', c.colors)
        self.assertIn('w', c.colors)
        self.assertIn('y', c.colors)
        self.assertIn('o', c.colors)

    def test_facing_to_color(self):
        self.assertEqual(Cubie.Cubie.facing_to_color('F'), 'R')
        self.assertEqual(Cubie.Cubie.facing_to_color('B'), 'O')
        self.assertEqual(Cubie.Cubie.facing_to_color('R'), 'G')
        self.assertEqual(Cubie.Cubie.facing_to_color('L'), 'B')
        self.assertEqual(Cubie.Cubie.facing_to_color('U'), 'Y')
        self.assertEqual(Cubie.Cubie.facing_to_color('D'), 'W')

    def test_color_to_facing(self):
        self.assertEqual(Cubie.Cubie.color_to_facing('R'), 'F')
        self.assertEqual(Cubie.Cubie.color_to_facing('O'), 'B')
        self.assertEqual(Cubie.Cubie.color_to_facing('G'), 'R')
        self.assertEqual(Cubie.Cubie.color_to_facing('B'), 'L')
        self.assertEqual(Cubie.Cubie.color_to_facing('Y'), 'U')
        self.assertEqual(Cubie.Cubie.color_to_facing('W'), 'D')

    def test_color_facing(self):
        c = Cubie.Cubie(F = 'r', B = 'g', U = 'b', D = 'w', L = 'y', R = 'o')
        self.assertEqual(c.color_facing('r'), 'F')
        self.assertEqual(c.color_facing('g'), 'B')
        self.assertEqual(c.color_facing('b'), 'U')
        self.assertEqual(c.color_facing('w'), 'D')
        self.assertEqual(c.color_facing('y'), 'L')
        self.assertEqual(c.color_facing('o'), 'R')

        self.assertEqual(c.color_facing('R'), 'F')
        self.assertEqual(c.color_facing('G'), 'B')
        self.assertEqual(c.color_facing('B'), 'U')
        self.assertEqual(c.color_facing('W'), 'D')
        self.assertEqual(c.color_facing('Y'), 'L')
        self.assertEqual(c.color_facing('O'), 'R')

        c = Cubie.Cubie()
        self.assertIsNone(c.color_facing('R'))
        self.assertIsNone(c.color_facing('G'))
        self.assertIsNone(c.color_facing('B'))
        self.assertIsNone(c.color_facing('W'))
        self.assertIsNone(c.color_facing('Y'))
        self.assertIsNone(c.color_facing('O'))

class TestCenter(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            c = Cubie.Center(F = 'r', D = 'r')
        
        # Lol, don't know how to test a OK case
        self.assertEqual(Cubie.Center(F = 'r').facings['F'], 'r')

class TestEdge(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            c = Cubie.Edge(F = 'r')

        with self.assertRaises(ValueError):
            c = Cubie.Edge(F = 'r', D = 'r', R = 'r')

class TestCorner(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            c = Cubie.Corner(F = 'r')

        with self.assertRaises(ValueError):
            c = Cubie.Corner(F = 'r', D = 'r')

class TestCube(unittest.TestCase):
    def test_init(self):
        c = Cubie.Cube()

        for cubie in c.cubies:
            cubie = Cubie.Cube._t_key(cubie)
            self.assertIn(cubie, Cubie.Cube.CUBIES)
            cubie_list = list(cubie)
            for face in cubie_list:
                self.assertIn(face, c.cubies[cubie].faces)
                self.assertIn(Cubie.Cubie.facing_to_color(face), c.cubies[cubie].colors)
                self.assertEqual(c.cubies[cubie].facings[face], Cubie.Cubie.facing_to_color(face))
            
    def test__t_key(self):
        self.assertEqual(Cubie.Cube._t_key('UR'), 'RU')
        self.assertEqual(Cubie.Cube._t_key('RU'), 'RU')
        self.assertEqual(Cubie.Cube._t_key('ULFD'), 'DFLU')
        
    def test_move_changes(self):
        with self.assertRaises(ValueError):
            Cubie.Cube.move_changes('X')
        
        with self.assertRaises(ValueError):
            Cubie.Cube.move_changes(1)

    def test_move(self):
        cr = Cubie.Cube()
        for m, implications in Cubie.Cube.MOVES.items():
            c = Cubie.Cube()
            c.move(Move.Move(m))
            moved_cubies = set()
            for orig, dest in implications:
                moved_cubies.add(Cubie.Cube._t_key(orig))
                or_cubie = cr.cubies[Cubie.Cube._t_key(orig)]
                dest_cubie = c.cubies[Cubie.Cube._t_key(dest)]
                for i in range(len(dest)):
                    self.assertEqual(or_cubie.facings[orig[i]], dest_cubie.facings[dest[i]], msg = "Fail in move %s" % m)
            
            # Check the rest of cubies aren't moved
            for cubie in Cubie.Cube.CUBIES:
                if cubie not in moved_cubies:
                    or_cubie = cr.cubies[Cubie.Cube._t_key(cubie)]
                    dest_cubie = c.cubies[Cubie.Cube._t_key(cubie)]
                    for i in range(len(cubie)):
                        self.assertEqual(or_cubie.facings[cubie[i]], dest_cubie.facings[cubie[i]])


    def test_search_by_colors(self):
        c = Cubie.Cube()
        # Just a few cases, elaborate more in future
        # self.assertIsNone(c.search_by_colors('r', 'r'))
        self.assertIsNone(c.search_by_colors('y', 'w'))
        self.assertIsNone(c.search_by_colors('r', 'o'))
        self.assertIsNone(c.search_by_colors('j'))

        for cubie in c.cubies:
            colors = [Cubie.Cubie.facing_to_color(f) for f in list(cubie)]
            self.assertEqual(c.search_by_colors(*colors), cubie)

if __name__ == '__main__':
    unittest.main()
