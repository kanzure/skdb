#!/usr/bin/python
'''this file more or less describes the grammar used for constructing things out of Lego
not done. see http://mr-bucket.co.uk/GLIDE/LCD_File_Format.html#Implimentation
for part examples see http://guide.lugnet.com/partsref/search.cgi?q=XXXX
or http://img.lugnet.com/ld/XXXX.gif
'''
from skdb import Interface

class Joint:
    '''should pull in some kinematics from elsewhere; PyODE?'''
    pass

class SphericalJoint(Joint): pass

class RevoluteJoint(Joint): pass

class PrismaticJoint(Joint): pass

class GearJoint(Joint): pass

class Discrete:
    '''allows only a certain set of values'''
    pass

class Feature(Interface):
    def __repr__(self):
        try: part_name = self.part.name
        except AttributeError: part_name = None
        
        try: name = self.name
        except AttributeError: name = None
        
        return "%s(part=%s,name=%s)" % (self.__class__.__name__, part_name, name)

class PressFit(Feature):
    '''this should probably link up with some other class'''
    pass

class SnapFit(Feature):
    '''same as PressFit but with no friction, and a restorative force'''
    pass

class Edge(Feature, PrismaticJoint):
    def __init__(self):
        self.complement=[Edge, Tire]

class Stud(RevoluteJoint, PressFit):
    def __init__(self):
        self.complement = AntiStud
        self.example = 3005
        
class AntiStud(RevoluteJoint, PressFit):
    def __init__(self):
        self.complement = Stud
        self.example = 3005
        
class SingleAntiStud(AntiStud):
    #self.example = 3062a
    pass #something about fitting between 4 studs as well

class DuploStud(PressFit):
    def __init__(self):
        self.complement = DuploAntiStud

class DuploAntiStud(PressFit):
    def __init__(self):
        self.complement = DuploStud

class Rod(RevoluteJoint, PressFit):
    def __init__(self):
        self.complement = Claw
        self.example = 3957
        
class Claw(RevoluteJoint, PressFit):
    def __init__(self):
        self.complement = Rod
        self.example = 6019

class Pin(RevoluteJoint, SnapFit):
    def __init__(self):
        self.complement = PinHole
        self.example = 3673

class PinHole(RevoluteJoint, PrismaticJoint, SnapFit, PressFit): #egad
    def __init__(self):
        self.complement = Pin
        self.example = 3700

class MiniPin(Pin):
    def __init__(self):
        self.complement = MiniPinHole
        self.example = 4488

class MiniPinHole(SnapFit, RevoluteJoint):
    def __init__(self):
        self.complement = MiniPin
        self.example = None #find one then!

class ShortPin(SnapFit, RevoluteJoint):
    def __init__(self):
        self.complement = PlateHole
        self.example = 'that step file pin0 or whatever'

class PlateHole(PinHole):
    '''add something about stacking two plates is compatible with Pin'''
    def __init__(self):
        self.complement  = Shortpin
        self.example = '3709b'

class TowBall(SphericalJoint, SnapFit):
    def __init__(self):
        self.complement = TowBallSocket
        self.example = 3184

class TowBallSocket(SphericalJoint, SnapFit):
    def __init__(self):
        self.complement = TowBall
        self.example = 3183

class Magnet(Feature):
    '''do magnets have the same stubAxle as wheels?'''
    def __init__(self):
        self.complement = Magnet
        self.example = 73092

class WheelHolder(RevoluteJoint, SnapFit):
    '''is this the same as 2607?'''
    def __init__(self):
        self.complement = WheelAxle
        self.example = 8

class WheelAxle(RevoluteJoint, SnapFit ): #SnapFit?
    def __init__(self):
        self.complement = WheelHolder
        self.example = 3464

class WheelRim(PressFit):
    def __init__(self):
        self.complement = TireInner
        self.example = 3464

class TireInner(PressFit):
    def __init__(self):
        self.complement = WheelRim

class TireOuter(GearJoint, Feature):
    def __init__(self):
        self.complement = Edge

class Hinge(SnapFit, RevoluteJoint):
    '''blah blah blah flexible kinematic constraint stuff goes here'''
    pass

class ElevationHingeHolder(Hinge):
    def __init__(self):
        self.complement = ElevationHinge
        self.example = 3937

class ElevationHinge(Hinge):
    def __init__(self):
        self.complement = ElevationHingeHolder
        self.example = 3938

class FlatHinge2(Hinge):
    def _init__(self):
        self.complement = FlatHinge3
        self.example = 4276
        
class FlatHinge3(Hinge):
    def __init__(self):
        self.complement = FlatHinge2
        self.example = 2452

class WideHingeM(Hinge):
    def __init__(self):
        self.complement = WideHingeF
        self.example = 4315

class WideHingeF(Hinge):
    def __init__(self):
        self.complement = WideHingeM
        self.example = 2872

class TrailerHingeM(Hinge):
    def __init__(self):
        self.complement = [TrailerHingeF, Claw]
        self.example = 3639

class TrailerHingeF(Hinge):
    def __init__(self):
        self.complement = [TrailerHingeM, Rod]
        self.example = 3640

class RoundHinge2(Hinge):
    def __init__(self):
        self.complement = RoundHinge3
        self.example = 6048

class RoundHinge3(Hinge):
    def __init__(self):
        self.complement = RoundHinge2
        self.example = 6217

class LockingHinge1(Hinge, Discrete):
    '''sorta iffy on these as i've never seen them'''
    def __init__(self):
        self.complement = LockingHinge2
        self.example = 30364
    
class LockingHinge2(Hinge, Discrete):
    def __init__(self):
        self.complement = LockingHinge1
        self.example = 30365

class Axle(RevoluteJoint, Feature, PrismaticJoint):
    def __init__(self):
        self.complement = [AntiAxle, PinHole]
        self.example = 3705

class AntiAxle(Feature, Discrete, PrismaticJoint):
    def __init__(self):
        self.complement = Axle
        self.example = 32064
        self.angle = rev/4

class ToothedJoint(Feature, RevoluteJoint, Discrete):
    '''there are 16 possible mates between two ToothedJoint interfaces'''
    def __init__(self):
        self.complement = ToothedJoint
        self.example = 4263
        self.angle = rev/16 

class MinifigNeck(Stud):
    def __init__(self):
        self.complement = [MinifigNeckHole, AntiStud]
        self.example = 973

class MinifigNeckHole(AntiStud):
    def __init__(self):
        self.complement = [MinifigNeck, Stud]
        self.example = 'standard lego head'

class MinifigBackpack(PressFit): #not actually a PressFit; it's loose
    def __init__(self):
        self.complement = MinifigTorso
        self.example = 'wtf srsly where is it'

class MinifigTorso(PressFit): #not actually a PressFit; it's loose
    '''for backpacks and armor and so on'''
    def __init__(self):
        self.complement = MinifigBackpack
        self.example = 973

class MinifigWrist(PressFit, RevoluteJoint):#is this a snap fit?
    def __init__(self):
        self.complement = MinifigWristHole
        self.example = 983

class MinifigWristHole(PressFit, RevoluteJoint):#is this a snap fit?
    def __init__(self):
        self.complement = MinifigWrist
        self.example = 976

class MinifigShoulder(PressFit, RevoluteJoint):
    def __init__(self):
        self.complement = MinifigShoulderHole
        self.example = 976

class MinifigShoulderHole(PressFit, RevoluteJoint):
    def __init__(self):
        self.complement = MinifigShoulder
        self.example = 973

class MinifigWaist(PressFit):
    def __init__(self):
        self.complement = MinifigHip
        self.example = 973

class MinifigHipStud(PressFit):
    '''does this really not interface with anything else?'''
    def __init__(self):
        self.complement = MinifigWaist
        self.example = 970

class MinifigLegPin(PressFit, RevoluteJoint):
    def __init__(self):
        self.complement = MinifigLegHole
        self.example = 970

class MinifigLegHole(PressFit, RevoluteJoint):
    def __init__(self):
        self.complement = MinifigLegPin
        self.example = 971



