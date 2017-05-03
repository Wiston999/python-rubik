from rubik_solver.Move import Move
from .. import Solver
from ..Beginner.WhiteFaceSolver import WhiteFaceSolver

class F2LSolver(Solver):
    STEPS = {
        'FUR': {
            'UB': ["R", "U", "R'"],
            'FU': ["U'", "F'", "U", "F"],
            'FR': ["U", "F'", "U", "F", "U", "F'", "U2", "F"],
            'RF': ["U", "F'", "U'", "F", "Y", "U'", "F", "U", "F'", "Y'"],
            'RU': ["R", "U'", "R'", "U", "Y'", "U", "R'", "U'", "R", "Y"],
            'BU': ["U", "F'", "U2", "F", "U", "F'", "U2", "F"],
            'LU': ["U", "F'", "U'", "F", "U", "F'", "U2", "F"],
            'UR': ["U'", "R", "U'", "R'", "U", "R", "U", "R'"],
            'UL': ["U'", "R", "U", "R'", "U", "R", "U", "R'"],
            'UF': ["U", "F'", "U2", "F", "U'", "R", "U", "R'"],
        },
        'URF': {
            'LU': ["F'", "U'", "F"],
            'UR': ["U", "R", "U'", "R'"],
            'FR': ["U'", "R", "U'", "R'", "U'", "R", "U2", "R'"],
            'RF': ["U'", "R", "U", "R'", "Y'", "U", "R'", "U'", "R", "Y"],
            'UF': ["F'", "U", "F", "U'", "Y", "U'", "F", "U", "F'", "Y'"],
            'UL': ["U'", "R", "U2", "R'", "U'", "R", "U2", "R'"],
            'UB': ["U'", "R", "U", "R'", "U'", "R", "U2", "R'"],
            'FU': ["U", "F'", "U", "F", "U'", "F'", "U'", "F"],
            'BU': ["U", "F'", "U'", "F", "U'", "F'", "U'", "F"],
            'RU': ["U'", "R", "U2", "R'", "U", "F'", "U'", "F"],
        },
        'FRD': {
            'FU': ["U", "R", "U'", "R'", "U'", "F'", "U", "F"],
            'RU': ["U2", "R", "U'", "R'", "U'", "F'", "U", "F"],
            'LU': ["R", "U'", "R'", "U'", "F'", "U", "F"],
            'BU': ["U'", "R", "U'", "R'", "U'", "F'", "U", "F"],
            'UR': ["U'", "F'", "U", "F", "U", "R", "U'", "R'"],
            'UL': ["U", "F'", "U", "F", "U", "R", "U'", "R'"],
            'UB': ["F'", "U", "F", "U", "R", "U'", "R'"],
            'UF': ["U2", "F'", "U", "F", "U", "R", "U'", "R'"],
            'RF': ["R", "U'", "R'", "Y'", "U", "R'", "U2", "R", "U", "R'", "U2", "R", "Y"],
            'FR': [],
        },
        'DFR': {
            'FU': ["F'", "U", "F", "U'", "F'", "U", "F"],
            'UR': ["R", "U", "R'", "U'", "R", "U", "R'"],
            'FR': ["R", "U'", "R'", "U", "R", "U2", "R'", "U", "R", "U'", "R'"],
            'RF': ["R", "U", "R'", "U'", "R", "U'", "R'", "U", "Y'", "U", "R'", "U'", "R", "Y"],
        },
        'RDF': {
            'FU': ["F'", "U'", "F", "U", "F'", "U'", "F"],
            'UR': ["R", "U'", "R'", "U", "R", "U'", "R'"],
            'FR': ["R", "U'", "R'", "U'", "R", "U", "R'", "U'", "R", "U2", "R'"],
            'RF': ["R", "U'", "R'", "Y'", "U", "R'", "U'", "R", "U'", "R'", "U'", "R", "Y"]
        },
        'RFU':{
            'FR': ["R", "U", "R'", "U'", "R", "U", "R'", "U'", "R", "U", "R'"],
            'RF': ["R", "U'", "R'", "Y'", "U", "R'", "U", "R", "Y"],
            'UF': ["R", "U", "R'", "U'", "U'", "R", "U", "R'", "U'", "R", "U", "R'"],
            'UL': ["U2", "R", "U", "R'", "U", "R", "U'", "R'"],
            'UB': ["U", "R", "U2", "R'", "U", "R", "U'", "R'"],
            'UR': ["R", "U2", "R'", "U'", "R", "U", "R'"],
            'LU': ["U'", "F'", "U2", "F", "U'", "F'", "U", "F"],
            'BU': ["U2", "F'", "U'", "F", "U'", "F'", "U", "F"],
            'RU': ["Y'", "R'", "U'", "R", "U2", "R'", "U'", "R", "U", "R'", "U'", "R", "Y"],
            'FU': ["F'", "U2", "F", "U", "F'", "U'", "F"],
        },
    }
    @staticmethod
    def get_step(corner, edge):
        '''
        This method returns the step to place to 2 cubies in place,
        the variables encodes the cubies position and orientation.
        corner must be a string with 3 letters, each letter represents
        the facing of the colors in the following way:
            1st letter: where the front color (cubie F) is facing in the corner to move
            2nd letter: where the right color (cubie R) is facing in the corner to move
            3rd letter: where the bottom color (cubie B, usually white) is facing in the corner to move
        The same applies with the edge variable
        '''
        return F2LSolver.STEPS[corner][edge]

    def move(self, s, solution):
        self.cube.move(Move(s))
        solution.append(s)

    def solution(self):
        solution = []
        for _ in range(4):
            front_color = self.cube.cubies['F'].facings['F'].color
            right_color = self.cube.cubies['R'].facings['R'].color

            corner = self.cube.search_by_colors(front_color, right_color, 'W')
            step_solution = WhiteFaceSolver.first_step(corner, self.cube.cubies[corner].color_facing('W'))
            solution.extend(step_solution)
            for s in step_solution:
                self.cube.move(Move(s))
            edge = self.cube.search_by_colors(front_color, right_color)

            # If edge is in BL or BR, WAF!, this case is not expected in any manual
            if edge == 'BL':
                self.move("B'", solution)
                self.move("U'", solution)
                self.move("B", solution)
            elif edge == 'BR':
                self.move("B", solution)
                self.move("U", solution)
                self.move("B'", solution)
            elif edge == 'FL':
                self.move("L'", solution)
                self.move("U'", solution)
                self.move("L", solution)

            corner = self.cube.search_by_colors(front_color, right_color, 'W')
            #Place corner in FRU if needed
            if 'U' in corner:
                while corner != 'FRU':
                    self.move("U", solution)
                    corner = self.cube.search_by_colors(front_color, right_color, 'W')

            edge = self.cube.search_by_colors(front_color, right_color)

            corner_facings = ''.join([
                self.cube.cubies[corner].color_facing(front_color),
                self.cube.cubies[corner].color_facing(right_color),
                self.cube.cubies[corner].color_facing('W')
            ])
            edge_facings = ''.join([
                self.cube.cubies[edge].color_facing(front_color),
                self.cube.cubies[edge].color_facing(right_color)
            ])

            step_solution = F2LSolver.get_step(corner_facings, edge_facings)
            solution.extend(step_solution)
            for s in step_solution:
                self.cube.move(Move(s))

            self.cube.move(Move("Y"))
            solution.append("Y")

        return solution
