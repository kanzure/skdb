#!/usr/bin/python

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

