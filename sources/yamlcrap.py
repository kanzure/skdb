import yaml

class FennObject(yaml.YAMLObject):
    '''so i dont repeat generic yaml stuff everywhere'''
    def __setstate__(self, attrs):
        for (k,v) in attrs.items():
            k = re.sub(' ', '_', k) #replace spaces with underscores because "foo.the attr" doesn't work
            self.__setattr__(k,v)
    @classmethod
    def to_yaml(cls, dumper, data):
        if hasattr(cls, 'yaml_repr'):
            tmp = cls.yaml_repr(data)
            return dumper.represent_scalar(cls.yaml_tag, tmp)
        else: 
            #i want to return the default yaml dump; but how?       
            #cls.to_yaml = yaml.YAMLObject.to_yaml
            #return cls.to_yaml(dumper, data)
            ##return dumper.represent_mapping(cls.yaml_tag, data)
            tmp = cls.__repr__(data)
            return dumper.represent_scalar(cls.yaml_tag, tmp)

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