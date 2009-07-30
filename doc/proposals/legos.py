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
        return "Mate(%s, %s)" % (self.interface1, self.interface2)

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
    def __init__(self, part, hermaphroditic=False):
        self.mated = None
        self.part = part
        self.identifier = None #part's #identifier-th/st Interface
        self.hermaphroditic = hermaphroditic
    def compatible(self, other):
        '''really really generic: it's compatible if it's the first one'''
        if not other.mated:
            return True
        else: return False
    def __repr__(self):
        return "Interface(part=%s,id=%d)" % (self.part.name, self.identifier)

class Hole(Interface):
    def compatible(self, other):
        if isinstance(other, Peg): 
            if not other.mated:
                return True #ok so type based checking sucks. wah.
        else: return False
    def __repr__(self):
        return "Hole(part=%s,id=%s)" % (self.part.name, self.identifier)

class Peg(Interface):
    def compatible(self, other):
        if isinstance(other, Hole):
            if not other.mated:
                return True
        else: return False
    def __repr__(self):
        return "Peg(part=%s,id=%s)" % (self.part.name, self.identifier)

class Lego:
    def __init__(self, name, num_pegs=0, num_holes=0):
        self.name = name
        self.interfaces = []
        for each in range(num_holes):
            new_hole = Hole(self)
            new_hole.identifier = len(self.interfaces)
            self.interfaces.append(new_hole)
        for each in range(num_pegs):
            new_peg = Peg(self)
            new_peg.identifier = len(self.interfaces)
            self.interfaces.append(new_peg)
    def pegs(self):
        '''returns a list of peg interfaces that this Lego has'''
        results = []
        for each in self.interfaces:
            if each.__class__.__name__ == "Peg":
                results.append(each)
        return results
    def holes(self):
        '''returns a list of hole interfaces that this Lego has'''
        results = []
        for each in self.interfaces:
            if each.__class__.__name__ == "Hole":
                results.append(each)
        return results
    def __repr__(self):
        return "Lego(name=%s, num_pegs=%d, num_holes=%d)" % (self.name, len(self.pegs()), len(self.holes()))

def has_no_peg_peg_hole_hole(results):
    '''returns True if there is no peg-to-peg and no hole-to-hole connections in a list of potential Mate objects'''
    result = True
    for each in results:
        #this check is only valid for pegs and holes
        #other connectors might be hermaphrodites
        if each.interface1.__class__.__name__ == each.interface2.part.__class__.__name__ and not each.interface1.hermaphroditic:
            result = False
    return result

class TestLego(unittest.TestCase):
    def test_lego(self):
        brick1 = Lego("brick1", num_pegs=4, num_holes=2)
        self.assertTrue(len(brick1.interfaces) == 6)
        self.assertTrue(len(brick1.pegs()) == 4)
        self.assertTrue(len(brick1.holes()) == 2)
        brick2 = Lego("brick2", num_pegs=2, num_holes=1)
        brick3 = Lego("brick3", num_holes=3)
        brick4 = Lego("brick4", num_pegs=4)
        brick5 = Lego("brick5", num_pegs=0, num_holes=0)
        #print brick1.interfaces[0].__class__.__name__
        bricklist = [brick1, brick2, brick3, brick4, brick5]

        results = options(brick1.interfaces[0], bricklist)
        #print results
        
        self.assertTrue(has_no_peg_peg_hole_hole(results))

        #have to convert a set to a list to get to the elements
        list(results)[0].apply()
        #there should be no more options involving brick1's interface0
        self.assertTrue(len(options(brick1.interfaces[0], bricklist)) == 0)

        results2 = options(brick1.interfaces[1], bricklist)
        #print results2

        self.assertTrue(has_no_peg_peg_hole_hole(results2))
        #list(results2)[0].apply()

        pass
    def test_interface(self):
        pass
    def test_hole(self):
        pass
    def test_peg(self):
        pass
    def test_mate(self):
        pass

if __name__ == '__main__':
    unittest.main()
