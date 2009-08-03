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
        if hasattr(cls, 'yaml_repr'):
            tmp = cls.yaml_repr(data)
            return dumper.represent_scalar(cls.yaml_tag, tmp)
        else: 
            #return the default yaml dump
            if len(data.__dict__) > 0: return dumper.represent_mapping(cls.yaml_tag, data.__dict__.iteritems())
            else: return dumper.represent_scalar(cls.yaml_tag, data)

    @classmethod
    def from_yaml(cls, loader, node):
        '''see http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers'''
        data = loader.construct_scalar(node)
        if hasattr(cls, 'yaml_pattern') and hasattr(cls, 'yaml_parse_args') and cls.yaml_parse_args == True:
            match = re.search(cls.yaml_pattern, data)
            if match:
                return cls(match.groups()) #i guess this will stuff the regex groups into the positional args #TODO unit test
        else:
            return cls(data)

class Dummy(object):
    def __init__(self, node):
        if hasattr(node, 'iteritems'):
            for (k,v) in node.iteritems(): setattr(self, k,v)
        else: self = node
    @staticmethod
    def multi_constructor(loader, tag_suffix, node):
        print yaml.dump(node)
        data = loader.construct_scalar(node)
        if type(node) == yaml.ScalarNode:
            data = loader.construct_scalar(node)
        if type(node) == yaml.MappingNode:
            data = loader.construct_mapping(node)
        #else: raise TypeError, node#, 'i dont know what to do with this node'
        print '---------------'
        print yaml.dump(data)
        return Dummy(data)
        
#foo = yaml.load_all('!!python/object:skdb.tag_hack \n tags: "!hello"\n---\n test: !hello\n  1234')

class tag_hack:
    '''allows loading of a template file containing tags that do not exist yet'''
    def __setstate__ (self, attrs):
        for i in attrs['tags']:
            yaml.add_multi_constructor('!', Dummy.multi_constructor)
