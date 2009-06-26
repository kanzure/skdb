'''example code for yaml magic from pyyaml.org documentation.
see http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers'''

import yaml, re
#def  dice_constructor(Dice, data):
    #major, minor =[int(x) for x in data.split('d')]
    #return Dice(major, minor)

class Dice:
    yaml_tag = '!dice'
    yaml_pattern = re.compile('^\d+d\d+$')
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor
    def __repr__(self):
        return "Dice(%s,%s)" % (self.major, self.minor)
    def yaml_repr(self):
        return "%sd%s" % (self.major, self.minor)
    def constructor (cls, data): #constructor takes class as first argument
        major, minor = [int(x) for x in data.split('d')]
        return cls(major, minor)
    constructor = classmethod(constructor)

#the class we want to load/dump
cls = Dice 

#how yaml will dump a Dice object
#def dice_representer(dumper, data):
#    return dumper.represent_scalar('!dice', '%sd%s' %(data.major, data.minor))
#yaml.add_representer(Dice, dice_representer)

#now do it generically instead
yaml.add_representer(cls, lambda dumper, instance: dumper.represent_scalar(instance.yaml_tag, instance.yaml_repr()))

#teach yaml to parse !dice with dice_constructor
#yaml.add_constructor(Dice.yaml_tag, lambda loader, node: Dice.constructor(loader.construct_scalar(node)))
#yaml.add_constructor('!dice', dice_constructor)

#the generic (and object-oriented) way
yaml.add_constructor(cls.yaml_tag, lambda loader, node: cls.constructor(loader.construct_scalar(node)))


#teach PyYAML that any untagged plain scalar that looks like XdY has the implicit tag !dice.
#yaml.add_implicit_resolver('!dice', re.compile('^\d+d\d+$')  )

#the generic way
yaml.add_implicit_resolver(cls.yaml_tag, cls.yaml_pattern)


def load(foo):
    return yaml.load(foo)

def dump(foo):
    return yaml.dump(foo, default_flow_style=False)

print "loading '2d6 turns into:  ", load('2d6')
print "dumping Dice(2,6) looks like:  ",  dump(Dice(2,6))
