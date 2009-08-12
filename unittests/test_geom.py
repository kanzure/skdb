import unittest
import skdb

class TestGeom(unittest.TestCase):
    def init_interface(self):
        foo = skdb.Interface(name='foo', point=(1,1,1), orientation=[2,2,2], rotation=0)
        return foo
    def test_interface(self):
        '''this really probably shouldnt go here, but if interface screws up then so will everything else'''
        self.init_interface()
    def init_part(self):
        foo = self.init_interface()
        part = skdb.Part(name='unitcube') #, file='../pymates/models/block-with-hole.step')#too big, want 2x2x2
        #self.part.load_CAD()
        part.interfaces.append(foo)
        return part
    def test_part(self):
        '''ditto'''
        part = self.init_part()
    def test_translation(self):
        trsf1 = skdb.geom.gp_Trsf()
        transform1 = skdb.Transform(trsf1, description="a blank transformation")
        transform1.SetTranslation([0,0,0], [0,10,0])
        print transform1
        #now test it by throwing a point through it
