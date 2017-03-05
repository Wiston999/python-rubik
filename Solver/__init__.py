import copy

class Solver(object):
	def __init__(self, cube):
		self.cube = copy.copy(cube)
		
	def solution(self):
		'''Should return a list of moves or an iterable'''
		raise NotImplementedError("This method must be override")