import src.Cubie as Cubie
import unittest

class TestSticker(unittest.TestCase):
    allowed_chars = 'rgbywo.'
    def test_init(self):
        not_allowed_chars = 'acdefhijklmnpqstuvxz'
        allowed_chars = 'rgbywo.'

        for c in not_allowed_chars:
            self.assertRaises(ValueError, Cubie.Sticker, c)
            self.assertRaises(ValueError, Cubie.Sticker, c.upper())

        for c in self.allowed_chars:
            s = Cubie.Sticker(c)
            self.assertEqual(s.color, c)
            self.assertEqual(Cubie.Sticker(c.upper()).color, c)
    
    def test_cmp(self):
        for c in self.allowed_chars:
            s = Cubie.Sticker(c)
            self.assertTrue(s == c)
            self.assertTrue(c == s)
            self.assertTrue(s == Cubie.Sticker(c.upper()))
            self.assertFalse(s == 'a')
            self.assertRaises(TypeError, s.__cmp__, 1)
        
if __name__ == '__main__':
    unittest.main()
