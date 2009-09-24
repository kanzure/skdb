#!/usr/bin/python
#fixes the output of repo_to_yaml.py
import yaml

def has_number(thing):
    result = thing.count("0") + thing.count("1") + thing.count("2") + thing.count("3") + thing.count("4") + thing.count("5") + thing.count("6") + thing.count("7") + thing.count("8") + thing.count("9")
    if result>0: return True
    else: return False

def make_lists(some_dictionary):
    for key in some_dictionary:
        if has_number(key):
            if some_dictionary.has_key(remove_number(key)):
                if isinstance(some_dictionary[key], list):
                    some_dictionary[remove_number(key)].append(some_dictionary[key])
                else: #make it into a list
            else: #actually i'm not so sure what should happen here.
                pass
    for key in some_dictionary:
        if hasattr(some_dictionary[key], "__dict__"):
            some_dictionary[key] = make_lists(some_dictionary[key])
    return some_dictionary

oo = yaml.load(open("roomba.yaml"))
system = oo["roomba.repo.xml"]["System"]




