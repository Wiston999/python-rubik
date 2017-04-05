from __future__ import print_function
import sys
import os
import re
import time
from src.Move import Move
from src.Printer import TtyPrinter, OpenGLPrinter
from src.Solver.Kociemba import KociembaSolver
from src.Solver.Beginner import BeginnerSolver
from src.Cubie import Cube
from src.NaiveCube import NaiveCube
from src.Move import Move

if __name__ == '__main__':
    c = Cube(3)
    p = OpenGLPrinter(c)
    tp = TtyPrinter(c, True)
    c.shuffle()
    p.pprint()
    tp.pprint()

    solver = BeginnerSolver(c)
    solver = KociembaSolver(c)

    while True:
        m = raw_input('Input move: ')
        if re.match("[RLBFUDXYZ]'?2?", m, re.I):
            c.move(Move(m))
            tp.pprint()
        elif m.upper() == 'SH':
            print("Shuffling")
            c.shuffle()
        elif m.upper() == 'S':
            print("Solving")
            start = time.time()
            solution = solver.solution()
            end = time.time()
            print("Solved in", (end - start), "seconds")
            print("Solution:", ' '.join(str(m) for m in solution))
            for m in solution:
                # time.sleep(1)
                c.move(m)
            tp.pprint()
            print("SOLVED!")
        elif m.upper() == 'Q':
            print("Bye")
            p.stop()
            break
        else:
            print("Invalid move, try one of R, L, B, F, U, D, X, Y, Z, SH, S")
