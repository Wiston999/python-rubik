class Solver(object):
    def __init__(self, cube):
        self.cube = cube

    def solution(self):
        '''Should return a list of moves or an iterable'''
        raise NotImplementedError("This method must be override")
