from __future__ import print_function
import argparse
import re
import time
from rubik_solver.Move import Move
from rubik_solver.Printer import TtyPrinter
from rubik_solver.Solver.Kociemba import KociembaSolver
from rubik_solver.Solver.CFOP import CFOPSolver
from rubik_solver.Solver.Beginner import BeginnerSolver
from rubik_solver.Cubie import Cube

arg_parser = argparse.ArgumentParser(description = 'python-rubik tool')
arg_parser.add_argument('-c', '--colors', dest = 'colors', action = 'store_true', help = 'Use colors with TtyPrinter')
arg_parser.add_argument('-s', '--solver', dest = 'solver', default = 'Beginner', choices = ['Beginner', 'CFOP', 'Kociemba'], help = 'Default solver to use')

# Python 2/3 compatible
try:
    input = raw_input
except NameError:
    pass

def select_solver(solver_name, cube):
    if solver_name == 'Beginner':
        solver = BeginnerSolver(cube)
    elif solver_name == 'CFOP':
        solver = CFOPSolver(cube)
    elif solver_name == 'Kociemba':
        solver = KociembaSolver(cube)
    else:
        raise ValueError('Invalid Solver')
    return solver

if __name__ == '__main__':
    args = arg_parser.parse_args()
    cube = Cube(3)
    ttyprinter = TtyPrinter(cube, args.colors)
    cube.shuffle()
    ttyprinter.pprint()

    solver = select_solver(args.solver, cube)

    while True:
        move = input('Input move: ')
        if re.match("[RLBFUDXYZMSE]'?2?$", move, re.I):
            cube.move(Move(move))
            ttyprinter.pprint()
        elif move.upper().startswith('CH'):
            input_solver = move.split()[-1]
            try:
                solver = select_solver(input_solver, cube)
            except Exception as e:
                print("Unrecognized solver")
        elif move.upper() == 'SH':
            print("Shuffling")
            cube.shuffle()
        elif move.upper() == 'SO':
            print("Solving with", solver.__class__.__name__, "solver")
            start = time.time()
            solution = solver.solution()
            end = time.time()
            print("Solved in", (end - start), "seconds")
            print("Solution:", ' '.join(str(m) for m in solution))
            for move in solution:
                cube.move(move)
            ttyprinter.pprint()
            print("SOLVED!")
        elif move.upper() == 'Q':
            print("Bye")
            break
        else:
            print("Invalid action, try one of R, L, B, F, U, D, X, Y, Z, SH, CH, S")
