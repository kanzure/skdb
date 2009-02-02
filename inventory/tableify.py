#writes out a pretty html table with categories side by side

import yaml

f = open("comparison.yaml")
a = yaml.load(f)

#find the superset
categories = []
labs = [lab for lab in a]
for lab in labs:
  categories += lab.keys()
categories = [i for i in set(categories)]
categories.sort()
print categories
