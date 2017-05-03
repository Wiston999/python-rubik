from past.builtins import basestring
import re


class Move(object):
    def __init__(self, move):
        if not re.match("[fblrudxyzmse]'?2?", move, re.I):
            raise ValueError("Invalid move format, must be [face]' or [face]2, got %s" % move)

        self.raw = move.upper()

    @property
    def face(self):
        return self.raw[0].upper()

    @face.setter
    def face(self, new_face):
        self.raw = new_face + self.raw[1:]

    @property
    def double(self):
        return '2' in self.raw

    @double.setter
    def double(self, new_double):
        if new_double:
            self.raw = self.raw.replace('2', '').replace("'", '') + '2'
        else:
            self.raw = self.raw.replace('2', '').replace("'", '')

    @property
    def counterclockwise(self):
        return "'" in self.raw

    @counterclockwise.setter
    def counterclockwise(self, value):
        if value:
            self.raw = self.raw.replace("'", '').replace("2", '') + "'"
        else:
            self.raw = self.raw.replace("'", '').replace("2", '')

    @property
    def clockwise(self):
        return not self.counterclockwise and not self.double

    @clockwise.setter
    def clockwise(self, value):
        self.counterclockwise = not value

    def reverse(self):
        return Move(self.face + ("'" if self.clockwise else "2" if self.double else ""))

    def __eq__(self, move):
        if isinstance(move, (str, basestring)):
            return self.raw == move.upper()
        elif isinstance(move, Move):
            return self.raw == move.raw
        else:
            return False

    def __str__(self):
        return self.raw

    def __repr__(self):
        return str(self)

    def __ne__(self, move):
        return not self == move

    def __add__(self, move):
        if isinstance(move, (str, basestring)):
            return self + Move(move)
        elif move is None:
            return self
        elif isinstance(move, Move):
            if self.face != move.face:
                raise ValueError("Only same faces can be added")

            if self.clockwise and move.counterclockwise:
                return None
            if self.double and move.double:
                return None

            offset = (
                (self.clockwise + (self.double * 2) + (self.counterclockwise * 3)) +
                (move.clockwise + (move.double * 2) + (move.counterclockwise * 3))
            ) % 4

            if offset == 0:
                return None

            return Move(self.face + [None, "", "2", "'"][offset])
        else:
            raise ValueError("Unable to add %s and %s" %(self.raw, str(move)))

    def __mul__(self, times):
        offset = ((self.clockwise + (self.double * 2) + (self.counterclockwise * 3)) * times % 4)

        if offset == 0:
            return None

        return Move(self.face + [None, "", "2", "'"][offset])
