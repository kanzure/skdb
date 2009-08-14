import skdb, yaml
from copy import deepcopy
# OUT: Couldn't import OCC.Utils.DataExchange.STEP: Is pythonOCC installed properly?
lego = skdb.load_package('lego')
lego.load_data()
brick1 = deepcopy(lego.parts[0])
brick1.post_init_hook() #not sure why this isnt called automatically
brick2 = deepcopy(lego.parts[0])
brick2.post_init_hook()
#print yaml.dump(brick1.interfaces[1].options([brick1, brick2]))
for i in brick1.interfaces:
    #print "brick1's "+i.name+" is compatible with: ", [x.interface1.name for x in brick1.interfaces[5].options([brick1, brick2])]
    print "brick1's "+i.name+" is compatible with: ", [x.interface2.name for x in i.options([brick1, brick2])]

