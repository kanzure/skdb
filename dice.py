'''example code for yaml magic from pyyaml.org documentation.
see http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers'''

import yaml, re
#def  dice_constructor(Dice, data):
    #major, minor =[int(x) for x in data.split('d')]
    #return Dice(major, minor)

class Dice(yaml.YAMLObject):
    yaml_tag = '!dice'
    yaml_pattern = re.compile('^\d+d\d+$')
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor
    def __repr__(self):
        return "Dice(%s,%s)" % (self.major, self.minor)
    def yaml_repr(self):
        return "%sd%s" % (self.major, self.minor)
    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, cls.yaml_repr(data)) #not sure this is right
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_scalar(node)
        major, minor = [int(x) for x in data.split('d')]
        return cls(major, minor)

class Foo(yaml.YAMLObject):
    yaml_tag = '!foo'
    yaml_pattern = re.compile('foo(.*)')
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return "Foo(%s)" %(self.value)
    def yaml_repr(self):
        return "foo%s" % self.value
    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, cls.yaml_repr(data)) #not sure this is right
    @classmethod
    def from_yaml(cls, loader, node):
        match = re.search(cls.yaml_pattern, loader.construct_scalar(node))
        if match:
            return Foo(match.group(1))
        else:
            return  Foo(loader.construct_scalar(node))

class FirstResolver(yaml.YAMLObject):
    yaml_tag="!first"
    some_attr="foobars"
    def __init__(self, extra):
        if extra: some_attr=extra
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_scalar(node)
        return cls(data)

class SecondResolver(yaml.YAMLObject):
    yaml_tag="!second"
    some_attr="barfoo"
    def __init__(self, extra):
        if extra: some_attr=extra
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_scalar(node)
        return cls(data)

#teach PyYAML that any untagged scalar with the path [a] has an implict tag !first
yaml.add_path_resolver("!first", ["a"], str)

#teach PyYAML that any untagged scalar with the path [a,b,c] has an implicit tag !second.
yaml.add_path_resolver("!second", ["a", "b", "c"], str)

#teach PyYAML that any untagged plain scalar that looks like XdY has the implicit tag !dice.
for cls in [Dice, Foo]:
    yaml.add_implicit_resolver(cls.yaml_tag, cls.yaml_pattern)

def load(foo):
    return yaml.load(foo)

def dump(foo):
    return yaml.dump(foo, default_flow_style=False)

print "loading '2d6' turns into:  ", load('2d6')
print "dumping Dice(2,6) looks like:  ",  dump(Dice(2,6))
print "loading foomoo: ", load('foomoo')
print "loading !foo bar: ", load('!foo bar')
print "dumping Foo(moo): ", dump(Foo("moo"))
print "loading a: moo ", load("a: moo")
print "loading a: b: c: input goes here", load("a:\n b:\n  c: input goes here")


