from .. import Solver
from rubik_solver.Move import Move

class YellowFaceSolver(Solver):
    def apply_edges_algorithm(self, solution):
        for move in ["R", "U", "R'", "U", "R", "U2", "R'"]:
            self.move(move, solution)

    def apply_corner_place_algorithm(self, solution):
        for move in ["U", "R", "U'", "L'", "U", "R'", "U'", "L"]:
            self.move(move, solution)

    def apply_corner_orient_algorithm(self, solution):
        for move in ["R'", "D'", "R", "D"]:
            self.move(move, solution)

    def edges_are_placed(self):
        color_order = 'GOBR'
        front_color = str(self.cube.cubies['FU'].facings['F'])
        back_color = str(self.cube.cubies['BU'].facings['B'])
        left_color = str(self.cube.cubies['LU'].facings['L'])
        right_color = str(self.cube.cubies['RU'].facings['R'])

        actual_order = [front_color, right_color, back_color, left_color]
        green_index = actual_order.index('G')
        actual_order = ['G']+actual_order[green_index+1:]+actual_order[:green_index]

        return ''.join(actual_order) == color_order

    def corner_is_placed(self, corner):
        corner = self.cube.cubies[corner]
        related_edges = ''.join(corner.faces).replace('U', '')
        for edge in related_edges:
            if self.cube.cubies[edge+'U'].facings[edge] not in corner.colors:
                return False

        return True

    def placed_corners(self):
        return [c for c in ['FRU', 'FLU', 'BRU', 'BLU'] if self.corner_is_placed(c)]

    def move(self, m, solution):
        self.cube.move(Move(m))
        solution.append(m)

    def solution(self):
        solution = []
        # Locate edge with front_color
        turns = 0
        while not self.edges_are_placed():
            turns += 1
            # If we are rotating over the same solutions, apply twice algorithm to break cycle
            if turns >= 4:
                turns = 0
                self.apply_edges_algorithm(solution)
            self.apply_edges_algorithm(solution)
            self.move("Y'", solution)

        # Place corner in their place
        while True:
            placed_corners = self.placed_corners()
            if len(placed_corners) == 4:
                break
            # If only 1 corner is well placed, place it at FRU and perform algorithm once or twice
            elif len(placed_corners) == 1:
                while self.placed_corners()[0] != 'FRU':
                    self.move("U", solution)
                self.apply_corner_place_algorithm(solution)
            # If no placed corners, perform algorithm and 1 corner will be placed
            else:
                self.apply_corner_place_algorithm(solution)

        # Orient corners
        for _ in range(4):
            # Get corner at FRU
            corner = self.cube.cubies['FRU']
            while corner.facings['U'] != 'Y':
                # Apply corner orientation algorithm
                self.apply_corner_orient_algorithm(solution)
            self.move("U", solution)

        # Finally, align the top layer
        while self.cube.cubies['F'].facings['F'] != self.cube.cubies['FU'].facings['F']:
            self.move("U", solution)
        return solution
