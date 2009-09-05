from __future__ import division
#from skdb import Unit, Package
import yaml
from string import Template
from skdb import Unit
import skdb

#used to inherit from skdb.Package but that no longer works?
class Thread(yaml.YAMLObject): #inherit from Helix?
    yaml_tag = '!thread'
    '''examples: ballscrews, pipe threads, bolts - NOT any old helix'''
    def __init__(self, diameter, pitch, gender='male', length=None, handedness='right', starts=1):
        self.diameter, self.pitch = Unit(diameter), Unit(pitch)
        self.gender, self.length, self.handedness = gender, length, handedness
        self.starts = starts #number of threads per turn
        #pitch is distance from the peak of one thread to the peak of the next
        self.lead = self.pitch * self.starts #Lead is the axial advance of a helix for one complete turn
        
        #TODO delete crap below
        self.interfaces = [
                (self.pitch_diameter, 'in'), # conversion function .. so this is wrong.
                (self.minor_diameter, 'in'),
                (self.clamping_force, 'lbf')]
        
    def pitch_diameter(self):
        assert self.form=="UN" and Unit(self.pitch).compatible('mm/rev'), "this only works for triangular threads atm"
        s = Template('($diameter)-0.6495919rev*($pitch)') #machinery's handbook 27ed page 1502
        string = s.safe_substitute(diameter=self.diameter, pitch=self.pitch)
        return Unit(string).to('in')
  
    def minor_diameter(self):
        assert self.form=="UN" and Unit(self.pitch).compatible('mm/rev'), "this only works for triangular threads atm"
        s = Template('($diameter)-1.299038rev*($pitch)')  #machinery's handbook 27ed page 1502
        string = s.safe_substitute(diameter=self.diameter, pitch=self.pitch)
        return Unit(string).to('in')
    
    def clamping_force(self, torque, efficiency=0.1):
        s = Template('($torque)*($pitch)*$efficiency')
        string = s.safe_substitute(torque=torque, pitch=self.pitch, efficiency=efficiency) #fill in template keywords
        force = Unit(string).to('lbf') #I guess this looks better than kg*m/s^2, but there should be a default Units setting somewhere
        return force
  
    def tensile_area(self):
        assert Unit(self.pitch).compatible('mm/rev')
        s = Template('pi/4*(($Dm+$Dp)/2)^2') #machinery's handbook 27ed page 1502 formula 9 "tensile-stress area of screw thread"
        string = s.safe_substitute(Dm=self.minor_diameter(), Dp=self.pitch_diameter())
        return Unit(string).to('in^2')
  #max torque requires finding the combined "von mises" stress, given on MH27 page 1498
  #because the screw body will twist off as a combination of tensile and torque shear loads

class BoltThread(Thread):
    '''thread found on common nuts and bolts'''
    yaml_tag = '!UN'
    included_angle = Unit('60 degrees')
    icon = skdb.package_file('threads', 'ISO_and_UTS_Thread_Dimensions.svg')
    def __init__(self, diameter, pitch):
        if diameter.compatible('inch'): self.diameter = diameter
        #TODO note to self for future: skdb.parameter('diameter', 'inch')
        else: raise skdb.UnitError, 'diameter must be a distance. got:'+str(diameter)
        if pitch.compatible('rev/inch'): self.pitch = Unit('1')/pitch
        elif pitch.compatible('mm/rev'): self.pitch = pitch
        #TODO skdb.parameter('pitch', 'mm/rev')
        else: raise skdb.UnitError, "thread pitch must be a ratio of angle and distance. got:"+str(pitch)

    #is it worth worring about the distinction between UN and UNR?
    def root_radius(self):
        pass #something like .108P to .140P, also min and max radii

class ISO_Thread(BoltThread):
    '''thread found on metric nuts and bolts'''
    yaml_tag = '!thread_ISO'
    urls = ['http://en.wikipedia.org/wiki/ISO_metric_screw_thread']
    _diam_regex = '(?P<diam>M\d+)'
    _pitch_regex = '(?P<pitch>\s*\d+(\.\d+)?)'
    preferred_sizes = {1:0.25, 1.2:0.25, 1.6:0.35, 2:0.4, 2.5:0.45, 3:0.5, 4:0.7, 5:0.8, 6:1, 8:1.25, 10:1.5, 12:1.75, 16:2, 20:2.5, 24:3, 30:3.5, 36:4, 42:4.5, 48:5, 56:5.5, 64:6}
    second_choice = {1.4:0.3, 1.8:0.35, 3.5:0.6, 7:1, 14:2, 18:2.5, 22:2.5, 27:3, 33:3.5, 39:4, 45:4.5, 52:5, 60:5.5}

class ISO_Fine_Thread(ISO_Thread):
    '''thread found on some metric nuts and bolts'''
    #not sure about i.e. M10-1 vs M10-1.25 (10, 12, 18, 22)
    preferred_sizes = {8:1, 10:1.25, 12:1.5, 16:1.5, 20:2, 24:2, 30:2, 36:3, 42:3, 48:3, 56:4, 64:4}
    second_choice = {14:1.5, 18:2, 22:2, 27:3, 33:2, 39:3, 45:3, 52:4, 60:4}

class ISO_Extra_Fine_Thread(ISO_Thread):
    #this can't be complete..
    prefered_sizes = {10:1, 12:1.25, 20:1.5}
    second_choice = {18:1.5, 22:1.5}

#i hate this, i wish it were a @staticmethod of UN_Thread, but then UN_Thread can't call it
def numbered_thread_diameter(size):
    '''a #2 thread has a major diameter of 0.086".'''
    if size == '00': size = -1
    if size == '000': size = -2
    return 0.060+0.013*int(size)

_n = numbered_thread_diameter

class UN_Thread(BoltThread):
    '''base class for constructing UN thread series. don't use.'''
    yaml_tag = '!thread_UN'
    preferred_sizes = { _n(0):'#0',
                        _n(2):'#2',
                        _n(4):'#4',
                        _n(6):'#6',
                        _n(8):'#8',
                        _n(10):'#10',
                        _n(12):'#12',
                        1/4:'1/4',
                        5/16:'5/16',
                        3/8:'3/8',
                        7/16:'7/16',
                        1/2:'1/2',
                        5/8:'5/8',
                        3/4:'3/4',
                        7/8:'7/8',
                        1:'1' }
    _diam_regex = '((#(?P<size>\d+))|((?P<whole>\d+)\s+)?(?P<frac>(?P<numer>\d+)/(?P<denom>\d+)))"?' #'1 5/16' or '1/4' or '#10' 
    _separator = '\s*-\s*'
    _tpi_regex = '(?P<tpi>\d+\s*(TPI|tpi)?)'
    def parse_bolt_spec(self, spec):
        '''returns diameter and pitch given something like '#8x32' or '3/8" - 16'.'''
        match = re.match(_diam_regex+'('+_separator+_tpi_regex+')?')
        if not match: raise ValueError, "couldn't parse "+self.__class__.series+" series bolt spec '"+str(spec)+"'"
        print match.groups()
        diameter = 0
        whole = match.group('whole')
        if whole: diameter += float(whole)
        frac = match.group('frac')
        if frac: diameter += float(match.groups('numer'))/float(match.groups('denom'))

        if match.group('size'): 
            assert not whole and not frac
            diameter = self.numbered_thread_diameter(match.groups('size'))
        if match.group('size') in self.preferred_sizes.values():
            print 'yay, a standard bolt!' 
        if match.group('tpi'): pitch = match.group('tpi')
        else: #no pitch specified
            if hasattr(self.__class__, 'standard_pitch') and diameter in self.__class__.preferred_sizes:
                pitch = self.__class__.standard_pitch[diameter]
        return self.__class__(diameter, pitch)        
class UNC_Thread(UN_Thread):
    '''unified national coarse thread. found on most american nuts and bolts'''
    yaml_tag = '!thread_UNC'
    series = 'UNC' 
    standard_pitch={_n(8):24,
                    1/4:20}

class UNF_Thread(UN_Thread):
    '''unified national fine thread. found on some american nuts and bots'''
    yaml_tag = '!thread_UNF'
    series = 'UNF'
    standard_pitch={_n(8):32,
                    1/4:28}


#TODO http://www.ring-plug-thread-gages.com/ti-UNJ-vs-UN.htm
#TODO http://www.ring-plug-thread-gages.com/ti-UNR-vs-UN.htm ?
