import sys
from .. import Solver
from Printer import TtyPrinter
from Face import Face
from CrossSolver import CrossSolver

class CFOPSolver(Solver):
	MOVES = ['F', 'B', 'R', 'L', 'U', 'D']
	def __init__(self, cube, max_depth = 1):
		self._solution = []
		self.max_depth = max_depth
		self.backtracks = 0
		super(CFOPSolver, self).__init__(cube)
		self.p = TtyPrinter(self.cube, True)
		
	def solution(self):
		crossSolver = CrossSolver(self.cube)
		self._solution = crossSolver.solution()
		# if not self.solve_white_cross([]):
			# return None
			
		# if not self.solve_white_corner(self._solution[:]):
			# return None
			
		# if not self.solve_second_layer(self._solution[:]):
			# return None
		return self._solution
		
	def solve_white_cross(self, current_solution):
		if self.is_white_cross():
			self._solution = current_solution[:]
			return True
		elif len(current_solution) < self.max_depth:
			for move in self.MOVES:
				self.cube.move(move)
				current_solution.append(move)
				if not self.solve_white_cross(current_solution):
					## Reverse move
					self.cube.move("%s'" % move)
					current_solution.pop()
				else:
					return True
		else:
			self.backtracks += 1
			if (self.backtracks % 1000) == 0:
				sys.stderr.write("# backtracks: %d\r" % self.backtracks)
				sys.stderr.flush()
		
		return False
	
	def is_white_cross(self):
		if self.cube.faces['D'] != Face(init = '.w.www.w.', check = False):
			return False
			
		if self.cube.faces['R'] != Face(init = '....b..b.', check = False):
			return False
		
		if self.cube.faces['L'] != Face(init = '....g..g.', check = False):
			return False
			
		if self.cube.faces['F'] != Face(init = '....o..o.', check = False):
			return False
			
		if self.cube.faces['B'] != Face(init = '....r..r.', check = False):
			return False
		
			
		return True
		
	def solve_white_corner(self, current_solution):
		while not self.is_white_corner():
			current_solution.append("R'")
			current_solution.append("D'")
			current_solution.append("R")
			current_solution.append("D")
			
			self.cube.move("R'")
			self.cube.move("D'")
			self.cube.move("R")
			self.cube.move("D")
		
		print "IS WHITE CORNER"
		self.p.pprint()
		self._solution = current_solution[:]
		return True
		
	def is_white_corner(self):
		if self.cube.faces['D'] != Face(init = 'wwwwwwwww', check = False):
			return False
		
		if self.cube.faces['R'] != Face(init = '...bbbbbb', check = False):
			return False
		
		if self.cube.faces['L'] != Face(init = '...gggggg', check = False):
			return False
			
		if self.cube.faces['F'] != Face(init = '...oooooo', check = False):
			return False
			
		if self.cube.faces['B'] != Face(init = '...rrrrrr', check = False):
			return False
		
		# for i in range(self.cube.size):
			# for j in range(self.cube.size):
				# if self.cube.faces['U'].get_colour(i, j) != 'w':
					# print 1
					# return False
		
		# for i in range(self.cube.size):
			# if self.cube.faces['R'].get_colour(0, i) != 'g':
				# print 2
				# return False
		
		# if self.cube.faces['R'].get_colour(1, 1) != 'g':
			# print 3
			# return False
			
		# for i in range(self.cube.size):
			# if self.cube.faces['L'].get_colour(0, i) != 'b':
				# print 4
				# return False
		
		# if self.cube.faces['L'].get_colour(1, 1) != 'b':
			# print 5
			# return False
			
		# for i in range(self.cube.size):
			# if self.cube.faces['F'].get_colour(0, i) != 'o':
				# print 6
				# return False
		
		# if self.cube.faces['F'].get_colour(1, 1) != 'o':
			# print 7
			# return False
			
		# for i in range(self.cube.size):
			# if self.cube.faces['B'].get_colour(0, i) != 'r':
				# print 8
				# return False
		
		# if self.cube.faces['B'].get_colour(1, 1) != 'r':
			# print 9
			# return False
		
		return True
		
	def solve_second_layer(self, current_solution):
		current_solution.append("U'")
		current_solution.append("L'")
		current_solution.append("U")
		current_solution.append("L")
		current_solution.append("U")
		current_solution.append("F")
		current_solution.append("U'")
		current_solution.append("F'")
		
		self.cube.move("U'")
		self.cube.move("L'")
		self.cube.move("U")
		self.cube.move("L")
		self.cube.move("U")
		self.cube.move("F")
		self.cube.move("U'")
		self.cube.move("F'")
		
		self._solution = current_solution[:]
		
		return True