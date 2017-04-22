from __future__ import print_function
import argparse
import re
import time
from src.Move import Move
from src.Printer import TtyPrinter, OpenGLPrinter
from src.Solver.Kociemba import KociembaSolver
from src.Solver.CFOP import CFOPSolver
from src.Solver.Beginner import BeginnerSolver
from src.Cubie import Cube
from src.Move import Move

parser = argparse.ArgumentParser(description = 'python-rubik tool')
parser.add_argument('-o', '--opengl', dest = 'opengl', action = 'store_true', help = 'Print cube with openGL printer')
parser.add_argument('-c', '--colors', dest = 'colors', action = 'store_true', help = 'Use colors with TtyPrinter')
parser.add_argument('-s', '--solver', dest = 'solver', default = 'Beginner', choices = ['Beginner', 'CFOP', 'Kociemba'], help = 'Default solver to use')

def select_solver(s, cube):
    if s == 'Beginner':
       solver = BeginnerSolver(cube)
    elif s == 'CFOP':
        solver = CFOPSolver(cube)
    elif s == 'Kociemba':
        solver = KociembaSolver(cube)
    else:
        raise ValueError('Invalid Solver')
    return solver

if __name__ == '__main__':
    args = parser.parse_args()
    c = Cube(3)
    tp = TtyPrinter(c, args.colors)
    c.shuffle()
    tp.pprint()
    if args.opengl:
        p = OpenGLPrinter(c)
        p.pprint()

    solver = select_solver(args.solver, c)

    while True:
        m = raw_input('Input move: ')
        if re.match("[RLBFUDXYZMSE]'?2?$", m, re.I):
            c.move(Move(m))
            tp.pprint()
        elif m.upper().startswith('CH'):
            s = m.split()[-1]
            try:
                solver = select_solver(s, c)
            except:
                print("Unrecognized solver")
        elif m.upper() == 'SH':
            print("Shuffling")
            c.shuffle()
        elif m.upper() == 'SO':
            print("Solving with", solver.__class__.__name__, "solver") 
            start = time.time()
            solution = solver.solution()
            end = time.time()
            print("Solved in", (end - start), "seconds")
            print("Solution:", ' '.join(str(m) for m in solution))
            for m in solution:
                c.move(m)
            tp.pprint()
            print("SOLVED!")
        elif m.upper() == 'Q':
            print("Bye")
            if args.opengl:
                p.stop()
            break
        else:
            print("Invalid action, try one of R, L, B, F, U, D, X, Y, Z, SH, CH, S")
