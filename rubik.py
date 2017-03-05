import sys
import os
import re
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Cube import Cube
from Move import Move
from Printer import TtyPrinter, OpenGLPrinter
from Solver.Kociemba import KociembaSolver
from Solver.Beginner.WhiteCrossSolver import WhiteCrossSolver
from Cubie import Cube as CubieCube
from Move import Move

if __name__ == '__main__':
    c = Cube(3)
    p = OpenGLPrinter(c)
    tp = TtyPrinter(c, True)
    # c.set_cube('owyryyygwwgbrbbbbgryrrroygbbrrggbwbrgogwowgyyowoywooow')
    c.shuffle()
    tp.pprint()
    p.pprint()

    solver = WhiteCrossSolver(c)

    sys.exit(1)
    while True:
        m = raw_input('Input move: ')
        if re.match("[RLBFUD]'?2?", m, re.I):
            c.move(Move(m))
            tp.pprint()
        elif m.upper() == 'SH':
            print "Shuffling"
            c.shuffle()
        elif m.upper() == 'S':
            print "Solving"
            solution = solver.solution(maxDepth=23)
            print "Solution:", ' '.join(solution)
            for m in solution:
                time.sleep(1)
                c.move(Move(m))
            tp.pprint()
            print "SOLVED!"
        elif m.upper() == 'Q':
            print "Bye"
            p.stop()
            break
        else:
            print "Invalid move, try one of R, L, B, F, U, D, SH, S"
