import unittest, math
from skdb.geom import *
from skdb import load_package, Package, close_enough

#well, i dunno how to verify these except by looking
class TestGui(unittest.TestCase):
    def test_coordinate_arrows(event=None):
        '''should draw a dandelion puff of flags'''
        for a in 0, 1, -1:
            for b in 0, 1, -1:
                for c in 0, 1, -1:
                    try: coordinate_arrow([a, b, c], flag=True)
                    except RuntimeError:
                        pass

    def test_transformation(event=None):
        '''should draw 4 colored bricks rotated around Z'''
        brick = get_brick()
        point = [10,10,10]
        colors = [ 'WHITE', 'BLUE', 'RED', 'GREEN', 'YELLOW',
                        'WHITE', 'BLUE', 'RED', 'GREEN', 'YELLOW',
                        'WHITE', 'BLUE', 'RED', 'GREEN', 'YELLOW']
        #testfile = '20vert.yaml'
        #testfile = '60horz.yaml'
        #testfile = '60twist.yaml'
        #testfile = '60all.yaml'
        #testfile = '90vert.yaml'
        #testfile = '90horz.yaml'
        testfile = '90twist.yaml'
        for (i, color) in zip(skdb.load(open(testfile)), colors):
            trsf = build_trsf(i.point, i.x_vec, i.y_vec)
            display.DisplayColoredShape(BRepBuilderAPI_Transform(brick._shapes[0], trsf).Shape(), color)


if __name__ == "__main__":
    unittest.main()