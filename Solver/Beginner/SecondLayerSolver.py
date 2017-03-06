from .. import Solver
from Move import Move
from Cubie import Sticker
from Printer import TtyPrinter

class SecondLayerSolver(Solver):
    def is_solved(self):
        # Check if edges FL, FR, BL and BR are correctly placed and oriented
        front_color = self.cube.cubies['F'].facings['F']
        back_color = self.cube.cubies['B'].facings['B']
        left_color = self.cube.cubies['L'].facings['L']
        right_color = self.cube.cubies['R'].facings['R']

        success = self.cube.cubies['FL'].facings['F'] == front_color and self.cube.cubies['FL'].facings['L'] == left_color
        success = success and self.cube.cubies['FR'].facings['F'] == front_color and self.cube.cubies['FR'].facings['R'] == right_color
        success = success and self.cube.cubies['BL'].facings['B'] == back_color and self.cube.cubies['BL'].facings['L'] == left_color
        success = success and self.cube.cubies['BR'].facings['B'] == back_color and self.cube.cubies['BR'].facings['R'] == right_color

        return success
        
    def move(self, move, solution):
        solution.append(move)
        self.cube.move(Move(move))

    def solution(self):
        solution = []
        pprint = TtyPrinter(self.cube, True)
        # Place FR and FL
        # front_color = self.cube.cubies['F'].facings['F']
        # right_color = self.cube.cubies['R'].facings['R']
        # left_color = self.cube.cubies['L'].facings['L']

        # goal_fr_cubie = self.cube.search_by_colors(front_color, right_color)
        # goal_fl_cubie = self.cube.search_by_colors(front_color, left_color)

        # self.move("Y2", solution)

        # While there are pending cubies to place
        round = 0
        while True:
            if self.is_solved():
                break

            if round > 3:
                # We have made a full round to the cube and haven't found a well cubie to place 
                # and cube isn't solved yet
                print "RONDA"
                break
            current_cubie = self.cube.cubies['FU']
            # If not yellow on FL, we place it
            round += 1
            if current_cubie.color_facing('Y') is None:
                round = 0
                front_color = current_cubie.facings['F']
                correct_face = self.cube.search_by_colors(front_color)

                print "Front color is", front_color
                print "Correct face is", correct_face

                if correct_face == 'L':
                    self.move("U", solution)
                    self.move("Y'", solution)
                elif correct_face == 'R':
                    self.move("U'", solution)
                    self.move("Y", solution)
                elif correct_face == 'B':
                    self.move("U2", solution)
                    self.move("Y2", solution)
                
                # Right now we are able to use the F2L or F2R algorithms
                if self.cube.cubies['FU'].facings['U'] == self.cube.cubies['R'].facings['R']:
                    print "F2R"
                    # F2R: U R U' R' U' F' U F
                    self.move("U", solution)
                    self.move("R", solution)
                    self.move("U'", solution)
                    self.move("R'", solution)
                    self.move("U'", solution)
                    self.move("F'", solution)
                    self.move("U", solution)
                    self.move("F", solution)
                else:
                    print "F2L"
                    # F2L: U' L' U L U F U' F'
                    self.move("U'", solution)
                    self.move("L'", solution)
                    self.move("U", solution)
                    self.move("L", solution)
                    self.move("U", solution)
                    self.move("F", solution)
                    self.move("U'", solution)
                    self.move("F'", solution)
            pprint.pprint()
            raw_input()
            self.move("Y", solution)
        return solution