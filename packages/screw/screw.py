import skdb
from skdb import Part, Thread, Interface, Unit, UnitError
from string import Template

__author__ = "ben lipkowitz, bryan bishop"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "ben lipkowitz"
__email__ = 'no thank you, sir'
__status__ = "Development"

class Screw(Part):
    yaml_tag = "!screw"
    '''a screw by itself isn't a fastener, it needs a nut of some sort'''
    ##i suppose this stuff should go in a screws.yaml file or something, along with standard diameters
    proof_load = {#grade:load
        '1':'33ksi',
        '2':'55ksi',
        '3':'85ksi',
        '5':'85ksi',
        '7':'105ksi',
        '8':'120ksi',
        }
    tensile_strength = {#grade:load
        '1':'60ksi',
        '2':'74ksi',
        '3':'110ksi',
        '5':'120ksi',
        '7':'133ksi',
        '8':'150ksi',
        }
    def __init__(self, thread=None, length=None, grade="2"):
        '''length is defined as the distance from bottom of the head for all screws but 
        flat head and set screws which use the top of the head instead'''
        #thread.__init__()
        self.thread, self.length, self.grade = thread, length, grade
        if not (self.thread == None and self.length == None):
            if self.thread.length is None: self.thread.length = self.length
            assert self.length.compatible('m')

        thread_loosen = Interface("thread-loosen", part=self)
        thread_tighten = Interface("thread-tighten", part=self)
        compression_face = Interface("compression-face", part=self)
        torque_spline = Interface("torque-spline", part=self)
        if thread == None:
            thread = Thread(diameter='1mm',pitch='1rev/in')
            self.thread = thread
        #the following if should be commented out when skdb/core/threads.py Thread interfaces is fixed
        #if thread.interfaces == None or len(thread.interfaces) == 0:
        thread.interfaces = [thread_loosen, thread_tighten]
        if len(thread.interfaces) > 0:
            #if the thread already has interfaces with name "thread_loosen"/"thread_tighten", use them.
            thread_loosen = thread.interfaces[0] #FIXME: this is very, very wrong
            thread_tigthen = thread.interfaces[1] #FIXME too.
        self.interfaces = [thread_loosen, thread_tighten, compression_face, torque_spline]

        for (k,v) in {'pitch': 'rev/in', 'diameter': 'in', 'tensile_area': 'in^2'}.items():
            unit = getattr(self.thread, k)
            try:
                Unit(unit)
                assert (getattr(self.thread, k)).compatible(v)
            except UnitError, e:
                #ok it's not a Unit object
                #and instead a method in the Thread class
                res = unit()
                assert res.compatible(v)
        #note these tables vary from source to source; might want to check if it really matters to you
        
    def max_force(self):
        '''load screw can withstand without permanent set, in lbf'''
        s = Template('$area*$strength')
        string = s.safe_substitute(area=self.thread.tensile_area(), strength=Screw.proof_load[self.grade])
        return skdb.Unit(string).to('lbf') 
  
    def breaking_force(self):
        '''load screw can withstand without breaking, in lbf'''
        s = Template('$area*$strength')
        string = s.safe_substitute(area=self.thread.tensile_area(), strength=Screw.tensile_strength[self.grade])
        return skdb.Unit(string).to('lbf')
