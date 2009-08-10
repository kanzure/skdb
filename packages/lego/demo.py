import skdb, yaml
from copy import copy
# OUT: Couldn't import OCC.Utils.DataExchange.STEP: Is pythonOCC installed properly?
lego = skdb.load_package('lego')
lego.load_data()
brick1 = copy(lego.parts[0])
brick2 = copy(lego.parts[0])
#print yaml.dump(brick1.interfaces[1].options([brick1, brick2]))
print "brick1's stud is compatible with: ", [x.interface1.name for x in brick1.interfaces[5].options([brick1, brick2])]
