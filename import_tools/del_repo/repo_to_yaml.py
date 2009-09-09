#!/usr/bin/python
#python repo-to-yaml.py roomba.repo.xml > roomba.yaml
import sys
import yaml
from xml.dom import minidom

def determine_key_name(results, node_name):
    '''from a node_name, figure out a unique key name'''
    if node_name == "#text": return False #return determine_key_name(results, "no name error")
    key_name = node_name
    if not results.has_key(key_name):
        return key_name
    n = 0
    while True:
        if n>5000:
            raise OverflowError, "recursion depth exceeded"
            return False
        if not results.has_key(key_name):
            return key_name
        key_name = node_name + " " + str(n)
        n=n+1

def process_node(node):
    results = {}
    if node.nodeName == "#text": return results
    if node.attributes:
        for attr_key in node.attributes.keys():
            value = node.attributes[attr_key].value
            key_name = determine_key_name(results, attr_key)
            if not key_name==False and not key_name=="False":
                results[str(unicode(key_name))] = str(unicode(value))
            #print "results[%s] = %s" % (key_name, value)
    for child_node in node.childNodes:
        result = process_node(child_node)
        key_name = determine_key_name(results, child_node.nodeName)
        if not key_name==False and not key_name == "False":
            results[str(unicode(key_name))] = result
    return results

def parse_file(file):
    artifacts = []
    doc = minidom.parse(file)
    system = doc
    #system = doc.childNodes[0]
    #print system.childNodes[0].nodeName=="#text"
    huge_thing = process_node(system)
    return huge_thing
    #for node in system.childNodes:
    #    if node.nodeName == "Artifact":
    #        artifact = process_artifact(node)
    #        artifacts.append(artifact)

def main():
    rval = {}
    if len(sys.argv)>1 and sys.argv[1] == '-':
        rval['stdin'] = parse_file(sys.stdin)
    else:
        for i in sys.argv[1:]:
            rval[i] = parse_file(open(i))
    print yaml.dump(rval, default_flow_style=False)
    return rval

if __name__ == "__main__":
    main()

