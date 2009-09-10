#for volume interference
from OCC.BRepGProp import *
from OCC.GProp import *

def shape_volume(shape): #should probably be a method of Shape
    '''returns the volume of a TopoDS_Shape or Shape'''
    tmp = GProp_GProps()
    BRepGProp().VolumeProperties(shape, tmp)
    volume = tmp.Mass()
    return volume

def assembly_volume_estimate(parts):
    '''returns the volume of an assembly given a list of parts
    returns a sum of the volumes of each part
    does not consider interference (see assembly_volume_actual)'''
    total_volume = 0
    for part in parts:
        total_volume += part.volume()
    return total_volume

def assembly_volume_actual(parts):
    '''computes the actual volume of an assembly
    interference between two parts tends to decrease the volume'''
    #total_volume = assembly_volume_estimate(parts)
    #box = BRepPrimAPI_MakeBox(Point(0,0,0), Point(1,1,1))
    shape = None
    #FIXME you should actually set no initial shape, and then make an initial shape in the for loop if there isn't one already
    #shape = TopoDS_Shape() #start with nothing
    for part in parts:
        if shape is None:
            shape = part.shapes[0]
        else:
            #is it ok to fuse non-touching objects into the same shape?
            tmp_shape = BRepAlgoAPI_Fuse(shape, part.shapes[0])
            shape = tmp_shape.Shape()
    return shape_volume(shape)

def estimate_interference_volume(parts):
    '''figures out how much volume should be missing from assembly_volume_actual compared to assembly_volume_estimate
    not particularly special or enlightening'''
    total_expected_missing_volume = 0
    interfaces = []
    for part in parts:
        for interface in part.interfaces:
            if interface.connected == True and interface not in interfaces:
                #it's important to go over the interfaces as many times as they are mated
                #because complementary interfaces should have complementary (positive, negative) volumes
                #thus the total resulting volume should be zero if everything has a perfect fit

                #if you disagree:
                ##no_go = False #it's ok
                ##mates = interface.connected
                ##for mate in mates:
                ##    if mate in interfaces:
                ##        no_go = True #not ok, it's already considered
                ##if not no_go:

                total_expected_missing_volume += interface.volume
                interfaces.append(interface) #so we don't count it twice
    return total_expected_missing_volume

#this is the one you want to use after adding a part to an assembly
def estimate_collision_existence(parts, threshold=-1):
    '''determines whether or not there is an illegal collision in the assembly.
    threshold determines how much leeway you're willing to give the assembly. 0 means nothing should be out of place.
    uses estimate_interference_volume, assembly_volume_actual, assembly_volume_estimate'''
    assembly_volume = assembly_volume_estimate(parts)
    estimated_interference = estimate_interference_volume(parts)
    better_estimate = assembly_volume - estimated_interference
    actual_volume = assembly_volume_actual(parts)
    difference = actual_volume - better_estimate
    if diff_diff >= threshold: return True
    else: return False
    print "estimated volume = ", estimated
    print "estimated_interference = ", estimated_interference
    print "difference = ", difference
    print "threshold = ", threshold
    if difference >= threshold:
        return True
    else:
        return False

def common_volume(part1, part2):
    '''returns the volume of the intersection of two parts'''
    shape1 = part1.shapes[0]
    shape2 = part2.shapes[0]
    common = BRepAlgoAPI_Common(shape1, shape2).Shape() #this takes too long

    tmp = GProp_GProps()
    BRepGProp().VolumeProperties(common, tmp)
    volume = tmp.Mass()
    return volume 

def part_collision(part1, part2, threshold=0.0):
    '''determines whether or not two parts are colliding, given a threshold of maximum allowable intersection
    returns True or False'''
    volume = common_volume(part1, part2)
    if volume > threshold: return True
    else: return False

def _connection_interference(self, threshold=0.0): #call this as a method please
    '''determines whether or not a connection has a geometric collision (only for the two mating parts) within a threshold
    returns True or False'''
    part1 = self.interface1.part
    part2 = self.interface2.part
    #the threshold should be the volume of interface1 + interface2 if we can isolate those regions
    return part_collision(part1, part2, threshold=threshold)
Connection.interference = _connection_interference

def _volume(self):
    '''determines the volume of the shape'''
    tmp = GProp_GProps()
    BRepGProp().VolumeProperties(self.shapes[0], tmp)
    vol = tmp.Mass()
    return vol
Part.volume = _volume

def deep_part_collider(parts):
    '''given a list of parts, checks whether or not any of them geometrically overlap
    returns a list of triples in the form: (volume, part1, part2) where volumetric interference was found'''
    errors = []
    for part in parts:
        for part2 in parts:
            volume = common_volume(part1, part2)
            if volume > 0:
               errors.append((volume, part1, part2))
    return errors