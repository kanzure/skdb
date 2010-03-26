#!/usr/bin/python
#author: Bryan Bishop <kanzure@gmail.com>
#url: http://heybryan.org/
#date: 2010-03-26
#filename: thingiverse.py
#license: gpl2+
#purpose: simple demo interface to thingiverse.com, not to be used in production environments
import os
from BeautifulSoup import BeautifulSoup
import pycurl
from StringIO import StringIO

#sudo apt-get install python-pip; pip install -e git+git://github.com/kanzure/optfunc.git#egg=optfunc
import optfunc

def thingiverse_get(thing_id):
    files = []

    if thing_id.count("thing:") > 0:
        thing_id = thing_id.replace("thing:", "")

    buffer1 = StringIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, "http://www.thingiverse.com/thing:" + str(thing_id))
    curl.setopt(curl.VERBOSE, 0)
    curl.setopt(curl.WRITEFUNCTION, buffer1.write)
    curl.perform()
    curl.close()

    html = buffer1.getvalue().strip()
    soup = BeautifulSoup(html)

    h3s = soup.findAll(attrs={"class": "file_info"})
    for h3 in h3s:
        filename = h3.contents[0].strip()
        link = h3.parent.parent.findAll(name="a")[0].attrs[0][1]

        files.append((filename, link))

    output = "Which file do you want to download?\n\n"

    counter = 0
    for file in files:
        filename = file[0]
        output = output + "\t[" + str(counter) + "] " + filename + "\n"
        counter = counter + 1
    output = output + "\n"
    
    print output
    selection = raw_input("Please type a number: ")

    files_to_get = [int(selection)]
    #if selection.count(",") > 0:
    #    files_to_get = selection.split(",")

    for file in files_to_get:
        print "Beginning download of: ", files[file][0]
        os.system("wget \"http://thingiverse.com" + str(files[file][1]) + "\" --output-document=\"" + files[file][0] + "\"")

if __name__ == "__main__":
    optfunc.run(thingiverse_get)
