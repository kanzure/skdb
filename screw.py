import skdb
from string import Template

class Screw(skdb.Component):
    yaml_tag = "!screw"
    '''a screw by itself isn't a fastener, it needs a nut of some sort'''
    ##i suppose this stuff should go in a screws.yaml file or something, along with standard diameters
    proof_load = {#grade:load, proof load is defined as load bolt can withstand without permanent set
        '1':'33ksi',
        '2':'55ksi',
        '3':'85ksi',
        '5':'85ksi',
        '7':'105ksi',
        '8':'120ksi',
        }
    tensile_strength = {#grade:load, tensile strength is defined as load bolt can withstand without breaking
        '1':'60ksi',
        '2':'74ksi',
        '3':'110ksi',
        '5':'120ksi',
        '7':'133ksi',
        '8':'150ksi',
        }
    def __init__(self, thread, length, grade="2"):
        '''length is defined as the distance from bottom of the head for all screws but 
        flat head and set screws which use the top of the head instead'''
        #thread.__init__()
        self.thread, self.length, self.grade = thread, length, grade
        if self.thread.length is None: self.thread.length = self.length
        #note these tables vary from source to source; might want to check if it really matters to you
        
    def max_force(self):
        s = Template('$area*$strength')
        string = s.safe_substitute(area=self.thread.tensile_area(), strength=Screw.proof_load[self.grade])
        return skdb.Unit(string).to('lbf') 
  
    def breaking_force(self):
        s = Template('$area*$strength')
        string = s.safe_substitute(area=self.thread.tensile_area(), strength=Screw.tensile_strength[self.grade])
        return skdb.Unit(string).to('lbf')
