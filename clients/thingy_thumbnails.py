#!/usr/bin/python
#author: Bryan Bishop
#date: 2010-03-27
#license: gpl 2+
#download thumbnail urls
import os
import yaml

for each in os.listdir("thingiverse_packages"):
    metadata = yaml.load(open("thingiverse_packages/" + each + "/metadata.yaml", "r").read())
    thumbnails = metadata["image_thumbnails"]
    for img_url in thumbnails:
        os.system("cd thingiverse_packages/" + each + "/; wget \"" + img_url + "\"; ")

