import yaml, re

class FennObject(yaml.YAMLObject):
    '''so i dont repeat generic yaml stuff everywhere'''
    def __setstate__(self, attrs):
        for (k,v) in attrs.items():
            k = re.sub(' ', '_', k) #replace spaces with underscores because "foo.the attr" doesn't work
            self.__setattr__(k,v)
        if hasattr(self, post_setstate_hook):
            self.post_setstate_hook()
    @classmethod
    def to_yaml(cls, dumper, data):
        if hasattr(data, 'yaml_repr'):
            return dumper.represent_scalar(data.yaml_tag, data.yaml_repr())
            #yaml_type is used to determine whether or not it is a scalar or a mapping (you set this)
        else: 
            #return the default yaml dump
            if len(data.__dict__) > 0: return dumper.represent_mapping(cls.yaml_tag, data.__dict__.iteritems())
            else: return dumper.represent_scalar(cls.yaml_tag, data)

    @classmethod
    def from_yaml(cls, loader, node):
        '''see http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers'''
        if hasattr(cls,"yaml_type"):
            if cls.yaml_type == "scalar":
                data = loader.construct_scalar(node)
            elif cls.yaml_type == "mapping":
                data = loader.construct_mapping(node) #will this break path_resolver?
                rval = cls()
                #stuff data into object's attributes
                for (key, value) in data.iteritems():
                    if value is not None:
                        setattr(rval, key, value)
                return rval
            else: raise ValueError, "yaml_type must be either \"scalar\" or \"mapping\"; got: " + str(cls.yaml_type)
        else: 
            data = loader.construct_scalar(node)
            return cls(data)

class Dummy(object):
    def __init__(self, node):
        if hasattr(node, 'iteritems'):
            for (k,v) in node.iteritems(): setattr(self, k,v)
        else: self = node
    @staticmethod
    def multi_constructor(loader, tag_suffix, node):
        if type(node) == yaml.ScalarNode:
            data = loader.construct_scalar(node)
        elif type(node) == yaml.MappingNode:
            data = loader.construct_mapping(node)
        else: raise TypeError, 'I dont know what to do with this node: ' + str(node)
        return Dummy(data)
        
#foo = yaml.load_all('!!python/object:skdb.tag_hack \n tags: "!hello"\n---\n test: !hello\n  1234')

class tag_hack(FennObject):
    '''allows loading of a template file containing tags that do not exist yet.
     prepend something like this to the actual document: 
    !tag_hack tags: ["!one", "!two", "!three"]\n---\n'''
    yaml_tag="!tag_hack"
    yaml_type="mapping" #assume it's a mapping
    def __init__(self):
        pass
    def __setstate__ (self, attrs):
        for i in attrs['tags']:
            yaml.add_multi_constructor(i, Dummy.multi_constructor)
