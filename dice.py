'''example code for yaml magic from pyyaml.org documentation'''

import yaml
def  dice_constructor(data):
    major, minor =[int(x) for x in data.split('d')]
    return Dice(major, minor)
    
class Dice():
    yaml_tag='!dice'
    def __new__():
        return Dice(1,2)
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor
    def __repr__(self):
        return "Dice(%s,%s)" % (self.major, self.minor)
    def representer(self):
        return "%sd%s" % (self.major, self.minor)
    constructor = dice_constructor
    

#def dice_representer(dumper, data):
#    return dumper.represent_scalar('!dice', '%sd%s' %(data.major, data.minor))

#yaml.add_representer(Dice, dice_representer)

yaml.add_representer(Dice, lambda dumper, x: dumper.represent_scalar('!dice', x.representer()))

def dice_constructor(loader, node):
    value = loader.construct_scalar(node)
    a, b = map(int, value.split('d'))
    return Dice(a, b)

#yaml.add_representer(name, lambda dumper, x: dumper.represent_scalar(name.yaml_tag, x.yaml_repr()))
#yaml.add_constructor(Dice.yaml_tag, lambda loader, node: Dice.constructor(Dice.__new__(), loader.construct_scalar(node)))
yaml.add_constructor(Dice.yaml_tag, lambda loader, node: Dice.constructor(loader.construct_scalar(node)))
#yaml.add_constructor('!dice', dice_constructor)

def load(foo):
    return yaml.load(foo)

def dump(foo):
    return yaml.dump(foo)

#teach PyYAML that any untagged plain scalar that looks like XdY has the implicit tag !dice.
import re
pattern = re.compile('^\d+d\d+$')
yaml.add_implicit_resolver('!dice', pattern)

print "load:", load('2d6')
print "dump:",  dump(Dice(2,6))