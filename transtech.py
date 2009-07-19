#!/usr/bin/python
#kanzure@gmail.com 2009-07-19
import yaml
import copy
import dep.topsort

yamlfile = yaml.load(open("trans-tech.yaml"))
keys = yamlfile.keys()

#for each in keys:
#    print yamlfile[each]

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

def find_path(something,current_path,yamlfile_subset):
    if current_path == None:
        yamlfile_subset = yamlfile
        current_path = ["root"]
    for key in yamlfile_subset.keys():
        if yamlfile_subset[key] == something or key == something:
            return copy.copy(current_path).append(key)
        else:
            print "current_path is ", current_path
            print "something is ", something
            print "yamlfile_subset[key] is ", yamlfile_subset[key]
            print "yamlfile_subset[key].keys() is: ", yamlfile_subset[key].keys()
            print "key is ", key
            result = find_path(something,copy.copy(current_path).append(key),copy.copy(yamlfile_subset[key]))
            if result: return result
            else: return False #sorry, didn't find it at all.

#print find_path("autoscholar",current_path=[],yamlfile_subset=yamlfile)

def find_parents(something):
    '''find all parents to something'''
    path = find_path(something)

def to_pair_list(some_dict):
    return_list = []
    for key in some_dict.keys():
        if type(some_dict[key]) == type({}):
            return_list.append((key, to_pair_list(some_dict[key])))
        else:
            return_list.append((key, some_dict[key]))
    return return_list

def add_information(some_dict,list_of_parents):
    for key in some_dict.keys():
        if type(some_dict[key]) == type({}):
            new_list = copy.copy(list_of_parents)
            new_list.append(key)
            some_dict[key] = add_information(copy.copy(some_dict[key]),new_list)
        else:
            some_dict[key] = list_of_parents
    return some_dict

def search(some_dict,some_key):
    some_stuff = some_dict
    #if type(some_dict) == type(""): return some_key
    if type(some_dict) == type({}): some_stuff = some_dict.keys()
    if type(some_dict) == type([]): some_stuff = some_dict
    for key in some_stuff:
        if key == some_key:
            if type(some_dict) == type([]): return key
            return [key, some_dict[key]]
        else:
            if type(some_dict) == type({}): return [key,search(some_dict[key],some_key)]
            if type(some_dict) == type([]): return [key, search(key,some_key)]
            #return "" #ok nothing left

blah = add_information(yamlfile, [])
blah2 = search(yamlfile, "computer stuff")
print blah2


