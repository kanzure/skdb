#from skdb import Unit, Package
import yaml
from string import Template
from skdb import Unit

#used to inherit from skdb.Package but that no longer works?
class Thread(yaml.YAMLObject):
    yaml_tag = '!thread'
    '''examples: ballscrews, pipe threads, bolts - NOT any old helix'''
    def __init__(self, diameter, pitch, gender='male', length=None, form="UN"):
        self.diameter, self.pitch, self.form = Unit(diameter), Unit(pitch), form
        self.gender, self.length, self.form = gender, length, form
        #wtf were we thinking?
        self.interfaces = [
                (self.pitch_diameter, 'in'), # conversion function .. so this is wrong.
                (self.minor_diameter, 'in'),
                (self.clamping_force, 'lbf')]
    def pitch_diameter(self):
        assert self.form=="UN" and Unit(self.pitch).compatible('rev/inch'), "this only works for triangular threads atm"
        s = Template('($diameter)-0.6495919rev/($pitch)') #machinery's handbook 27ed page 1502
        string = s.safe_substitute(diameter=self.diameter, pitch=self.pitch)
        return Unit(string).to('in')
  
    def minor_diameter(self):
        assert self.form=="UN" and Unit(self.pitch).compatible('rev/inch'), "this only works for triangular threads atm"
        s = Template('($diameter)-1.299038rev/($pitch)')  #machinery's handbook 27ed page 1502
        string = s.safe_substitute(diameter=self.diameter, pitch=self.pitch)
        return Unit(string).to('in')
    
    def clamping_force(self, torque, efficiency=0.1):
        s = Template('($torque)*($pitch)*$efficiency')
        string = s.safe_substitute(torque=torque, pitch=self.pitch, efficiency=efficiency) #fill in template keywords
        force = Unit(string).to('lbf') #I guess this looks better than kg*m/s^2, but there should be a default Units setting somewhere
        return force
  
    def tensile_area(self):
        assert Unit(self.pitch).compatible('rev/inch')
        s = Template('pi/4*(($Dm+$Dp)/2)^2') #machinery's handbook 27ed page 1502 formula 9 "tensile-stress area of screw thread"
        string = s.safe_substitute(Dm=self.minor_diameter(), Dp=self.pitch_diameter())
        return Unit(string).to('in^2')
  #max torque requires finding the combined "von mises" stress, given on page 1498
  #because the screw body will twist off as a combination of tensile and torque shear loads
