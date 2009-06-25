'''example code for yaml magic from pyyaml.org documentation'''

import yaml

class Dice():
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor
    def __repr__(self):
        return "Dice(%s,%s)" % (self.major, self.minor)

def dice_representer(dumper, data):
    return dumper.represent_scalar('!dice', '%sd%s' %(data.major, data.minor))

yaml.add_representer(Dice, dice_representer)

def dice_constructor(loader, node):
    value = loader.construct_scalar(node)
    a, b = map(int, value.split('d'))
    return Dice(a, b)

yaml.add_constructor('!dice', dice_constructor)

def load(foo):
    return yaml.load(foo)

def dump(foo):
    return yaml.dump(foo)

#teach PyYAML that any untagged plain scalar that looks like XdY has the implicit tag !dice.
import re
pattern = re.compile('^\d+d\d+$')
yaml.add_implicit_resolver('!dice', pattern)

print load('2d6')
print dump(Dice(2,6))