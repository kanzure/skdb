import unittest, math
from skdb.geom import *

def point_trsf(point1, transform):
    '''point_trsf(point1, transform) -> [x,y,z]'''
    point1 = safe_point(point1)
    result_pnt = point1.Transformed(transform)
    return usable_point(result_pnt)

class TestGeom(unittest.TestCase):
    def init_interface(self):
        foo = Interface(name='foo', point=(1,1,1), orientation=[2,2,2], rotation=0)
        return foo
    def test_interface(self):
        '''this really probably shouldnt go here, but if interface screws up then so will everything else'''
        self.init_interface()
    def init_part(self):
        foo = self.init_interface()
        part = Part(name='unitcube') #, file='../pymates/models/block-with-hole.step')#too big, want 2x2x2
        #self.part.load_CAD()
        part.interfaces.append(foo)
        return part
    def test_part(self):
        '''ditto'''
        part = self.init_part()
    def test_point(self):
        point = Point(1,2,3)
        point = Point([1,2,3])
    def test_point_eq(self):
        self.assertEqual(geom.Point(0,0,0), geom.Point(0,0,0))
        self.assertEqual(geom.Point(0,0,1e-9), geom.Point(0,0,0))
        #not equals?
    def test_point_yaml(self):
        import yaml
        self.assertEqual(yaml.dump(geom.Point(0, 0, 0.00000001)), "!point ['0.0', '0.0', 1e-08]\n")
        self.assertEqual(yaml.dump(geom.Point(0, 0, 0.000000000000001)), "!point ['0.0', '0.0', '0.0']\n")
        self.assertEqual(yaml.load("!point ['0.0', '0.0', 1e-08]"), geom.Point(0, 0, 0.00000001))
        self.assertEqual(yaml.load("!point [0.0, 0.0, 1e-08]"), geom.Point(0, 0, 0.00000001))    
        self.assertEqual(yaml.dump(geom.Point(0,0,1e-8)), "!point ['0.0', '0.0', 1e-08]\n")
    def test_vec(self):
        vec = Vector(1,2,3)
        vec = Vector([1,2,3])
    def test_vec_eq(self):                                                                         
        self.assertEqual(geom.Vector(0,0,0), geom.Vector(0,0,0))
        self.assertEqual(geom.Vector(0,0,1e-9), geom.Vector(0,0,0)) 
        #not equals? 
    def test_vec_yaml(self):
        import yaml
        self.assertEqual(yaml.dump(geom.Vector(0, 0, 0.00000001)), "!vector ['0.0', '0.0', 1e-08]\n")
        self.assertEqual(yaml.load("!vector ['0.0', '0.0', 1e-08]"), geom.Vector(0, 0, 0.00000001))
    def test_dir(self):
        dir = Direction(1,2,3)
    def test_translation(self):
        '''test translation'''
        y_displacement = 10
        y_init = 5
        point = [0,y_init,0]
        trsf1 = translation(point1=[0,0,0], point2=[0,y_displacement,0])
        result_point = point_trsf(point, trsf1)
        if not y_displacement == 0:
            self.assertFalse(result_point == point)
        self.assertTrue(result_point == [point[0],point[1]+y_displacement,point[2]])
        #TODO: test translation(vector)
    def test_rotation(self):
        '''test rotation'''
        #test rotation(rotation_pivot_point, direction, angle)
        rotation_pivot_point = [0,0,0]
        direction = [0, 0, 1]
        angle = math.pi
        point = [5,0,0]
        trsf1 = rotation(rotation_pivot_point=rotation_pivot_point, direction=direction, angle=angle)
        result_point = point_trsf(point, trsf1)
        for n in range(3):
            self.assertTrue(result_point[n] - [-5,0,0][n] < Precision().Confusion()) #idk the real answer
        #TODO: test rotation(gp_Ax1, angle)
    def test_transform(self):
        '''transforms should not be stored in yaml'''
        pass
    def test_stacked_transforms(self):
        pass
    def test_rotation_transform(self):
        '''test Rotation (not rotation())'''
        pass
    def test_translation_transform(self):
        '''test Translation (not translation())'''
        pass
    #now some unit tests for part mating

if __name__ == "__main__":
    unittest.main()
