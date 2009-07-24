import csv
import yaml
materials = {}
parser = csv.reader(open('friction.csv'))  
for fields in parser:
    name = fields[0].lower()
    try: foo = materials[name]
    except KeyError: materials[name]={}
    rec= materials[name][fields[1].lower()] = {'static_min':fields[2], 'static_max':fields[3], 'kinetic_min':fields[4], 'kinetic_max':fields[5]}
    #for pos, name in enumerate(['static_min', 'static_max', 'kinetic_min', 'kinetic_max']):
    #    try: rec[name] = float(fields[pos+2])
    #    except ValueError: rec[name] = None
    
    #print name

print yaml.dump(materials, default_flow_style=False)