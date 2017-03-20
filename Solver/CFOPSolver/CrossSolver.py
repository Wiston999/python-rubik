from Face import Face
from Move import Move

import math

class CrossSolver(object):
	def __init__(self, cube):
		self.cube = cube
		self._solution = []
	
	@staticmethod
	def goal(cube):
		if cube.faces['D'] != Face(init = '.w.www.w.', check = False):
			return False
		
		if cube.faces['R'] != Face(init = '....b..b.', check = False):
			return False
		
		if cube.faces['L'] != Face(init = '....g..g.', check = False):
			return False
			
		if cube.faces['F'] != Face(init = '....o..o.', check = False):
			return False
			
		if cube.faces['B'] != Face(init = '....r..r.', check = False):
			return False
		
		return True

	def solution(self):
		return self.solve([], CrossSolver.succesors_generator, CrossSolver.score, CrossSolver.goal)
		
	def solve(self, start, successors, score, goal):
		solution = []
		if goal(self.cube):
			return solution
		explored = []
		g = 1
		h = score(self.cube)
		f = g + h
		p = [start]
		frontier = [(f, g, h, p)]
		while frontier:
			f, g, h, path = frontier.pop(0)
			if isinstance(path[-1], Move):
				self.cube.move(path[-1])
			for move in successors(path[-1]):
				self.cube.move(move)
				if (move.raw, self.cube.get_cube()) not in explored:
					explored.append((move.raw, self.cube.get_cube()))
					path2 = path + [move]
					h2 = score(self.cube)
					g2 = g + 1
					f2 = h2 + g2
					if goal(self.cube):
						return path2
					elif len(path2) <= 7:
						frontier.append((f2, g2, h2, path2))
						frontier.sort(key=lambda x:x[:3])
				self.cube.move(move.reverse())
		print "Explored", explored
		return None
		
	@staticmethod
	def score(cube):
		score = 0
		reference_cube = Cube(3)
		reference_cube.set_cube('.............b..b.....o..o.....g..g.....r..r..w.www.w.')
		
		## Each square out of place
		for face in 'FRLBD':
			for i in range(cube.size):
				for j in range(cube.size):
					if reference_cube.faces[face].get_colour(i, j) != '.' and i != 1 and j != 1:
						if reference_cube.faces[face].get_colour(i, j) != cube.faces[face].get_colour(i, j):
							score += CrossSolver.find_shortest_movement(face, i, j, cube)
							
		return score
	
	
	
	@staticmethod
	def find_shortest_movement(face, i, j, cube):
		colour = cube.faces[face].get_colour(i, j)
		positions = cube.get_colour_positions(colour)
		
		score = 0
		for cf, ci, cj in positions:
			if cf != face and ci != i and cj != j:
				score = max(score, manhatan_3d(face, i, j, cf, ci, cj))
		
		return score
		
	@staticmethod
	def manhatan_3d(face0, i0, j0, face1, i1, j1):
		faces_distance = 0
		i_distance = 0
		j_distance = 0
		if face0 == 'F':
			if face1 == 'B':
				faces_distance += 2
			elif face1 != 'F':
				faces_distance += 1
		elif face0 == 'B':
			if face1 == 'F':
				faces_distance += 2
			elif face1 != 'B':
				faces_distance += 1
		elif face0 == 'R':
			if face1 == 'L':
				faces_distance += 2
			elif face1 != 'R':
				faces_distance += 1
		elif face0 == 'L':
			if face1 == 'R':
				faces_distance += 2
			elif face1 != 'L':
				faces_distance += 1
		elif face0 == 'U':
			if face1 == 'D':
				faces_distance += 2
			elif face1 != 'U':
				faces_distance += 1
		elif face0 == 'D':
			if face1 == 'U':
				faces_distance += 2
			elif face1 != 'D':
				faces_distance += 1
		
		i_distance = math.abs(i0 - i1)
		j_distance = math.abs(j0 - j1)
		
		return (faces_distance * faces_distance) + (i_distance * i_distance) + (j_distance * j_distance)
		
	@staticmethod
	def succesors_generator(last_movement = None):
		for move in 'ULFRBD':
			for modifier in ["", "'", "2"]:
				current_move = Move(move + modifier)
				if last_movement is None or last_movement != current_move.reverse():
					yield current_move
