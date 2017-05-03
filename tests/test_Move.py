from rubik_solver.Move import Move
import string
import unittest

class TestMove(unittest.TestCase):
    allowed_moves = 'fblrudxyzmse'
    def test_init(self):
        for c in string.ascii_lowercase:
            if c in self.allowed_moves:
                self.assertEqual(Move(c).raw, c.upper())
                self.assertEqual(Move(c.upper()).raw, c.upper())

                self.assertEqual(Move(c+"2").raw, c.upper()+"2")
                self.assertEqual(Move(c.upper()+"2").raw, c.upper()+"2")

                self.assertEqual(Move(c+"'").raw, c.upper()+"'")
                self.assertEqual(Move(c.upper()+"'").raw, c.upper()+"'")

                self.assertEqual(Move(c).face, c.upper())
                self.assertEqual(Move(c.upper()).face, c.upper())

                self.assertEqual(Move(c+"2").face, c.upper())
                self.assertEqual(Move(c.upper()+"2").face, c.upper())

                self.assertEqual(Move(c+"'").face, c.upper())
                self.assertEqual(Move(c.upper()+"'").face, c.upper())

                self.assertTrue(Move(c).clockwise)
                self.assertFalse(Move(c).counterclockwise)
                self.assertFalse(Move(c).double)

                self.assertFalse(Move(c+"'").clockwise)
                self.assertTrue(Move(c+"'").counterclockwise)
                self.assertFalse(Move(c+"'").double)

                self.assertFalse(Move(c+"2").clockwise)
                self.assertFalse(Move(c+"2").counterclockwise)
                self.assertTrue(Move(c+"2").double)
                
            else:
                with self.assertRaises(ValueError):
                    Move(c)
                with self.assertRaises(ValueError):
                    Move(c+"'")
                with self.assertRaises(ValueError):
                    Move(c+"2")

    def test_logic(self):
        m = Move(self.allowed_moves[0])

        self.assertTrue(m.clockwise)
        self.assertFalse(m.counterclockwise)
        self.assertFalse(m.double)

        m.double = True
        self.assertFalse(m.clockwise)
        self.assertFalse(m.counterclockwise)
        self.assertTrue(m.double)
        
        m.double = False
        self.assertTrue(m.clockwise)
        self.assertFalse(m.counterclockwise)
        self.assertFalse(m.double)

        m.counterclockwise = True
        self.assertFalse(m.clockwise)
        self.assertTrue(m.counterclockwise)
        self.assertFalse(m.double)
        
        m.counterclockwise = False
        self.assertTrue(m.clockwise)
        self.assertFalse(m.counterclockwise)
        self.assertFalse(m.double)

    def test_reverse(self):
        m = Move(self.allowed_moves[0])
        m1 = m.reverse()

        self.assertFalse(m1.clockwise)
        self.assertTrue(m1.counterclockwise)
        self.assertFalse(m1.double)
        
        m.double = True
        m1 = m.reverse()
        self.assertFalse(m1.clockwise)
        self.assertFalse(m1.counterclockwise)
        self.assertTrue(m1.double)

        m.counterclockwise = True
        m1 = m.reverse()
        self.assertTrue(m1.clockwise)
        self.assertFalse(m1.counterclockwise)
        self.assertFalse(m1.double)

    def test_equals(self):
        self.assertEqual(Move("F"), 'f')
        self.assertEqual(Move("f"), 'f')
        self.assertEqual(Move("F"), 'F')
        self.assertEqual(Move("f"), 'F')

        self.assertEqual(Move("F"), Move("f"))

        self.assertNotEqual(Move("F"), "B")
        self.assertNotEqual(Move("F"), "b")
        self.assertNotEqual(Move("F"), Move("B"))

        self.assertEqual(Move("F'"), "f'")
        self.assertEqual(Move("f'"), "f'")
        self.assertEqual(Move("F'"), "F'")
        self.assertEqual(Move("f'"), "F'")

        self.assertEqual(Move("F'"), Move("f'"))

        self.assertNotEqual(Move("F'"), "B")

        self.assertEqual(Move("F2"), "f2")
        self.assertEqual(Move("f2"), "f2")
        self.assertEqual(Move("F2"), "F2")
        self.assertEqual(Move("f2"), "F2")

        self.assertEqual(Move("F2"), Move("f2"))

        self.assertNotEqual(Move("F2"), "B")

    def test_maths(self):
        m = Move(self.allowed_moves[0])

        for c in self.allowed_moves[1:]:
            with self.assertRaises(ValueError):
                m1 = m + Move(c)

        self.assertIsNone(Move("f") + Move("f'"))

        self.assertIsNone(Move("f2") + Move("f2"))

        self.assertEqual(Move("f") + Move("f"), "F2")
        self.assertEqual(Move("f") + Move("f") + Move("f"), "F'")
        self.assertEqual(Move("f2") + Move("f"), "F'")
        self.assertIsNone(Move("f") + Move("f") + Move("f") + Move("f"))
        
        self.assertIsNone(Move("f") * 4)
        self.assertIsNone(Move("f") * 8)

        self.assertEqual(Move("f") * 2, Move("f2"))
        self.assertEqual(Move("f") * 3, Move("f'"))

        self.assertEqual(Move("f'") * 2, Move("f2"))
        self.assertEqual(Move("f'") * 3, Move("f"))

        self.assertIsNone(Move("f2") * 2)
        self.assertIsNone(Move("f2") * 4)
