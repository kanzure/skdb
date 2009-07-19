#!/usr/bin/python
#kanzure@gmail.com 2009-07-19
import yaml

yamlfile = yaml.load(open("trans-tech.yaml"))
keys = yamlfile.keys()

for each in keys:
    print yamlfile[each]

def print_total(somedict,depth=""):
    if not type(somedict) == type({}): return #blah
    keys = somedict.keys()
    for each in keys:
        print depth, each
        print_total(somedict[each],depth=depth+"\t")

def list_requirements(something):
    result=[]
    [result.append(list_requirements(requirement)) for requirement in something.requirements]
    return result

