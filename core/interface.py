#!/usr/bin/python
from yamlcrap import FennObject
from package import package_file
import math

#Interface.volume should be some positive float if it is the male
#or some negative number if it is the female.
#thus summing the volume of two interfaces in a Connection should give 0 for a perfect fit

try: 
  import igraph; use_igraph=True
  #TODO this should go in its own file i guess
  class FakeIGraph:
    '''provides more pythonic interface to igraph'''
    def __init__(self):
        self.graph = igraph.Graph(0)
        self.g = self.graph
        
    def __repr__(self):
        return self.graph.summary()
        
    def add_connection(self, connection, technique=None):
        i1, i2 = connection.interface1, connection.interface2
        v1, v2 = self.g.vs(interface_eq=i1), self.g.vs(interface_eq=i2)
        assert len(v1)==1 and len(v2)==1, 'There Can Only Be One!!!'
        v1, v2 = v1[0], v2[0] #we want the vertex, not the VertexSeq
        e = self.new_edge(v1, v2)
        e['technique'] = technique
        
    def add_part(self, part):
        vp = self.new_vertex()
        vp['part'] = part
        vp['label'] = str(part.name)
        vp['fontcolor'] = 'saddlebrown'
        if hasattr(part, 'ldraw'): #FIXME should be 'icon'
            vp['image'] = package_file(part.package.name, str(part.ldraw)+'.png').name #abs path
            vp['shape'] = 'none' #otherwise it will draw a circle around the icon
        else:
            vp['image'] = ''
            vp['shape'] = 'box'
        for i in part.interfaces:
            vi = self.new_vertex()
            vi['interface'] = i
            vi['label'] = str(part.interfaces.index(i))
            #vi['label'] = i.name
            vi['fontcolor'] = 'black'
            vi['shape'] = 'none'
            vi['image'] = 'none'
            self.g.add_edges((vp.index, vi.index))
            
    def del_part(self, part):
        vp = self.g.vs(part_eq=part)
        assert len(vp) == 1, "there should be exactly one of each part in the graph"
        for i in vp[0]['part'].interfaces:
            vi = self.g.vs(interface_eq=i)
            assert len(vi) == 1, "there should be exactly one of each interface in the graph"
            self.g.delete_vertices(vi)
        self.g.delete_vertices(vp)
        
    def new_edge(self, v1, v2):
        self.g.add_edges((v1.index, v2.index))
        return self.g.es[self.g.ecount()-1]
        
    def new_vertex(self):
        self.g.add_vertices(1)
        return self.g.vs[self.g.vcount()-1]
        
    def dict(self):
        #this ought to be a generator i guess
        rval = {}
        for i in self.g.vs():
            part = i.attributes()['part']
            if part is not None:
                rval.update({i.index : part}) #um, should i return the vertex instead of the part?
            interface = i.attributes()['interface']
            if interface is not None:
                rval.update({i.index : interface})
        return rval
except ImportError: 
    use_igraph=False
    class FakeIGraph:
        '''igraph is not installed'''
        def add_connection(self, conn): pass
        def add_part(self, part): pass
        def del_part(self, part): pass
        def dict(self): return {}

class Interface(FennObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry. theinterface geometry is located at "point" (in mm for now, sorry) and rotated about its Z vector clockwise "rotation" degrees looking away from the origin. (TODO: verify) The geometry is then rotated such that its Z vector points along "orientation".
    
    An alternative way to specify geometry is with "point" and two vectors: "x_vec" and "y_vec".
    in both cases the mating trajectory is along the Z vector.'''
    yaml_tag = '!interface'
    converted = False
    def __init__(self, name=None, units=None, geometry=None, point=[0,0,0], orientation=[0,0,1], rotation=0, part=None, max_connections=1):
        self.name, self.units, self.geometry, self.part = name, units, geometry, part
        #self.point, self.orientation, self.rotation = point, orientation, rotation
        self.max_connections = max_connections
        self.connected = []
        self.identifier = None
        self.complement = None #should be overwritten for specific problem domains
    def is_busy(self):
        if len(self.connected) >= self.max_connections: return True
        else: return False
    def compatible(self, other):
        '''returns True if other is complementary. this method should probably get overwritten for specific problem domains.'''
        for t in self.setify(self.complement):
            if isinstance(other, t): return True
        return False
    def options(self, parts):
        '''what other interfaces can this interface connect to?'''
        parts = self.setify(parts) #yay sets!
        if self.part in parts: parts.remove(self.part) #unless it's really flexible
        rval = set()
        for part in parts:
            for i in part.interfaces:
                if i.compatible(self) and self.compatible(i):
                    if not i.is_busy() and not self.is_busy():
                        rval.add(Connection(self,i))
        return list(rval)     
    def __repr__(self):
        if self.part:
            part_name = self.part.name
        else: part_name = None
        return 'Interface("%s", part="%s")' % (self.name, part_name)

class Connection:
    '''a temporary scenario to see if we should connect these two interfaces'''
    def __init__(self, interface1, interface2):
        assert hasattr(interface1, 'connected')
        assert hasattr(interface2, 'connected')
        self.interface1 = interface1
        self.interface2 = interface2
        
    def connect(self, technique='connect', cgraph=None):
        '''make interface1 and interface2 aware of this connection; update interface2.part's transformation attribute.'''
        #add edge to connection graph
        if cgraph is not None:
            assert self.interface1.part in cgraph.dict().values()
            assert self.interface2.part in cgraph.dict().values()
            cgraph.add_connection(self, technique=technique)
        
        i1 = self.interface1.part.interfaces.index(self.interface1)
        i2 = self.interface2.part.interfaces.index(self.interface2)
        print "connecting %s's %s  to %s's %s brick1[%s] to brick2[%s])" %(self.interface1.part.name,  self.interface1.name, self.interface2.part.name, self.interface2.name,  i1, i2)
        self.interface1.connected.append(self) #.append(self.interface2)?
        self.interface2.connected.append(self)
        return
        
    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.interface1, self.interface2)
        
    def makes_sense(self): #should we include is_busy()?
        return self.interface1.compatible(self.interface2) and self.interface2.compatible(self.interface1)

