import yaml, re

def add_yaml_resolvers(classes):
    for cls in classes: #only one at a time works so far?
        if hasattr(cls, 'yaml_pattern') and cls not in implicit_resolved:
            yaml.add_implicit_resolver(cls.yaml_tag, re.compile(cls.yaml_pattern))
            implicit_resolved.append(cls)

implicit_resolved=[]
def load(string):
    global implicit_resolved

    tmp = yaml.load_all(string)
    rval = tmp.next() #this might be tag_hack
    if type(rval) == tag_hack:
        other_return_value = tmp.next() #a document listing which tags to ignore comes before the real metadata
        #now remove the tag_hack tags from the system
        for tag in rval.tags:
            rval.undo_tag_hack_for_tag(tag)
        return other_return_value
    else: return rval

def dump(value, filename=None):
    retval = yaml.dump(value, default_flow_style=False)
    if filename is not None:
        f = open(filename, 'w')
        f.write(retval)
    else:
        return retval

class FennObject(yaml.YAMLObject):
    '''so i dont repeat generic yaml stuff everywhere'''
    #TODO fix bad characters spaces etc
    
    @staticmethod
    def setify(var):
        '''converts whatever to a set; dicts become a set of their values'''
        if not hasattr(var, '__iter__'): var = set([var])
        if isinstance(var, dict): var = set([var.values()]) #that's right, not keys
        if isinstance(var, list): var = set(var)
        return var
        
    def overlay(self, other):
        if type(other)==dict: 
            attrs = other.iteritems()
        else: 
            attrs = other.__dict__.iteritems()
        for (k, v) in attrs:
            setattr(self, k, v)
            
    @classmethod
    def to_yaml(cls, dumper, data):
        if hasattr(data, "yaml_flow_style"):
            flow = data.yaml_flow_style
        else: flow=None
        if hasattr(data, 'yaml_repr'):
            repr, tag = data.yaml_repr(), data.yaml_tag
            if isinstance(repr, list) or isinstance(repr, tuple):
                return dumper.represent_sequence(tag, repr, flow)
            elif isinstance(repr, dict):
                return dumper.represent_mapping(tag, repr, flow)
            else:
                return dumper.represent_scalar(tag, repr)
        else: 
            #return the default yaml dump
            if len(data.__dict__) > 0: return dumper.represent_mapping(cls.yaml_tag, data.__dict__.iteritems())
            else: return dumper.represent_scalar(cls.yaml_tag, data)

    @classmethod
    def from_yaml(cls, loader, node):
        '''see http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers'''
        if type(node)==yaml.ScalarNode:
            data = loader.construct_scalar(node)
            return cls(data) #assuming that the class has one positional arg
        elif type(node) == yaml.MappingNode:
            data = loader.construct_mapping(node) #will this break path_resolver?
            rval = cls()
            #stuff data into object's attributes
            for (key, value) in data.iteritems():
                if value is not None:
                    setattr(rval, key, value)
            #this isn't actually used anywhere:
            if hasattr(rval, "post_init_hook"):
                rval.post_init_hook()
            return rval
        elif type(node) == yaml.SequenceNode:
            data = loader.construct_sequence(node)
            return cls(data)
        else: raise ValueError, "node type must be scalar, mapping, or sequence; got: " + str(cls.yaml_type)

class Dummy(object):
    def __init__(self, node):
        if hasattr(node, 'iteritems'):
            for (k,v) in node.iteritems(): setattr(self, k,v)
        else: self = node
    @staticmethod
    def multi_constructor(loader, tag_suffix, node):
        #if the real class is actually loaded, return it
        #so search through the classes that inherit from YAMLObject and hasattr(blah,"yaml_type") and the right yaml_type
        #if 
        #    tag_hack.yaml_loader.yaml_constructors..
        #    return .. the correct object .. 
        if type(node) == yaml.ScalarNode:
            data = loader.construct_scalar(node)
        elif type(node) == yaml.MappingNode:
            data = loader.construct_mapping(node)
        elif type(node) == yaml.SequenceNode:
            data = loader.construct_sequence(node)
        else: raise TypeError, 'I dont know what to do with this node: ' + str(node)
        return Dummy(data)
        
#foo = yaml.load_all('!!python/object:skdb.tag_hack \n tags: "!hello"\n---\n test: !hello\n  1234')

class tag_hack(FennObject):
    '''allows loading of a template file containing tags that do not exist yet.
     prepend something like this to the actual document: 
    !tag_hack tags: ["!one", "!two", "!three"]\n---\n'''
    yaml_tag="!tag_hack"
    tags=[]
    def __init__(self):
        pass
    def __setstate__ (self, attrs):
        for i in attrs['tags']:
            yaml.add_multi_constructor(i, Dummy.multi_constructor)
            self.tags.append(i)
    def undo_tag_hack_for_tag(self, tag):
        '''undoes a tag hack for a particular tag'''
        #for key in yaml.YAMLObject.yaml_loader.yaml_constructors.keys():
        #    if key:
        #        if key[:1] == "!":
        #            print key
        if tag in self.yaml_loader.yaml_multi_constructors:
           self.yaml_loader.yaml_multi_constructors.pop(tag)
        self.tags.remove(tag) #this might need to be indented
        return
