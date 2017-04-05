from past.builtins import basestring
import math
import re


class Face(object):
    colours = ['w', 'r', 'b', 'g', 'y', 'o', '.']

    def __init__(self, size=3, init=None, check=True):
        self.size = size

        if init:
            init = init.replace(' ', '')
            if check and not isinstance(init, (str, basestring)):
                raise ValueError("Init configuration must be a string")

            if check and int(math.sqrt(len(init))) != math.sqrt(len(init)):
                raise ValueError(
                    "Init configuration length must be a power of 2")

            self.size = int(math.sqrt(self.size))
            self.squares = init
        else:
            self.squares = '.' * (self.size * self.size)

    def set_colour(self, x, y, c):
        if c not in self.colours:
            raise ValueError('Invalid color, got %s and should be one of %s' % (
                c, ','.join(Face.colours)))

        if (0 > x or x >= self.size) or (0 > y or y >= self.size):
            raise ValueError('Invalid face position, got (%d, %d)' % (x, y))

        self.squares = self.squares[:(
            x * self.size + y)] + c + self.squares[(x * self.size + y + 1):]

    def get_colour(self, x, y):
        if (0 > x or x >= self.size) or (0 > y or y >= self.size):
            raise ValueError('Invalid face position, got (%d, %d)' % (x, y))

        return self.squares[x * self.size + y]

    def __eq__(self, otherFace):
        return re.match(otherFace.squares, self.squares) is not None

    def __ne__(self, otherFace):
        return not self == otherFace

    def is_solved(self):
        return len(set(self.squares)) == 1
