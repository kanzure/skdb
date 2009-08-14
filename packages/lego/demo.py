import skdb, yaml
from copy import deepcopy
lego = skdb.load_package('lego')
lego.load_data()
brick1 = deepcopy(lego.parts[0])
brick1.post_init_hook() #not sure why this isnt called automatically
brick2 = deepcopy(lego.parts[0])
brick2.post_init_hook()
for i in brick1.interfaces:
    print "brick1's "+i.name+" is compatible with: ", [x.interface2.name for x in i.options([brick1, brick2])]
    
