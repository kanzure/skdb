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
from string import join
import yaml

#sudo apt-get install python-pip; pip install -e git+git://github.com/kanzure/optfunc.git#egg=optfunc
import optfunc

def download_thingiverse_partial(start=0, end=434):
    '''creates a backup from thing:434 to thing:2073'''

    if not os.path.exists("thingiverse_data"): os.mkdir("thingiverse_data")

    for current in range(start, end):
        os.system("cd thingiverse_data; wget http://thingiverse.com/thing:%s --output-document \"%s\"" % (str(current), str(current)))

def title_fixer(messy_title):

    to_space = ["[", "]", "...", " | ", ". ", "!", "<", ">", "&", ";", ":-)", ":)", "(", ")", "/", "...", "  ", "?"]
    to_blank = ["$", "'"]
    to_dash = [" - ", " ", "--", u"\xe3\x80\x80"]
    
    if type(messy_title) == unicode: messy_title = messy_title.encode('ascii', 'replace')

    for char in to_space:
        messy_title = messy_title.replace(char, " ")

    for char in to_blank:
        messy_title = messy_title.replace(char, "")

    for char in to_dash:
        messy_title = messy_title.replace(char, "-")

    #replace some bad characters

    if messy_title.count(",") > 0:
        messy_title = messy_title.split(",")[0]

    if messy_title[-1] == "-": messy_title = messy_title[:-1]
    if messy_title[0] == "-": messy_title = messy_title[1:]
    if messy_title[-1] == ".": messy_title = messy_title[:-1]

    return messy_title.lower()

#keep track of which unix names are already taken
thingiverse_thing_names = []

def extract_image_links(html, http=False):
    '''finds all links to /image: stuff. set http to 'true' if you want the full thingiverse.com link'''
    relevant_links = []
    all_links = html.findAll(name="a")
    for link in all_links:
        for arg in link.attrs:
            if arg[0] == "href":
                if arg[1][0:7] == "/image:": relevant_links.append(arg[1])
    return relevant_links

def extract_images(html):
    '''finds all thumbnail images'''
    relevant_images = []
    all_images = html.findAll(name="img")
    for image in all_images:
        for arg in image.attrs:
            if arg[0] == "src":
                if "renders" in arg[1]: relevant_images.append(arg[1])
    return relevant_images

def extract_h2(html, name):
    
    desc = html.findAll(name="h2", text=name)
    if len(desc) == 0: return ""

    desc = desc[0].parent
    
    guh = []
    for each in desc.nextSibling.nextSibling.contents:
        guh.append(str(each))

    actual_description = join(guh).strip()
    return actual_description

def extract_license(html):
    license_link = html.findAll(name="a", attrs={"rel": "license"})[0]
    license_link = license_link.attrs[1][1] #value of "href"
    return license_link

def extract_description(html): return extract_h2(html, "Description")
def extract_instructions(html): return extract_h2(html, "Instructions")
def extract_files(soup):
    files = []
    h3s = soup.findAll(attrs={"class": "file_info"})
    for h3 in h3s:
        filename = h3.contents[0].strip()
        link = h3.parent.parent.findAll(name="a")[0].attrs[0][1]
        stats = h3.parent.contents[2].strip().split("/")

        messy_downloads = stats[1]
        downloads = ''.join([letter for letter in messy_downloads if letter.isdigit()])

        messy_size = stats[0]
        size = ''.join([letter for letter in messy_size if letter.isdigit()])
        if "MB" in messy_size:
            size = size + " MB"
        if "kb" in messy_size:
            size = size + " kb"

        files.append({"filename": filename, "link": link, "size": size, "downloads": downloads})
    return files

def process_thing(thing_id):
    file_handler = open("thingiverse_data/" + str(thing_id))
    original_html = file_handler.read()
    file_handler.close()

    html = BeautifulSoup(original_html)
    messy_title, messy_author = html.findAll(attrs={"id": "pageTitle"})[0].contents

    #fix up the title a bit
    messy_title = messy_title[:-4] #get rid of the " by " at the end
    unix_name = title_fixer(messy_title)

    #make sure the name isn't already used
    #also a cheap hack to fix the name in those awkward situations
    if unix_name in thingiverse_thing_names:
        current = 0
        while unix_name in thingiverse_thing_names:
            unix_name = unix_name + str(current)
            current = current + 1
    
    #make sure nothing else uses this name
    thingiverse_thing_names.append(unix_name)

    #get the author deets
    author = messy_author.contents[0]

    image_links = extract_image_links(html)
    image_thumbnails = extract_images(html)
    description = extract_description(html)
    instructions = extract_instructions(html)
    license = extract_license(html)
    files = extract_files(html) #a list of filenames and the link

    #TODO: discussion

    #print "unix_name: ", unix_name
    #print "author: ", author
    #print "image_links: ", image_links
    #print "image_thumbnails: ", image_thumbnails
    #if description and not description == "": print "description: ", description
    #if instructions and not instructions == "": print "instructions: ", instructions
    #print "files: ", files

    if not os.path.exists("thingiverse_packages/" + str(unix_name)): os.mkdir("thingiverse_packages/" + str(unix_name))

    metadata = {"name": str(unix_name).encode("ascii", "replace"), "author": str(author).encode('ascii', 'replace'), "urls": ["http://thingiverse.com/thing:" + str(thing_id)], "image_links": image_links, "image_thumbnails": image_thumbnails, "description": str(description).encode("ascii", "replace"), "files": files, "license": str(license)}
    #metadata = {"author": author}
    output = yaml.dump(metadata).encode("ascii", "replace")

    file_handle = open("thingiverse_packages/" + str(unix_name) + "/metadata.yaml", "w")
    file_handle.write(output)
    file_handle.close()

    #download the files
    for file in files:
        link = file["link"]
        os.system("cd thingiverse_packages/" + str(unix_name) + "/; wget http://thingiverse.com" + str(link) +";")

def tester():
    #just process one for now
    #process_thing("1446")
    #exit()

    for each in os.listdir("thingiverse_data"):
        try:
            print "each: ", each
            process_thing(each)
        except: pass

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
    #optfunc.run(download_thingiverse_partial)
    #optfunc.run(tester)
