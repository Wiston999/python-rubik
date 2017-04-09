from src.Move import Move
from .. import Solver

class PLLSolver(Solver):
    STEPS = {
        "821345670": ["X", "R'", "U", "R'", "D2", "R", "U'", "R'", "D2", "R2"],
        "018345276": ["X'", "R", "U'", "R", "D2", "R'", "U", "R", "D2", "R2"],
        "012743658": ["R2", "U", "R", "U", "R'", "U'", "R'", "U'", "R'", "U", "R'"],
        "012547638": ["R", "U'", "R", "U", "R", "U", "R", "U'", "R'", "U'", "R2"],
        "072543718": ["M2", "U", "M2", "U2", "M2", "U", "M2"],
        "018543672": ["R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'", "R", "U", "R'", "F'"],
        "230145678": ["R'", "U", "L'", "U2", "R", "U'", "R'", "U2", "R", "L", "U'"],
        "018347652": ["R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'"],
        "210745638": ["L", "U2′", "L'", "U2′", "L", "F'", "L'", "U'", "L", "U", "L", "F", "L2′", "U"],
        "210347658": ["R'", "U2", "R", "U2", "R'", "F", "R", "U", "R'", "U'", "R'", "F'", "R2", "U'"],
        "852341670": ["R'", "U", "R'", "d'", "R'", "F'", "R2", "U'", "R'", "U", "R'", "F", "R", "F"],
        "650143278": ["R2", "u", "R'", "U", "R'", "U'", "R", "u'", "R2", "y'", "R'", "U", "R"],
        "832745016": ["R'", "U'", "R", "y", "R2", "u", "R'", "U", "R", "U'", "R", "u'", "R2"],
        "812743056": ["R2", "u'", "R", "U'", "R", "U", "R'", "u", "R2", "y", "R", "U'", "R'"],
        "670145238": ["R", "U", "R'", "y'", "R2", "u", "'R", "U'", "R'", "U", "R'", "u", "R2"],
        "012543876": ["R'", "U2", "R'", "d'", "R'", "F'", "R2", "U'", "R'", "U", "R'", "F", "R", "U'", "F"],
        "032147658": ["M2", "U", "M2", "U", "M'", "U2", "M2", "U2", "M'", "U2"],
        "832145670": ["F", "R", "U'", "R'", "U'", "R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R", "F'"],
        "872345610": ["L", "U'", "R", "U2", "L'", "U", "R'", "L", "U'", "R", "U2", "L'", "U", "R'", "U"],
        "076345218": ["R'", "U", "L'", "U2", "R", "U'", "L", "R'", "U", "L'", "U2", "R", "U'", "L", "U'"],
        "618345072": ["X", "R", "U'", "R'", "D", "R", "U", "R'", "u2", "R'", "U", "R", "D", "R'", "U'", "R"]
    }

    @staticmethod
    def get_orientations(cube):
        cubies = ['BLU', 'BU', 'BRU', 'LU', 'U', 'RU', 'FLU', 'FU', 'FRU']
        orientation = []
        for cubie in cubies:
            o = PLLSolver.get_correct_cubie(cube, cubie)
            orientation.append(cubies.index(o))
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
        for _ in range(4):
            orientation = PLLSolver.get_orientations(self.cube)
            if orientation in PLLSolver.STEPS:
                step_solution = PLLSolver.STEPS[orientation]
                for s in step_solution:
                    self.move(s, solution)
                break
            self.move("Y", solution)
        return solution
