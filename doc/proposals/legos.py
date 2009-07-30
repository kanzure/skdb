#!/usr/bin/python
'''
python + legos

Bryan Bishop (<kanzure@gmail.com>)
2009-07-29

This program is free software.
'''
import unittest

class Mate:
    def __init__(self, interface1, interface2):
        assert hasattr(interface1, 'mated')
        assert hasattr(interface2, 'mated')
        self.interface1 = interface1
        self.interface2 = interface2
    def apply(self):
        self.interface1.mated = self
        self.interface2.mated = self
        return
    def __repr__(self):
        return "mate(%s, %s)" % (self.interface1.part.name, self.interface2.part.name)

def options(interface, parts):
    '''what can this interface connect to?'''
    parts = set(parts) #yay sets!
    if interface.part in parts: parts.remove(interface.part) #unless it's really flexible
    rval = set()
    for part in parts:
        for i in part.interfaces:
            if i.compatible(interface) and interface.compatible(i):
                rval.add(Mate(i, interface))
    return rval

class Interface:
    def __init__(self, part):
        self.mated = None
        self.part = part

class Hole(Interface):
    def compatible(self, other):
        if isinstance(other, Peg): 
            if not other.mated:
                return True #ok so type based checking sucks. wah.
        else: return False

class Peg(Interface):
    def compatible(self, other):
        if isinstance(other, Hole):
            if not other.mated:
                return True
        else: return False

class Lego:
    def __init__(self, name, num_pegs=0, num_holes=0):
        self.name = name
        self.interfaces = []
        for each in range(num_holes):
            new_hole = Hole(self)
            self.interfaces.append(new_hole)
        for each in range(num_pegs):
            new_peg = Peg(self)
            self.interfaces.append(new_peg)
    def mates(self, part):
        #how many options are there for different pegs and holes?
        possibilities = Mates(self, part).options()
        return possibilities

class TestLego(unittest.TestCase):
    def test_lego(self):
        brick1 = Lego("brick1", num_pegs=4, num_holes=2)
        brick2 = Lego("brick2", num_pegs=2, num_holes=1)
        brick3 = Lego("brick3", num_holes=3)
        brick4 = Lego("brick4", num_pegs=4)
        #print brick1.interfaces[0].__class__.__name__
        print options(brick1.interfaces[0], [brick1, brick2, brick3, brick4])
        pass
    def test_interface(self):
        pass
    def test_hole(self):
        pass
    def test_peg(self):
        pass
    def test_mates(self):
        pass
    def test_mate(self):
        pass

if __name__ == '__main__':
    unittest.main()
