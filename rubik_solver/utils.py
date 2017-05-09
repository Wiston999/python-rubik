from __future__ import print_function
import argparse
import time
from past.builtins import basestring
from .Solver import Solver
from .Solver import Beginner
from .Solver import CFOP
from .Solver import Kociemba
from .NaiveCube import NaiveCube
from .Cubie import Cube
from .Printer import TtyPrinter

__author__ = 'Victor Cabezas'

METHODS = {
    'Beginner': Beginner.BeginnerSolver,
    'CFOP': CFOP.CFOPSolver,
    'Kociemba': Kociemba.KociembaSolver
}

def _check_valid_cube(cube):
    '''Checks if cube is one of str, NaiveCube or Cubie.Cube and returns
    an instance of Cubie.Cube'''

    if isinstance(cube, basestring):
        c = NaiveCube()
        c.set_cube(cube)
        cube = c

    if isinstance(cube, NaiveCube):
        c = Cube()
        c.from_naive_cube(cube)
        cube = c

    if not isinstance(cube, Cube):
        raise ValueError('Cube is not one of (str, NaiveCube or Cubie.Cube)')

    return cube

def solve(cube, method = Beginner.BeginnerSolver, *args, **kwargs):
    if isinstance(method, basestring):
        if not method in METHODS:
            raise ValueError('Invalid method name, must be one of (%s)' %
                ', '.join(METHODS.keys())
            )
        method = METHODS[method]

    if not issubclass(method, Solver):
        raise ValueError('Method %s is not a valid Solver subclass' %
            method.__class__.__name__
        )

    cube = _check_valid_cube(cube)

    solver = method(cube)

    return solver.solution(*args, **kwargs)

def pprint(cube, color = True):
    cube = _check_valid_cube(cube)
    printer = TtyPrinter(cube, color)
    printer.pprint()

def main(argv = None):
    arg_parser = argparse.ArgumentParser(description = 'rubik_solver command line tool')
    arg_parser.add_argument('-i', '--cube', dest = 'cube', required = True, help = 'Cube definition string')
    arg_parser.add_argument('-c', '--color', dest = 'color', default = True, action = 'store_false', help = 'Disable use of colors with TtyPrinter')
    arg_parser.add_argument('-s', '--solver', dest = 'solver', default = 'Beginner', choices = METHODS.keys(), help = 'Solver method to use')
    args = arg_parser.parse_args(argv)

    cube = args.cube.lower()
    print ("Read cube", cube)
    pprint(cube, args.color)

    start = time.time()
    print ("Solution", ', '.join(map(str, solve(cube, METHODS[args.solver]))))
    print ("Solved in", time.time() - start, "seconds")
