from __future__ import print_function

import time
import math

class bcolors:
    BLUE = '\033[44m'
    GREEN = '\033[102m'
    YELLOW = '\033[103m'
    RED = '\033[101m'
    WHITE = '\033[107m'
    ORANGE = '\033[48;5;214m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Printer(object):
    def __init__(self, cube):
        self._cube = cube

    @property
    def cube(self):
        '''
        Initial implementation worked with NaiveCube, this hack the whole class accesses to self.cube
        to work the same way as before
        '''
        return self._cube.to_naive_cube()

    def pprint(self):
        pass


class TtyPrinter(Printer):
    def __init__(self, cube, colours=False):
        self.colours = colours
        super(TtyPrinter, self).__init__(cube)

    def pprint(self):
        self.print_upper()
        self.print_center()
        self.print_down()

    def print_upper(self):
        for i in range(self.cube.size * 2 + 1):
            print(' ' * (self.cube.size * 6), end = ' ')
            if (i % 2) == 0:
                for j in range(self.cube.size * 2):
                    if (j % 2) == 0:
                        print('|', end = ' ')
                    else:
                        print('---', end = ' ')
                print('|')
            else:
                for j in range(self.cube.size * 2):
                    if (j % 2) == 0:
                        print('|', end = ' ')
                    else:
                        self.print_square(self.cube.faces['U'].get_colour(int(i / 2), int(j / 2)))
                print('|')

    def print_center(self):
        for i in range(self.cube.size * 2 + 1):
            for face in ['L', 'F', 'R', 'B']:
                if (i % 2) == 0:
                    for j in range(self.cube.size * 2):
                        if (j % 2) == 0:
                            print('|', end = ' ')
                        else:
                            print('---', end = ' ')
                else:
                    for j in range(self.cube.size * 2):
                        if (j % 2) == 0:
                            print('|', end = ' ')
                        else:
                            self.print_square(self.cube.faces[face].get_colour(int(i / 2), int(j / 2)))
                print('|', end = ' ')
            print()

    def print_down(self):
        for i in range(self.cube.size * 2 + 1):
            print(' ' * (self.cube.size * 6), end = ' ')
            if (i % 2) == 0:
                for j in range(self.cube.size * 2):
                    if (j % 2) == 0:
                        print('|', end = ' ')
                    else:
                        print('---', end = ' ')
                print('|')
            else:
                for j in range(self.cube.size * 2):
                    if (j % 2) == 0:
                        print('|', end = ' ')
                    else:
                        self.print_square(self.cube.faces['D'].get_colour(int(i / 2), int(j / 2)))
                print('|')

    def print_square(self, c):
        if self.colours:
            if c == 'w':
                print(bcolors.WHITE, end = ' ')
            elif c == 'b':
                print(bcolors.BLUE, end = ' ')
            elif c == 'g':
                print(bcolors.GREEN, end = ' ')
            elif c == 'r':
                print(bcolors.RED, end = ' ')
            elif c == 'y':
                print(bcolors.YELLOW, end = ' ')
            elif c == 'o':
                print(bcolors.ORANGE, end = ' ')
            print(' ', bcolors.ENDC, end = ' ')
        else:
            print(c.upper(), end = ' ')

