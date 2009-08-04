#!/usr/bin/python
#defines a template used in skdb package metadata.yaml files
import yaml

class Template(yaml.YAMLObject):
    '''defines a template used in skdb package metadata.yaml files'''
    yaml_tag="!template"
    def __init__(self):
        pass
