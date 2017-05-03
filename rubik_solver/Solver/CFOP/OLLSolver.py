from rubik_solver.Move import Move
from .. import Solver

class OLLSolver(Solver):
    STEPS = {
        "LBRLURLFR": ["R", "U", "B'", "X'", "R", "U", "X2", "R2", "X'", "U'", "R'", "F", "R", "F'"],
        "LBRLURFFF": ["R'", "F", "R", "F'", "U2", "R'", "F", "R", "Y'", "R2", "U2", "R"],
        "BBRLURLFU": ["Y", "M", "U", "X", "R'", "U2", "X'", "R", "U", "L'", "U", "L", "M'"],
        "LBULURFFR": ["R'", "U2", "X", "R'", "U", "R", "U'", "Y", "R'", "U'", "R'", "U", "R'", "F", "Z'"],
        "UBBLURLFU": ["R", "U", "R'", "U", "R'", "F", "R", "F'", "U2", "R'", "F", "R", "F'"],
        "UBULURUFU": ["M'", "U2", "M", "U2", "M'", "U", "M", "U2", "M'", "U2", "M"],
        "UBULURLFR": ["R'", "U2", "F", "R", "U", "R'", "U'", "Y'", "R2", "U2", "X'", "R", "U", "X"],
        "BBBLURUFU": ["F", "R", "U", "R'", "U", "Y'", "R'", "U2", "R'", "F", "R", "F'"],
        "BURLURFUR": ["R'", "U'", "Y", "L'", "U", "L'", "Y'", "L", "F", "L'", "F", "R"],
        "LURLURLUR": ["R", "U'", "Y", "R2", "D", "R'", "U2", "R", "D'", "R2", "Y'", "U", "R'"],
        "BBRUUUFFR": ["F", "U", "R", "U'", "R'", "U", "R", "U'", "R'", "F'"],
        "LBRUUULFR": ["L'", "B'", "L", "U'", "R'", "U", "R", "U'", "R'", "U", "R", "L'", "B", "L"],
        "BURUUUFUR": ["L", "U'", "R'", "U", "L'", "U", "R", "U", "R'", "U", "R"],
        "LURUUULUR": ["R", "U", "R'", "U", "R", "U'", "R'", "U", "R", "U2", "R'"],
        "LUBUUUFUU": ["L'", "U", "R", "U'", "L", "U", "R'"],
        "BURUUULUU": ["R'", "U2", "R", "U", "R'", "U", "R"],
        "UUBUUUUUF": ["R'", "F'", "L", "F", "R", "F'", "L'", "F"],
        "UUUUUUFUF": ["R2", "D", "R'", "U2", "R", "D'", "R'", "U2", "R'"],
        "UUBUUULUU": ["R'", "F'", "L'", "F", "R", "F'", "L", "F"],
        "UBUUURUUU": ["M'", "U'", "M", "U2", "M'", "U'", "M"],
        "UBUUUUUFU": ["L'", "R", "U", "R'", "U'", "L", "R'", "F", "R", "F'"],
        "BURUURUFF": ["L", "F", "R'", "F", "R", "F2", "L'"],
        "UURUURFFU": ["F", "R'", "F'", "R", "U", "R", "U'", "R'"],
        "LUBUURFFU": ["R'", "U'", "R", "Y'", "X'", "R", "U'", "R'", "F", "R", "U", "R'", "X"],
        "BUBUURUFU": ["U'", "R", "U2", "R'", "U'", "R", "U'", "R2", "Y'", "R'", "U'", "R", "U", "B"],
        "LUBUURLFF": ["F", "R", "U", "R'", "U'", "R", "U", "R'", "U'", "F'"],
        "BUBUURFFF": ["L", "F'", "L'", "F", "U2", "L2", "Y'", "L", "F", "L'", "F"],
        "BUBLUUUFU": ["U'", "R'", "U2", "R", "U", "R'", "U", "R2", "Y", "R", "U", "R'", "U'", "F'"],
        "LUULUUFFR": ["X", "L", "U2", "R'", "U'", "R", "U'", "X'", "L'"],
        "BUULUUUFR": ["R'", "U2", "X'", "R", "R", "U'", "R'", "U", "X", "R'", "U2", "R"],
        "BURLUUFFR": ["F'", "L'", "U'", "L", "U", "L'", "U'", "L", "U", "F"],
        "LUBLUULFF": ["R'", "F", "R'", "F'", "R2", "U2", "X'", "U'", "R", "U", "R'", "X"],
        "BUBLUUFFF": ["R'", "F", "R", "F'", "U2", "R2", "Y", "R'", "F'", "R", "F'"],
        "BBUUURLUF": ["R", "U", "R'", "Y", "R'", "F", "R", "U'", "R'", "F'", "R"],
        "UBBUURFUR": ["L'", "B'", "L", "U'", "R'", "U", "R", "L'", "B", "L"],
        "LBBUURFUU": ["U2", "X", "L", "R2", "U'", "R", "U'", "R'", "U2", "R", "U'", "M"],
        "UBUUURLUR": ["X'", "U'", "R", "U'", "R2", "F", "X", "R", "U", "R'", "U'", "R", "B2"],
        "LBBLUULUF": ["L", "U'", "Y'", "R'", "U2", "R'", "U", "R", "U'", "R", "U2", "R", "Y", "U'", "L'"],
        "BBRLUUUUF": ["U2", "X", "R'", "L2", "U", "L'", "U", "L", "U2", "L'", "U", "M"],
        "UBULUULUR": ["Y2", "F", "U", "R", "U'", "X'", "U", "R'", "D'", "R", "U'", "R'", "X"],
        "BBRLUULUU": ["X'", "L'", "U2", "R", "U", "R'", "U", "X", "L"],
        "UURLURUUR": ["R", "U", "X'", "R", "U'", "R'", "U", "X", "U'", "R'"],
        "LBRUUUUFU": ["R", "U", "R'", "U'", "X", "D'", "R'", "U", "R", "E'", "Z'"],
        "LBBUUUFFU": ["R'", "F", "R", "U", "R'", "F'", "R", "Y", "L", "U'", "L'"],
        "BBRUUUUFF": ["L", "F'", "L'", "U'", "L", "F", "L'", "Y'", "R'", "U", "R"],
        "BBRUUULFU": ["L'", "B'", "L", "R'", "U'", "R", "U", "L'", "B", "L"],
        "LBBUUUUFR": ["R", "B", "R'", "L", "U", "L'", "U'", "R", "B'", "R'"],
        "UURUURUFR": ["F", "U", "R", "U'", "R'", "F'"],
        "BUULUUFFU": ["R'", "Y", "U'", "L", "Y'", "U", "R", "U'", "R'", "F'", "R"],
        "UUBUURUFF": ["L", "Y'", "U", "R'", "Y", "U'", "L'", "U", "L", "F", "L'"],
        "LUULUULFU": ["F'", "U'", "L'", "U", "L", "F"],
        "LBUUUULFU": ["F", "R", "U", "R'", "U'", "F'"],
        "BBUUUUFFU": ["R", "U", "R'", "U'", "R'", "F", "R", "F'"],
        "LBULUUUUF": ["L", "U", "L'", "U", "L", "U'", "L'", "U'", "Y2", "R'", "F", "R", "F'"],
        "UBRUURFUU": ["R'", "U'", "R", "U'", "R'", "U", "R", "U", "Y", "F", "R'", "F'", "R"],
        "UBBUUULFU": ["R'", "F", "R", "U", "R'", "U'", "Y", "L'", "Y'", "U", "R"],
        "BBUUUUUFR": ["L", "F'", "L'", "U'", "L", "U", "Y'", "R", "Y", "U'", "L'"]
    }

    @staticmethod
    def get_orientations(cube, color = 'Y'):
        return ''.join([
            cube.cubies['BLU'].color_facing(color),
            cube.cubies['BU'].color_facing(color),
            cube.cubies['BRU'].color_facing(color),
            cube.cubies['LU'].color_facing(color),
            cube.cubies['U'].color_facing(color),
            cube.cubies['RU'].color_facing(color),
            cube.cubies['FLU'].color_facing(color),
            cube.cubies['FU'].color_facing(color),
            cube.cubies['FRU'].color_facing(color)
        ])

    def move(self, s, solution):
        self.cube.move(Move(s))
        solution.append(s)

    def solution(self):
        solution = []
        for _ in range(4):
            orientation = OLLSolver.get_orientations(self.cube)
            if orientation in OLLSolver.STEPS:
                step_solution = OLLSolver.STEPS[orientation]
                for s in step_solution:
                    self.move(s, solution)
                break
            self.move("Y", solution)
        return solution 
