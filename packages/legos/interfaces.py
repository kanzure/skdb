#!/usr/bin/python
from skdb.pymates import Interface

class Peg(Interface):
    def compatible(self, other):
        if isinstance(other, Hole):
            if not other.mated:
                return True
        else: return False
    def __repr__(self):
        if not hasattr(self,"part") or self.part == None:
            part_name = "None"
        else:
            part_name = self.part.name
        return "Peg(part=%s,id=%s)" % (part_name, self.identifier)

class Hole(Interface):
    def compatible(self, other):
        if isinstance(other, Peg):
            if not other.mated:
                return True #ok so type based checking sucks. wah.
        else: return False
    def __repr__(self):
        if not hasattr(self,"part") or self.part == None:
            part_name = "None"
        else:
            part_name = self.part.name
        return "Hole(part=%s,id=%s)" % (part_name, self.identifier)

