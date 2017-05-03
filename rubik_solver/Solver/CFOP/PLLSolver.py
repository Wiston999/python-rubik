from rubik_solver.Move import Move
from .. import Solver

class PLLSolver(Solver):
    STEPS = {
        "810345672": ["X", "R'", "U", "R'", "D2", "R", "U'", "R'", "D2", "R2", "X'"],
        "018345276": ["X'", "R", "U'", "R", "D2", "R'", "U", "R", "D2", "R2", "X"],
        "012743658": ["R2", "U", "R", "U", "R'", "U'", "R'", "U'", "R'", "U", "R'"],
        "012547638": ["R", "U'", "R", "U", "R", "U", "R", "U'", "R'", "U'", "R2"],
        "072543618": ["M2", "U", "M2", "U2", "M2", "U", "M2"],
        "018543672": ["R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'", "R", "U", "R'", "F'"],
        "230145678": ["R'", "U", "L'", "U2", "R", "U'", "R'", "U2", "R", "L", "U'"],
        "018347652": ["R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'"],
        "210745638": ["L", "U2", "L'", "U2", "L", "F'", "L'", "U'", "L", "U", "L", "F", "L2", "U"],
        "210347658": ["R'", "U2", "R", "U2", "R'", "F", "R", "U", "R'", "U'", "R'", "F'", "R2", "U'"],
        "852341670": ["R'", "U", "R'", "Y", "U'", "R'", "F'", "R2", "U'", "R'", "U", "R'", "F", "R", "F"],
        "650143278": ["R2", "Y", "D", "R'", "U", "R'", "U'", "R", "Y'", "D'", "R2", "Y'", "R'", "U", "R"],
        "832745016": ["R'", "U'", "R", "Y", "R2", "Y", "D", "R'", "U", "R", "U'", "R", "Y'", "D'", "R2"],
        "812743056": ["R2", "Y'", "D'", "R", "U'", "R", "U", "R'", "Y", "D", "R2", "Y", "R", "U'", "R'"],
        "670145238": ["R", "U", "R'", "Y'", "R2", "Y'", "D'", "R", "U'", "R'", "U", "R'", "Y", "D", "R2"],
        "012543876": ["R'", "U2", "R'", "Y", "U'", "R'", "F'", "R2", "U'", "R'", "U", "R'", "F", "R", "U'", "F"],
        "032147658": ["M2", "U", "M2", "U", "M'", "U2", "M2", "U2", "M'", "U2"],
        "832145670": ["F", "R", "U'", "R'", "U'", "R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R", "F'"],
        "872345610": ["L", "U'", "R", "U2", "L'", "U", "R'", "L", "U'", "R", "U2", "L'", "U", "R'", "U"],
        "076345218": ["R'", "U", "L'", "U2", "R", "U'", "L", "R'", "U", "L'", "U2", "R", "U'", "L", "U'"],
        "618345072": ["X'", "R", "U'", "R'", "D", "R", "U", "R'", "D'", "R", "U", "R'", "D", "R", "U'", "R'", "D'", "X"]
    }

    @staticmethod
    def get_orientations(cube):
        cubies = ['BLU', 'BU', 'BRU', 'LU', 'U', 'RU', 'FLU', 'FU', 'FRU']
        orientation = []
        for cubie in cubies:
            o = PLLSolver.get_correct_cubie(cube, cubie)
            orientation.append(str(cubies.index(o)))
        return ''.join(orientation)

    def move(self, s, solution):
        self.cube.move(Move(s))
        solution.append(s)

    @staticmethod
    def get_correct_cubie(cube, cubie):
        colors = [cube.cubies[c].facings[c].color for c in cubie.replace('U', '')]
        return cube.search_by_colors('Y', *colors)

    def solution(self):
        solution = []
        while True:
            for _ in range(4):
                self.move('U', solution)
                for _ in range(4):
                    self.move('Y', solution)
                    orientation = PLLSolver.get_orientations(self.cube)

                    if orientation in PLLSolver.STEPS:
                        for s in PLLSolver.STEPS[orientation]:
                            self.move(s, solution)
                        return solution
            # Apply shortest and expect to be solvable after that
            for s in PLLSolver.STEPS["072543618"]:
                self.move(s, solution)
        return []
