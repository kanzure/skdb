#!/usr/bin/python
'''
python + legos

Bryan Bishop (<kanzure@gmail.com>)
2009-07-29

This program is free software.
'''
import unittest

class mate:
    def __init__(self, part1interface, part2interface):
        self.part1interface = part1interface
        self.part2interface = part2interface
        #part1.mate = self
        #part2.mate = self
    def apply(self):
        self.part1interface.mate = self
        self.part2interface.mate = self
        return
    def __repr__(self):
        return "mate(%s, %s)" % (self.part1interface.part.name, self.part2interface.part.name)

class mates:
    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2
    def options(self):
        #return a list of possible mates
        local_options = []
        for hole in self.part1.holes:
            for peg in self.part2.pegs:
                #do something
                if not hole.mate and not peg.mate:
                    local_options.append(mate(hole, peg))
        for peg in self.part1.pegs:
            for hole in self.part2.holes:
                #do something
                if not hole.mate and not peg.mate:
                    local_options.append(mate(hole,peg))
        return local_options

class interface_mates():
    def __init__(self, interface1, interface2):
        self.interface1 = interface1
        self.interface2 = interface2
    def options(self):
        return "not implemented"

class interface:
    def __init__(self, part):
        self.mate = None
        self.part = part
        pass
    def mates(self, other_interface):
        return interface_mates(self, other_interface).options()

class hole(interface):
    pass

class peg(interface):
    pass

class lego:
    def __init__(self, name, num_pegs=4, num_holes=1):
        self.name = name
        self.holes = []
        self.pegs = []
        for each in range(num_holes):
            new_hole = hole(self)
            self.holes.append(new_hole)
        for each in range(num_pegs):
            new_peg = peg(self)
            self.pegs.append(new_peg)
    def mates(self, part):
        #how many options are there for different pegs and holes?
        possibilities = mates(self, part).options()
        return possibilities

class TestLego(unittest.TestCase):
    def test_lego(self):
        brick = lego("brick", num_pegs=8, num_holes=2)
        brick2 = lego("brick2", num_pegs=4, num_holes=1)
        print brick.mates(brick2)
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
