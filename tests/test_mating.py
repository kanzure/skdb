import unittest, math
from skdb.geom import *
from skdb import load_package, Package, close_enough
class TestMating(unittest.TestCase):
    def test_part_mating(self):
        pass
        lego_pack = Package("lego")
        brick1 = deepcopy(lego_pack.parts[0])
        brick2 = deepcopy(lego_pack.parts[0])
        #they should be the same thing so far
        #self.assertTrue(brick1 == brick2)
        options = brick1.options([brick2])
        #select one of the Connection instances to test with
        selected = options[1]
        selected.connect()
        blah = mate_connection(selected)
        #print blah #TopoDS shape (is this useful?)
        #not sure what to do with that. brick2 has already been transformed, brick2.transformation = some new transformation. 
        self.assertNotEqual(brick1.transformation, brick2.transformation)
        self.assertNotEqual(brick1, brick2)
        
    def test_lego_volume(self):
        pack = Package("lego")
        round_brick_volume = shape_volume(pack.parts[0].shapes[0])
        self.assertEqual(round(round_brick_volume), 865)

        brick1 = deepcopy(pack.parts[0])
        brick2 = deepcopy(pack.parts[0])
        options = brick1.options(brick2)
        option = options[0]
        option.connect()
        print estimate_collision_existence([brick1, brick2])


if __name__ == "__main__":
    unittest.main()