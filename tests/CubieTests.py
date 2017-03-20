import Cubie
import unittest

class TestSticker(unittest.TestCase):
    def test_init(self):
        not_allowed_chars = 'acdefhijklmnpqstuvxz'
        allowed_chars = 'rgbywo.'

        for c in not_allowed_chars:
            self.assertRaises(ValueError, Cubie.Sticker, c)

        for c in allowed_chars:
            s = Cubie.Sticker(c)
            self.assertEqual(s.color, c)



if __name__ == '__main__':
    unittest.main()